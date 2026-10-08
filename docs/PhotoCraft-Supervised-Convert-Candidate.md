# PhotoCraft supervised conversion candidate

Plugin dev.48 pins source dev.42, packaging internal run/batch/convert supervisor candidates. Public cli.py and maintained craft.1 runtime remain unchanged; craft.4 is a separately built, unactivated candidate.

The read-only metadata gate rejects unsupported runtimes before submitting edits. Conversion preserves native open/save semantics, validates each reply and acknowledges sequence1 before save and sequence2 before success. Invalid post-save replies retain the real saved output and unknown receipt; requests are never replayed. Capability metadata is separate from binary provenance validation.

[Candidate evidence](evidence/optimization/supervised-convert/candidate.json) records30 focused tests and58 Rust tests. [Complete source regression](evidence/optimization/supervised-convert/source-validation.json):270 passed, zero skips, unchanged execution source. Old-runtime zero-edit refusal, four formats and six post-save fault classes are covered. Publication does not establish fixed candidate installation, streaming, droplet or full PC-TX-005 acceptance. Task9.6 stays open;129/157 tasks complete,28 open. Earlier dev.47 fixed-installation evidence remains historical and is not acceptance for this release.

[Source design](https://github.com/full-aigc-skills/photocraft-skills/blob/v0.1.0-dev.42/docs/PhotoCraft-Supervised-Convert-Candidate.md).
