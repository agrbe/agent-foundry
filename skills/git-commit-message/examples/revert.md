# Revert example

## Input situation

- the change must be rolled back
- the original commit subject is known
- the reason for the revert should be preserved

## Recommended message

```text
revert: feat(invoices): add CSV export for filtered lists

This reverts commit 1a2b3c4d5e6f7g8h9i0j.

Reason: the export endpoint caused repeated timeouts under peak load.
```

## Why this works

- clearly signals a revert
- preserves the original target
- records the practical reason for backing it out

