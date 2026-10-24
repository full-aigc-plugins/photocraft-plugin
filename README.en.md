# PhotoCraft（图片编辑）

> Layers, masks, cutouts and retouching into editable image projects

**Version**: 0.1.0-dev.20261019.1 · **License**: Apache-2.0 · **Skills**: 22 · **MCP server**: 1

[简体中文](README.md) · [Install](#installation) · [Quick start](#quick-start) · [Project layout](#project-layout)

## Positioning

Layers, masks, cutouts, retouching and filters with text and resize variants. Projects stay editable and export to PSD, PNG and other formats.

This plugin belongs to the content-creation line and is for users who need an editable result, not a script or a flat image.

## At a glance

```text
assets / requirements / old drafts
        │
        ▼
PhotoCraft（图片编辑） skill (inspect → plan → execute → read back)
        │
        ├── native CLI / MCP tools
        └── MCP editor (in-browser review and local edits)
        │
        ▼
editable project + export + review
```

## Capabilities and boundaries

| Capability | What it does | Boundary |
|---|---|---|
| Inspect | Read the current project and assets | No edits without authorization |
| Create | Build an editable structure from the goal | Facts and assets come from input |
| Edit | Change the requested scope only | Reopen after every edit |
| Export | Produce the target format and verify | A successful export is not correct layout |
| Review | Check against explicit criteria | Not a substitute for final human acceptance |

## Architecture and core flow

```text
Host / agent
   │  invokes a skill
   ▼
skills/photocraft-*  ──►  MCP editor / native CLI
                              │
                              ▼
                     editable project + export
                              │
                              ▼
                     read back, review, deliver
```

Rules:

1. Inspect read-only, then plan, then execute.
2. Keep the original or a rollback version.
3. Reopen the export before trusting it.
4. Mark uncertain results for review; never replay automatically.

## Compatibility

| Item | Status |
|---|---|
| Host | Hosts with MCP Apps or a built-in browser |
| Node.js | 24+ (editor) |
| Platforms | Follow the actual package and release notes |

## Installation

```bash
codex plugin marketplace add partme-ai/full-aigc-plugins
codex plugin add photocraft@full-aigc-plugins
```

Restart the host and start read-only.

## Quick start

1. Confirm goal, inputs, and delivery format.
2. Inspect the current project and list gaps.
3. Make one bounded change.
4. Reopen the output and verify structure and key content.
5. Complete visual or content review before delivery.

## Configuration

| Variable | Purpose | Default |
|---|---|---|
| `CRAFT_WORKSPACE_ROOT` | Workspace bound to the editor | current project |
| `CRAFT_EDITOR_UPDATE` | Set to `off` to skip the enhanced editor download | enabled |

Never write secrets, tokens, or private paths into projects or configuration.

## Extension contract

New skills use the `photocraft-` prefix, declare triggers and boundaries, operate through MCP or the pinned CLI, and reopen after every edit.

## Retry, idempotency, and recovery

- Inspect the current project after a failure.
- Do not replay operations with side effects.
- Retry with a new output path and keep the old receipt.

## Data and state

- Inputs are read-only.
- Outputs, exports, and temporary directories are separate.
- Confirm the file opens and content is complete before delivery.

## Security

- Do not upload unauthorized assets to third-party services.
- Redact sensitive content before delivery.
- On a suspected leak, rotate credentials before cleaning files.

## Observability and operation

Record command, output file, key structure, and review result; inspect at least one real output before delivery.

## Development and verification

```bash
node --test
python3 -m pytest
```

## Packaging and release

Version matches manifests, marketplace, and tag; the ZIP root is `photocraft-plugin`.

## Upgrade and migration

Back up projects before upgrading; keep older files openable; recheck structure and export after migration.

## Troubleshooting

| Symptom | Check |
|---|---|
| Project will not open | File integrity and version |
| Blank editor | Node.js version and workspace permissions |
| Export fails | Fonts, assets, output path |
| Result differs | Reopen and inspect |

## Project layout

```text
photocraft-plugin/
├── .zcode-plugin/      # ZCode manifest and UI surface
├── skills/             # 22 skills
├── ui/                 # MCP Apps editor
├── commands/open.md    # open-editor command
├── docs/               # architecture and verification
└── assets/             # icons and templates
```

## Contributing and support

Include plugin version, host, input type, command, output file, and expected result. Do not attach sensitive assets.

## License

Apache-2.0. See [LICENSE](LICENSE).
