<#
.SYNOPSIS
Link this repo's skills and commands into ~/.claude so they load in every project.

.DESCRIPTION
Claude Code discovers personal skills flat, as ~/.claude/skills/<name>/SKILL.md,
so each skill directory needs its own junction — a single junction of skills/
would nest everything one level too deep and nothing would load.

Junctions (not symlinks) are used deliberately: they work on Windows without
admin rights or developer mode.

Re-run after adding or removing a skill. Existing Synapse junctions are replaced;
real directories are never touched.

.PARAMETER Remove
Remove the junctions instead of creating them.
#>
param([switch]$Remove)

$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
$skillsHome = Join-Path $env:USERPROFILE '.claude\skills'
$commandsHome = Join-Path $env:USERPROFILE '.claude\commands'

function Test-Junction($path) {
  (Test-Path $path) -and ((Get-Item $path -Force).LinkType -in @('Junction', 'SymbolicLink'))
}

function Set-Link($link, $target) {
  if (Test-Junction $link) {
    Remove-Item $link -Force
  } elseif (Test-Path $link) {
    Write-Warning "$link exists and is a real directory - skipping"
    return
  }
  if (-not $Remove) {
    New-Item -ItemType Junction -Path $link -Target $target | Out-Null
    Write-Host "  linked $(Split-Path $link -Leaf)"
  } else {
    Write-Host "  removed $(Split-Path $link -Leaf)"
  }
}

New-Item -ItemType Directory -Force -Path $skillsHome, $commandsHome | Out-Null

Write-Host 'skills:'
foreach ($skill in Get-ChildItem (Join-Path $repo 'skills') -Directory) {
  Set-Link (Join-Path $skillsHome $skill.Name) $skill.FullName
}

Write-Host 'commands:'
Set-Link (Join-Path $commandsHome 'synapse') (Join-Path $repo 'commands')

Write-Host ''
Write-Host $(if ($Remove) { 'Unlinked.' } else { 'Linked. Restart Claude Code to pick up changes.' })
