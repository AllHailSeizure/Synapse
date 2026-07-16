param(
  [ValidateSet('claude-release', 'codex-release')]
  [string]$TargetBranch,
  [string[]]$ChangedPath,
  [switch]$SelfTest
)

if ($SelfTest) {
  $cases = @(
    @{ Branch = 'claude-release'; Paths = @('.claude-plugin/plugin.json', 'skills/goal-oriented-development/SKILL.md', 'README.md'); Pass = $true },
    @{ Branch = 'claude-release'; Paths = @('.codex-plugin/plugin.json'); Pass = $false },
    @{ Branch = 'codex-release'; Paths = @('.codex/agents/synapse/goal-writer.toml', 'AGENTS.md', 'docs/spec.md'); Pass = $true },
    @{ Branch = 'codex-release'; Paths = @('.claude-plugin/plugin.json', 'CLAUDE.md'); Pass = $false }
  )
  foreach ($case in $cases) {
    $branch = $case['Branch']
    $paths = $case['Paths']
    $shouldPass = [bool]$case['Pass']
    & $PSCommandPath -TargetBranch $branch -ChangedPath $paths
    if (($LASTEXITCODE -eq 0) -ne $shouldPass) { throw "Unexpected policy result for $branch" }
  }
  exit 0
}

$shared = @(
  'README.md', '.gitignore', 'LICENSE', 'LICENSE.md',
  'docs/', 'skills/', '.github/'
)
$platform = @{
  'claude-release' = @('.claude-plugin/', '.claude/', 'CLAUDE.md', 'agents/')
  'codex-release' = @('.codex-plugin/', '.codex/', 'AGENTS.md')
}
$allowed = $shared + $platform[$TargetBranch]
$forbidden = $ChangedPath | Where-Object {
  $path = $_.Replace('\', '/')
  -not ($allowed | Where-Object { $path -eq $_ -or $path.StartsWith($_) })
}

if ($forbidden) {
  $forbidden | ForEach-Object { Write-Error "$_ is not allowed in $TargetBranch" }
  exit 1
}

exit 0
