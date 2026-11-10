# tools/preflight.ps1 — единая проверка проекта (Ф0.6)
# Запуск:  pwsh -File tools/preflight.ps1 [-Art]
# Итог:    PREFLIGHT OK  (exit 0)  или список ошибок (exit 1)
param([switch]$Art)

$ErrorActionPreference = 'Continue'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
$fail = 0

function Resolve-Tool($known, $name) {
  if ($known -and (Test-Path -LiteralPath $known)) { return $known }
  $c = Get-Command $name -ErrorAction SilentlyContinue
  if ($c) { return $c.Source }
  return $null
}

function Skip($msg) { Write-Host "[--] $msg" -ForegroundColor DarkGray }
function Fail($msg) { Write-Host "[!!] $msg" -ForegroundColor Red; $script:fail = $script:fail + 1 }
function Pass($msg) { Write-Host "[OK] $msg" -ForegroundColor Green }

$stylua = Resolve-Tool 'D:\DSH\20-tools\stylua\stylua.exe' 'stylua'
$selene = Resolve-Tool 'D:\DSH\20-tools\selene\selene.exe' 'selene'
$rojo   = Resolve-Tool 'D:\DSH\20-tools\rojo\rojo.exe' 'rojo'
$luac   = Resolve-Tool (Join-Path $root 'tools\luau\luau-compile.exe') 'luau-compile'
$py     = Resolve-Tool 'C:\Users\ARK\AppData\Local\Programs\Python\Python312\python.exe' 'python'

$src = Join-Path $root 'ROBLOX_IMPLEMENTATION\src'
$luas = @()
if (Test-Path -LiteralPath $src) {
  $luas = @(Get-ChildItem -Path $src -Recurse -Filter *.lua -ErrorAction SilentlyContinue)
}

Write-Host ""
Write-Host "=== THREE HORIZONS preflight ===" -ForegroundColor Cyan
Write-Host ("python:  {0}" -f $py)
Write-Host ("stylua:  {0}" -f $stylua)
Write-Host ("selene:  {0}" -f $selene)
Write-Host ("rojo:    {0}" -f $rojo)
Write-Host ("luau:    {0}" -f $luac)
Write-Host ("lua-файлов в src: {0}" -f $luas.Count)
Write-Host ""

# 1. StyLua
if ($luas.Count -eq 0) { Skip "stylua — нет .lua файлов" }
elseif (-not $stylua) { Fail "stylua не найден" }
else {
  & $stylua --check $src *> $null
  if ($LASTEXITCODE -ne 0) { Fail "stylua: есть неотформатированные файлы (запустите stylua $src)" }
  else { Pass "stylua --check" }
}

# 2. selene
if ($luas.Count -eq 0) { Skip "selene — нет .lua файлов" }
elseif (-not $selene) { Fail "selene не найден" }
else {
  & $selene $src *> $null
  if ($LASTEXITCODE -ne 0) { Fail "selene: есть замечания" }
  else { Pass "selene" }
}

# 3. luau-compile
if ($luas.Count -eq 0) { Skip "luau-compile — нет .lua файлов" }
elseif (-not $luac) { Fail "luau-compile не найден" }
else {
  $bad = 0
  foreach ($f in $luas) {
    & $luac $f.FullName *> $null
    if ($LASTEXITCODE -ne 0) { Fail ("luau-compile: " + $f.FullName); $bad = $bad + 1 }
  }
  if ($bad -eq 0) { Pass ("luau-compile ({0} файлов)" -f $luas.Count) }
}

# 4. rojo build
$proj = Join-Path $root 'ROBLOX_IMPLEMENTATION\default.project.json'
if (-not (Test-Path -LiteralPath $proj)) { Skip "rojo build — нет ROBLOX_IMPLEMENTATION/default.project.json" }
elseif (-not $rojo) { Fail "rojo не найден" }
else {
  $out = Join-Path $root 'ROBLOX_IMPLEMENTATION\build\TH_dev.rbxlx'
  New-Item -ItemType Directory -Force -Path (Split-Path $out) | Out-Null
  & $rojo build $proj -o $out *> $null
  if ($LASTEXITCODE -ne 0) { Fail "rojo build" }
  else { Pass ("rojo build -> {0}" -f $out) }
}

# 5. арт (-Art)
if ($Art) {
  $val = Join-Path $root 'blender\validate_assets.py'
  $exp = Join-Path $root 'blender\export'
  if (-not (Test-Path -LiteralPath $val)) { Skip "-Art: нет blender/validate_assets.py (появится в Ф3.5)" }
  elseif (-not (Test-Path -LiteralPath $exp)) { Skip "-Art: нет blender/export" }
  elseif (-not $py) { Fail "-Art: python не найден" }
  else {
    & $py -X utf8 $val
    if ($LASTEXITCODE -ne 0) { Fail "-Art: валидатор FBX нашёл ошибки" }
    else { Pass "-Art: валидатор FBX" }
  }
}

Write-Host ""
if ($fail -eq 0) {
  Write-Host "PREFLIGHT OK" -ForegroundColor Green
  exit 0
}
Write-Host ("PREFLIGHT FAILED: {0} ошибок" -f $fail) -ForegroundColor Red
exit 1
