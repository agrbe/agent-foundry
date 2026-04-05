# Agent Foundry

**agent-foundry** is a shared repository for future **agents**, **skills**, and **MCP integrations** designed to support workflows across tools such as **Codex** and **Claude Code**.

This repository is intended to become a central, curated source of reusable AI building blocks, including:
- agent definitions
- skills and workflows
- MCP integration templates
- governance and provenance metadata
- licensing and attribution records

## Status

This repository is currently in its initial setup phase.

At this stage, it contains:
- repository governance files
- licensing and notice files
- initial catalog metadata
- supporting documentation
- initial native skill definitions
- Codex subagents under `agents/`

## Goals

The main goals of this repository are:

- provide a structured home for reusable AI development assets
- support both native and adapted artifacts
- keep provenance and licensing clear
- make future imports and adaptations easier to track
- establish a clean foundation before adding operational content

## Repository Structure

Current structure:

```text
agent-foundry/
├─ LICENSE
├─ NOTICE
├─ README.md
├─ registry.yaml
├─ agents/
├─ docs/
├─ skills/
└─ third_party/
   └─ THIRD_PARTY_NOTICES.md
```

Planned future areas may include:

```text
mcp/
catalog/
templates/
hooks/
scripts/
```

## Licensing

This repository is licensed under **Apache License 2.0** for original content unless stated otherwise.

Third-party materials, when added, will retain their original license terms and required notices.  
Attribution and provenance will be documented in the appropriate notice and registry files.

## Provenance and Attribution

This repository is being designed with provenance tracking in mind.

When third-party content is imported or adapted, the project aims to document:
- original source repository
- original license
- modification status
- ownership and maintenance metadata

## Registry

The `registry.yaml` file is intended to act as the base catalog for repository contents.

Over time, it may track:
- agents
- skills
- MCP integrations
- ownership
- status
- licensing metadata
- provenance details

## Documentation

The `docs/` directory contains supporting research and reference material relevant to the repository’s long-term direction.

These documents help define the architectural and operational basis for future additions.

## Third-Party Notices

The `third_party/` directory is reserved for third-party attribution and notice records.

As external materials are added in the future, this area will be used to keep licensing and attribution clear and organized.

## Roadmap

Planned next steps include:

1. define the initial catalog model
2. establish import and adaptation rules
3. curate imported agents and add the first native or adapted agents
4. expand the initial skill definitions
5. add MCP integration templates
6. introduce validation and maintenance workflows

## Contribution Philosophy

This repository is intended to prioritize:
- clarity
- traceability
- maintainability
- compatibility across tools
- responsible reuse of external artifacts

## Maintainer

Initial owner: `@agrbe`
