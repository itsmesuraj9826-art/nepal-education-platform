# Nepal Education Platform - Vercel API Deployment Script
# Run this in PowerShell: Right-click -> Run with PowerShell
# You only need to paste your Vercel token once.

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Nepal Education Platform - Vercel Deploy" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To get your token:" -ForegroundColor Yellow
Write-Host "  1. Go to https://vercel.com/account/tokens" -ForegroundColor Yellow
Write-Host "  2. Click 'Create Token'" -ForegroundColor Yellow
Write-Host "  3. Name it 'nepal-deploy', set expiry to 1 day" -ForegroundColor Yellow
Write-Host "  4. Copy the token and paste it below" -ForegroundColor Yellow
Write-Host ""

$tokenSecure = Read-Host "Paste your Vercel token" -AsSecureString
$token = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [Runtime.InteropServices.Marshal]::SecureStringToBSTR($tokenSecure)
)

$headers = @{
    "Authorization" = "Bearer $token"
    "Content-Type"  = "application/json"
}

# ── Step 1: Verify token ──────────────────────────────────
Write-Host ""
Write-Host "[1/5] Verifying token..." -ForegroundColor Green
$me = Invoke-RestMethod -Uri "https://api.vercel.com/v2/user" -Headers $headers
Write-Host "  Logged in as: $($me.user.email)" -ForegroundColor Green

# ── Step 2: Create project linked to GitHub ───────────────
Write-Host ""
Write-Host "[2/5] Creating Vercel project linked to GitHub..." -ForegroundColor Green

$projectBody = @{
    name      = "nepal-education-platform"
    framework = $null
    gitRepository = @{
        type = "github"
        repo = "itsmesuraj9826-art/nepal-education-platform"
    }
    buildCommand    = $null
    outputDirectory = $null
    installCommand  = "pip install -r requirements.txt"
    devCommand      = $null
} | ConvertTo-Json -Depth 5

try {
    $project = Invoke-RestMethod -Uri "https://api.vercel.com/v10/projects" `
        -Method POST -Headers $headers -Body $projectBody
    Write-Host "  Project created: $($project.name)" -ForegroundColor Green
    $projectId = $project.id
} catch {
    # Project might already exist
    Write-Host "  Project may already exist, fetching..." -ForegroundColor Yellow
    $projects = Invoke-RestMethod -Uri "https://api.vercel.com/v9/projects/nepal-education-platform" -Headers $headers
    $projectId = $projects.id
    Write-Host "  Found project: $($projects.name)" -ForegroundColor Green
}

# ── Step 3: Set environment variables ─────────────────────
Write-Host ""
Write-Host "[3/5] Setting environment variables..." -ForegroundColor Green

$secretKey = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 50 | % {[char]$_})
$jwtKey    = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 50 | % {[char]$_})

$envVars = @(
    @{ key = "SECRET_KEY";     value = $secretKey; target = @("production") }
    @{ key = "JWT_SECRET_KEY"; value = $jwtKey;    target = @("production") }
    @{ key = "FLASK_ENV";      value = "production"; target = @("production") }
    @{ key = "AI_PROVIDER";    value = "openai";   target = @("production") }
    @{ key = "UPLOAD_FOLDER";  value = "/tmp/uploads"; target = @("production") }
)

foreach ($env in $envVars) {
    $envBody = @{
        key    = $env.key
        value  = $env.value
        type   = "plain"
        target = $env.target
    } | ConvertTo-Json

    try {
        Invoke-RestMethod -Uri "https://api.vercel.com/v10/projects/$projectId/env" `
            -Method POST -Headers $headers -Body $envBody | Out-Null
        Write-Host "  Set: $($env.key)" -ForegroundColor Green
    } catch {
        Write-Host "  Skipped (already set): $($env.key)" -ForegroundColor Yellow
    }
}

# ── Step 4: Trigger deployment ────────────────────────────
Write-Host ""
Write-Host "[4/5] Triggering deployment from GitHub..." -ForegroundColor Green

$deployBody = @{
    name   = "nepal-education-platform"
    gitSource = @{
        type   = "github"
        repo   = "itsmesuraj9826-art/nepal-education-platform"
        ref    = "main"
    }
    projectId = $projectId
} | ConvertTo-Json -Depth 5

$deploy = Invoke-RestMethod -Uri "https://api.vercel.com/v13/deployments" `
    -Method POST -Headers $headers -Body $deployBody
$deployUrl = "https://$($deploy.url)"
Write-Host "  Deployment started!" -ForegroundColor Green
Write-Host "  URL: $deployUrl" -ForegroundColor Cyan

# ── Step 5: Summary ───────────────────────────────────────
Write-Host ""
Write-Host "[5/5] Done!" -ForegroundColor Green
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Deployment URL: $deployUrl" -ForegroundColor Cyan
Write-Host ""
Write-Host "  NEXT: Add Postgres storage" -ForegroundColor Yellow
Write-Host "  Go to: https://vercel.com/dashboard" -ForegroundColor Yellow
Write-Host "  Your project -> Storage -> Create -> Postgres" -ForegroundColor Yellow
Write-Host "  Then run schema_postgres.sql in the Query tab" -ForegroundColor Yellow
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Read-Host "Press Enter to close"
