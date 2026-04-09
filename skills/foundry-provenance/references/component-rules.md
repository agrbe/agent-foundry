# Component Intake Rules

Use this reference when `agent-foundry` needs a new artifact registered with
clear provenance and licensing.

## Kind Inference

Use these defaults unless the repository already defines something more specific:

| Kind | Typical path | Structural signal |
| --- | --- | --- |
| `skill` | `skills/<name>/` | `SKILL.md` exists |
| `agent` | `agents/.../*.toml` | Codex-native `.toml` file with `name` and `description` |
| `mcp` | `mcp/` or `mcps/` | server/config/docs bundle |
| `hook` | `hooks/` | executable or config-driven hook definition |
| `other` | anywhere else | no established structure yet |

If a kind is unclear, inspect neighboring repository content before creating a
new convention.

## Origin Rules

Use only:
- `native`
- `third_party`
- `adapted`

Interpret them this way:
- `native`: authored for this repository
- `third_party`: imported from elsewhere without meaningful modification
- `adapted`: imported from elsewhere and changed for this repository

Prefer explicit metadata over inference. If the upstream repo, path, or license
is unknown, ask instead of guessing.

## License Rules

- `native`: default to the repository license when no override exists
- `third_party` or `adapted`: require an explicit upstream license
- external content must keep license text near the imported artifact or in a
  clearly linked shared location

Practical placement:
- single imported skill: `skills/<name>/LICENSE.txt`
- single imported agent file in a shared folder: folder-level `LICENSE.txt`
- large shared import: folder-level `LICENSE.txt` plus
  `third_party/licenses/<source>.txt`

Use `NOTICE.txt` when adjacent attribution helps explain mixed imported and
repo-local files in the same folder.

## Registry Guidance

Keep the registry aligned to the real artifact kind.

Recommended agent entry shape:

```yaml
- id: backend-developer
  path: agents/01-application-roles/backend-developer.toml
  title: Backend Developer
  description: Use when a task needs scoped backend implementation or backend bug fixes after the owning path is known.
  origin: third_party
  owner: "@agrbe"
  license: MIT
  source_repo: VoltAgent/awesome-codex-subagents
  source_path: categories/01-core-development/backend-developer.toml
  modified_from_source: false
  status: draft
  tags:
    - codex
    - subagent
    - core-development
```

Recommended skill entry shape:

```yaml
- id: intake-skill
  path: skills/intake-skill
  title: Intake Skill
  description: Validate and register newly added skill folders with provenance, licensing, and catalog updates.
  origin: native
  owner: "@agrbe"
  license: Apache-2.0
  source_repo: ""
  source_path: ""
  modified_from_source: false
  status: draft
```

Rules:
- never overwrite an existing `id` or `path` silently
- update `repo.updated_at` when `registry.yaml` changes
- if a section for the kind does not exist, add it instead of misfiling the item

## Notice Strategy

Update the root `NOTICE` when a new third-party source is introduced.

Update `third_party/THIRD_PARTY_NOTICES.md` with:
1. a source-level block for the upstream repository and license
2. either:
   - one aggregate block for a bulk import that shares source and license, or
   - one per-artifact block when the import is small or mixed

Keep notices concise. Use `registry.yaml` for detailed per-artifact provenance.

## Bulk Import Rules

When importing many agents or similar artifacts from one upstream:
- preserve imported files verbatim when possible
- keep folder structure stable so `source_path` mapping stays obvious
- generate registry entries mechanically from the imported files
- aggregate notices by shared upstream source
- add repo-local metadata files around the import rather than editing each
  imported file unless adaptation is required
