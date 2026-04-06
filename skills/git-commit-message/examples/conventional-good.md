# Conventional Commits example

## Input situation

- repository uses Conventional Commits
- scope is commonly used
- issue number is known

## Recommended message

```text
feat(invoices): add CSV export for filtered lists

Add a CSV export action to the invoice list page and stream the
response from the server to avoid high memory usage.

Closes: #1842
```

## Why this works

- matches typed repository convention
- scope improves clarity
- body preserves rationale
- trailer uses known issue metadata

