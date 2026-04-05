---
name: intake-skill
description: Validate and register newly added skill folders with provenance, licensing, and catalog updates. Use when Codex needs to inspect a folder under `skills/`, verify the minimum skill structure, read `foundry.yaml` when present, classify the skill as `native`, `third_party`, or `adapted`, ask concise follow-up questions for missing provenance, propose updates to `registry.yaml`, and optionally update `third_party/THIRD_PARTY_NOTICES.md` before applying any edits.
---

# Intake Skill

## Overview

Register skills without relying on brittle guesswork. Inspect the target folder first, prefer explicit metadata, collect any missing provenance information, and only then patch the repository catalog and notices.

## Workflow

1. Locate the target skill folder and the repository files that govern cataloging.
   Expect the target under `skills/<skill-name>/`.
   Read `registry.yaml` and, when external content may be involved, `third_party/THIRD_PARTY_NOTICES.md`.

2. Inspect the skill before proposing any edits.
   Run `python3 scripts/inspect_skill.py --skill-dir <path-to-skill> --registry <path-to-registry> --third-party-notices <path-to-notices>`.
   Use `--json` when you want machine-readable output for follow-up steps.

3. Prefer explicit metadata over inference.
   Read `foundry.yaml` when it exists.
   Treat `SKILL.md` as the source for the skill name and triggering description.
   Never assume third-party provenance from folder contents alone.

4. Resolve missing provenance with concise questions.
   Ask only for fields that are still missing after inspection.
   Keep the questions short:
   - `Is this skill native, third_party, or adapted?`
   - `If it is external, what are the source repo and source path?`
   - `What license applies to this skill?`
   - `Was the imported content modified?`

5. Enforce provenance rules before editing repository metadata.
   A skill is minimally well-formed only when `SKILL.md` exists and has valid frontmatter.
   A non-native skill must not be registered until its provenance and license are explicit.
   For `third_party` or `adapted`, require both metadata and a local `LICENSE.txt` before treating the intake as complete.

6. Show the proposed change set before writing.
   Summarize:
   - structural findings
   - inferred or confirmed origin
   - missing inputs
   - the exact registry entry to add or update
   - the notice block to append when external material is included

7. Apply edits only after the proposal is clear.
   Update `registry.yaml` without overwriting an existing entry silently.
   If an entry already exists for the same `id` or `path`, stop and warn instead of replacing it.
   Update `third_party/THIRD_PARTY_NOTICES.md` only when the skill actually includes copied or adapted third-party content.

8. Re-run validation after edits.
   Re-run `scripts/inspect_skill.py` on the target skill.
   Re-run the repository's normal skill validation flow when available.

## Decision Rules

- Use metadata first.
  Read `foundry.yaml` before asking questions or classifying provenance.

- Treat origin classification as policy, not guesswork.
  If metadata is absent or incomplete, ask the user instead of inventing provenance.

- Derive origin from explicit fields when possible.
  Use this order:
  1. `origin` from `foundry.yaml`
  2. Otherwise, if `source_repo` exists and `modified_from_source` is known, classify as `third_party` or `adapted`
  3. Otherwise, if metadata exists and no source is declared, treat it as `native`
  4. Otherwise, ask

- Apply license policy consistently.
  `native` skills may inherit the repository license when no skill-specific license is declared.
  `third_party` and `adapted` skills must carry an explicit upstream license and local license text.

- Preserve operator control.
  Propose diffs before patching repository metadata.
  Do not silently replace an existing registry entry.

## Bundled Resources

- Use `references/metadata-and-registry.md` for:
  - the recommended `foundry.yaml` schema
  - origin classification rules
  - the registry entry shape
  - the third-party notice template

- Use `scripts/inspect_skill.py` to:
  - validate the target folder structure
  - parse `SKILL.md` frontmatter and `foundry.yaml`
  - detect duplicate registry entries
  - surface missing provenance inputs
  - print a proposed registry entry
  - print a proposed notice block for external skills

## Output Expectations

Return a short intake summary before editing files. Include the target path, origin, missing inputs, and a preview of the catalog changes.

After editing, report what changed and whether the final state is ready for merge or still blocked on provenance or licensing.
