[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $repoRoot

$venvPython = Join-Path $repoRoot ".venv\Scripts\python.exe"
if (Test-Path -LiteralPath $venvPython) {
    $pythonExe = $venvPython
} else {
    $pythonExe = (Get-Command python -ErrorAction Stop).Source
}

$nodeExe = (Get-Command node -ErrorAction Stop).Source

$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

function Invoke-Step {
    param(
        [Parameter(Mandatory)]
        [string]$Label,
        [Parameter(Mandatory)]
        [scriptblock]$Action
    )

    Write-Host "==> $Label"
    & $Action
    if ($LASTEXITCODE -ne 0) {
        throw "$Label failed with exit code $LASTEXITCODE"
    }
}

function Invoke-PythonStep {
    param(
        [Parameter(Mandatory)]
        [string]$Label,
        [Parameter(Mandatory)]
        [string[]]$Arguments
    )

    Invoke-Step -Label $Label -Action {
        & $script:pythonExe @Arguments
    }
}

Invoke-Step -Label "Validate example scene" -Action {
    & $nodeExe "scripts\validate.js" "examples\shoply-scene.js"
}
Invoke-Step -Label "CLI version" -Action {
    & $nodeExe "bin\cli.js" "--version"
}
Invoke-Step -Label "CLI help" -Action {
    & $nodeExe "bin\cli.js" "--help"
}
Invoke-PythonStep -Label "Compile fork Python" -Arguments @(
    "-m", "compileall", "-q", "tools", "tests"
)
Invoke-PythonStep -Label "Ruff (E9 + F)" -Arguments @(
    "-m", "ruff", "check", "--select", "E9,F", "tools", "tests"
)
Invoke-PythonStep -Label "Pytest" -Arguments @("-m", "pytest", "tests", "-q")
Invoke-PythonStep -Label "Check fork Markdown links" -Arguments @(
    "tools\check_links.py"
)

Write-Host "WINDOWS DEV CHECK GREEN"
