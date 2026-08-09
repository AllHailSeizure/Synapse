<#
.SYNOPSIS
Build importable Cursor automation JSON from the generic prompt sources.

.DESCRIPTION
The prompts in prompts/*.md are repo-agnostic — they read SYNAPSE.md from
whatever repo they run against. The only thing that binds an automation to a
repo is its trigger, so that is the only thing this script generates.

Prompts live as markdown rather than inside the JSON because a 20KB prompt
stored as a single escaped string produces unreadable diffs, and these get
edited far more often than they get imported.

.PARAMETER Repo
Target repository as owner/name.

.PARAMETER Label
Human-readable suffix for the automation name. Defaults to the repo name.

.PARAMETER OutDir
Where to write the JSON. Defaults to build/<repo-name>/ beside this script.

.EXAMPLE
./Build-Automations.ps1 -Repo AllHailSeizure/hotel-kline-game -Label "Hotel Kline"
#>
param(
  [Parameter(Mandatory)][ValidatePattern('^[^/]+/[^/]+$')][string]$Repo,
  [string]$Label,
  [string]$OutDir
)

$ErrorActionPreference = 'Stop'
$here = $PSScriptRoot
$owner, $repoName = $Repo -split '/', 2
if (-not $Label) { $Label = $repoName }
if (-not $OutDir) { $OutDir = Join-Path $here "build\$repoName" }
$repoUrl = "https://github.com/$Repo"

function Read-Frontmatter($path) {
  $lines = Get-Content $path
  if ($lines[0].Trim() -ne '---') { throw "$path has no frontmatter" }
  $end = 1; while ($lines[$end].Trim() -ne '---') { $end++ }
  $fm = @{}; $key = $null; $folded = @()
  foreach ($line in $lines[1..($end - 1)]) {
    if ($line -match '^(\w[\w.-]*):\s*(.*)$') {
      if ($key) { $fm[$key] = ($folded -join ' ').Trim(); $folded = @() }
      $key, $val = $Matches[1], $Matches[2].Trim()
      if ($val -eq '>-' -or $val -eq '>' -or $val -eq '') { continue }
      $fm[$key] = $val.Trim('"'); $key = $null
    } elseif ($key) {
      $folded += $line.Trim()
    }
  }
  if ($key) { $fm[$key] = ($folded -join ' ').Trim() }
  $body = ($lines[($end + 1)..($lines.Count - 1)] -join "`n").Trim()
  return @{ Meta = $fm; Body = $body }
}

function New-Trigger($type, $contains) {
  $inner = [ordered]@{ repos = @($repoUrl); commentContains = $contains }
  switch ($type) {
    'issueComment' { return @{ git = @{ issueComment = $inner } } }
    'pullRequestReviewComment' { return @{ git = @{ pullRequestReviewComment = $inner } } }
    'pullRequest' {
      # prAction 4 = commented. Allowlist keeps a stray mention from a bot or
      # outside contributor from spending a run.
      $inner['repo'] = $repoUrl
      $inner['prAction'] = 4
      $inner['commenterAllowlist'] = @($owner)
      return @{ git = @{ pullRequest = $inner } }
    }
    default { throw "unknown trigger type '$type'" }
  }
}

New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
Write-Host "repo:   $Repo"
Write-Host "output: $OutDir`n"

foreach ($src in Get-ChildItem (Join-Path $here 'prompts') -Filter '*.md' | Sort-Object Name) {
  $parsed = Read-Frontmatter $src.FullName
  $m = $parsed.Meta
  foreach ($required in 'name', 'trigger', 'contains', 'model') {
    if (-not $m[$required]) { throw "$($src.Name): frontmatter missing '$required'" }
  }

  $automation = [ordered]@{
    name                 = "$($m.name): $Label"
    triggers             = @(New-Trigger $m.trigger $m.contains)
    actions              = @(@{ prComment = @{} })
    prompts              = @(@{ prompt = $parsed.Body })
    model                = $m.model
    memoryEnabled        = $true
    disabledDefaultTools = @()
    scope                = 'private'
  }
  if ($m.description) { $automation.Insert(1, 'description', $m.description) }

  $out = Join-Path $OutDir ($src.BaseName + '.json')
  $automation | ConvertTo-Json -Depth 12 | Set-Content $out -Encoding utf8
  Write-Host ("  {0,-22} {1,6:N1} KB  requires: {2}" -f $src.BaseName, ((Get-Item $out).Length / 1KB), $m.requires)
}

Write-Host "`nImport these into Cursor. The target repo needs a SYNAPSE.md at its root"
Write-Host "or every run stops at Gate 0 - see docs/TEMPLATES/SYNAPSE.md."
