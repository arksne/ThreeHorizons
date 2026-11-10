# tools/backup.ps1 — снимок проекта в backups/ (Ф0.9)
# Запуск: pwsh -File tools/backup.ps1 [-Note "перед Ф4"]
param([string]$Note = "")

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

$verRaw = Get-Content (Join-Path $root 'version.json') -Raw
$ver = ($verRaw | ConvertFrom-Json).version
$day = Get-Date -Format 'yyyy-MM-dd'
$name = "v$ver`_$day"
$dest = Join-Path $root "backups\$name"
New-Item -ItemType Directory -Force -Path $dest | Out-Null

$targets = @('docs', 'GAME_DESIGN', 'ROBLOX_IMPLEMENTATION\src', 'tools', 'tests')
$stamp = Get-Date -Format 'yyyy-MM-dd HH:mm'
Set-Content -Path (Join-Path $dest 'BACKUP.txt') -Value @(
  "version: $ver"
  "date: $stamp"
  "note: $Note"
) -Encoding utf8

foreach ($t in $targets) {
  $src = Join-Path $root $t
  if (-not (Test-Path -LiteralPath $src)) { Write-Host "[--] нет $t" -ForegroundColor DarkGray; continue }
  $to = Join-Path $dest $t
  New-Item -ItemType Directory -Force -Path $to | Out-Null
  Copy-Item -Path (Join-Path $src '*') -Destination $to -Recurse -Force -ErrorAction SilentlyContinue
  Write-Host "[OK] $t" -ForegroundColor Green
}

Copy-Item -Path (Join-Path $root 'version.json') -Destination $dest -Force -ErrorAction SilentlyContinue
# вендорные бинарники в бэкап не тянем (Blender/Luau — восстанавливаются отдельно)
Remove-Item (Join-Path $dest 'tools\luau') -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item (Join-Path $dest 'tools\blender') -Recurse -Force -ErrorAction SilentlyContinue
$free = Get-ChildItem $dest -Recurse -File | Measure-Object -Property Length -Sum
Write-Host ""
Write-Host ("backup: {0}  ({1:N1} MB)" -f $dest, ($free.Sum / 1MB)) -ForegroundColor Cyan
