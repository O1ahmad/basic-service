#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CHART_DIR="${ROOT_DIR}/helm"
RELEASE_NAME="basic-service-ci"

if ! command -v helm >/dev/null 2>&1; then
  curl -fsSL https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
fi

helm lint "${CHART_DIR}"
helm template "${RELEASE_NAME}" "${CHART_DIR}" -f "${CHART_DIR}/values.yaml" >/dev/null
helm template "${RELEASE_NAME}" "${CHART_DIR}" -f "${CHART_DIR}/values-test.yaml" >/dev/null

RENDERED_VALUES="${ROOT_DIR}/tests/fixtures/k8s-rendered-values.yaml"
if [[ -f "${RENDERED_VALUES}" ]]; then
  helm template "${RELEASE_NAME}" "${CHART_DIR}" -f "${RENDERED_VALUES}" >/dev/null
fi

echo "Helm chart validation succeeded."
