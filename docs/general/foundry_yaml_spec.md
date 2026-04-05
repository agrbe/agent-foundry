# `foundry.yaml` Specification
## Practical metadata design for `agent-foundry` skills

This document defines a **proposed custom metadata file** called `foundry.yaml` for the `agent-foundry` repository.

`foundry.yaml` is **not** part of the official Codex skill standard. It is a **repository-specific governance and provenance file** intended to help classify, track, register, and maintain skills over time.

## 1. Why `foundry.yaml` exists

Official Codex skills already have:
- a required `SKILL.md`
- optional `scripts/`, `references/`, `assets/`
- optional `agents/openai.yaml`

In other words, Codex already has a runtime structure for using skills. `foundry.yaml` should **not** replace those files. It should store the metadata that **your repository** needs in order to manage:
- ownership
- provenance
- licensing
- import/adaptation status
- registration in `registry.yaml`
- review and lifecycle state

## 2. Design principle

Use `foundry.yaml` for **foundry-specific metadata**, not for skill runtime behavior.

### Good uses
- identify whether a skill is native or third-party
- record source repo and source path
- record which license applies to the skill
- define who owns the skill in your catalog
- control whether the skill should be registered automatically

### Avoid putting here
- the main skill instructions
- MCP dependency declarations that should live in `agents/openai.yaml`
- Codex-facing visual metadata that already belongs in `agents/openai.yaml`
- duplicate metadata that already exists in `SKILL.md`, unless you explicitly want a mirrored catalog field

## 3. Recommended file location

Place `foundry.yaml` inside each skill directory:

```text
skills/
  my-skill/
    SKILL.md
    foundry.yaml
```

For imported or adapted skills, you may also have:

```text
skills/
  imported-skill/
    SKILL.md
    foundry.yaml
    LICENSE.txt
```

## 4. Minimal recommended structure

This is the smallest useful version:

```yaml
version: 1
id: my-skill
title: My Skill
origin: native
owner: "@agrbe"
license: Apache-2.0
status: draft
```

This is enough to:
- identify the skill
- decide whether it is native or third-party
- associate ownership
- understand the effective license
- track lifecycle state

## 5. Full proposed structure

Below is a complete, future-proof version with all recommended fields.

```yaml
version: 1

id: my-skill
kind: skill
title: My Skill
description: Short catalog description of the skill.

origin: native
owner: "@agrbe"
maintainers: []
license: Apache-2.0
license_file: ""

status: draft
visibility: internal
tags: []

source_repo: ""
source_path: ""
source_url: ""
source_license: ""
modified_from_source: false

paths:
  skill_file: SKILL.md
  foundry_file: foundry.yaml
  license_file: ""
  openai_metadata_file: ""
  scripts_dir: ""
  references_dir: ""
  assets_dir: ""

targets:
  codex: true
  claude_code: false

registry:
  register: true
  category: ""
  notes: ""

review:
  reviewed: false
  reviewed_by: ""
  reviewed_at: ""
  review_notes: ""

lifecycle:
  created_at: "2026-04-04"
  updated_at: "2026-04-04"
  deprecated_at: ""
  archived_at: ""

notes: []
```

## 6. Field-by-field reference

### 6.1 Core identity

#### `version`
**Type:** integer  
**Required:** yes  
**Purpose:** schema version for your custom metadata format.

Recommended:
```yaml
version: 1
```

Use this so you can evolve the file later without breaking automation.

---

#### `id`
**Type:** string  
**Required:** yes  
**Purpose:** stable machine-readable identifier for the skill.

Recommended conventions:
- lowercase
- hyphen-separated
- stable over time
- match the folder name when possible

Example:
```yaml
id: intake-skill
```

---

#### `kind`
**Type:** string  
**Required:** optional  
**Recommended default:** `skill`  
**Purpose:** lets the same metadata model be reused in the future for agents or MCP artifacts if desired.

Example:
```yaml
kind: skill
```

---

#### `title`
**Type:** string  
**Required:** yes  
**Purpose:** human-readable display title for cataloging.

Example:
```yaml
title: Intake Skill
```

---

#### `description`
**Type:** string  
**Required:** strongly recommended  
**Purpose:** short catalog description.

This does not need to duplicate the full `SKILL.md` description exactly. It can be a cleaner repository-facing summary.

Example:
```yaml
description: Validates and registers a new skill into the repository catalog.
```

## 6.2 Provenance and ownership

#### `origin`
**Type:** enum  
**Required:** yes  
**Allowed values:**
- `native`
- `third_party`
- `adapted`

**Purpose:** classify where the skill comes from.

Recommended meaning:
- `native`: created by you for this repository
- `third_party`: imported from elsewhere without meaningful modifications
- `adapted`: derived from third-party content and modified for your repo

Example:
```yaml
origin: adapted
```

---

#### `owner`
**Type:** string  
**Required:** yes  
**Purpose:** main owner of the skill inside your repository.

Recommended format:
```yaml
owner: "@agrbe"
```

Using a GitHub handle is a good choice because it is compact and stable in repository workflows.

