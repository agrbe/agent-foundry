# Review mode example

## Input message

```text
fixed stuff
```

## Review output

Verdict: weak

Strengths:
- short

Weaknesses:
- does not identify the affected area
- does not explain what changed
- does not preserve why the change was needed
- too vague to stand alone in history

Improved message:
```text
Fix login redirect after session timeout

Return users to the page they were viewing before authentication
expires instead of always sending them to the dashboard.
```

