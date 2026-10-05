# PhotoCraft V1 — Requirements-Analysis

> **Purpose**: V1 implementation reading view; OpenSpec is normative.
>
> **Version**: 1.0.0
> **Updated**: 2026-10-05
> **Status**: Target design, not implemented. Observations and acceptance evidence are identified separately.

Related documents: [Brand boundary](../1%E3%80%81PhotoCraft-Naming-and-Brand.md) · [Technical plan](../5%E3%80%81PhotoCraft-Technical-Plan.md) · [Detailed architecture](../../../../docs/PhotoCraft-Runtime-Architecture.md) · [OpenSpec](../../../../openspec/changes/establish-v1-plugin/proposal.md) · [Evidence](../../../../docs/evidence/runtime-baseline.json)

## 1. User stories

| Role | Need | Completion condition |
| :--- | :--- | :--- |
| Creator | Layer-preserving image editing and visual design | Create a poster and cover from product images; after reopening .pcraft, text, product and background remain independently editable; export verified PSD where applicable. |
| Reviewer | Inspect the current revision and localized findings | Every finding points to an object or frame |
| Maintainer | Diagnose and recover failures | Runtime identity, state ledger and reusable checkpoints exist |


## 2. Requirement analysis and acceptance mapping

| ID | Requirement | Behavior summary | Priority | Authority |
| :--- | :--- | :--- | :--- | :--- |
| PC-SK-001 | Canonical independent skills | Only immutable skill snapshots may be packaged. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/skills-distribution/spec.md) |
| PC-SK-002 | Standalone skills and dependencies | Standalone distribution must declare executable dependencies. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/skills-distribution/spec.md) |
| PC-RT-001 | Runtime provenance and integrity | Install verified, versioned runtime artifacts atomically. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/runtime-distribution/spec.md) |
| PC-RT-002 | Capabilities and isolated upgrades | Version, commands and execution mode are distinct compatibility gates. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/runtime-distribution/spec.md) |
| PC-TX-001 | Revision binding and single writer | Reject stale plans and concurrent native-project writers. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/task-execution/spec.md) |
| PC-TX-002 | Idempotency and unknown outcome recovery | An acknowledgement or timeout does not establish completion or failure. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/task-execution/spec.md) |
| PC-TX-003 | Cancellation and bounded execution | Cancellation requests require execution-side confirmation. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/task-execution/spec.md) |
| PC-AR-001 | Artifact lineage and bundle integrity | Paths alone are insufficient evidence of artifact identity. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/artifact-delivery/spec.md) |
| PC-AR-002 | Native editability and interchange loss | Preview success cannot prove native editability. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/artifact-delivery/spec.md) |
| PC-QA-001 | Separate technical and creative evidence | Each quality claim must identify its evidence and scope. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/quality-review/spec.md) |
| PC-QA-002 | Bounded targeted revision | Revisions must target evidence-backed findings within a bounded budget. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/quality-review/spec.md) |
| PC-RL-001 | Host and release evidence | Release readiness requires actual host and task evidence. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/release-compatibility/spec.md) |
| PC-RL-002 | Permissions and secret boundaries | Reject path escape, unsafe arguments and secret persistence. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/release-compatibility/spec.md) |
| PC-DM-001 | Layered documents and edit identities | Keep explicit text, product and background layers with names, IDs, order, blend modes and visibility; flattening the entire document cannot satisfy editability acceptance. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/domain-workflow/spec.md) |
| PC-DM-002 | Masks and local adjustments | Bind masks to target layers and record their scope; compare protected regions before and after local edits to prevent unintended modifications. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/domain-workflow/spec.md) |
| PC-DM-003 | Typography and font dependencies | Preserve text, font, size, leading and layout; block typography-sensitive delivery when fonts are missing unless substitution is explicitly accepted. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/domain-workflow/spec.md) |
| PC-DM-004 | Poster and cover variants | Derive separate aspect-ratio variants from the source project, recording crops, spacing and safe areas without overwriting the source. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/domain-workflow/spec.md) |
| PC-DM-005 | Native and PSD fidelity | Use .pcraft as native authority; validate the PSD features used and record compatibility losses rather than promising universal lossless PSD support. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/domain-workflow/spec.md) |
| PC-DM-006 | Flat export and provenance | Bind flat exports to source revisions, color profiles and transparency requirements; preserve receipts for generated inputs and account for generation separately from layer editing. | P0 | [OpenSpec](../../../../openspec/changes/establish-v1-plugin/specs/domain-workflow/spec.md) |


## 3. Conflict handling

When format, budget or asset permissions conflict, preserve explicit user constraints and block dependent steps while allowing independent inspection. Changes create new revisions and compute invalidation, rather than overwriting old plans and acceptance.



---

**Document version**: 1.0.0
**Created**: 2026-10-05
**Updated**: 2026-10-05
**Document status**: Ready for review; implementation status is governed by OpenSpec tasks and evidence.
