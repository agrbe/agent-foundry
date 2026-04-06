---
name: git-commit-message
description: Draft, review, rewrite, and explain Git commit messages using repository conventions first, then plain Git or Conventional Commits defaults when needed. Use when the agent has staged changes, a diff, a file list, a change summary, or an existing commit message to evaluate.
---

# Git Commit Message

## What this skill does

Use this skill to produce durable, readable commit messages or to review an existing message against Git, GitHub, and repository-specific best practices.

This skill supports four task modes:

1. Draft a new commit message
2. Review an existing commit message
3. Rewrite a message into another style
4. Explain commit-message structure and rationale

## When to use

Use this skill when at least one of the following is available:

- staged changes
- a git diff
- a list of touched files
- a user-written summary of the change
- an existing commit message to review
- repository commit conventions to follow

## When not to use

Do not use this skill as a substitute for:

- writing pull request titles or descriptions
- generating release notes
- inventing missing product or engineering context
- deciding how code should change

If the change set contains unrelated work, recommend split commits before drafting a message.

## Required inputs

At least one of:

- diff or staged changes
- file list
- user summary
- existing commit message

## Optional inputs

- repository conventions
- `CONTRIBUTING.md`
- recent commit history
- linting or release configuration
- issue or PR references
- desired style such as plain, Conventional Commits, or repository-native
- whether the message is temporary, such as `fixup!`

## Core rules

- Prefer repository conventions before generic defaults.
- Keep each commit message aligned to one logical change.
- Explain what changed and why it changed.
- Do not invent ticket numbers, scopes, breaking changes, or behavior changes.
- Use structured trailers only when supported by the repository, workflow, or supplied context.
- Return one strong recommendation by default unless the user asks for alternatives.

## Decision process

1. Determine the task mode.
   Decide whether the user wants drafting, review, rewrite, or explanation.

2. Inspect available context.
   Use the diff, file list, and summary to identify the actual change.
   If the change mixes unrelated concerns, recommend splitting it before drafting.

3. Detect repository conventions.
   Look for:
   - `CONTRIBUTING.md`
   - commitlint or semantic-release configuration
   - recent commit subjects in `git log`
   - documented ticket, scope, or trailer rules

4. Choose the message style.
   Apply the first matching option:
   - repository-native format
   - Conventional Commits if the repository uses them or the user asked for them
   - plain Git subject/body/trailers format as the default fallback

5. Choose the message subtype when relevant.
   Support these subtypes when the context calls for them:
   - normal durable commit
   - `fixup!` or `squash!` review commit
   - revert commit
   - breaking-change commit
   - docs-only or test-only commit

6. Draft the subject line.
   The subject must:
   - describe one coherent change
   - be specific enough to stand alone in `git log`
   - use imperative wording when that matches the chosen style
   - omit a trailing period
   - avoid vague summaries like `fix`, `update`, `misc`, or `stuff`

7. Draft the body only when it adds value.
   Add a body when the change is non-trivial, the reason is not obvious from the diff, or trade-offs must be preserved.
   The body should explain:
   - why the change exists
   - the high-level behavior change
   - important side effects, limitations, or trade-offs

8. Add trailers when justified.
   Add trailers only when the context supports them, such as:
   - issue closing references
   - breaking changes
   - co-author or sign-off metadata

9. Review the message before returning it.
   Check:
   - one logical change
   - correct style for the repository
   - clear and specific subject
   - body explains why when needed
   - trailers are correct and not invented

## Output modes

### Draft mode

Return a commit message in plain text:

```text
<subject>

<optional body>

<optional trailers>
```

### Review mode

Return:
- verdict
- strengths
- weaknesses
- improved message if needed

### Rewrite mode

Return the rewritten message in the requested style.
State assumptions briefly if repository rules were not available.

### Explain mode

Explain the structure in practical terms and give a short example.

## Style guidance

### Plain Git default

Use:

```text
<Subject>

<Optional body>

<Optional trailers>
```

Guidelines:
- keep the subject concise
- use imperative phrasing where natural
- separate subject and body with one blank line
- wrap body lines for terminal readability
- preserve rationale over implementation trivia

### Conventional Commits

Use:

```text
<type>[optional scope]: <description>

<optional body>

<optional trailers>
```

Common types:
- `feat`
- `fix`
- `docs`
- `refactor`
- `perf`
- `test`
- `build`
- `ci`
- `chore`
- `revert`

Use this mode only when the repository or user expects it.

## Guardrails

- Never invent missing metadata.
- Never force Conventional Commits onto a repository that does not use them.
- Never claim a breaking change without supporting context.
- Never hide unrelated work behind a single misleading subject.
- Never over-explain details already obvious from the diff unless they preserve rationale.

## Resources

Use these files as the support system for this skill:

- `references/commit-message-rules.md`
- `references/repo-detection-checklist.md`
- `examples/`
- `templates/`
- `scripts/`

