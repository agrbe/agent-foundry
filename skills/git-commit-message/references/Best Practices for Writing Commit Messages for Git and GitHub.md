# Best Practices for Writing Commit Messages for Git and GitHub

## Executive summary

Commit messages are part of the permanent project record: they travel with the change, are surfaced by many Git commands (and GitHub UIs), and are frequently reused as inputs to downstream workflows like PR merges, changelogs, and releases. Git’s own documentation recommends starting with a short summary line (treated as the “title” throughout Git), separating it from the body with a blank line, and then adding a fuller explanation when needed. citeturn3search12

The most broadly applicable “baseline” for high-quality commit messages is: (a) a single-line summary that is concise and action-oriented, (b) a body that explains *what changed and why*, and (c) a structured footer/trailer block for machine-readable metadata (issue closing keywords, breaking changes, co-authors, sign-offs). This is aligned with Git’s patch submission guidance (“convey the why”) and with empirical research that defines “good” commit messages as those that explain both *what* and *why*—and finds a substantial fraction of real-world messages lack that information. citeturn3search9turn14view3

If you need automation (semantic versioning, automated release notes, changelog generation, CI rules based on change type), adopt a **structured convention** (most commonly **Conventional Commits** or an Angular-derived format) and enforce it with tooling (commit-msg hooks + CI linting). The Conventional Commits specification is explicitly designed to be machine-readable and to “dovetail with SemVer,” and tools like semantic-release depend on such structure to automate versioning and release notes. citeturn20view0turn9search8

On GitHub specifically, commit-message quality is strongly shaped by your merge strategy: squash merges and merge commits generate default commit messages that can be configured (title only vs title+description, etc.). Setting these defaults intentionally—and teaching reviewers to police the final merge commit message—prevents “good local commits” from turning into “bad main-branch history.” citeturn6search2turn6search27

## Why commit messages matter

Git itself elevates the first paragraph of the commit message (up to the first blank line) into a *title* used “throughout Git,” including email-oriented workflows like `git format-patch` where the title becomes the email subject line. That design decision makes message structure (short title, blank line, explanatory body) more than aesthetics—it directly affects how changes are communicated and reviewed. citeturn3search12

The Git project’s own patch-submission guidance frames commit messages as durable engineering documentation: the “goal” is to convey the *why* behind a change for future developers, with a short first line and conventions like omitting a trailing period. citeturn3search9 This “why” emphasis is consistent with later empirical work: **Tian et al.** define a good commit message as one that explains “what was changed” and “why a change was made,” and in their sample of ~1,600 messages from five OSS projects they find roughly **44%** could be improved (e.g., missing enough information). citeturn14view3

There is also evidence that commit-message *detail* is not just “nice to have,” but correlates with measurable engineering outcomes. **Barnett et al. (MSR 2016)** study just-in-time defect prediction models and report that commit-message *volume* (length) and *content* features add statistically significant explanatory power in many systems (e.g., message volume contributing in 43% of studied systems; content in 80%, with large potential contribution in some models). citeturn14view0 While this does *not* prove causation (“longer causes fewer defects”), it does show that commit messages encode signals relevant to software quality and risk, and that systematically low-detail messages can impair later analysis. citeturn14view0

Finally, research on commit-message “quality” increasingly treats *semantic completeness* as central (what+why), not just formatting. For example, **Li et al. (ICSE’23)** motivate that low-quality commit messages can impede comprehension and (via comprehension errors) contribute to future defects; they also question whether merely linking to an issue/PR is enough to supply “why” context, since linked content may not reliably provide it. citeturn14view2

## Official guidance from Git and GitHub

Git’s official documentation provides a clear structural baseline. In the `git-commit` documentation (DISCUSSION), Git recommends beginning with “a single short (no more than 50 characters) line,” then a blank line, then a more thorough description if necessary; and it explains that the pre-blank-line text is treated as the commit title throughout Git. citeturn3search12

The Git project’s patch submission guidance adds pragmatic details: the subject line has a “soft limit” of 50 characters, should skip a full stop, and often benefits from a leading “area: ” prefix naming the subsystem/file area touched. citeturn3search9 (This “area” prefix is conceptually similar to “scope” fields in later community standards.)

