# tools/blender.ps1 — безопасный запуск Blender (Ф2.9, Ф3.1)
#
# Зачем: Blender без ограничений ест CPU на 99 % и подвешивает машину.
# Правила: --threads 2 и BelowNormal. Никогда не запускать blender.exe напрямую.
#
# Запуск:
#   pwsh -File tools/blender.ps1 -Script blender/blockout.py
#   pwsh -File tools/blender.ps1 -Script blender/hero_export.py -- --all
param(
  [Parameter(Mandatory = $true)][string]$Script,
  [string[]]$ScriptArgs = @(),
  [switch]$Background
)

$ErrorActionPreference = 'Continue'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

$blender = Join-Path $root 'tools\blender\blender-4.5.15-windows-x64\blender.exe'
if (-not (Test-Path -LiteralPath $blender)) {
  Write-Host "[!!] Blender не найден: $blender" -ForegroundColor Red
  Write-Host "     Восстановить: ../_ThreeHorizons_archive_2026-11-10/tools/blender/" -ForegroundColor Yellow
  exit 1
}

$scriptPath = if ([System.IO.Path]::IsPathRooted($Script)) { $Script } else { Join-Path $root $Script }
if (-not (Test-Path -LiteralPath $scriptPath)) {
  Write-Host "[!!] Скрипт не найден: $scriptPath" -ForegroundColor Red
  exit 1
}

# приоритет процесса — ниже обычного, чтобы не мешать работе
$proc = Start-Process -FilePath $blender `
  -ArgumentList (@('--background', '--threads', '2', '--python', $scriptPath) + $ScriptArgs) `
  -NoNewWindow -PassThru -Wait

# Blender на Windows не всегда возвращает код через Start-Process — дублируем проверкой вывода
$code = $proc.ExitCode
if ($code -ne 0) { Write-Host "[!!] Blender завершился с кодом $code" -ForegroundColor Red }
else { Write-Host "[OK] Blender: $Script" -ForegroundColor Green }
exit $code
