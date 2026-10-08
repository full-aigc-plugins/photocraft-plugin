# Cancellation artifact observation

The PC-TX-003 candidate now registers late files separately from technical and creative acceptance. A stop request and a stopped worker remain different states. Existing stop evidence is still required before an attempted task can become cancelled.

The harness records `photocraft-late-artifacts/v1` observations with the original task ID, request identity, owned worker token, output directory, per-file SHA-256, and observation time. Reconcile also observes already-cancelled tasks, allowing a fresh ledger session to register files that arrived after stop confirmation. Repeated identical observations do not add events. Changed snapshots append observations without replacing the earlier evidence.

Observation never executes the skill, replays an edit, parses a delivery claim as acceptance, or changes a cancelled task into completed. Files are hashed with bounded buffers. Symlinks, special files, concurrent changes, and inventories beyond 10,000 entries produce incomplete observations without following an external path or blocking the cancellation transition. Incomplete observations are evidence of missing inventory, not proof of absence or a verified artifact.

The regression uses synthetic worker and native-file fixtures to prove ownership binding, persistence, deduplication, and symlink refusal. It does not prove real native cancellation, interrupted native worker recovery, fixed-install acceptance, or creative quality. Tasks 3.9 and 10.12 remain open until all normative scenarios have current real evidence. Existing public releases do not contain this candidate change.
