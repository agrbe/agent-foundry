# Git Commit Message Guide

This reference distills the guidance from
`docs/github/Best Practices for Git Commit Messages.pdf`.

## Core Principles

- Keep each commit atomic. A message should describe one logical change.
- Write for the future reader, not just the current author.
- Emphasize what changed and why it changed.
- Prefer clarity over cleverness or brevity that hides meaning.

## Recommended Structure

Use this layout unless the repository defines a stricter format:

```text
<subject line>

<body, when useful>

<footer, when useful>
```

- Keep the first line concise.
- Separate the subject and body with one blank line.
- Use the footer for issue references or breaking changes.

## Subject Line Rules

- Keep the subject near 50 characters.
- Use imperative mood: `Fix`, `Add`, `Refactor`, `Remove`.
- Capitalize the first word.
- Do not end the subject with a period.
- Prefer specific summaries such as `Fix null pointer in user service`
  over vague summaries such as `Bugfix`.

## Body Guidelines

Add a body for non-trivial changes.

- Explain why the change is needed.
- Summarize the behavior change at a high level.
- Capture trade-offs, side effects, or important context.
- Avoid restating details that are already obvious from the diff.
- Wrap lines near 72 characters.
- Use bullets only when they improve readability.

## Footer Guidelines

Use footers for structured metadata.

- Reference work items consistently: `Resolves: #123`
- Link related work when useful: `See also: #456`
- Call out incompatible behavior explicitly:
  `BREAKING CHANGE: removes legacy session cookie auth`

## Conventional Commits

Use Conventional Commits when the repository or tooling expects them.

```text
<type>[optional scope]: <description>
```

Common types:

- `feat`: new functionality
- `fix`: bug fix
- `docs`: documentation-only change
- `refactor`: code restructuring without behavior change
- `perf`: performance improvement
- `test`: test-only change
- `chore`: maintenance work

Use an optional scope when it improves clarity, for example
`feat(auth): add JWT refresh tokens`.

## Process Habits

- Make small commits so each message can stay accurate.
- Commit often while working, then squash or reorder noisy intermediate
  commits before sharing.
- Review commit history before opening a pull request.
- Follow repository-specific rules for scopes, ticket IDs, or typed commits.

## Example Patterns

Good plain-format commit:

```text
Fix login redirect

Return users to the page they were viewing before login instead of
always sending them to the dashboard.
```

Poor commit:

```text
fixed stuff
```

Good Conventional Commit:

```text
feat(auth): add JWT refresh tokens

Allow clients to obtain new access tokens without forcing users to
sign in again as often. Keep short-lived access tokens for security.

BREAKING CHANGE: removes legacy session cookie auth
Resolves: #123
```

## Quick Checklist

- Keep the message scoped to one change.
- Make the subject imperative and specific.
- Add a body only when it preserves useful context.
- Keep the message readable in terminal tools.
- Match repository conventions before applying generic defaults.
