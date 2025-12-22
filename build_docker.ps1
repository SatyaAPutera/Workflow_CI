# Script to build Docker image for MLflow project (Windows)
param(
    [string]$BuildTag = "latest",
    [string]$Registry = $env:DOCKER_REGISTRY,
    [string]$Username = $env:DOCKER_USERNAME
)

if (-not $Registry) { $Registry = "docker.io" }
if (-not $Username) { $Username = "satya" }

$ProjectName = "sentiment-analysis-ml"
$ImageName = "${Registry}/${Username}/${ProjectName}"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Building Docker Image for MLflow Project" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Image: ${ImageName}:${BuildTag}" -ForegroundColor Yellow
Write-Host ""

# Build the Docker image
Write-Host "📦 Building Docker image..." -ForegroundColor Yellow
docker build -t "${ImageName}:${BuildTag}" `
             -t "${ImageName}:latest" `
             -f Dockerfile `
             .

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Build completed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "To push to Docker Hub:" -ForegroundColor Yellow
    Write-Host "  docker push ${ImageName}:${BuildTag}"
    Write-Host "  docker push ${ImageName}:latest"
    Write-Host ""
    Write-Host "To run the image:" -ForegroundColor Yellow
    Write-Host "  docker run -v `${PWD}/mlruns:/app/mlruns ${ImageName}:${BuildTag}"
} else {
    Write-Host ""
    Write-Host "❌ Build failed!" -ForegroundColor Red
    exit 1
}
