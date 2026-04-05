# Third-Party Notices

This repository includes and may adapt third-party materials.

Unless otherwise stated:
- Original material authored for `agent-foundry` is licensed under Apache-2.0.
- Imported or adapted third-party materials remain subject to their original licenses.
- Attribution notices for third-party materials must be preserved.

## Distribution Policy

When material is copied or adapted from a third-party source:
1. Keep the upstream license text available in `third_party/licenses/` or an equivalent location.
2. Preserve attribution in the copied/adapted file when practical.
3. Mark modified files clearly, for example:
   - `Adapted from <repo/path>`
   - `Original license: MIT`
   - `Modifications Copyright (c) 2026 Alexandre Garbelini Filho`
4. Record provenance in your catalog/registry if you maintain one.

## Suggested Per-File Header for Adapted Files

```text
Adapted from: <upstream repo and path>
Original license: MIT
Modifications Copyright (c) 2026 Alexandre Garbelini Filho
See THIRD_PARTY_NOTICES.md and third_party/licenses/ for details.
```

## Suggested Provenance Record

```yaml
id: <agent-or-skill-id>
source_repo: <owner/repo>
source_path: <path/in/upstream>
source_license: MIT
import_mode: imported|adapted
owner: agrbe
status: draft|validated|deprecated
last_synced: 2026-04-04
notes:
  - <what was changed>
```

## Notes

This file is an attribution and provenance aid. It does not replace the need to:
- keep upstream license texts,
- preserve required notices,
- and mark substantial modifications when you distribute adapted files.
