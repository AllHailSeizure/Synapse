#!/usr/bin/env python3
"""agent-utils: tiny helper for safe agent coordination via .synapse artifacts.

Features (minimal):
- create/read task artifact
- atomic update with lock file
- validate/reserve spawn budget and spawn limit (leader-only)
- record worker result and append cost log (no raw prompts by default)
- simple CLI wrapper so non-Python runtimes can call it

This file is intentionally dependency-free and Windows-friendly.
"""
import argparse
import json
import os
import time
import tempfile
import hashlib
from datetime import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SYNAPSE_ROOT = os.path.join(ROOT, '.synapse')
TASKS_ROOT = os.path.join(SYNAPSE_ROOT, 'tasks')

LOCK_RETRY_DELAY = 0.1
LOCK_TIMEOUT = 5.0


def ensure_task_paths(task_id):
    task_dir = os.path.join(TASKS_ROOT, task_id)
    workers_dir = os.path.join(task_dir, 'workers')
    os.makedirs(workers_dir, exist_ok=True)
    return task_dir


def artifact_path(task_id):
    return os.path.join(TASKS_ROOT, task_id, 'artifact.json')


def lock_path(task_id):
    return os.path.join(TASKS_ROOT, task_id, '.lock')


def acquire_lock(task_id, timeout=LOCK_TIMEOUT):
    start = time.time()
    lp = lock_path(task_id)
    while True:
        try:
            fd = os.open(lp, os.O_CREAT | os.O_EXCL | os.O_RDWR)
            os.write(fd, str(os.getpid()).encode())
            os.close(fd)
            return True
        except FileExistsError:
            if time.time() - start > timeout:
                return False
            time.sleep(LOCK_RETRY_DELAY)


def release_lock(task_id):
    lp = lock_path(task_id)
    try:
        os.remove(lp)
    except FileNotFoundError:
        pass


def create_task(task_id, leader, spawn_budget_tokens=2000, spawn_limit=3, metadata=None):
    ensure_task_paths(task_id)
    path = artifact_path(task_id)
    artifact = {
        'task_id': task_id,
        'leader': leader,
        'status': 'pending',
        'spawn_budget_tokens': int(spawn_budget_tokens),
        'spawn_limit': int(spawn_limit),
        'worker_ids': [],
        'log': [],
        'metadata': metadata or {}
    }
    tmp = path + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(artifact, f, indent=2)
    os.replace(tmp, path)
    return artifact


def read_task(task_id):
    path = artifact_path(task_id)
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def atomic_update_task(task_id, updater_fn, timeout=LOCK_TIMEOUT):
    if not acquire_lock(task_id, timeout=timeout):
        raise RuntimeError('lock timeout')
    try:
        path = artifact_path(task_id)
        with open(path, 'r', encoding='utf-8') as f:
            artifact = json.load(f)
        updater_fn(artifact)
        tmp = path + '.tmp'
        with open(tmp, 'w', encoding='utf-8') as f:
            json.dump(artifact, f, indent=2)
        os.replace(tmp, path)
        return artifact
    finally:
        release_lock(task_id)


def validate_spawn(task_id, requester, tokens_needed, workers_requested=1):
    art = read_task(task_id)
    if requester != art.get('leader'):
        return False, 'only leader may spawn workers'
    if tokens_needed > art.get('spawn_budget_tokens', 0):
        return False, 'insufficient spawn budget'
    current_workers = len(art.get('worker_ids', []))
    if current_workers + workers_requested > art.get('spawn_limit', 0):
        return False, 'spawn_limit exceeded'
    return True, ''


def reserve_spawn_budget(task_id, tokens, worker_ids=None):
    def updater(art):
        if int(art.get('spawn_budget_tokens', 0)) < int(tokens):
            raise RuntimeError('insufficient budget')
        art['spawn_budget_tokens'] = int(art.get('spawn_budget_tokens', 0)) - int(tokens)
        for wid in (worker_ids or []):
            if wid not in art['worker_ids']:
                art['worker_ids'].append(wid)
        art['log'].append({'ts': datetime.utcnow().isoformat() + 'Z', 'event': 'reserve_spawn', 'tokens': int(tokens), 'workers': worker_ids or []})
    return atomic_update_task(task_id, updater)


