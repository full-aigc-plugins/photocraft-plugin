# Step-confirmed serve batches

PC-TX-005 /9.6 increment for source dev.53 and plugin dev.68. Stdio and TCP `batch` requests are decomposed into native single-step calls in the same pinned craft.5 session. Strict preflight covers the entire request before installation, launch or output creation; oversized native 1 MiB outer frames and invalid later steps are refused first.

Each reply passes identity, envelope and semantic validation and the cumulative response budget before a reply_validated receipt and the next step. Healthy `{completed,failed,results}` output and compound/absent client IDs remain valid. The original total deadline does not restart per step. Retained results preserve the native 8 MiB response budget with request-ID/envelope reservation.

Malformed post-save replies and inner errors stop immediately. Diagnostics retain the original request, current child request, zero-based stepIndex, confirmedSteps and validated child receipts. No aggregate success or replay is emitted. `stopOnError:false` cannot bypass the declared failure-stop/unknown-reconciliation contract: the prior outer supervisor already refused failed batches; this change stops before the next edit. TCP holds the shared lock through the entire batch and delivery, then quarantines all connections on failure. Saved and source files remain; no rollback is claimed.

Tests cover actual intermediate native failures, seven actual post-save reply faults for each transport, cumulative response-budget refusal and healthy mixed command/document/PNG batches. Candidate and public fixed-installation evidence are separate. MCP command_batch, aggregate tools in command plans, the full entry input matrix and complete9.6 still require their own acceptance. This increment closes no tasks.
