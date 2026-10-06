# PhotoCraft smart content architecture

## Status and authority

This is an implementation checkpoint, not a published capability. OpenSpec PC-DM-001-SMART and PC-RT-002-SMART own the behavior. The official 0.2.0 runtime rejects ambient smart file commands, as exposed by the native first-use gate. The maintained runtime build and real candidate first use remain pending.

## Public workflow

`asset.placeSmart` accepts a registered image alias and optional center, fit and scale. Conversion and embedding require explicit layer IDs or explicit result references. Replace/relink accepts `{layer, asset}`; arbitrary paths, unknown fields, invalid IDs and nonfinite geometry are rejected. Paths are generated as collected relative filenames.

```mermaid
flowchart LR
    A[Registered image and digest] --> S[Collected staging file]
    S --> R[Directory capability read]
    R --> B[Validated image bytes]
    B --> E[Native smart object engine]
    E --> P[Embedded editable project]
    P --> O[Save and reopen]
    O --> M[Moved package and selective revision]
```

## Runtime boundary

The maintained patch routes only embedded placement and content replacement through directory-capability reads. It passes verified bytes to existing engine APIs rather than allowing ambient file operations. Collected relink requests become embedded replacements; embedding rejects an unregistered linked source. All other engine command guards remain intact. Absolute paths, escape paths and symlinks are rejected. Source kind and transform are exposed for preservation checks without disclosing external paths.

## Delivery and verification

Inputs retain hashes in the manifest. A native gate checks original and moved packages, smart transform, masks, unaffected layers, three independently decoded image pixels and invalid-path rejection. Persistent external links, all smart filters and external PSD editing require separate acceptance. [Checkpoint evidence](evidence/smart-workflow-checkpoint-20261006.json) records failed official-runtime first use, three passing input tests and 46 candidate automation tests. Build success alone will not close installation or editable-delivery gates.

Fixed Photo plugin dev.11 / source dev.10 / CLI 0.2.0-craft.1 installed-domain acceptance now passes; Art mixed upgrade remains pending. [Evidence / 证据](evidence/codex-photocraft11-smart-first-use-20261006.json)。
