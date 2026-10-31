# Script untuk menghasilkan file LAPORAN.pdf secara otomatis
$htmlPath = (Resolve-Path "laporan.html").Path
$pdfPath = Join-Path (Get-Location) "LAPORAN.pdf"

$edgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
$chromePath = "C:\Program Files\Google\Chrome\Application\chrome.exe"

if (Test-Path $edgePath) {
    Write-Host "Mengonversi laporan.html ke LAPORAN.pdf menggunakan Microsoft Edge..." -ForegroundColor Cyan
    & $edgePath --headless --disable-gpu --run-all-compositor-stages-before-draw --print-to-pdf="$pdfPath" "$htmlPath"
} elseif (Test-Path $chromePath) {
    Write-Host "Mengonversi laporan.html ke LAPORAN.pdf menggunakan Google Chrome..." -ForegroundColor Cyan
    & $chromePath --headless --disable-gpu --run-all-compositor-stages-before-draw --print-to-pdf="$pdfPath" "$htmlPath"
} else {
    Write-Host "Edge/Chrome tidak ditemukan. Silakan buka laporan.html di browser dan tekan Ctrl+P -> Save as PDF." -ForegroundColor Yellow
    exit 1
}

Start-Sleep -Seconds 1
if (Test-Path $pdfPath) {
    Write-Host "Berhasil! File PDF tersimpan di: $pdfPath" -ForegroundColor Green
}

