# Intake Metadata And Registry

Use this reference when the target skill needs provenance clarification or when you need to format registry and notice updates consistently.

## Minimum Structure

Required:
- `SKILL.md`

Recommended:
- `foundry.yaml`
- `agents/openai.yaml`

Conditional:
- `LICENSE.txt` for `third_party` and `adapted`
- `scripts/`
- `references/`
- `assets/`

## Recommended `foundry.yaml`

```yaml
id: intake-skill
title: Intake Skill
origin: native
owner: "@agrbe"
license: Apache-2.0
source_repo: ""
source_path: ""
modified_from_source: false
status: draft
tags:
  - workflow
  - catalog
  - provenance
```

## Origin Rules

Use these values only:
- `native`
- `third_party`
- `adapted`

Classification rules:
1. If `origin` is present, use it and verify it is internally consistent.
2. Otherwise, if `source_repo` is present and `modified_from_source` is `false`, classify as `third_party`.
3. Otherwise, if `source_repo` is present and `modified_from_source` is `true`, classify as `adapted`.
4. Otherwise, if metadata exists and no source is declared, classify as `native`.
5. Otherwise, ask the user instead of guessing.

Consistency checks:
- `native` should not declare `source_repo`.
- `third_party` should not declare `modified_from_source: true`.
- `adapted` should usually declare both `source_repo` and `modified_from_source: true`.

## License Rules

- `native`: default to the repository license when the skill does not declare its own.
- `third_party` or `adapted`: require an explicit license and a local `LICENSE.txt`.

## Registry Entry Shape

Use a single entry under `catalog.skills`:

```yaml
- id: intake-skill
  path: skills/intake-skill
  title: Intake Skill
  description: <description copied from SKILL.md frontmatter>
  origin: native
  owner: "@agrbe"
  license: Apache-2.0
  source_repo: ""
  source_path: ""
  modified_from_source: false
  status: draft
  tags:
    - workflow
    - catalog
    - provenance
```

Rules:
- Keep `id` aligned with the folder name and SKILL frontmatter `name`.
- Do not overwrite an existing entry with the same `id` or `path` without warning.
- Update `repo.updated_at` when `registry.yaml` changes.

## Third-Party Notice Block

Append a short block only when external content is actually copied or adapted:

```md
## Registered Skills

### Intake Skill (`intake-skill`)
- Path: `skills/intake-skill`
- Origin: `adapted`
- Source: `owner/repo` (`skills/original-path`)
- License: `MIT`
- Modified: `yes`
- Owner: `@agrbe`
- Status: `draft`
```

If the `## Registered Skills` section does not exist yet, create it near the end of `third_party/THIRD_PARTY_NOTICES.md`.
