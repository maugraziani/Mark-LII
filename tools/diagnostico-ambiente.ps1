param(
    [string]$ProjectPath = "C:\Users\mauri\Projetos\jarvis-mark52"
)

$ErrorActionPreference = "Continue"

function Write-Check {
    param(
        [string]$Name,
        [bool]$Ok,
        [string]$Details
    )
    $status = if ($Ok) { "OK" } else { "NOK" }
    $color = if ($Ok) { "Green" } else { "Red" }
    Write-Host ("[{0}] {1} - {2}" -f $status, $Name, $Details) -ForegroundColor $color
}

Write-Host "`n=== JARVIS MARK 52 - DIAGNOSTICO DE AMBIENTE ===" -ForegroundColor Cyan
Write-Host "Data: $(Get-Date -Format 'dd/MM/yyyy HH:mm:ss')"
Write-Host "Projeto: $ProjectPath`n"

# 1. Pasta do projeto
$projectExists = Test-Path $ProjectPath
Write-Check "Pasta do projeto" $projectExists $ProjectPath
if (-not $projectExists) {
    Write-Host "`nDiagnostico interrompido: a pasta do projeto nao foi encontrada." -ForegroundColor Yellow
    exit 2
}

Set-Location $ProjectPath

# 2. Arquivos essenciais
$essential = @(
    "main.py",
    "ui.py",
    "requirements.txt",
    "setup.py",
    "core",
    "actions",
    "plugins",
    "memory",
    "dashboard"
)
foreach ($item in $essential) {
    $exists = Test-Path (Join-Path $ProjectPath $item)
    Write-Check "Estrutura: $item" $exists $(if ($exists) { "presente" } else { "ausente" })
}

# 3. Git
$git = Get-Command git -ErrorAction SilentlyContinue
Write-Check "Git" ($null -ne $git) $(if ($git) { (& git --version) } else { "nao encontrado no PATH" })
if ($git) {
    $insideRepo = (& git rev-parse --is-inside-work-tree 2>$null) -eq "true"
    Write-Check "Repositorio Git" $insideRepo $(if ($insideRepo) { "valido" } else { "pasta nao reconhecida como repositorio" })

    if ($insideRepo) {
        $branch = (& git branch --show-current 2>$null).Trim()
        Write-Check "Branch atual" ($branch -eq "jarvis-dev") $("atual: {0}; esperado para desenvolvimento: jarvis-dev" -f $branch)

        $remote = (& git remote get-url origin 2>$null).Trim()
        $remoteOk = $remote -match "maugraziani/Mark-LII"
        Write-Check "Remote origin" $remoteOk $remote

        $dirty = (& git status --porcelain 2>$null)
        Write-Check "Working tree" ([string]::IsNullOrWhiteSpace(($dirty -join ""))) $(if ($dirty) { "ha alteracoes locais nao commitadas" } else { "limpo" })
    }
}

# 4. Python
$pythonCmd = $null
foreach ($candidate in @("python", "py")) {
    $cmd = Get-Command $candidate -ErrorAction SilentlyContinue
    if ($cmd) { $pythonCmd = $candidate; break }
}

Write-Check "Python" ($null -ne $pythonCmd) $(if ($pythonCmd) { (& $pythonCmd --version 2>&1) } else { "nao encontrado no PATH" })

if ($pythonCmd) {
    $versionText = (& $pythonCmd -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')" 2>$null).Trim()
    $parts = $versionText.Split('.')
    $versionOk = $false
    if ($parts.Count -ge 2) {
        $major = [int]$parts[0]
        $minor = [int]$parts[1]
        $versionOk = ($major -eq 3 -and $minor -ge 10)
    }
    Write-Check "Python >= 3.10" $versionOk $versionText

    $pipOk = $false
    try {
        $pipVersion = (& $pythonCmd -m pip --version 2>&1)
        $pipOk = $LASTEXITCODE -eq 0
    } catch {}
    Write-Check "pip" $pipOk $(if ($pipOk) { $pipVersion } else { "pip indisponivel" })
}

# 5. Virtual environment
$venvCandidates = @(".venv", "venv")
$venvFound = $null
foreach ($v in $venvCandidates) {
    if (Test-Path (Join-Path $ProjectPath $v)) { $venvFound = $v; break }
}
Write-Check "Virtual environment" ($null -ne $venvFound) $(if ($venvFound) { "encontrado: $venvFound" } else { "nao encontrado - recomendado criar .venv antes da instalacao" })

# 6. Chave/API e configuracao - apenas nomes, nunca valores
$envNames = @("GEMINI_API_KEY", "GOOGLE_API_KEY")
foreach ($name in $envNames) {
    $value = [Environment]::GetEnvironmentVariable($name, "Process")
    if (-not $value) { $value = [Environment]::GetEnvironmentVariable($name, "User") }
    if (-not $value) { $value = [Environment]::GetEnvironmentVariable($name, "Machine") }
    Write-Check "Variavel $name" (-not [string]::IsNullOrWhiteSpace($value)) $(if ($value) { "definida" } else { "nao definida" })
}

# 7. Dependencias instaladas - checagem nao destrutiva
if ($pythonCmd -and (Test-Path "$ProjectPath\requirements.txt")) {
    Write-Host "`n--- Checagem de dependencias Python ---" -ForegroundColor Cyan
    $imports = @(
        @{Name="PyQt6"; Import="PyQt6"},
        @{Name="sounddevice"; Import="sounddevice"},
        @{Name="google-genai"; Import="google.genai"},
        @{Name="Pillow"; Import="PIL"},
        @{Name="requests"; Import="requests"},
        @{Name="playwright"; Import="playwright"},
        @{Name="opencv-python"; Import="cv2"},
        @{Name="numpy"; Import="numpy"},
        @{Name="psutil"; Import="psutil"},
        @{Name="fastapi"; Import="fastapi"},
        @{Name="uvicorn"; Import="uvicorn"},
        @{Name="pywin32"; Import="win32api"}
    )
    foreach ($dep in $imports) {
        & $pythonCmd -c "import $($dep.Import)" 2>$null
        Write-Check "Python: $($dep.Name)" ($LASTEXITCODE -eq 0) $(if ($LASTEXITCODE -eq 0) { "import OK" } else { "nao instalado ou import falhou" })
    }
}

Write-Host "`n=== FIM DO DIAGNOSTICO ===" -ForegroundColor Cyan
Write-Host "Este script nao instala, altera ou remove nada do ambiente.`n"
