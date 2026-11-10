# tools/start_blender_mcp.ps1 — поднять Blender с аддоном MCP (порт 9876)
#
# Нужен, чтобы MCP-сервер Claude Code (uvx mcp-for-blender) подключился к Blender.
# Проверка:  Test-NetConnection 127.0.0.1 -Port 9876
#
# Запуск:  pwsh -File tools/start_blender_mcp.ps1
param([switch]$Headless)

$ErrorActionPreference = 'Continue'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

$blender = Join-Path $root 'tools\blender\blender-4.5.15-windows-x64\blender.exe'
if (-not (Test-Path -LiteralPath $blender)) {
  Write-Host "[!!] Blender не найден: $blender" -ForegroundColor Red
  Write-Host "     Восстановить: ../_ThreeHorizons_archive_2026-11-10/tools/blender/" -ForegroundColor Yellow
  exit 1
}

$existing = Get-NetTCPConnection -LocalPort 9876 -ErrorAction SilentlyContinue
if ($existing) {
  Write-Host "[OK] Порт 9876 уже занят (pid $($existing.OwningProcess)) — Blender уже поднят" -ForegroundColor Green
  exit 0
}

$args = @('--threads', '2')
if (-not $Headless) { $args += @('--python', (Join-Path $root 'tools\start_blender_mcp.py')) }
else { $args += @('--background', '--python', (Join-Path $root 'tools\start_blender_mcp.py')) }

$p = Start-Process -FilePath $blender -ArgumentList $args -PassThru -WindowStyle Minimized
Write-Host "[OK] Blender запущен (pid $($p.Id)), ждём MCP-сокет…"

$deadline = (Get-Date).AddSeconds(60)
while ((Get-Date) -lt $deadline) {
  $c = Get-NetTCPConnection -LocalPort 9876 -ErrorAction SilentlyContinue
  if ($c) {
    Write-Host "[OK] MCP-сокет слушает 127.0.0.1:9876 — сервер Claude Code подключится сам" -ForegroundColor Green
    exit 0
  }
  if ($p.HasExited) { Write-Host "[!!] Blender упал (код $($p.ExitCode))" -ForegroundColor Red; exit 1 }
  Start-Sleep -Milliseconds 700
}
Write-Host "[!!] Сокет не поднялся за 60 с" -ForegroundColor Red
exit 1
