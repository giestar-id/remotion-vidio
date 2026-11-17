# =====================================================================
# Skrip Render Duo: Orang Indonesia Pertama & Sejarah Majapahit
# Tanpa menu opsional - langsung merender kedua video secara berurutan
# =====================================================================

$ErrorActionPreference = "Stop"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  MEMULAI RENDER DUO: ORANG INDO PERTAMA & MAJAPAHIT" -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Cyan

# Pastikan direktori out tersedia
if (-not (Test-Path "out")) {
    New-Item -ItemType Directory -Path "out" -Force | Out-Null
}

$startTime = Get-Date

# ---------------------------------------------------------------------
# 1. RENDER ORANG INDONESIA PERTAMA (Stickman ~5,12 Menit / 9.216 Frame)
# ---------------------------------------------------------------------
Write-Host ""
Write-Host "[1/2] Merender Video: OrangIndoPertama (Stickman)" -ForegroundColor Green
Write-Host "      Target Output: out/orang_indo_pertama_full.mp4" -ForegroundColor Gray
$t1 = Get-Date
npx remotion render OrangIndoPertama out/orang_indo_pertama_full.mp4
$dur1 = [math]::Round(((Get-Date) - $t1).TotalMinutes, 2)
Write-Host "      [OK] OrangIndoPertama selesai dalam $dur1 menit!" -ForegroundColor Green

# ---------------------------------------------------------------------
# 2. RENDER SEJARAH MAJAPAHIT (Dokumenter ~10,53 Menit / 18.952 Frame)
# ---------------------------------------------------------------------
Write-Host ""
Write-Host "[2/2] Merender Video: SejarahMajapahit (Dokumenter Sejarah)" -ForegroundColor Green
Write-Host "      Target Output: out/sejarah_majapahit_full.mp4" -ForegroundColor Gray
$t2 = Get-Date
npx remotion render SejarahMajapahit out/sejarah_majapahit_full.mp4
$dur2 = [math]::Round(((Get-Date) - $t2).TotalMinutes, 2)
Write-Host "      [OK] SejarahMajapahit selesai dalam $dur2 menit!" -ForegroundColor Green

$totalDur = [math]::Round(((Get-Date) - $startTime).TotalMinutes, 2)
Write-Host ""
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  SEMUA RENDER SELESAI DENGAN SUKSES! (Total: $totalDur menit)" -ForegroundColor Yellow
Write-Host "  1. out/orang_indo_pertama_full.mp4" -ForegroundColor White
Write-Host "  2. out/sejarah_majapahit_full.mp4" -ForegroundColor White
Write-Host "==========================================================" -ForegroundColor Cyan
