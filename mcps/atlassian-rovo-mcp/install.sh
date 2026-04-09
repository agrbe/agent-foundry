#!/usr/bin/env bash

set -euo pipefail

: "${CODEX_MCP_NAME:=atlassian-rovo-mcp}"
: "${ATLASSIAN_MCP_URL:=https://mcp.atlassian.com/v1/mcp}"
: "${ATLASSIAN_API_KEY_ENV_VAR:=}"

if ! command -v codex >/dev/null 2>&1; then
  echo "codex is required to install this MCP configuration." >&2
  exit 1
fi

if codex mcp get "${CODEX_MCP_NAME}" >/dev/null 2>&1; then
  echo "Replacing existing Codex MCP server '${CODEX_MCP_NAME}'."
  codex mcp remove "${CODEX_MCP_NAME}" >/dev/null
fi

args=(mcp add "${CODEX_MCP_NAME}" --url "${ATLASSIAN_MCP_URL}")

if [[ -n "${ATLASSIAN_API_KEY_ENV_VAR}" ]]; then
  args+=(--bearer-token-env-var "${ATLASSIAN_API_KEY_ENV_VAR}")
  if [[ -z "${!ATLASSIAN_API_KEY_ENV_VAR:-}" ]]; then
    echo "Warning: ${ATLASSIAN_API_KEY_ENV_VAR} is not set in the current shell." >&2
    echo "Codex will still be configured, but authentication will fail until it is exported." >&2
  fi
fi

codex "${args[@]}"

echo
echo "Installed Codex MCP server '${CODEX_MCP_NAME}'."
echo "Endpoint: ${ATLASSIAN_MCP_URL}"
if [[ -n "${ATLASSIAN_API_KEY_ENV_VAR}" ]]; then
  echo "Bearer token env var: ${ATLASSIAN_API_KEY_ENV_VAR}"
else
  echo "Auth mode: OAuth"
fi
echo "Start a new Codex session to pick up the new MCP configuration."
