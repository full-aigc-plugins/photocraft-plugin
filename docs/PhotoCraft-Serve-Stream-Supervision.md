# serve stdio reply supervision candidate

This increment implements the serve stdio portion of PC-TX-005 / task9.6 on published source dev.51 and pinned craft.5. It is not a new publication or fixed plugin installation acceptance. Full9.6 remains open.

Public cli.py serve installs and starts its owned native process only after the first valid JSON-lines request. Strict JSON, method, parameter containers, captured command parameters and batch steps are checked statically. doc.open/save/render paths follow native workspace syntax: absolute paths, traversal, Windows prefixes, empty components and reserved devices are refused. Native directory capabilities still control actual authority.

Success preserves id/ok/result, including absent and compound JSON ids, session.list objects, all file.new parameters through doc.new, PNG base64 and render-file receipts. Identity, structure, inner error and path validation precede success forwarding and the next request. Failure adds errorData with code/phase/outcome/retryable/recoveryAction, original request, validated receipts and replayAllowed:false; valid native error strings are preserved. No replay or claimed rollback; already saved files remain intact.

Actual craft.5 tests inject duplicate keys, nonfinite values, semantic failure, mismatched id, extra frame, malformed error and missing ok after a native save. No later edit is sent; original digests stay unchanged and saved projects reopen. Healthy tests cover image/file rendering, compound/absent ids, nullable params and additional file.new parameters.

```bash
python3 -I -B "$SKILL_DIR/scripts/cli.py" -- serve --automation-read-root "$READ_ROOT" --automation-write-root "$WRITE_ROOT"
```

TCP/port, batch interior supervision and the complete argv/dynamic authority input matrix still need implementation and fixed installation acceptance. Current batch checks all static steps and its outer reply; this cannot prove stopping inside an aggregate. This candidate does not close9.6 or fullV1.
