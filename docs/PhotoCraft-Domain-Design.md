# PhotoCraft Domain technical design

> **Purpose**: Translate domain scenarios into compilable plans, fixtures and artifact checks.
>
> **Version**: 1.0.0
> **Updated**: 2026-10-05
> **Status**: Target design, not implemented. Observations and acceptance evidence are identified separately.

## 1. Plan boundary

The fields below are a proposed domain-plan design, not released CLI arguments. Implement final JSON schemas and consumer tests through the corresponding OpenSpec tasks; ArtCraft specifications remain authoritative for the shared task envelope.

| Field | Shape | Semantics |
| :--- | :--- | :--- |
| document | id, width, height, colorMode, bitDepth, profileRef | Dimensions and color management constrain the document |
| layers[] | id, role, kind, sourceRef, order, transform | Text/product/background roles remain separately editable |
| masks[] | id, targetLayerId, sourceRef, bounds | Bound local edits and define protected regions |
| typography[] | layerId, text, fontRef, size, leading, bounds | Expose missing font dependencies; never substitute randomly from the machine |
| variants[] | id, sourceRevision, width, height, crop, layoutOverrides | Variants reference a source revision; overrides do not mutate the master |

## 2. Compilation and execution

1. Verify assets and native-project revisions and preserve a checkpoint.
2. Discover command schemas, object IDs, units and available capabilities in the actual session.
3. Validate the domain plan and reject unsupported mappings with field-level errors.
4. Compile operations with stable object mapping, plan hash and runtime identity.
5. Execute under a single-writer lease and persist confirmed steps.
6. Save, close and reopen the native project, then export and collect evidence.
7. Use input/object diffs for targeted revisions and preserve unchanged parts.

## 3. Observed entrypoints and capability gates

| MCP tool | Evidence boundary |
| :--- | :--- |
| command_list | Listed by the installed CLI through tools/list; only command_list has a recorded read-only execution probe. Other calls and editing outcomes are unverified |
| command_run | Listed by the installed CLI through tools/list; only command_list has a recorded read-only execution probe. Other calls and editing outcomes are unverified |
| doc_new | Listed by the installed CLI through tools/list; only command_list has a recorded read-only execution probe. Other calls and editing outcomes are unverified |
| doc_inspect | Listed by the installed CLI through tools/list; only command_list has a recorded read-only execution probe. Other calls and editing outcomes are unverified |
| doc_render_preview | Listed by the installed CLI through tools/list; only command_list has a recorded read-only execution probe. Other calls and editing outcomes are unverified |
| doc_save | Listed by the installed CLI through tools/list; only command_list has a recorded read-only execution probe. Other calls and editing outcomes are unverified |

Tool names route discovery; parameters must come from actual inputSchema or describe results. Never guess object IDs from examples.

## 4. First acceptance fixture

A 1200×1600 poster and 1600×900 cover with editable text, product and background and a mask-bound local adjustment. Reopen the native document and inspect all three object roles; compare protected regions, not just thumbnails.

Test assets and references must be redistributable and record fixed seeds or inputs. Set technical thresholds before execution; do not relax them after failures. Visual judgments record reference revision, evaluator and localized evidence.

## 5. Targeted revision and invalidation

Operation cache keys cover input hashes, object selection, edit parameters, runtime identity and output settings. Object IDs are not globally unique across projects and must bind a project revision. Re-inspect after user edits; if mapping is ambiguous, reject automatic overwrite and retain both versions. Local project edits and partial renderer caching are different capabilities: preserve untouched objects, but claim render-cache reuse only when upstream support is actually tested.

## 6. Delivery checklist and downstream consumption

| File or record | Check | Failure behavior |
| :--- | :--- | :--- |
| .pcraft | Reopen and inspect objects and dependencies | Do not claim editable delivery |
| Preview and final export | Identify format, dimensions, duration and color/alpha | Retain diagnostics and rerun affected steps |
| Asset dependencies | Hashes, licensing, fonts and relative references | List missing items and block incomplete delivery |
| Acceptance record | Bind current artifacts, plan and runtime identity | Invalidate stale records without inheriting acceptance |

## 7. Specifications and implementation tasks

[Domain OpenSpec](../openspec/changes/establish-v1-plugin/specs/domain-workflow/spec.md) · [Tasks](../openspec/changes/establish-v1-plugin/tasks.md) · [Traceability](traceability.json)

---

**Document version**: 1.0.0
**Created**: 2026-10-05
**Updated**: 2026-10-05
**Document status**: Ready for review; implementation status is governed by OpenSpec tasks and evidence.
