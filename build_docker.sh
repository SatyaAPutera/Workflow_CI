#!/bin/bash
# Script to build Docker image for MLflow project

set -e

PROJECT_NAME="sentiment-analysis-ml"
REGISTRY="${DOCKER_REGISTRY:-docker.io}"
USERNAME="${DOCKER_USERNAME:-satya}"
IMAGE_NAME="${REGISTRY}/${USERNAME}/${PROJECT_NAME}"
BUILD_TAG="${1:-latest}"

echo "==========================================="
echo "Building Docker Image for MLflow Project"
echo "==========================================="
echo "Image: ${IMAGE_NAME}:${BUILD_TAG}"
echo ""

# Build the Docker image
echo "📦 Building Docker image..."
docker build -t "${IMAGE_NAME}:${BUILD_TAG}" \
             -t "${IMAGE_NAME}:latest" \
             -f Dockerfile \
             .

echo ""
echo "✅ Build completed successfully!"
echo ""
echo "Image details:"
docker image inspect "${IMAGE_NAME}:${BUILD_TAG}" | grep -E "ID|Created|RepoTags" || true

echo ""
echo "To push to Docker Hub:"
echo "  docker push ${IMAGE_NAME}:${BUILD_TAG}"
echo "  docker push ${IMAGE_NAME}:latest"
echo ""
echo "To run the image:"
echo "  docker run -v \$(pwd)/mlruns:/app/mlruns ${IMAGE_NAME}:${BUILD_TAG}"
