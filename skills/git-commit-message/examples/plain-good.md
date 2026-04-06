# Plain Git example

## Input situation

- repository style is unknown
- change is one coherent bug fix
- no issue number was provided

## Recommended message

```text
Fix login redirect after session timeout

Return users to the page they were viewing before authentication
expires instead of always sending them to the dashboard.
```

## Why this works

- one coherent change
- subject stands alone
- body explains why the behavior changed
- no invented metadata