The entity["book","Pro Git","chacon and straub 2e"] book reiterates this baseline and explains why it exists: wrap body text around ~72 characters and use the imperative mood (“Fix bug …”), an approach that matches Git-generated messages for merges and reverts. citeturn3search20turn0search11 This aligns with both human readability (terminal tools like `git log`) and email-era tooling constraints for patch workflows. citeturn3search20

Git also supports standardized **trailers**—structured lines at the end of a commit message that resemble RFC 822 headers (e.g., `Signed-off-by: …`). The official `git-interpret-trailers` docs define trailers and show how they are parsed/added, and they specify that trailer blocks are placed at the end of the otherwise free-form message. citeturn3search2turn3search14 This matters because multiple ecosystems (not just Git itself) build meaning on trailer conventions.

On GitHub, two commit-message behaviors are especially important:

GitHub recognizes specific **closing keywords** (e.g., `fixes #123`, `closes #10`) in PR descriptions *and* in commit messages; the referenced issue is closed when the commit lands in the repository’s default branch (subject to GitHub’s documented constraints). citeturn0search9turn0search2

GitHub supports **co-authored commits** by reading `Co-authored-by:` trailers in the commit message. GitHub’s documentation describes the required trailer format and notes that multiple co-authors should each have their own trailer line. citeturn0search3turn3search11 GitHub’s product guidance also recommends placing trailers at the end of the message with a blank line before them. citeturn0search21

Finally, GitHub repository settings can materially change the “final” commit message that ends up on the default branch. For example, GitHub lets maintainers configure the default commit message format for merge commits (e.g., include PR number + title, or title only, or title+description). citeturn6search27 Squash merges similarly have defaults based on PR title/commit list, and GitHub added settings to default squash-merge commit messages to PR titles. citeturn6search2turn6search18

## Community standards and style guides

Community practice clusters into three “families,” each optimized for different goals:

The 50/72 + imperative “classic Git” style (popularized by the entity["people","Tim Pope","vim and rails developer"] note on commit messages and echoed by Git docs) focuses on terminal/email readability and human comprehension: short subject, blank line, wrapped body, imperative mood. citeturn1search1turn3search12turn3search20

The “7 rules” style (popularized by entity["people","Chris Beams","software engineer writer"]) codifies the classic style into a checklist and points out UI constraints in modern hosting platforms. citeturn1search16turn0search12

Structured, machine-readable conventions (Angular / Conventional Commits) introduce a typed header (and sometimes structured footers) so tooling can classify changes. The entity["organization","Angular","web framework by google"] commit-message guidelines explicitly state that their format is analyzable for changelog generation, define a typed header, and specify “what to put where” (summary, body motivation, footer breaking changes and issue references). citeturn12view0 The Conventional Commits specification generalizes this approach and makes its automation intent explicit (“makes it easier to write automated tools on top”). citeturn20view0

### Decision table comparing popular standards

The table below summarizes commonly used styles/standards based on their primary specifications/guidelines (Git docs, Tim Pope/Chris Beams essays, Angular guidelines, Conventional Commits spec, and Gitmoji spec). citeturn3search12turn3search9turn1search1turn1search16turn12view0turn20view0turn4search3

| Style / standard | Format (header/body/footer) | Scope support | Tooling support | SemVer / release automation compatibility | Learning curve |
|---|---|---|---|---|---|
| Git docs “classic” | Free-form; short title + blank line + optional body | Informal (“area: …” suggested in Git patch guidance) | Low (mostly human discipline) | Indirect (possible, but needs custom parsing rules) | Low |
| “Tim Pope 50/72” | Free-form with strict line discipline | Optional (via wording/subsystem prefix) | Low–medium (editor rulers, templates) | Indirect | Low |
| “Chris Beams 7 rules” | Free-form + explicit rules | Optional | Medium (linting possible but less standardized) | Indirect | Low–medium |
| Angular commit format | `<type>(<scope>): <summary>` + body + footer conventions | Yes (enumerated scopes encouraged) | High (many linters/presets target Angular-like formats) | High (explicitly designed for changelog/release notes) | Medium |
| Conventional Commits | `<type>[scope][!]: <description>` + optional body + optional footers (trailer-like) | Yes (optional) | Very high (commitlint presets, release tooling) | Very high (explicit mapping: feat/fix/breaking → SemVer bumps) | Medium |
| Gitmoji | Emoji “intention” + optional scope + message | Yes (optional) | Medium (ecosystem exists; can conflict with strict parsers if not configured) | Indirect unless integrated with a typed convention | Medium |

