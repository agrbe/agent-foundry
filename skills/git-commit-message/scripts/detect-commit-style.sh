#!/usr/bin/env bash
set -euo pipefail

# Heuristic detector for repository commit-message style.
# Output: plain | conventional | custom | unknown

repo_root="${1:-.}"

if [[ ! -d "$repo_root" ]]; then
  echo "error: repository path not found: $repo_root" >&2
  exit 1
fi

cd "$repo_root"

has_file() {
  [[ -f "$1" ]]
}

contains_pattern() {
  local file="$1"
  local pattern="$2"
  [[ -f "$file" ]] && grep -Eiq "$pattern" "$file"
}

# 1) Explicit config signals
if has_file "commitlint.config.js" || has_file ".commitlintrc" || has_file ".commitlintrc.json" || has_file ".commitlintrc.yml" || has_file ".commitlintrc.yaml"; then
  echo "conventional"
  exit 0
fi

if has_file ".releaserc" || contains_pattern "package.json" "semantic-release|commitlint|conventional-changelog"; then
  echo "conventional"
  exit 0
fi

# 2) Documentation signals
if contains_pattern "CONTRIBUTING.md" "conventional commits|commitlint|semantic-release"; then
  echo "conventional"
  exit 0
fi

if contains_pattern "CONTRIBUTING.md" "ticket|jira|scope|required subject|commit message"; then
  echo "custom"
  exit 0
fi

# 3) Recent history heuristic
if git rev-parse --git-dir >/dev/null 2>&1; then
  subjects="$(git log --format=%s -n 30 2>/dev/null || true)"
  if [[ -n "$subjects" ]]; then
    conventional_count="$(printf '%s
' "$subjects" | grep -Ec '^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\([^)]+\))?!?: .+' || true)"
    plain_count="$(printf '%s
' "$subjects" | grep -Ec '^[A-Z][^.]{3,}$|^[a-z][^.]{3,}$' || true)"

    if (( conventional_count >= 10 )); then
      echo "conventional"
      exit 0
    fi

    if (( conventional_count >= 3 && conventional_count > plain_count / 2 )); then
      echo "conventional"
      exit 0
    fi

    if (( plain_count >= 10 )); then
      echo "plain"
      exit 0
    fi
  fi
fi

echo "unknown"
