# Model Context Protocol Inspector

This folder tracks the upstream MCP Inspector as a minimal MCP artifact entry
for this repository.

It does not vendor upstream source. It only documents how to install and run
the upstream npm package.

## Upstream

- Repository: `https://github.com/modelcontextprotocol/inspector`
- Package: `@modelcontextprotocol/inspector`
- License: `Apache-2.0`
- Default version used by the install script: `0.21.1`
- Docs: `https://modelcontextprotocol.io`

## Included here

- `install.sh`: installs the upstream package with `npm` by default
- `foundry.yaml`: local catalog metadata and provenance for this MCP artifact

## Install

Install globally with the provided script:

```bash
./install.sh
```

By default this runs:

```bash
npm install -g @modelcontextprotocol/inspector@0.21.1
```

Install locally in the current directory instead:

```bash
INSTALL_SCOPE=local ./install.sh
```

## Run

Run directly with `npx` without installing globally:

```bash
npx @modelcontextprotocol/inspector@0.21.1
```

If you installed globally with `npm`, you can also use:

```bash
mcp-inspector
```

To inspect a local stdio server:

```bash
npx @modelcontextprotocol/inspector@0.21.1 node build/index.js
```

## Options

The install script accepts:
- `MCP_INSPECTOR_VERSION`
- `INSTALL_SCOPE=global|local`

Example:

```bash
MCP_INSPECTOR_VERSION=0.21.1 INSTALL_SCOPE=local ./install.sh
```

## Runtime requirements

- Node.js `>=22.7.5` according to the upstream package metadata

## Security notes

Keep the inspector bound to localhost unless you are on a trusted network. The
upstream project documents that the proxy can spawn local processes and connect
to arbitrary MCP servers, so it should not be exposed to untrusted networks and
authentication should remain enabled.
