# Breaking change example

## Input situation

- repository uses Conventional Commits
- the change removes a legacy authentication path
- the breaking behavior is confirmed by the change context

## Recommended message

```text
feat(auth): remove legacy session cookie fallback

Remove the deprecated session cookie fallback and require token-based
authentication for all API clients.

BREAKING CHANGE: clients must use bearer tokens for authenticated API calls
```

## Why this works

- clearly identifies the domain
- body explains the behavior change
- breaking trailer is explicit and justified