---

#### `maintainers`
**Type:** array of strings  
**Required:** optional  
**Purpose:** additional maintainers or collaborators.

Example:
```yaml
maintainers:
  - "@agrbe"
  - "@someone-else"
```

## 6.3 Licensing

#### `license`
**Type:** string  
**Required:** yes  
**Purpose:** effective license of the skill artifact inside your repository.

Examples:
```yaml
license: Apache-2.0
license: MIT
```

For native skills, this often matches the repository root license.  
For third-party or adapted skills, use the license that applies to that specific imported artifact.

---

#### `license_file`
**Type:** string  
**Required:** optional but strongly recommended for third-party/adapted skills  
**Purpose:** path to the applicable license file for this skill.

Example:
```yaml
license_file: LICENSE.txt
```

If the imported skill carries its own license text, preserve it and point to it here.

---

#### `source_license`
**Type:** string  
**Required:** optional  
**Purpose:** record the original upstream license when useful.

This is especially helpful when:
- the current skill is adapted
- you want to distinguish the upstream license from how the artifact is cataloged internally

Example:
```yaml
source_license: MIT
```

## 6.4 Source metadata

#### `source_repo`
**Type:** string  
**Required:** required when `origin` is `third_party` or `adapted`  
**Purpose:** upstream repository identifier.

Examples:
```yaml
source_repo: openai/skills
source_repo: nyldn/claude-octopus
```

---

#### `source_path`
**Type:** string  
**Required:** recommended for `third_party` or `adapted`  
**Purpose:** original path inside the upstream repository.

Example:
```yaml
source_path: skills/.experimental/create-plan
```

---

#### `source_url`
**Type:** string  
**Required:** optional  
**Purpose:** full URL to the source page or directory.

Example:
```yaml
source_url: https://github.com/openai/skills/tree/main/skills/.experimental/create-plan
```

---

#### `modified_from_source`
**Type:** boolean  
**Required:** yes for imported/adapted skills  
**Purpose:** explicit statement about modification state.

Recommended rule:
- `false` for unchanged imports
- `true` for adapted skills

Examples:
```yaml
modified_from_source: false
modified_from_source: true
```

## 6.5 Status and lifecycle

#### `status`
**Type:** enum  
**Required:** yes  
**Recommended values:**
- `draft`
- `active`
- `validated`
- `deprecated`
- `archived`

Suggested meaning:
- `draft`: not ready
- `active`: available for use
- `validated`: reviewed and approved
- `deprecated`: still present, but should not be used for new work
- `archived`: retained only for historical reference

Example:
```yaml
status: active
```

---

#### `visibility`
**Type:** enum  
**Required:** optional  
**Recommended values:**
- `internal`
- `public`
- `private`

Use this if you want a policy distinction between local/internal and shareable skills.

Example:
```yaml
visibility: internal
```

---

#### `lifecycle`
**Type:** object  
**Required:** optional  
**Purpose:** timeline metadata.

Example:
```yaml
lifecycle:
  created_at: "2026-04-04"
  updated_at: "2026-04-04"
  deprecated_at: ""
  archived_at: ""
```

Use ISO dates as strings unless you later introduce stricter validation.

## 6.6 Paths

#### `paths`
**Type:** object  
**Required:** optional  
**Purpose:** normalize local file references for automation.

Suggested fields:
- `skill_file`
- `foundry_file`
- `license_file`
- `openai_metadata_file`
- `scripts_dir`
- `references_dir`
- `assets_dir`

Example:
```yaml
paths:
  skill_file: SKILL.md
  foundry_file: foundry.yaml
  license_file: LICENSE.txt
  openai_metadata_file: agents/openai.yaml
  scripts_dir: scripts
  references_dir: references
  assets_dir: assets
```

This is useful if you want your intake skill to validate folder completeness.

## 6.7 Tool targets

#### `targets`
**Type:** object  
**Required:** optional  
**Purpose:** indicate intended runtime/tool compatibility.

Example:
```yaml
targets:
  codex: true
  claude_code: true
```

This field is for repository governance only. It does not configure either platform by itself.

## 6.8 Registry integration

#### `registry`
**Type:** object  
**Required:** optional  
**Purpose:** control how this skill should be reflected in `registry.yaml`.

Suggested fields:
- `register`
- `category`
- `notes`

Example:
```yaml
registry:
  register: true
  category: github
  notes: "Catalog under workflow skills."
```

This allows your future intake automation to behave consistently.

## 6.9 Review metadata

#### `review`
**Type:** object  
**Required:** optional  
**Purpose:** quality and governance review state.

Example:
```yaml
review:
  reviewed: true
  reviewed_by: "@agrbe"
  reviewed_at: "2026-04-04"
  review_notes: "Validated provenance and license handling."
```

This is useful when you start curating third-party artifacts more seriously.

## 6.10 Tags and notes

#### `tags`
**Type:** array of strings  
**Required:** optional  
**Purpose:** filter and classify the skill.

Example:
```yaml
tags:
  - github
  - workflow
  - commit
```

---

