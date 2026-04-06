# Commit message rules

This document is the rulebook for the skill. When `SKILL.md` gives a short operational instruction, this file provides the deeper interpretation.

## 1. Primary objective

A good commit message should help a future reader understand:

- what changed
- why it changed
- whether structured metadata matters

The message should still make sense months later without relying on the author's memory.

## 2. Atomicity first

Before drafting any message, ask whether the commit represents one logical change.

Signals that the commit should probably be split:
- unrelated feature work and cleanup together
- formatting-only changes mixed with behavior changes
- refactor plus bug fix with no single dominant reason
- docs, tests, and implementation all changed for unrelated reasons

If the commit is mixed, recommend splitting it instead of writing a vague umbrella message.

## 3. Style priority order

Apply styles in this order:

1. repository-native style
2. Conventional Commits if required or clearly established
3. plain Git subject/body/trailers format

Do not assume a style without evidence if repository material is available.

## 4. Subject-line guidance

The subject line should:
- describe one coherent change
- be concrete and standalone
- avoid filler and vague wording
- omit a trailing period

Good:
- `Fix login redirect after session timeout`
- `docs(api): clarify token refresh example`
- `refactor(search): extract query parser`

Weak:
- `fix stuff`
- `updates`
- `misc cleanup`
- `changes`

### Imperative mood

Imperative mood is a useful default for plain Git style:
- `Fix`
- `Add`
- `Remove`
- `Refactor`

For typed conventions, the description should match the repository's existing pattern.
Do not force title-style capitalization if the repository uses lowercase descriptions.

## 5. Body guidance

Add a body when it preserves useful context.

Use the body to capture:
- why the change was made
- what user-visible or system-visible behavior changed
- side effects or trade-offs
- limits, risks, or follow-up notes when relevant

Avoid:
- replaying the entire diff
- listing files unless that list is itself meaningful
- including implementation trivia that is obvious from the patch

## 6. Trailer guidance

Treat trailers as structured metadata at the end of the message.

Common trailers:
- `Closes: #123`
- `Fixes: #456`
- `Refs: #789`
- `BREAKING CHANGE: removes legacy session cookie auth`
- `Co-authored-by: Name <email@example.com>`
- `Signed-off-by: Name <email@example.com>`

Rules:
- add trailers only when supported by the workflow or provided context
- keep trailers consistent within a repository
- do not invent issue identifiers or authors

## 7. Supported message subtypes

### Normal durable commit

Use the standard style selected for the repository.

### `fixup!` commit

Use when the commit is intentionally temporary and will later be autosquashed.

Pattern:
```text
fixup! <target subject>
```

Do not rewrite the original subject unnecessarily.

### `squash!` commit

Use when the author intends to combine the body during autosquash.

### Revert commit

Use when backing out a previous change.

Pattern:
```text
revert: <original subject>

This reverts commit <sha>.

<optional reason>
```

### Breaking-change commit

Include a clear explanation in the body and use a breaking-change trailer or the repository's defined equivalent.

## 8. Repository-aware decisions

Check for:
- recent commit history
- `CONTRIBUTING.md`
- commitlint config
- release tooling
- ticket or scope conventions
- merge strategy effects on final history

Repository evidence beats generic advice.

## 9. Review rubric

A strong commit message should answer yes to all of these:

- Does it describe one logical change?
- Does the subject stand alone in `git log`?
- Does it match repository conventions?
- Does the body explain why when needed?
- Are trailers correct, useful, and non-fictional?
- Will it still make sense to a future maintainer?

If any answer is no, rewrite before returning.

## 10. Practical defaults

If repository rules are unknown:
- default to plain Git style
- keep the subject concise and specific
- add a body only when it preserves rationale
- avoid structured trailers unless explicitly supported

