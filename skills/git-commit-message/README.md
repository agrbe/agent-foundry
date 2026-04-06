# Git Commit Message Skill

A complete Codex/ChatGPT skill package for drafting, reviewing, rewriting, and explaining Git commit messages.

This package is designed to be:
- small enough to be reusable,
- strict enough to be reliable,
- flexible enough to adapt to repository-specific conventions.

## Goal

Help the agent produce commit messages that:
- describe one coherent change,
- remain readable in `git log`,
- preserve the reason behind the diff,
- match repository conventions before generic defaults,
- support structured metadata when the repository or tooling expects it.

## Package layout

### Required files

These files are the minimum recommended package for installation and day-to-day use:

- `SKILL.md` — the executable playbook for the agent
- `agents/openai.yaml` — display metadata and default invocation
- `references/commit-message-rules.md` — durable rulebook
- `references/repo-detection-checklist.md` — repository-style detection guidance

### Optional files

These files improve consistency, onboarding, and maintainability:

- `references/index.md`
- `references/source-notes.md`
- `examples/*.md`
- `templates/commit-message-template.txt`
- `templates/commit-review-checklist.md`
- `scripts/detect-commit-style.sh`
- `scripts/check-commit-message.sh`

## Recommended installation strategy

1. Start with the required files.
2. Keep the examples and templates if you want stronger, more repeatable behavior.
3. Keep the scripts if your environment allows Codex to execute shell utilities.
4. Customize the examples and templates to match your repository or organization.

## Customization points

Adjust these parts first when adopting this skill for a specific repository:

- preferred style:
  - plain Git style
  - Conventional Commits
  - repository-native custom format

- allowed trailers:
  - `Closes:`
  - `Fixes:`
  - `BREAKING CHANGE:`
  - `Co-authored-by:`
  - `Signed-off-by:`

- scope rules:
  - whether scopes are required
  - whether subsystem prefixes are preferred
  - whether ticket IDs must appear in the subject

- merge strategy:
  - merge commits
  - squash merges
  - rebase merges

## Design principles

- Prefer one strong message over many weak options.
- Never invent missing facts such as ticket IDs or breaking changes.
- Recommend splitting mixed changes rather than hiding them behind a vague umbrella subject.
- Match repository conventions before applying generic defaults.
- Keep the skill focused on commit messages rather than pull requests or changelog generation.

## Suggested maintenance routine

- Review `references/source-notes.md` when updating rules.
- Refresh examples when your team's conventions change.
- Re-run the helper scripts against representative repositories.
- Keep `SKILL.md` short and operational; move long explanations into `references/`.

## Quick start

Use the skill for tasks like:

- draft a commit message from staged changes
- review whether an existing commit message is good
- rewrite a message into Conventional Commits
- explain why a commit message is weak
- generate a `fixup!` message during review iteration