#### `notes`
**Type:** array of strings  
**Required:** optional  
**Purpose:** free-form operational notes.

Example:
```yaml
notes:
  - "Imported for evaluation."
  - "May be split into smaller skills later."
```

## 7. Required rules by origin

### 7.1 Native skill

Minimum recommendation:
```yaml
version: 1
id: intake-skill
title: Intake Skill
origin: native
owner: "@agrbe"
license: Apache-2.0
status: draft
```

Rules:
- `source_repo` should be empty
- `source_path` should be empty
- `modified_from_source` should be `false` or omitted
- `license_file` is optional unless you want per-skill licensing

### 7.2 Third-party imported skill

Recommended example:
```yaml
version: 1
id: create-plan
title: Create Plan
description: Imported planning workflow skill.
origin: third_party
owner: "@agrbe"
license: MIT
license_file: LICENSE.txt
source_repo: openai/skills
source_path: skills/.experimental/create-plan
source_url: https://github.com/openai/skills/tree/main/skills/.experimental/create-plan
source_license: MIT
modified_from_source: false
status: active
targets:
  codex: true
  claude_code: false
```

Rules:
- `source_repo` is required
- `license` is required
- `license_file` is strongly recommended
- `modified_from_source` should be `false`

### 7.3 Adapted third-party skill

Recommended example:
```yaml
version: 1
id: create-plan-foundry
title: Create Plan (Foundry Adaptation)
description: Adapted planning skill based on upstream source.
origin: adapted
owner: "@agrbe"
license: MIT
license_file: LICENSE.txt
source_repo: openai/skills
source_path: skills/.experimental/create-plan
source_url: https://github.com/openai/skills/tree/main/skills/.experimental/create-plan
source_license: MIT
modified_from_source: true
status: draft
tags:
  - planning
  - adapted
notes:
  - "Adjusted for agent-foundry workflow."
```

Rules:
- `source_repo` is required
- `license` is required
- `license_file` is strongly recommended
- `modified_from_source` should be `true`

### 7.4 Archived skill

```yaml
version: 1
id: old-commit-helper
title: Old Commit Helper
origin: native
owner: "@agrbe"
license: Apache-2.0
status: archived
lifecycle:
  created_at: "2026-03-20"
  updated_at: "2026-04-04"
  deprecated_at: "2026-04-10"
  archived_at: "2026-04-15"
notes:
  - "Replaced by commit-workflow-v2."
```

## 8. Validation rules for automation

If you build an intake skill later, these are good validation rules:

### Always required
- `version`
- `id`
- `title`
- `origin`
- `owner`
- `license`
- `status`

### Required when `origin = third_party` or `adapted`
- `source_repo`
- `modified_from_source`

### Strongly recommended when `origin = third_party` or `adapted`
- `license_file`
- `source_path`
- `source_url`
- `source_license`

### Recommended consistency checks
- folder name should match `id`
- `paths.skill_file` should exist if declared
- `license_file` should exist if declared
- if `origin = native`, `source_repo` should be empty
- if `origin = third_party`, `modified_from_source` should be `false`
- if `origin = adapted`, `modified_from_source` should be `true`

## 9. Relationship to official Codex files

Use this separation:

### `SKILL.md`
Use for:
- official skill metadata (`name`, `description`)
- instructions
- workflow behavior

### `agents/openai.yaml`
Use for:
- optional Codex-facing metadata
- appearance
- invocation policy
- MCP dependencies

### `foundry.yaml`
Use for:
- provenance
- licensing
- ownership
- review state
- registration and governance

This separation avoids duplication and drift.

## 10. Recommended starter template

This is the template I recommend for day-to-day use:

```yaml
version: 1

id: my-skill
title: My Skill
description: Short repository-facing summary.

origin: native
owner: "@agrbe"
maintainers: []

license: Apache-2.0
license_file: ""

status: draft
visibility: internal
tags: []

source_repo: ""
source_path: ""
source_url: ""
source_license: ""
modified_from_source: false

paths:
  skill_file: SKILL.md
  foundry_file: foundry.yaml
  license_file: ""
  openai_metadata_file: ""
  scripts_dir: ""
  references_dir: ""
  assets_dir: ""

targets:
  codex: true
  claude_code: false

registry:
  register: true
  category: ""
  notes: ""

review:
  reviewed: false
  reviewed_by: ""
  reviewed_at: ""
  review_notes: ""

lifecycle:
  created_at: "2026-04-04"
  updated_at: "2026-04-04"
  deprecated_at: ""
  archived_at: ""

notes: []
```

## 11. Final recommendation

For the beginning of `agent-foundry`, keep `foundry.yaml` simple.

My practical recommendation is:
- always fill the core identity fields
- always fill provenance when the skill is not native
- keep license handling explicit for imported/adapted skills
- avoid duplicating runtime metadata from `SKILL.md` and `agents/openai.yaml`
- evolve the schema only when automation truly needs more structure

That gives you a file that is:
- easy to create by hand
- easy to validate automatically
- easy to use in a future intake skill
- and simple enough not to become bureaucracy
