# =============================================================================
# deploy.ps1 — Log Solutions | Script di versioning e deploy automatico
# =============================================================================
# Uso:
#   .\deploy.ps1                          → incrementa versione e fa commit+push
#   .\deploy.ps1 -Messaggio "Fix login"   → usa messaggio personalizzato
#   .\deploy.ps1 -SoloBump                → solo bump versione, senza git
#   .\deploy.ps1 -Major                   → incrementa versione major (es. 1.33 → 2.0)
# =============================================================================

param(
    [string]  $Messaggio  = "",
    [switch]  $SoloBump,
    [switch]  $Major
)

$ErrorActionPreference = "Stop"
$frontendPath = Join-Path $PSScriptRoot "frontend"
$swFile       = Join-Path $frontendPath "sw.js"

# ─── 1. LEGGI VERSIONE ATTUALE ────────────────────────────────────────────────
$swContent = Get-Content $swFile -Raw
if ($swContent -notmatch "CACHE_NAME = 'log-solution-v(\d+)\.(\d+)'") {
    Write-Error "❌ Impossibile trovare CACHE_NAME in sw.js"
    exit 1
}

$vMajor = [int]$Matches[1]
$vMinor = [int]$Matches[2]

if ($Major) {
    $newMajor = $vMajor + 1
    $newMinor = 0
} else {
    $newMajor = $vMajor
    $newMinor = $vMinor + 1
}

$oldVersion = "$vMajor.$vMinor"
$newVersion = "$newMajor.$newMinor"

Write-Host ""
Write-Host "======================================================" -ForegroundColor Cyan
Write-Host "  Log Solutions — Deploy automatico" -ForegroundColor Cyan
Write-Host "  Versione: v$oldVersion  →  v$newVersion" -ForegroundColor Yellow
Write-Host "======================================================" -ForegroundColor Cyan
Write-Host ""

# ─── 2. AGGIORNA sw.js (CACHE_NAME) ──────────────────────────────────────────
Write-Host "📦 Aggiorno sw.js..." -ForegroundColor Green
$swContent = $swContent -replace "log-solution-v$oldVersion", "log-solution-v$newVersion"
Set-Content $swFile -Value $swContent -NoNewline -Encoding UTF8

# ─── 3. AGGIORNA ?v= IN TUTTI I FILE HTML E JS ───────────────────────────────
Write-Host "🔄 Aggiorno query string ?v= in HTML e JS..." -ForegroundColor Green

$htmlFiles = Get-ChildItem $frontendPath -Filter "*.html"
$jsFiles   = Get-ChildItem $frontendPath -Filter "*.js" | Where-Object { $_.Name -ne "sw.js" }
$allFiles  = @($htmlFiles) + @($jsFiles)

$count = 0
foreach ($f in $allFiles) {
    $content = Get-Content $f.FullName -Raw
    $updated = $content -replace "v=$oldVersion", "v=$newVersion"
    if ($updated -ne $content) {
        Set-Content $f.FullName -Value $updated -NoNewline -Encoding UTF8
        Write-Host "   ✅ $($f.Name)" -ForegroundColor Gray
        $count++
    }
}

# ─── 4. AGGIORNA APP_VERSION IN script.js ────────────────────────────────────
$scriptJs = Join-Path $frontendPath "script.js"
$jsContent = Get-Content $scriptJs -Raw
$jsUpdated = $jsContent `
    -replace 'APP_VERSION = "' + $oldVersion + '"', 'APP_VERSION = "' + $newVersion + '"' `
    -replace '// script\.js - v' + $oldVersion, '// script.js - v' + $newVersion
Set-Content $scriptJs -Value $jsUpdated -NoNewline -Encoding UTF8

Write-Host ""
Write-Host "✅ Versione aggiornata in $count file." -ForegroundColor Green

# ─── 5. GIT COMMIT + PUSH (se non --SoloBump) ────────────────────────────────
if (-not $SoloBump) {
    $msg = if ($Messaggio -ne "") { $Messaggio } else { "Release v$newVersion" }

    Write-Host ""
    Write-Host "🚀 Git commit + push..." -ForegroundColor Yellow
    Write-Host "   Messaggio: $msg" -ForegroundColor Gray

    Push-Location $PSScriptRoot
    try {
        git add -A
        git commit -m "[v$newVersion] $msg"
        git push
        Write-Host ""
        Write-Host "✅ Deploy completato! Versione v$newVersion pubblicata." -ForegroundColor Green
    } catch {
        Write-Warning "⚠️ Git push fallito: $_"
        Write-Host "   I file sono stati aggiornati localmente. Fai push manualmente." -ForegroundColor Yellow
    } finally {
        Pop-Location
    }
} else {
    Write-Host ""
    Write-Host "✅ Bump completato (solo locale, senza git)." -ForegroundColor Green
}

Write-Host ""
Write-Host "======================================================" -ForegroundColor Cyan
Write-Host "  Versione attiva: v$newVersion" -ForegroundColor Cyan
Write-Host "======================================================" -ForegroundColor Cyan
Write-Host ""
