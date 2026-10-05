# PhotoCraft — Technical-Plan

> **Purpose**: Product boundaries and cross-version decisions.
>
> **Version**: 1.0.0
> **Updated**: 2026-10-05
> **Status**: Target design, not implemented. Observations and acceptance evidence are identified separately.

Related documents: [Brand boundary](1%E3%80%81PhotoCraft-Naming-and-Brand.md) · [Technical plan](5%E3%80%81PhotoCraft-Technical-Plan.md) · [Detailed architecture](../../../docs/PhotoCraft-Runtime-Architecture.md) · [OpenSpec](../../../openspec/changes/establish-v1-plugin/proposal.md) · [Evidence](../../../docs/evidence/runtime-baseline.json)

## 1. Technical decisions and alternatives

| ADR | Decision and rationale | Alternative and reversal condition |
| :--- | :--- | :--- |
| ADR-001 | Independent skills repositories with immutable snapshots inside plugin packages | Reject sibling symlinks; add host dependency resolution only after it is verified |
| ADR-002 | Reuse official Rust CLIs through controlled MCP/argv | Do not rewrite editors; surface missing APIs before adding adapters |
| ADR-003 | Target TypeScript and Node.js 24 LTS for orchestration, matching ecosystem experience | Pin patch versions and dependencies during implementation; design is not compatibility proof |
| ADR-004 | SQLite ledger and content-addressed files for a local single-user workspace | Revisit service storage only when multi-machine collaboration is required |
| ADR-005 | ArtCraft OpenSpec owns shared task and artifact protocols | Domain repositories own mappings and consumer tests, not competing field definitions |
| ADR-006 | Separate technical gates from creative review; preserve valid existing authorization | Do not require approval per call; obtain new authority only when scope changes |

## 2. Independent skill supply chain

`photocraft-skills` is the planned independent knowledge repository and is not yet published. It owns SKILL.md, references and portable helper scripts where required. The plugin resolves a fixed tag to a commit, verifies the whole skill tree and packages it in `skills/`. Release checks run in a clean export and verify links, licenses, inventory and locks. The current skills lock has no sources; no version or digest is fabricated.

| Stage | Input | Failure rule |
| :--- | :--- | :--- |
| resolve | repository + immutable tag | Stop on unresolved tags or disallowed provenance |
| verify | commit + tree digests | Reject any content drift |
| package | skills inventory | Reject escaping links and duplicate names |
| audit | clean install fixture | Standalone skill installs must resolve public dependencies |

## 3. Domain plan compilation strategy

| Capability | Behavioral boundary | Status |
| :--- | :--- | :--- |
| Layered documents and edit identities | Keep explicit text, product and background layers with names, IDs, order, blend modes and visibility; flattening the entire document cannot satisfy editability acceptance. | Planned |
| Masks and local adjustments | Bind masks to target layers and record their scope; compare protected regions before and after local edits to prevent unintended modifications. | Planned |
| Typography and font dependencies | Preserve text, font, size, leading and layout; block typography-sensitive delivery when fonts are missing unless substitution is explicitly accepted. | Planned |
| Poster and cover variants | Derive separate aspect-ratio variants from the source project, recording crops, spacing and safe areas without overwriting the source. | Planned |
| Native and PSD fidelity | Use .pcraft as native authority; validate the PSD features used and record compatibility losses rather than promising universal lossless PSD support. | Planned |
| Flat export and provenance | Bind flat exports to source revisions, color profiles and transparency requirements; preserve receipts for generated inputs and account for generation separately from layer editing. | Planned |

The planner emits a declarative plan. The compiler validates command availability, fields, units and bounds, then emits typed operations. Inspect source objects to obtain real IDs first. Compilation records planHash and capabilitySnapshotHash and returns unsupported_mapping for unsupported operations; only verified mappings reach submission.

## 4. Runtime installation and management

Runtime management separates discover, verify, install, probe, activate, upgrade and rollback. Reuse compatible existing installs after verification. Pin download URLs and digests, reject archive traversal and escaping symlinks, and verify before execution. Versioned installs do not overwrite active binaries and preserve prior receipts. An untested platform is unverified; a universal ZIP does not prove every architecture works.

## 5. Submission, recovery and artifact protocol

Use persisted intent, idempotency keys and single-writer leases. Even synchronous CLIs without external task IDs require attempt IDs, process identity, checkpoints and expected outputs. After process failure, inspect projects and files rather than blindly rerunning. Reconciliation handles the gap between file creation and ledger registration. Validate native projects and exports separately; list non-redistributable dependencies and fonts with verifiable acquisition instructions.

## 6. Test plan and acceptance assets

| Layer | Required coverage | Evidence |
| :--- | :--- | :--- |
| contract | Missing/unknown fields, idempotency and revision conflicts | schema + fixture results |
| adapter | Real command discovery, mode differences and error mapping | runtime identity + transcript |
| recovery | Disconnect after submit, late results and unconfirmed cancellation | ledger before/after + duplicate count |
| native | Create a poster and cover from product images; after reopening .pcraft, text, product and background remain independently editable; export verified PSD where applicable. | project reopen + output inspection |
| host | Clean host install, upgrade and user-data preserving uninstall | host/version/platform + logs |

## 7. Implementation route

| Phase | Deliverable | Exit evidence |
| :--- | :--- | :--- |
| D0 | Bilingual documentation and OpenSpec baseline | Document, link and spec validation; implementation tasks remain open |
| M1 | Independent skills and runtime adapter | Clean installation, checksums and real MCP invocation |
| M2 | Complete domain workflow | Representative task, native reopen, decode and targeted revision |
| M3 | ArtCraft cross-plugin collaboration | Version propagation, selective invalidation and interruption recovery |
| M4 | Host and release acceptance | Actual host installation, platform evidence and synchronized catalogs |

Use dependency order without invented dates or effort estimates. Each OpenSpec task carries a requirement ID, owner role, output and validation. Start with failing behavior tests, implement minimally, and leave tasks unchecked until evidence exists.

## 8. Operations, upgrade and release

Plugin, skills, upstream CLI and protocol versions evolve independently. Release matrices pin their combinations; host manifests and marketplace metadata must match verified commits and locks. The documentation baseline ships no installable plugin package; M4 gates the first installable release. Roll back to a previously verified plugin/skills/CLI combination; restore backups when state migrations are incompatible.

---

**Document version**: 1.0.0
**Created**: 2026-10-05
**Updated**: 2026-10-05
**Document status**: Ready for review; implementation status is governed by OpenSpec tasks and evidence.

Exchange delivery now includes exchange-loss.json binding native, reopened inspection and exports by digest. Derivatives never substitute for native projects; cross-editor font, effect and mask fidelity remains explicitly unknown until separate acceptance.
