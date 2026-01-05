$ErrorActionPreference = "Stop"

if (-not $env:MODEL_URL -or -not $env:MODEL_DIR) {
  Write-Error "MODEL_URL and MODEL_DIR must be set"
  exit 1
}

$modelDir = $env:MODEL_DIR
New-Item -ItemType Directory -Force -Path $modelDir | Out-Null

$uri = [System.Uri]$env:MODEL_URL
$filename = [System.IO.Path]::GetFileName($uri.AbsolutePath)
if (-not $filename) {
  Write-Error "Could not determine filename from MODEL_URL"
  exit 1
}

$outputPath = Join-Path $modelDir $filename
Invoke-WebRequest -Uri $env:MODEL_URL -OutFile $outputPath

if (-not (Test-Path $outputPath)) {
  Write-Error "Download failed: $outputPath not found"
  exit 1
}

Write-Host "Downloaded model to $outputPath"
