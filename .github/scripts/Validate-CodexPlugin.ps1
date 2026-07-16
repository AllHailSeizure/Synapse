$manifestPath = '.codex-plugin/plugin.json'

if (-not (Test-Path -LiteralPath $manifestPath)) {
  throw "Missing $manifestPath"
}

$manifest = Get-Content -Raw -LiteralPath $manifestPath | ConvertFrom-Json

foreach ($field in 'name', 'version', 'description', 'skills') {
  if ([string]::IsNullOrWhiteSpace([string]$manifest.$field)) {
    throw "Missing manifest field: $field"
  }
}

if ($manifest.version -notmatch '^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$') {
  throw 'version must be strict semver'
}

if ($null -eq $manifest.author -or [string]::IsNullOrWhiteSpace([string]$manifest.author.name)) {
  throw 'Missing manifest field: author.name'
}

if ($null -eq $manifest.interface) {
  throw 'Missing manifest field: interface'
}

foreach ($field in 'displayName', 'shortDescription', 'longDescription', 'developerName', 'category', 'defaultPrompt') {
  if ($null -eq $manifest.interface.$field -or [string]::IsNullOrWhiteSpace([string]$manifest.interface.$field)) {
    throw "Missing interface field: $field"
  }
}

if ($manifest.interface.capabilities -isnot [System.Array]) {
  throw 'interface.capabilities must be an array'
}

if (-not (Test-Path -LiteralPath $manifest.skills)) {
  throw "Skills path does not exist: $($manifest.skills)"
}

Write-Host 'Codex plugin manifest is valid.'
