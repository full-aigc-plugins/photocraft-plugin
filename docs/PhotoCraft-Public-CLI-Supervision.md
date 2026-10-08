# Supervised public CLI

Increment for PC-TX-005 / task 9.6; a development release that does not close the entire task.

After installation and digest verification, cli.py run, batch, convert and droplet verify native supervision metadata against the locked craft.5 version, then use per-step acknowledgements. Other read-only entries retain their existing invocation.

Each event validates strict JSON, sequence, tool, arguments and tool reply. Open/save replies validate paths; batch binds input/output order. Only validated replies receive continue. Valid calls retain their legacy visible output.

Malformed, semantic-error or unknown replies stop further acknowledgements and settle the owned child process. Failures retain code, phase, outcome, retryable, recoveryAction, receipts, lastAttempt and runtime digest, with replayAllowed false. Existing files remain; completed edits are not claimed to have rolled back.

Fifteen real native post-save fault scenarios cover all four entries. Tests inject faults only at the native reply transport, checking that later edits stop, original project digests remain unchanged, saved files reopen and no replay occurs. Installed-copy acceptance and source regression are recorded separately.

Streaming mcp/serve, TCP/port and nested aggregate replies are not integrated with this supervisor. This contract does not replace workflow protectedRegions, pixel preservation or full V1 acceptance.
