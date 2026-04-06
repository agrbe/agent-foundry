# Fixup example

## Input situation

- review feedback requires a temporary follow-up commit
- the branch will be cleaned up later with autosquash

## Recommended message

```text
fixup! feat(invoices): add CSV export for filtered lists
```

## Why this works

- uses the autosquash-recognized prefix
- targets the original subject directly
- stays intentionally minimal because it is temporary

