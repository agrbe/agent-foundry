# Atlassian Rovo MCP Server

This folder tracks a native Codex installer for Atlassian's hosted Rovo MCP
server with Jira-focused setup guidance.

It does not vendor Atlassian server source. It provides a Codex installer,
catalog metadata, and usage notes for connecting Jira-aware Codex sessions to
Atlassian's remote MCP endpoint.

## Upstream service

- Product: Atlassian Rovo MCP Server
- Default endpoint: `https://mcp.atlassian.com/v1/mcp`
- Deprecated endpoint: `https://mcp.atlassian.com/v1/sse` will no longer be
  supported after June 30, 2026
- Docs: `https://support.atlassian.com/atlassian-rovo-mcp-server/docs/getting-started-with-the-atlassian-remote-mcp-server/`

## Included here

- `install.sh`: registers this MCP in Codex using the native remote HTTP MCP
  support
- `foundry.yaml`: local catalog metadata for this MCP artifact

## Quick start for Codex

Codex can connect directly to Atlassian's remote MCP endpoint, so `mcp-remote`
is not required.

Install it into Codex:

```bash
./install.sh
```

This runs the equivalent of:

```bash
codex mcp add atlassian-rovo-mcp --url https://mcp.atlassian.com/v1/mcp
```

If Codex does not complete OAuth during install, start it explicitly with:

```bash
codex mcp login atlassian-rovo-mcp
```

Optional bearer-token mode for a service-account API key:

```bash
ATLASSIAN_API_KEY_ENV_VAR=ATLASSIAN_API_KEY ./install.sh
```

This configures Codex to read the bearer token from the named environment
variable when launching the MCP client.

## Authentication

Atlassian documents two supported authentication paths:

- OAuth 2.1: primary option for interactive user-driven flows
- API token authentication: optional, only when enabled by an Atlassian org admin

For local OAuth flows, Atlassian notes that the browser callback usually uses
`http://localhost:3334`, so local firewall and browser settings must allow it.

### OAuth 2.1

OAuth is the default choice for local interactive use. If your client supports
OAuth dynamic client registration, Atlassian says you do not need to manually
create an OAuth app.

### API token authentication

Atlassian's official examples use client headers rather than environment
variables.

For Codex specifically:

- OAuth works with the direct remote MCP configuration installed by
  `install.sh`
- Bearer-token service-account auth can be configured through
  `--bearer-token-env-var`
- Personal API token Basic auth is documented by Atlassian, but is not wired by
  the Codex installer because `codex mcp add --url` does not expose arbitrary
  custom HTTP headers

Personal API token:

```json
{
  "mcpServers": {
    "atlassian-rovo-mcp": {
      "url": "https://mcp.atlassian.com/v1/mcp",
      "headers": {
        "Authorization": "Basic BASE64_ENCODED_EMAIL_AND_TOKEN"
      }
    }
  }
}
```

Service account API key:

```json
{
  "mcpServers": {
    "atlassian-rovo-mcp": {
      "url": "https://mcp.atlassian.com/v1/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY_HERE"
      }
    }
  }
}
```

Atlassian also documents that API token auth can expose fewer tools than OAuth
and is not bound to a single `cloudId`.

## Jira tools currently documented by Atlassian

- `getJiraIssue`
- `searchJiraIssuesUsingJql`
- `getVisibleJiraProjects`
- `getJiraProjectIssueTypesMetadata`
- `getJiraIssueTypeMetaWithFields`
- `getTransitionsForJiraIssue`
- `lookupJiraAccountId`
- `createJiraIssue`
- `editJiraIssue`
- `transitionJiraIssue`
- `addCommentToJiraIssue`
- `addWorklogToJiraIssue`

Typical scopes are `read:jira-work` and `write:jira-work`, depending on the
tool used.

## Runtime requirements

- An Atlassian Cloud site with Jira access
- A modern browser for OAuth flows

## Script options

`install.sh` accepts:

- `CODEX_MCP_NAME`
- `ATLASSIAN_MCP_URL`
- `ATLASSIAN_API_KEY_ENV_VAR`

Example:

```bash
ATLASSIAN_API_KEY_ENV_VAR=ATLASSIAN_API_KEY ./install.sh
```

## Verification

After connecting, Atlassian recommends testing with a simple Jira prompt such
as:

```text
List my Jira issues.
```

## Security notes

- Jira actions run with the caller's existing Atlassian permissions.
- Review write operations before confirming them in the client.
- Prefer OAuth for interactive use.
- Use least privilege for API tokens and service-account keys.

## Sources

- Getting started:
  `https://support.atlassian.com/atlassian-rovo-mcp-server/docs/getting-started-with-the-atlassian-remote-mcp-server/`
- IDE setup:
  `https://support.atlassian.com/atlassian-rovo-mcp-server/docs/setting-up-ides/`
- Other MCP clients:
  `https://support.atlassian.com/atlassian-rovo-mcp-server/docs/using-with-other-supported-mcp-clients/`
- OAuth:
  `https://support.atlassian.com/atlassian-rovo-mcp-server/docs/configuring-oauth-2-1/`
- API token auth:
  `https://support.atlassian.com/atlassian-rovo-mcp-server/docs/configuring-authentication-via-api-token/`
- Supported tools:
  `https://support.atlassian.com/atlassian-rovo-mcp-server/docs/supported-tools/`
- Troubleshooting:
  `https://support.atlassian.com/atlassian-rovo-mcp-server/docs/troubleshooting-and-verifying-your-setup/`
