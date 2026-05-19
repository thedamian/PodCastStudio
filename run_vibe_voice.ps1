# VibeVoice Audio Generation Script
# This script clones VibeVoice, installs dependencies, and generates audio from podcast text

$ErrorActionPreference = 'Stop'

Write-Host "Step 1: Cloning VibeVoice repository..." -ForegroundColor Cyan
if (-not (Test-Path "VibeVoice")) {
    git clone https://github.com/vibevoice-community/VibeVoice.git
} else {
    Write-Host "VibeVoice directory already exists, skipping clone." -ForegroundColor Yellow
}

Write-Host "Step 2: Installing dependencies..." -ForegroundColor Cyan
Push-Location VibeVoice
uv pip install -e .

Write-Host "Step 3: Generating audio from podcast text..." -ForegroundColor Cyan
uv run demo/inference_from_file.py `
    --model_path vibevoice/VibeVoice-7B `
    --txt_path ..\src\02.Workflow-MultiAgent\03.Application\podcast.txt `
    --speaker_names Carter Alice

Pop-Location
Write-Host "Audio generation complete!" -ForegroundColor Green
