# serve TCP shared-session reply supervision

PC-TX-005 /9.6 increment:source dev.52 /plugin dev.67 on pinned craft.5. Stdio and TCP use the same serve request/reply contract. Candidate and fixed publication/installation evidence remain separate; full9.6 is open.

The TCP frontend binds only127.0.0.1 and retains native64-hex authentication,16 connections,1 MiB request lines and30-second network IO timeout. Explicit token and token-file options override their corresponding environment variables; conflicting sources fail. Missing token files use O_EXCL and0600; existing files are read and reused without overwrite. Generated token/readiness messages retain native stderr format. Authentication messages never enter editing receipts or errorData.

Static launch refusal precedes installation and directory creation. Failed authentication, oversized lines and invalid first authenticated requests do not install a runtime. The first valid request installs the integrity-verified pinned CLI and starts one shared native stdio session. Connections share documents; complete invocation, reply validation and delivery hold one mutual-exclusion boundary. Absent/compound ids, native JSON-lines successes, document and PNG outputs remain valid. Native port literals retain optional+ and arbitrary leading zeros.

Malformed replies, mismatched identity, inner semantic errors, extra frames or lost delivery preserve the original request and validated receipts with stable code/phase/outcome/retryable/recoveryAction and no-replay markers. The owned native process closes and the shared session is quarantined. Other connections return serve_session_quarantined/not_executed without implicit restart or editing. Saved and source files remain intact; no rollback is claimed. Delivery lost after native success validation records reply_validated/unknown and cannot be relabeled unexecuted.

```bash
python3 -I -B "$SKILL_DIR/scripts/cli.py" -- serve --port 0 --control-token-file "$TOKEN_FILE" --automation-read-root "$READ_ROOT" --automation-write-root "$WRITE_ROOT"
```

Healthy two-connection editing, seven actual native post-save faults, cross-connection delivery-loss racing and owned-process exit have separate tests. Authentication/token files, connection/frame limits and actual idle timeout are checked independently. Aggregate interior confirmation, the complete launch/MCP input matrix and fullV1 still require their own evidence. Current batch only validates static steps and its outer reply; this does not prove stopping inside aggregates.
