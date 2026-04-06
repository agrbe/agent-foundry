# Mixed change example

## Input situation

The commit includes:
- bug fix in authentication
- unrelated formatting changes
- README typo fixes
- test refactor

## Recommended response

Do not write a single polished umbrella message immediately.

Recommend splitting into separate commits such as:
- authentication bug fix
- formatting-only cleanup
- documentation typo fix
- test refactor

If the user still wants one commit message, state that the commit is mixed and provide a best-effort summary with that limitation made explicit.

## Why this example matters

A skill should prefer truthful history over cosmetically neat wording.

