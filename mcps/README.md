# MCP Catalog

This directory holds repository-managed MCP artifacts.

Each MCP artifact should live in its own folder under `mcps/<id>/` and stay
minimal unless the MCP server is actually implemented in this repository.

Recommended baseline:
- `README.md` explaining what the MCP is, how to install it, and how to run it
- `foundry.yaml` with catalog and provenance metadata
- one small shell script when setup or installation should be standardized

Current entries:
- `modelcontextprotocol-inspector`: install helper and usage notes for the
  upstream MCP Inspector package
