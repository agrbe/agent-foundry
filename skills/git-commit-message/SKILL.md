---
name: git-commit-message
description: Draft, refine, and review Git commit messages using clear subject/body/footer conventions and optional Conventional Commits typing. Use when Codex needs to generate a commit message from staged changes, diffs, or a described code change, validate an existing commit message against best practices, or explain how to structure commit history for readable logs and changelogs.
---

# Git Commit Message

## Overview

Draft commit messages that stay readable in `git log`, help reviewers understand the change, and preserve the reason behind the diff. Use the bundled reference as the default style guide; follow repository-specific rules first when they are stricter.

## Workflow

1. Inspect the change set.
   Review the staged diff, touched files, or the user's summary.
   Identify the single logical change the commit should represent.
   Recommend splitting the commit before drafting a message if the work mixes unrelated concerns.

2. Choose the format.
   Use a plain subject/body/footer message by default.
   Use Conventional Commits only when the repository already uses them, the user asks for them, or release tooling depends on typed commits.

3. Draft the subject.
   Keep it near 50 characters.
   Use imperative mood such as `Fix`, `Add`, `Refactor`, or `Remove`.
   Capitalize the first word.
   Omit the trailing period.
   Describe the outcome or behavior change, not the implementation steps.

4. Draft the body when it adds value.
   Insert exactly one blank line after the subject.
   Explain why the change exists, what behavior changed at a high level, and any trade-offs or side effects.
   Avoid narrating details that are already obvious from the diff.
   Wrap lines near 72 characters.

5. Add footers only when needed.
   Use footers for issue references, related work, or breaking changes.
   Prefer consistent patterns such as `Resolves: #123`, `See also: #456`, or `BREAKING CHANGE:`.

6. Review before returning the message.
   Remove vague wording such as `stuff`, `misc`, or `fixes`.
   Check that the message still makes sense months later without opening the diff.
   Return one strong message by default; provide multiple candidates only when the user asks or the change can be framed in more than one valid way.

## Output Patterns

### Default

```text
<Subject>

<Optional body>

<Optional footer>
```

### Conventional Commits

```text
<type>[optional scope]: <description>

<Optional body>

<Optional footer>
```

Common types: `feat`, `fix`, `docs`, `refactor`, `perf`, `test`, `chore`.

## Review Checklist

- Does the subject describe one coherent change?
- Does the subject use imperative mood?
- Is the subject specific enough to stand alone in `git log`?
- Does the body explain `why` instead of replaying the diff?
- Are footers reserved for issue links or breaking changes?
- Does the message match repository conventions if they exist?

## Reference

Read `references/github-commit-message-guide.md` for the full rule set and examples distilled from `docs/github/Best Practices for Git Commit Messages.pdf` in this repository.
