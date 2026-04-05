---
name: foundry-provenance
description: Register or review artifacts in `agent-foundry` with provenance, licensing, and catalog updates. Use when Codex needs to add, import, adapt, move, or audit a skill, agent, MCP, hook, template, or other tracked artifact; determine whether it is `native`, `third_party`, or `adapted`; gather source and license details; update `registry.yaml`, `NOTICE`, `third_party/THIRD_PARTY_NOTICES.md`, and any local `LICENSE.txt` or `NOTICE.txt`; and verify the repository is ready for merge.
---

# Foundry Provenance

## Overview

Register repository artifacts without guesswork. Inspect the target first,
classify origin from explicit metadata, require the right license and notice
files for external content, then patch the catalog and attribution records.

## Workflow

1. Identify the component kind and scope.
   Infer from the path when obvious:
   - `skills/<name>/` with `SKILL.md` -> `skill`
   - `agents/.../*.toml` -> `agent`
   - `mcp/` or `mcps/` -> `mcp`
   - `hooks/` -> `hook`
   For bulk imports, summarize the batch size and shared provenance instead of
   treating every file as an isolated manual intake.

2. Read the governing repository files first.
   Always inspect:
   - `registry.yaml`
   - `NOTICE`
   - `third_party/THIRD_PARTY_NOTICES.md`
   Then read nearby metadata when present:
   - `foundry.yaml`
   - `agents/openai.yaml`
   - `README.md`
   - `LICENSE.txt`
   - `NOTICE.txt`

3. Inspect the artifact with the bundled script.
   Run:
   ```bash
   python3 scripts/inspect_foundry_component.py --path <artifact-path> --repo-root <repo-root>
   ```
   Add `--kind`, `--origin`, `--license`, `--source-repo`, `--source-path`,
   and `--modified-from-source true|false` when you already know them.
   Use `--json` when you want machine-readable follow-up.

4. Resolve missing provenance before editing.
   Ask only for fields that remain unknown after inspection:
   - origin
   - upstream repository and source path
   - upstream license
   - whether imported content was modified
   - owner, only if the repository default owner is wrong

5. Apply repository policy by origin and kind.
   `native`:
   - default to the repository license unless the artifact declares a different one

   `third_party` or `adapted`:
   - require an explicit upstream license
   - require a local `LICENSE.txt` near the imported artifact or in a clearly
     adjacent shared location for the whole imported batch
   - add `NOTICE.txt` when a folder mixes imported upstream files with
     repo-local metadata, or when adjacent attribution reduces ambiguity

   Keep imported files unchanged when you want `modified_from_source: false`.

6. Propose the change set before patching.
   Include:
   - target path
   - detected kind
   - origin
   - missing inputs
   - registry section and entry shape
   - notice updates
   For bulk imports, state whether notices are aggregated by source and whether
   registry entries are per artifact.

7. Patch the repository carefully.
   - do not silently overwrite an existing `id` or `path` in `registry.yaml`
   - update `repo.updated_at` whenever `registry.yaml` changes
   - if the correct registry section does not exist yet, add it instead of
     placing the artifact under the wrong kind

8. Re-run inspection after edits.
   Re-run the bundled script on the changed path.
   Re-run any repo validation commands that exist.

## Decision Rules

- Prefer explicit metadata over inference.
- Use only `native`, `third_party`, or `adapted` for origin.
- Preserve upstream files verbatim unless adaptation is intentional.
- For bulk imports from one upstream source, keep one source block in notices and
  use `registry.yaml` for per-artifact provenance.
- For single imported artifacts, a local `LICENSE.txt` is usually sufficient.
  For shared imports, a folder-level `LICENSE.txt` or a clearly linked
  `third_party/licenses/` copy is acceptable when the relationship is obvious.
- If the artifact kind or required structure is unclear, read
  `references/component-rules.md`.

## Bundled Resources

- `references/component-rules.md`
  Use for structure expectations, registry guidance, and notice strategy by
  artifact kind.
- `scripts/inspect_foundry_component.py`
  Use to inspect one artifact or a bulk agent folder, surface missing
  provenance, detect duplicate registry entries, and print proposed registry and
  notice data.

## Output Expectations

Return a short intake summary before editing: target path, kind, origin, missing
inputs, and planned repository files to update.

After editing, report what changed, whether the artifact is ready for merge, and
any remaining provenance or license gaps.