Key differences to pay attention to when choosing a standard:

Capitalization & punctuation norms differ. Git/Tim Pope/Chris Beams commonly recommend capitalizing the subject and omitting a period, while Angular’s rules explicitly say the summary is not capitalized and has no period. citeturn3search20turn1search16turn12view0 Mixing norms without an explicit team decision is a frequent source of inconsistent history.

“Scope” semantics vary. Git’s SubmittingPatches suggests an “area” prefix typically grounded in files/subsystems; Angular uses scope as the affected package (as perceived by changelog readers); Conventional Commits defines scope as a noun in parentheses but does not prescribe meaning beyond “contextual information.” citeturn3search9turn12view0turn20view0

Machine parseability is the dividing line for automation. Conventional Commits is normative about parsing (MUST/MAY language) and explicitly describes trailer-like footers and breaking-change signaling with either `BREAKING CHANGE:` or `!`. citeturn20view0 That makes it a natural fit for semantic-release and similar tools that parse commit history to determine versions and generate release notes. citeturn9search8turn9search5turn9search2

Emoji conventions are optional and should be treated as a compatibility decision. Gitmoji describes an “intention + scope + message” structure and explains shortcode vs Unicode rendering on Git platforms. citeturn4search3 If you add emojis, ensure linters and release tooling still recognize the underlying semantic “type” signals (or explicitly configure them).

## Anatomy of an effective commit message

A rigorous commit message has three layers, each serving different consumers: humans scanning history, humans digging into rationale, and machines extracting metadata.

Summary line / title: Put the smallest accurate description of the change up front. Git recommends keeping this to roughly 50 characters, and Git treats this first paragraph as the title used throughout Git tooling. citeturn3search12turn3search9 If you follow the classic style, capitalization is typical; if you follow Angular, the summary is written in imperative present tense, not capitalized, and has no terminal period. citeturn3search20turn12view0 The deeper best practice is consistency: pick one rule set, enforce it, and people will learn it.

Body: Use the body to answer “what changed” and “why,” especially when the diff is non-obvious or when future readers will need motivation, trade-offs, alternatives considered, or behavior changes. Git’s patch guidance explicitly frames the log message as conveying *why*; Pro Git recommends explaining motivation and contrasting past vs new behavior; and the research definition of “good” commit messages centers the what+why pair. citeturn3search9turn3search20turn14view3 Wrap body lines for readability in terminals and email workflows (Pro Git suggests ~72). citeturn3search20

Footer and trailers: Reserve the footer for structured metadata that tooling and platforms can parse predictably. Conventional Commits standardizes footers (often trailer-like) and requires `BREAKING CHANGE:` or an exclamation marker in the header for breaking changes. citeturn20view0 Angular similarly prescribes `BREAKING CHANGE:` (and `DEPRECATED:`) blocks and places issue/PR references in the footer. citeturn12view0 Git’s trailer tooling (`git-interpret-trailers`) provides a general mechanism for RFC822-like trailer lines, and GitHub specifically recognizes trailers such as `Co-authored-by:` at the end of commit messages. citeturn3search2turn0search3turn0search21

Issue references and closing semantics deserve special care on GitHub. Closing keywords can be placed in PR descriptions or commit messages; when placed in commit messages, GitHub documents that issues close when the commit is merged into the default branch (and the PR containing the commit may not show as “linked”). citeturn0search9turn0search13 As a best practice, many teams prefer putting closing keywords in PR descriptions (clearer review context) while keeping commit messages focused on change rationale; but either approach should be consistent and documented.

### Examples and templates for common workflows

The examples below illustrate both “classic” and “structured” approaches. Choose one style per repository (or per organization) and enforce it with tooling.

```text
# Feature (classic, free-form)
Add CSV export for invoices

Users can now export filtered invoice lists as CSV from the UI.
This is requested by Finance for month-end reconciliation.

Notes:
- CSV uses RFC4180 quoting rules
- Column order matches the UI table to reduce confusion
```

