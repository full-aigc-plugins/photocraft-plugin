# PhotoCraft — Capabilities-and-Roadmap

> **Purpose**: Product boundaries and cross-version decisions.
>
> **Version**: 1.0.0
> **Updated**: 2026-10-05
> **Status**: Target design, not implemented. Observations and acceptance evidence are identified separately.

Related documents: [Brand boundary](1%E3%80%81PhotoCraft-Naming-and-Brand.md) · [Technical plan](5%E3%80%81PhotoCraft-Technical-Plan.md) · [Detailed architecture](../../../docs/PhotoCraft-Runtime-Architecture.md) · [OpenSpec](../../../openspec/changes/establish-v1-plugin/proposal.md) · [Evidence](../../../docs/evidence/runtime-baseline.json)

## 1. Capability entrypoints

| Entry | Purpose | Version |
| :--- | :--- | :--- |
| photocraft-use | Domain knowledge or workflow entry; currently planned | V1 |
| photocraft-setup | Domain knowledge or workflow entry; currently planned | V1 |
| photocraft-inspect | Domain knowledge or workflow entry; currently planned | V1 |
| photocraft-layers | Domain knowledge or workflow entry; currently planned | V1 |
| photocraft-masks | Domain knowledge or workflow entry; currently planned | V1 |
| photocraft-adjustments | Domain knowledge or workflow entry; currently planned | V1 |
| photocraft-typography | Domain knowledge or workflow entry; currently planned | V1 |
| photocraft-composition | Domain knowledge or workflow entry; currently planned | V1 |
| photocraft-preview | Domain knowledge or workflow entry; currently planned | V1 |
| photocraft-export | Domain knowledge or workflow entry; currently planned | V1 |
| photocraft-recover | Domain knowledge or workflow entry; currently planned | V1 |


## 2. Functional scope

| Capability | Behavioral boundary | Status |
| :--- | :--- | :--- |
| Layered documents and edit identities | Keep explicit text, product and background layers with names, IDs, order, blend modes and visibility; flattening the entire document cannot satisfy editability acceptance. | Planned |
| Masks and local adjustments | Bind masks to target layers and record their scope; compare protected regions before and after local edits to prevent unintended modifications. | Planned |
| Typography and font dependencies | Preserve text, font, size, leading and layout; block typography-sensitive delivery when fonts are missing unless substitution is explicitly accepted. | Planned |
| Poster and cover variants | Derive separate aspect-ratio variants from the source project, recording crops, spacing and safe areas without overwriting the source. | Planned |
| Native and PSD fidelity | Use .pcraft as native authority; validate the PSD features used and record compatibility losses rather than promising universal lossless PSD support. | Planned |
| Flat export and provenance | Bind flat exports to source revisions, color profiles and transparency requirements; preserve receipts for generated inputs and account for generation separately from layer editing. | Fixed RGB8 contract verified; live generation/billing unverified |


## 3. Navigation and routing

Route single-domain requests directly and mixed scenarios to ArtCraft. Inspect before execution and return bounded availability when capabilities are missing. Choose executors by requested native format, not silent substitution. Lifecycle operations are shared; concrete commands are adapter-specific.

## 4. Release cadence

| Phase | Deliverable | Exit evidence |
| :--- | :--- | :--- |
| D0 | Bilingual documentation and OpenSpec baseline | Document, link and spec validation; implementation tasks remain open |
| M1 | Independent skills and runtime adapter | Clean installation, checksums and real MCP invocation |
| M2 | Complete domain workflow | Representative task, native reopen, decode and targeted revision |
| M3 | ArtCraft cross-plugin collaboration | Version propagation, selective invalidation and interruption recovery |
| M4 | Host and release acceptance | Actual host installation, platform evidence and synchronized catalogs |




---

**Document version**: 1.0.0
**Created**: 2026-10-05
**Updated**: 2026-10-05
**Document status**: Ready for review; implementation status is governed by OpenSpec tasks and evidence.
