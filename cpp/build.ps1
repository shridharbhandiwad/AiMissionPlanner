# Build script for Trajectory Generator C++ application (Windows PowerShell)

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Building Trajectory Generator (Windows)" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check for ONNX Runtime
if (-not $env:ONNXRUNTIME_ROOT_DIR) {
    Write-Host "Warning: ONNXRUNTIME_ROOT_DIR not set" -ForegroundColor Yellow
    Write-Host "Attempting to download ONNX Runtime for Windows..." -ForegroundColor Yellow
    
    # Create libs directory
    $libsDir = Join-Path (Split-Path $PSScriptRoot) "libs"
    if (-not (Test-Path $libsDir)) {
        New-Item -ItemType Directory -Path $libsDir | Out-Null
    }
    Set-Location $libsDir
    
    # Download ONNX Runtime if not present
    $onnxDir = "onnxruntime-win-x64-1.16.3"
    if (-not (Test-Path $onnxDir)) {
        Write-Host "Downloading ONNX Runtime 1.16.3 for Windows..." -ForegroundColor Yellow
        $onnxUrl = "https://github.com/microsoft/onnxruntime/releases/download/v1.16.3/onnxruntime-win-x64-1.16.3.zip"
        $zipFile = "$onnxDir.zip"
        
        Invoke-WebRequest -Uri $onnxUrl -OutFile $zipFile -UseBasicParsing
        Expand-Archive -Path $zipFile -DestinationPath . -Force
        Remove-Item $zipFile
        Write-Host "ONNX Runtime downloaded" -ForegroundColor Green
    }
    
    $env:ONNXRUNTIME_ROOT_DIR = Join-Path (Get-Location) $onnxDir
    Set-Location (Join-Path (Split-Path $PSScriptRoot) "cpp")
} else {
    Write-Host "Using ONNX Runtime from: $env:ONNXRUNTIME_ROOT_DIR" -ForegroundColor Green
}

# Clean old CMake cache if it exists
$buildDir = Join-Path $PSScriptRoot "build"
if (Test-Path (Join-Path $buildDir "CMakeCache.txt")) {
    Write-Host "Cleaning old CMake cache..." -ForegroundColor Yellow
    Remove-Item (Join-Path $buildDir "CMakeCache.txt") -Force -ErrorAction SilentlyContinue
    Remove-Item (Join-Path $buildDir "CMakeFiles") -Recurse -Force -ErrorAction SilentlyContinue
}

# Create build directory
if (-not (Test-Path $buildDir)) {
    New-Item -ItemType Directory -Path $buildDir | Out-Null
}
Set-Location $buildDir

# Detect generator
Write-Host ""
Write-Host "Running CMake..." -ForegroundColor Cyan

# Try to use Ninja if available, otherwise use default generator
$generator = ""
$ninjaPath = Get-Command ninja -ErrorAction SilentlyContinue
if ($ninjaPath) {
    $generator = "-G Ninja"
    Write-Host "Using Ninja build system" -ForegroundColor Green
} else {
    Write-Host "Using default CMake generator" -ForegroundColor Yellow
}

# Run CMake
$cmakeArgs = @(
    $generator,
    "-DCMAKE_BUILD_TYPE=Release",
    "-DONNXRUNTIME_ROOT_DIR=$env:ONNXRUNTIME_ROOT_DIR",
    ".."
) | Where-Object { $_ -ne "" }

& cmake $cmakeArgs

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "CMake configuration failed!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please ensure you have:" -ForegroundColor Yellow
    Write-Host "  1. CMake installed (version 3.15 or higher)" -ForegroundColor Yellow
    Write-Host "  2. A C++ compiler (Visual Studio, MinGW, or Clang)" -ForegroundColor Yellow
    Write-Host "  3. CMake and your compiler in your PATH" -ForegroundColor Yellow
    Write-Host ""
    Set-Location ..
    exit 1
}

# Build
Write-Host ""
Write-Host "Building..." -ForegroundColor Cyan
cmake --build . --config Release

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Build failed!" -ForegroundColor Red
    Set-Location ..
    exit 1
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host "Build complete!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Executables:" -ForegroundColor Cyan
Write-Host "  - trajectory_app.exe  (Main application)" -ForegroundColor White
Write-Host "  - trajectory_demo.exe (Demo/test application)" -ForegroundColor White
Write-Host ""
Write-Host "To run:" -ForegroundColor Cyan
Write-Host "  cd build" -ForegroundColor White
Write-Host "  .\trajectory_app.exe --help" -ForegroundColor White
Write-Host ""

Set-Location ..