```text
# Feature (Conventional Commits)
feat(invoices): add CSV export for filtered invoice list

Add CSV export button to the invoice list page and implement
server-side streaming export to avoid high memory usage.

Closes #1842
```

```text
# Bugfix (Conventional Commits)
fix(auth): prevent refresh token reuse after logout

Cache invalidation bug caused refresh tokens to remain valid
for up to 5 minutes after logout.

Fixes #1920
```

```text
# Refactor (Conventional Commits)
refactor(search): extract query parser into dedicated module

No behavior change. Improves testability and isolates parsing
rules for future extensions.
```

```text
# Docs-only (Angular-style allows docs without body)
docs: fix typos in onboarding guide
```

```text
# Revert (Git recommends explaining why; Angular prescribes structure)
revert: feat(invoices): add CSV export for filtered invoice list

This reverts commit 1a2b3c4d5e6f7g8h9i0j.

Reason: export endpoint caused timeouts under peak traffic.
We will re-introduce with pagination + background jobs.
```

```text
# Merge commit (if you keep merge commits)
Merge pull request #512 from feature/invoice-csv-export

feat(invoices): add CSV export for filtered invoice list
```

```text
# Review feedback / WIP strategy using fixup + autosquash
fixup! feat(invoices): add CSV export for filtered invoice list
```

The last pattern matters because Git supports “fixup!” / “squash!” prefixed commits that are recognized by `git rebase --autosquash`, allowing teams to keep review-time iteration commits on the branch while producing a clean final history. citeturn7search2turn7search1 Angular’s contribution workflow explicitly recommends creating fixup commits when addressing review feedback. citeturn11view0

### Pitfalls and anti-patterns

Vague summaries (“fix”, “update”, “stuff”) are the most common failure mode. They violate Git’s stated goal of capturing the “why” and they align with research observations that many commit messages lack meaningful information. citeturn3search9turn14view3

Overloading a commit message with raw “how” details (lists of changed files, implementation minutiae) is also an anti-pattern. Both community guidelines and research-based definitions emphasize summarizing what changed and documenting why—details of how are usually in the diff itself. citeturn12view0turn1search16turn14view3

Relying on an issue/PR link as a substitute for a rationale sentence is risky. Research explicitly questions whether referenced links reliably provide “why” information, and links may rot or require context not preserved in the commit. citeturn14view2

Finally, “merge-process accidents” are a practical pitfall on GitHub: if you squash-merge and accept the default commit message, you may inadvertently publish a low-quality final commit—even if the underlying branch commits had good messages. GitHub provides settings to control default merge and squash commit message formats; use them to preserve history quality. citeturn6search2turn6search27turn6search18

## Tooling, automation, and team adoption

Commit-message standards work when they are (1) easy to follow locally, (2) enforced automatically, and (3) integrated into PR and release workflows.

```mermaid
flowchart LR
  A[Author writes commit message] --> B{Local enforcement}
  B -->|commit template + editor rulers| C[Draft message]
  B -->|commit-msg hook (commitlint)| D[Commit created]
  B -->|fails| X[Commit blocked for rewrite]

  D --> E[Push branch]
  E --> F[Pull Request]
  F --> G[CI: commit lint + tests]
  G -->|merge (merge/squash/rebase)| H[Default branch history]

  H --> I[Release automation]
  I --> J[Changelog + release notes]
  I --> K[Tag + GitHub Release]
```

This pipeline aligns with Git’s hook mechanism (commit-msg can reject commits by returning non-zero) and with commitlint’s goal of providing fast feedback “right when they are authored.” citeturn9search0turn19search4

### Recommended Git settings

A commit template reduces cognitive load and helps onboarding. Git’s `git commit` supports a template file (often set via `commit.template`) intended specifically to “guide participants with some hints on what to write.” citeturn8search0 The Pro Git customization guide also recommends templates when a team has a commit-message policy. citeturn8search12

```bash
# Use a commit message template (global)
git config --global commit.template ~/.gitmessage

# Optional: include the diff at the bottom of the commit editor so authors can
# see what they are describing (helpful for accuracy during message writing)
git config --global commit.verbose true

# Optional (advanced): if your workflow uses fixup commits
git config --global rebase.autosquash true
```

