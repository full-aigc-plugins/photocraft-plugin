# photocraft — DeepSeek Harness host

This directory adds a DeepSeek Harness host to the existing Agent Plugin. It does
not replace `plugin.json`, `mcp.json`, `hooks/`, or the other host manifests:
Claude Code, Codex, ZCode and Kimi keep using those.

The DSH package name is the bare plugin id, `photocraft`.

## Install

Install the plugin repository, not the marketplace repository:

```sh
dsh plugin --profile desktop add https://github.com/full-aigc-plugins/photocraft-plugin.git
```

For local development, link this directory instead:

```sh
dsh plugin --profile desktop add link:./dsh
```

The marketplace repository (`full-aigc-plugins`) stores catalog metadata only and
does not declare a DSH bundle, so it cannot be installed as a plugin.

## Editor panel (right Sidebar Browser)

The `photocraft-editor` MCP server is enabled by default. To turn it off, start DSH
with `DSH_MCP_PHOTOCRAFT=0`.

1. Ask the agent for the task. It calls `open_browser_editor` and returns an
   `editorUrl`.
2. Open that URL in DSH's right Sidebar Browser. Chat links open there by
   default (Settings → General → link opening = In-App Sidebar), so clicking the
   link the agent prints is enough.
3. Wait until `editor_status` reports `attached: true` (about 20 seconds after
   the page loads); then the editor tools work.
4. Do not launch an external browser and do not hard-code the port: each session
   gets a new loopback URL.

## What DSH gets

- every `skills/<name>/SKILL.md` (read live, no copy)
- every `commands/*.json` as a user-invocable `/name` skill
- one DSH-only skill, `photocraft-dsh`, that explains the Sidebar Browser handoff
- MCP server `photocraft-editor` (enabled by default, `DSH_MCP_PHOTOCRAFT=0` to disable)
