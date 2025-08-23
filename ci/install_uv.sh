#!/bin/bash

URL="https://astral.sh/uv/install.sh"
VERSION="latest"

if [[ -n "${1}" ]]; then
    VERSION="${1}"
fi

if [[ "${VERSION}" != "latest" ]]; then
    URL="https://astral.sh/uv/${VERSION}/install.sh"
fi

curl -LsSf https://astral.sh/uv/install.sh | sh
