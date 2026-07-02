import { describe, expect, it } from 'vitest';
import { parseOwnerRepoFromRemoteUrl } from '../src/github/repoContext';

describe('parseOwnerRepoFromRemoteUrl', () => {
  it('parses an SSH remote URL with .git suffix', () => {
    expect(parseOwnerRepoFromRemoteUrl('git@github.com:AllHailSeizure/Synapse.git')).toEqual({
      owner: 'AllHailSeizure',
      repo: 'Synapse',
    });
  });

  it('parses an SSH remote URL without .git suffix', () => {
    expect(parseOwnerRepoFromRemoteUrl('git@github.com:AllHailSeizure/Synapse')).toEqual({
      owner: 'AllHailSeizure',
      repo: 'Synapse',
    });
  });

  it('parses an HTTPS remote URL with .git suffix', () => {
    expect(parseOwnerRepoFromRemoteUrl('https://github.com/AllHailSeizure/Synapse.git')).toEqual({
      owner: 'AllHailSeizure',
      repo: 'Synapse',
    });
  });

  it('parses an HTTPS remote URL without .git suffix', () => {
    expect(parseOwnerRepoFromRemoteUrl('https://github.com/AllHailSeizure/Synapse')).toEqual({
      owner: 'AllHailSeizure',
      repo: 'Synapse',
    });
  });

  it('returns null for a non-GitHub remote URL', () => {
    expect(parseOwnerRepoFromRemoteUrl('git@gitlab.com:someone/somewhere.git')).toBeNull();
  });

  it('returns null for a malformed URL', () => {
    expect(parseOwnerRepoFromRemoteUrl('not a url')).toBeNull();
  });
});