Git also supports automatic cleaning of commit messages via `--cleanup` modes (strip comments, preserve whitespace, scissors cut lines, etc.), which can matter if your commit template includes commented instructions. citeturn8search9turn8search21

### Sample commit message template

```text
# ~/.gitmessage
# Follow your repo's convention. Examples:
#   feat(scope): short summary
#   fix(scope): short summary
#
# Summary rules (pick one standard and stick to it):
# - Imperative mood ("Add", "Fix", "Refactor")
# - Keep it concise (Git recommends ~50 chars; consider it a soft limit)
# - No trailing period

<type>(<scope>): <short summary>

# Body: explain WHAT and WHY (not a changelog of files)
# - Motivation / problem
# - What changed (high-level)
# - Why this approach (trade-offs, constraints)
#
# Wrap lines for readability (72 is a common choice).

# Footer / trailers (optional)
# Fixes #123
# BREAKING CHANGE: <summary + migration notes>
# Co-authored-by: Name <email@example.com>
```

This is compatible with Git’s guidance on title/body separation and with trailer-based footers used by Conventional Commits and GitHub co-authoring. citeturn3search12turn20view0turn0search3

### Sample commit-msg hook

Git’s `commit-msg` hook is invoked with a single parameter: the path to the file containing the proposed commit message, and a non-zero exit aborts the commit. citeturn9search0 This makes it the ideal place to run a linter.

```sh
#!/bin/sh
# .git/hooks/commit-msg
# Make executable: chmod +x .git/hooks/commit-msg
#
# Enforces Conventional Commits using commitlint.
# Requires dev dependencies: @commitlint/cli and a shareable config.

MSG_FILE="$1"

if [ -z "$MSG_FILE" ] || [ ! -f "$MSG_FILE" ]; then
  echo "commit-msg hook: commit message file not found: $MSG_FILE" >&2
  exit 1
fi

# Prefer local project tooling via npx
if command -v npx >/dev/null 2>&1; then
  npx --no -- commitlint --edit "$MSG_FILE"
  exit $?
fi

echo "commit-msg hook: npx not found; cannot run commitlint." >&2
exit 1
```

Commitlint’s own docs describe adding commit-msg hook linting (often via Husky) to catch issues before commits are created. citeturn19search9turn19search4

### Sample GitHub Action workflow to lint commits in PRs

Commitlint’s CLI supports linting a commit range with `--from` / `--to`. citeturn19search0 GitHub Actions’ workflow syntax supports running on PR events and restricting branches, enabling consistent enforcement at review time. citeturn9search7

```yaml
# .github/workflows/commitlint.yml
name: Lint commit messages

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  commitlint:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout (full history for commit range)
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: "npm"

      - name: Install dependencies
        run: npm ci

      - name: Lint commit messages in this PR
        run: |
          npx --no -- commitlint \
            --from "${{ github.event.pull_request.base.sha }}" \
            --to   "${{ github.event.pull_request.head.sha }}" \
            --verbose
```

Using `actions/setup-node` is a common approach for Node-based tooling in GitHub Actions, and GitHub’s own docs recommend it for consistent runner behavior. citeturn9search4turn9search1

If you prefer a dedicated action wrapper, there are GitHub Actions built around commitlint; ensure you review permissions and behavior (especially for merge queues). citeturn19search1

### Commitlint configuration example

```js
// commitlint.config.js
export default {
  extends: ['@commitlint/config-conventional'],
  rules: {
    // Example policy choices:
    'header-max-length': [2, 'always', 72],
  },
};
```

The Conventional Commits spec explicitly points to `@commitlint/config-conventional` as a recommended set of types (build/chore/ci/docs/refactor/perf/test, etc.), and commitlint’s docs outline configuration file discovery and conventions. citeturn20view0turn2search21turn2search17

### Commitizen prompts and consistent authoring

Interactive commit authoring tools reduce errors and shorten onboarding time by guiding authors through a structured message. The Commitizen ecosystem includes adapters such as `cz-conventional-changelog`, which prompts for Conventional-Commit-compatible fields and is configured via `config.commitizen`. citeturn2search3turn2search7

