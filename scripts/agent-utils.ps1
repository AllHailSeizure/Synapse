# PowerShell shim for agent-utils
# Calls the Python agent-utils CLI if Python is available.
param(
    [Parameter(ValueFromRemainingArguments=$true)]
    $Args
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$py = Get-Command python -ErrorAction SilentlyContinue
if (-not $py) {
    Write-Error "python not found in PATH. Install Python or call the module from a Python-capable runner."
    exit 1
}

$pyPath = $py.Source
$utilPath = Join-Path $scriptDir 'agent-utils.py'
if (-not (Test-Path $utilPath)) {
    Write-Error "agent-utils.py not found at $utilPath"
    exit 1
}

# Forward arguments to python script
& $pyPath $utilPath @Args
exit $LASTEXITCODE
