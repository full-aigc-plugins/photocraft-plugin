# Supervised MCP streaming replies

Incremental candidate for PC-TX-005 / 9.6, targeting source dev.51 / plugin dev.66. The complete task remains open.

Public cli.py mcp installs lazily and forwards serially. Invalid first strict JSON, tool structure or captured parameters fail before installation/session creation. Every skill carries independent resources. Valid requests trigger installation and digest verification of locked craft.5.

Client string/numeric IDs, initialization, notifications, valid tool JSON and image content retain their protocol. Initialization validates metadata structure/version; tool replies validate structure, inner semantics and open/save paths. Pending extra responses are rejected before success receipts or subsequent edits. JSON-RPC error.data preserves the request, phase, outcome, retryable, recoveryAction, validated receipts and no-replay marker. The owned process is settled; completed saves remain and are not claimed to be rolled back.

Actual public-entry tests inject duplicate keys, nonfinite numbers, semantic errors, mismatched IDs, extra responses and malformed JSON-RPC errors after real native saves. They verify no next edit is sent, original digests remain unchanged and saved files reopen. The extra-response red test sent the later rename before the fix. A healthy path separately verifies string IDs, notifications and actual image preview.

Example (both roots must be actual user-authorized directories; project parameters use paths relative to these roots):

```bash
python3 -I -B "$SKILL_DIR/scripts/cli.py" -- mcp --automation-read-root "$READ_ROOT" --automation-write-root "$WRITE_ROOT"
```

Serve stdio, TCP/port and per-step acknowledgement inside aggregates are not integrated in this increment. Outer reply validation does not prove internal aggregate stopping. Source regression, public fixed installation and complete task9.6 acceptance are recorded separately; full V1 remains open.
