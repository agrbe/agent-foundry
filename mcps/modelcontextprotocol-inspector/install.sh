#!/usr/bin/env bash

set -euo pipefail

: "${INSTALL_SCOPE:=global}"

PACKAGE="@modelcontextprotocol/inspector"

if ! command -v npm >/dev/null 2>&1; then
  echo "npm is required to install ${PACKAGE}." >&2
  exit 1
fi

case "${INSTALL_SCOPE}" in
  global)
    npm install -g "${PACKAGE}"
    ;;
  local)
    npm install "${PACKAGE}"
    ;;
  *)
    echo "INSTALL_SCOPE must be 'global' or 'local'." >&2
    exit 1
    ;;
esac

echo
echo "Installed ${PACKAGE}."
echo "Run it with:"
echo "  npx ${PACKAGE}"
echo "If you installed globally, you can also try:"
echo "  mcp-inspector"
