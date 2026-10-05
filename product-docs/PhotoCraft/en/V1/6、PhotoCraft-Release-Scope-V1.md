# PhotoCraft V1 — Release-Scope

> **Purpose**: V1 implementation reading view; OpenSpec is normative.
>
> **Version**: 1.0.0
> **Updated**: 2026-10-05
> **Status**: Target design, not implemented. Observations and acceptance evidence are identified separately.

Related documents: [Brand boundary](../1%E3%80%81PhotoCraft-Naming-and-Brand.md) · [Technical plan](../5%E3%80%81PhotoCraft-Technical-Plan.md) · [Detailed architecture](../../../../docs/PhotoCraft-Runtime-Architecture.md) · [OpenSpec](../../../../openspec/changes/establish-v1-plugin/proposal.md) · [Evidence](../../../../docs/evidence/runtime-baseline.json)

## 1. V1 entrypoints

| Skill entry | Purpose | Status |
| :--- | :--- | :--- |
| photocraft-use | Maintained in independent skills; plugin pins snapshots | Planned |
| photocraft-setup | Maintained in independent skills; plugin pins snapshots | Planned |
| photocraft-inspect | Maintained in independent skills; plugin pins snapshots | Planned |
| photocraft-layers | Maintained in independent skills; plugin pins snapshots | Planned |
| photocraft-masks | Maintained in independent skills; plugin pins snapshots | Planned |
| photocraft-adjustments | Maintained in independent skills; plugin pins snapshots | Planned |
| photocraft-typography | Maintained in independent skills; plugin pins snapshots | Planned |
| photocraft-composition | Maintained in independent skills; plugin pins snapshots | Planned |
| photocraft-preview | Maintained in independent skills; plugin pins snapshots | Planned |
| photocraft-export | Maintained in independent skills; plugin pins snapshots | Planned |
| photocraft-recover | Maintained in independent skills; plugin pins snapshots | Planned |


## 2. Capabilities and gates

| Capability | Behavioral boundary | Status |
| :--- | :--- | :--- |
| Layered documents and edit identities | Keep explicit text, product and background layers with names, IDs, order, blend modes and visibility; flattening the entire document cannot satisfy editability acceptance. | Planned |
| Masks and local adjustments | Bind masks to target layers and record their scope; compare protected regions before and after local edits to prevent unintended modifications. | Planned |
| Typography and font dependencies | Preserve text, font, size, leading and layout; block typography-sensitive delivery when fonts are missing unless substitution is explicitly accepted. | Planned |
| Poster and cover variants | Derive separate aspect-ratio variants from the source project, recording crops, spacing and safe areas without overwriting the source. | Planned |
| Native and PSD fidelity | Use .pcraft as native authority; validate the PSD features used and record compatibility losses rather than promising universal lossless PSD support. | Planned |
| Flat export and provenance | Bind flat exports to source revisions, color profiles and transparency requirements; preserve receipts for generated inputs and account for generation separately from layer editing. | Planned |


## 3. Release partition

| Phase | Deliverable | Exit evidence |
| :--- | :--- | :--- |
| D0 | Bilingual documentation and OpenSpec baseline | Document, link and spec validation; implementation tasks remain open |
| M1 | Independent skills and runtime adapter | Clean installation, checksums and real MCP invocation |
| M2 | Complete domain workflow | Representative task, native reopen, decode and targeted revision |
| M3 | ArtCraft cross-plugin collaboration | Version propagation, selective invalidation and interruption recovery |
| M4 | Host and release acceptance | Actual host installation, platform evidence and synchronized catalogs |


## 4. Scope change rule

Add capability rows, risks and acceptance fixtures before specifying more effects, formats, platforms or providers. Changing export formats cannot bypass required native delivery.



---

**Document version**: 1.0.0
**Created**: 2026-10-05
**Updated**: 2026-10-05
**Document status**: Ready for review; implementation status is governed by OpenSpec tasks and evidence.
