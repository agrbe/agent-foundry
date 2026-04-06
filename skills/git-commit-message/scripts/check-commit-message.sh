#!/usr/bin/env bash
set -euo pipefail

# Lightweight heuristic checker for a commit message file.
# Usage:
#   ./scripts/check-commit-message.sh .git/COMMIT_EDITMSG

msg_file="${1:-}"

if [[ -z "$msg_file" ]]; then
  echo "usage: $0 <commit-message-file>" >&2
  exit 2
fi

if [[ ! -f "$msg_file" ]]; then
  echo "error: file not found: $msg_file" >&2
  exit 2
fi

subject="$(grep -v '^#' "$msg_file" | head -n 1)"
body="$(grep -v '^#' "$msg_file" | tail -n +2)"

fail=0

warn() {
  echo "warning: $1"
  fail=1
}

if [[ -z "${subject// }" ]]; then
  warn "missing subject line"
fi

if [[ "${#subject}" -gt 72 ]]; then
  warn "subject is long (${#subject} chars)"
fi

if [[ "$subject" =~ \.$ ]]; then
  warn "subject ends with a period"
fi

if [[ "$subject" =~ ^(fix|update|changes|stuff|misc)$ ]]; then
  warn "subject is too vague"
fi

if grep -Eq '^[[:space:]]*$' <<< "$body"; then
  :
else
  if [[ "$(grep -n -v '^#' "$msg_file" | sed -n '2p' | cut -d: -f2-)" != "" ]]; then
    second_line="$(grep -v '^#' "$msg_file" | sed -n '2p')"
    if [[ -n "$second_line" ]]; then
      warn "missing blank line between subject and body"
    fi
  fi
fi

if (( fail == 0 )); then
  echo "ok: no obvious commit-message problems found"
else
  exit 1
fi