def record_worker_result(task_id, worker_id, result_obj):
    task_dir = ensure_task_paths(task_id)
    wpath = os.path.join(task_dir, 'workers', f'{worker_id}.json')
    tmp = wpath + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(result_obj, f, indent=2)
    os.replace(tmp, wpath)

    def updater(art):
        art['log'].append({'ts': datetime.utcnow().isoformat() + 'Z', 'event': 'worker_result', 'worker': worker_id, 'summary': result_obj.get('summary')})
    return atomic_update_task(task_id, updater)


def append_cost_log(task_id, agent_id, model, tokens_in, tokens_out, prompt_hash=None):
    task_dir = ensure_task_paths(task_id)
    clog = os.path.join(task_dir, 'cost.log')
    entry = {'ts': datetime.utcnow().isoformat() + 'Z', 'agent': agent_id, 'model': model, 'tokens_in': int(tokens_in), 'tokens_out': int(tokens_out)}
    if prompt_hash:
        entry['prompt_hash'] = prompt_hash
    with open(clog, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry) + "\n")
    return entry


def compact_brief_from_files(paths, max_chars=2000):
    parts = []
    for p in paths:
        if os.path.exists(p):
            try:
                with open(p, 'r', encoding='utf-8') as f:
                    txt = f.read(max_chars)
                parts.append({'path': p, 'snippet': txt[:max_chars]})
            except Exception:
                parts.append({'path': p})
        else:
            parts.append({'path': p, 'missing': True})
    return parts


def _hash_text(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


# CLI

def main():
    p = argparse.ArgumentParser(description='agent-utils: safe coordination helpers')
    sub = p.add_subparsers(dest='cmd')

    sp = sub.add_parser('create-task')
    sp.add_argument('--task-id', required=True)
    sp.add_argument('--leader', required=True)
    sp.add_argument('--spawn-budget', type=int, default=2000)
    sp.add_argument('--spawn-limit', type=int, default=3)

    sp = sub.add_parser('read-task')
    sp.add_argument('--task-id', required=True)

    sp = sub.add_parser('validate-spawn')
    sp.add_argument('--task-id', required=True)
    sp.add_argument('--requester', required=True)
    sp.add_argument('--tokens-needed', type=int, required=True)
    sp.add_argument('--workers', type=int, default=1)

    sp = sub.add_parser('reserve-spawn')
    sp.add_argument('--task-id', required=True)
    sp.add_argument('--tokens', type=int, required=True)
    sp.add_argument('--worker-ids', nargs='*')

    sp = sub.add_parser('record-result')
    sp.add_argument('--task-id', required=True)
    sp.add_argument('--worker-id', required=True)
    sp.add_argument('--summary', required=True)

    sp = sub.add_parser('append-cost')
    sp.add_argument('--task-id', required=True)
    sp.add_argument('--agent-id', required=True)
    sp.add_argument('--model', required=True)
    sp.add_argument('--tokens-in', type=int, required=True)
    sp.add_argument('--tokens-out', type=int, required=True)
    sp.add_argument('--prompt-hash')

    args = p.parse_args()
    if args.cmd == 'create-task':
        art = create_task(args.task_id, args.leader, spawn_budget_tokens=args.spawn_budget, spawn_limit=args.spawn_limit)
        print(json.dumps(art))
    elif args.cmd == 'read-task':
        print(json.dumps(read_task(args.task_id)))
    elif args.cmd == 'validate-spawn':
        ok, reason = validate_spawn(args.task_id, args.requester, args.tokens_needed, args.workers)
        print(json.dumps({'ok': ok, 'reason': reason}))
    elif args.cmd == 'reserve-spawn':
        art = reserve_spawn_budget(args.task_id, args.tokens, worker_ids=args.worker_ids)
        print(json.dumps(art))
    elif args.cmd == 'record-result':
        rec = {'summary': args.summary}
        record_worker_result(args.task_id, args.worker_id, rec)
        print('ok')
    elif args.cmd == 'append-cost':
        entry = append_cost_log(args.task_id, args.agent_id, args.model, args.tokens_in, args.tokens_out, prompt_hash=args.prompt_hash)
        print(json.dumps(entry))
    else:
        p.print_help()


if __name__ == '__main__':
    main()
