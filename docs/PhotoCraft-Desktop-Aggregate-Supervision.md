# PhotoCraft desktop aggregate supervision

The owned desktop wrapper now forwards the remaining aggregate timeout to the actual MCP stdio session and restores its original value after the batch. A wrapper must not reset the shared batch deadline for each child request. The canonical implementation is `skills/photocraft-use/scripts/desktop_session.py`; managed skills are synchronized from this source.

The candidate uses the locked signed PhotoCraft desktop 0.2.0 and maintained CLI craft.5. Twelve actual GUI cases cover healthy result references and checkpoint/save/reopen, legal notifications, native failure with explicit continue, seven reply faults, cumulative response budget and the aggregate deadline. Readonly live inspection is test observation, not automatic recovery or replay. Only the test-owned GUI and CLI are closed. The source and pre-batch checkpoint remain unchanged and reopenable; the later save is absent on failure.

A real stdio delayed-response test reproduces the wrapper defect. The same native GUI deadline case also fails against the public dev.54 source. This is candidate evidence; fixed dev.55 / plugin dev.70 installation and publication are recorded separately. The complete public input matrix and PC-TX-005 task 9.6 remain open until their own acceptance audit passes.

The signed desktop receives control through the owned loopback listener, token file and per-run data directory. The test does not attach to an existing user GUI or modify the global runtime. Technical/native evidence does not constitute creative acceptance.
