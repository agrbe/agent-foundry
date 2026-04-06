# Repository detection checklist

Use this checklist before choosing a commit-message format.

## Goal

Determine whether the repository expects:

- plain Git style
- Conventional Commits
- a custom repository-native format

## Step 1: Check for explicit documentation

Look for:
- `CONTRIBUTING.md`
- contributor guides
- engineering docs
- release docs
- pull request templates mentioning commit style

Questions:
- Does the repository require typed commits?
- Are scopes required or optional?
- Are ticket IDs required in the subject?
- Are issue references expected in trailers or in PR descriptions instead?
- Are merge commits, squash merges, or rebased histories preferred?

## Step 2: Check configuration files

Look for signals such as:
- `commitlint.config.js`
- `.commitlintrc`
- `.releaserc`
- `package.json` scripts referencing `commitlint` or `semantic-release`
- custom hooks under `.git/hooks` or repo tooling

Interpretation:
- commitlint usually indicates an enforced message policy
- semantic-release often indicates Conventional Commits or another structured convention
- custom hooks may enforce ticket IDs, scopes, or line-length rules

## Step 3: Inspect recent commit history

Sample recent commit subjects and look for patterns.

Questions:
- Are subjects plain English or typed?
- Are descriptions lowercase after `type:`?
- Are scopes common?
- Are ticket IDs present?
- Are trailers common?
- Are there many `fixup!` commits on active branches?

If one pattern clearly dominates, treat it as the likely house style.

## Step 4: Check merge behavior

Repository history may reflect merge strategy more than local authoring style.

Consider:
- squash merges may turn PR titles into final commit subjects
- merge commits may preserve branch history
- rebase merges preserve commit subjects more directly

If squash merges dominate, make sure the final message is strong enough to stand as default-branch history.

## Step 5: Resolve ambiguity conservatively

If evidence conflicts:
1. follow explicit docs over inferred history
2. follow enforced tooling over loose custom
3. prefer the dominant pattern in recent history
4. if still unclear, use plain Git style and state assumptions briefly

## Quick evidence matrix

### Strong evidence
- documented convention
- lint or release tooling
- consistent recent history

### Medium evidence
- examples in PR templates
- team habits in a subset of commits

### Weak evidence
- one or two recent commits
- author-specific style from a single contributor

## Output recommendation

After detection, classify the repository as one of:

- `plain`
- `conventional`
- `custom`

Then draft the message accordingly.

