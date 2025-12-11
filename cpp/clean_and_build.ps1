# Quick script to clean and rebuild from scratch

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Clean and Build Script" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "This will:" -ForegroundColor Yellow
Write-Host "1. Delete the entire build folder" -ForegroundColor White
Write-Host "2. Run a fresh build" -ForegroundColor White
Write-Host ""
Write-Host "WARNING: This will delete all files in the build folder!" -ForegroundColor Red
Write-Host ""

$confirm = Read-Host "Continue? (Y/N)"
if ($confirm -ne "Y" -and $confirm -ne "y") {
    Write-Host "Cancelled." -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "Cleaning build folder..." -ForegroundColor Cyan
$buildDir = Join-Path $PSScriptRoot "build"
if (Test-Path $buildDir) {
    Remove-Item -Recurse -Force $buildDir
    Write-Host "Build folder deleted." -ForegroundColor Green
} else {
    Write-Host "Build folder doesn't exist (nothing to clean)." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Starting fresh build..." -ForegroundColor Cyan
Write-Host ""

& (Join-Path $PSScriptRoot "build.ps1")

Write-Host ""
Write-Host "Done!" -ForegroundColor Green
