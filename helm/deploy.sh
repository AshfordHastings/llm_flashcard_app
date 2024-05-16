#!/bin/bash

# Variables
CHART_DIR="./flashcard-app"
BUILD_DIR="./build"
CHART_NAME="flashcard-app"
CHART_VERSION="0.1.0"
NAMESPACE="flashcard-services"
GHCR_OWNER="ashfordhastings"
GHCR_REPO="llm_flashcard-app"
GITHUB_PAT="$GITHUB_TOKEN"

ghcr_login() {
  echo "Logging into GitHub Container Registry..."
  echo $GITHUB_PAT | docker login ghcr.io -u $GHCR_OWNER --password-stdin
}

package_chart() {
  echo "Packaging Helm chart..."
  helm package $CHART_DIR --version $CHART_VERSION --destination $BUILD_DIR
}

push_chart() {
  echo "Pushing Helm chart to GitHub Container Registry..."
  helm push $BUILD_DIR/$CHART_NAME-$CHART_VERSION.tgz oci://ghcr.io/$GHCR_OWNER
}

main() {
    ghcr_login
    package_chart
    push_chart
}

main