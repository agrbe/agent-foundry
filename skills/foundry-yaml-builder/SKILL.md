---
name: foundry-yaml-builder
description: Generate, fill, and normalize `foundry.yaml` for skills in the `agent-foundry` repository. Use when Codex needs to create a missing `foundry.yaml`, rebuild one from `SKILL.md` and repository defaults, switch between the simple repository format and the full spec template, or populate provenance fields for `native`, `third_party`, or `adapted` skills under `skills/`.
---

# Foundry YAML Builder

## Overview

Build `foundry.yaml` from repository facts instead of copying stale blocks by hand. Read the target skill first, default to the simple repository shape, and only emit the full template when the task explicitly needs the extra governance fields.

## Workflow

1. Inspect the target skill folder.
   Confirm `skills/<name>/SKILL.md` exists.
   Read the frontmatter `name` and `description`.
   Reuse any existing `foundry.yaml` values as defaults instead of discarding them.
   Read `registry.yaml` to inherit `repo.default_owner` and `repo.license` when the skill is native and those fields are absent.

2. Choose the template.
   Use `simple` by default for day-to-day repository maintenance because `docs/general/foundry_yaml_spec.md` recommends keeping `foundry.yaml` simple at this stage.
   Use `full` only when the task explicitly needs fields such as `paths`, `targets`, `review`, or `lifecycle`.

3. Set origin and provenance explicitly.
   Use `native` when the skill was created in this repository.
   Use `third_party` when it was imported without meaningful changes.
   Use `adapted` when it was derived from external content and modified for this repository.
   Require explicit `source_repo` for `third_party` and `adapted`.
   Set `modified_from_source` to `false` for `third_party` and `true` for `adapted`.

4. Generate the file with the bundled script.
   Run `python3 skills/foundry-yaml-builder/scripts/build_foundry_yaml.py --skill-dir skills/<skill-name> --write`.
   Add `--template full` only when needed.
   Pass overrides for any fields that cannot be inferred, for example `--origin adapted --license MIT --source-repo openai/skills --source-path skills/.experimental/foo`.

5. Validate the result before stopping.
   Re-open the generated `foundry.yaml`.
   Check that `id` matches the folder name and `SKILL.md` frontmatter `name`.
   Check that native skills do not carry upstream source fields.
   For external skills, verify that license and provenance are explicit and that `LICENSE.txt` exists when repository policy requires it.
   When available, run `python3 skills/intake-skill/scripts/inspect_skill.py --skill-dir skills/<skill-name>` to confirm the metadata is consistent with the repository catalog.

## Script Usage

```bash
python3 skills/foundry-yaml-builder/scripts/build_foundry_yaml.py \
  --skill-dir skills/my-skill \
  --write
```

Use the simple template for a native skill.

```bash
python3 skills/foundry-yaml-builder/scripts/build_foundry_yaml.py \
  --skill-dir skills/create-plan \
  --origin adapted \
  --license MIT \
  --source-repo openai/skills \
  --source-path skills/.experimental/create-plan \
  --source-url https://github.com/openai/skills/tree/main/skills/.experimental/create-plan \
  --source-license MIT \
  --template full \
  --write
```

Use the full template for an adapted external skill.

## Decision Rules

- Prefer repository consistency over theoretical completeness.
  The current repository already stores a lean `foundry.yaml`; do not expand it unless the task calls for the full template.

- Prefer explicit overrides over guesswork.
  Do not invent `source_repo`, `source_path`, license, or tags for external skills.

- Preserve useful existing metadata.
  If a `foundry.yaml` already exists, keep compatible fields unless the user asked to rewrite them.

- Keep the title human-readable.
  Derive it from the skill `name` by converting hyphenated words to title case when no better title is already present.

## Bundled Resources

- Use `scripts/build_foundry_yaml.py` to generate or update `foundry.yaml` deterministically.
- Read `docs/general/foundry_yaml_spec.md` when the task needs field-by-field guidance or the full template shape.
- Use `skills/intake-skill/scripts/inspect_skill.py` after generation when the task also needs to confirm registry readiness or external-skill provenance.

## Output Expectations

Return the target path, the chosen template, the resolved origin, and whether the file was written or only previewed.