```json
// package.json (snippet)
{
  "scripts": {
    "commit": "cz"
  },
  "config": {
    "commitizen": {
      "path": "./node_modules/cz-conventional-changelog"
    }
  }
}
```

Commitizen’s documentation emphasizes consistent conventions (defaulting to Conventional Commits) to enable automatic versioning and changelog generation. citeturn2search22turn2search7

### semantic-release configuration example

semantic-release states that it uses commit messages to determine the “consumer impact” of changes and, following formalized conventions, can automatically determine the next semantic version, generate a changelog, and publish a release. citeturn1search2turn9search8 Its configuration documentation describes how overall behavior is controlled via branches and plugins. citeturn9search12

```js
// release.config.js
export default {
  branches: ['main'],
  plugins: [
    '@semantic-release/commit-analyzer',
    '@semantic-release/release-notes-generator',
    ['@semantic-release/changelog', { changelogFile: 'CHANGELOG.md' }],
    '@semantic-release/github'
  ]
};
```

The commit-analyzer and release-notes-generator plugins explicitly describe their roles (analyzing commits to determine release type; generating notes from commits since last release). citeturn9search5turn9search2 The changelog plugin provides a changelog file updater, with a warning to consider whether committing release notes to a file is worth the complexity. citeturn9search31

### GitHub PR merge settings that protect history quality

If you use squash merges, GitHub’s defaults can produce inconsistent final commit messages unless configured. GitHub documents how default commit messages are chosen for squash merges (single-commit PRs vs multi-commit PRs) and provides repository-level configuration options. citeturn6search2turn6search18 For merge commits, GitHub allows choosing whether the default merge commit message includes PR number/title, title only, or title+description. citeturn6search27

A practical “best practice” configuration for many teams is:

Use squash merging (or rebase+merge) for a clean linear history *and* require the PR title/description to be “merge-commit ready,” since GitHub can default squash messages to PR titles. citeturn6search9turn6search18

Alternatively, if you keep merge commits, configure merge commit message defaults to include the PR number + title to preserve traceability to the review artifact. citeturn6search27

### Cultural conventions, onboarding, and enforcement

Policy must be teachable. The best-performing teams treat commit-message rules like any other engineering standard: document them in CONTRIBUTING, provide templates, automate checks, and include “commit message quality” in code review. Angular’s contributor docs explicitly tie their conventions to automated release notes and provide guidance on fixup commits and amending commit messages, illustrating how standards + workflow become one system. citeturn11view0turn12view0

Automation can even include quality scoring. For example, Faragó & Färber propose a commit-message quality checker grounded in Chris Beams’ 7-rule guideline, and report a machine-learning approach that can assess semantic rule adherence with meaningful performance (e.g., F1 score reported for the most challenging task), suggesting that higher-level “what/why” checks are becoming more feasible. citeturn18view0

### Concise checklist for authors and reviewers

**Author checklist (before you hit commit):**
- Does the first line stand alone and describe the change outcome (not the coding steps), and is it short enough to scan in logs (≈50-char guideline)? citeturn3search12turn3search9
- If the change is non-trivial, does the body explain *what changed* and *why* (motivation, behavior change, constraints), not just “how”? citeturn3search9turn12view0turn14view3
- Are structured items in the footer (breaking changes, issue closing references, co-authors) placed as trailers after a blank line? citeturn3search2turn20view0turn0search21
- If using GitHub issue closing keywords, are they correct and will the commit land in the default branch as required? citeturn0search9
- If this is a revert, did you explain *why* the revert is necessary (Git strongly recommends this)? citeturn10view0

**Reviewer checklist (before approving/merging):**
- Will the default-branch history reflect a good final message given the repo’s merge strategy (squash/merge/rebase) and GitHub’s configured defaults? citeturn6search2turn6search27
- Do commit messages align with the repository’s chosen standard (classic vs Conventional/Angular), including breaking-change signaling rules? citeturn20view0turn12view0
- Are issue references used consistently (preferably in PR description and/or commit footer) and do they reflect intended automation? citeturn0search2turn0search9
- If release automation exists, will these commits produce correct changelog/release notes categories (types/scopes) and correct SemVer bumps? citeturn20view0turn9search8turn9search5