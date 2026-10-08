# PhotoCraft integer overflow contract

Plugin dev.49 pins source dev.43 with pre-install refusal of integer literals outside the native finite f64 range. Token text is checked before Python integer construction, preserving exact field paths even for5000-digit literals; finite large integers retain their previous type.

[Focused evidence](evidence/optimization/integer-overflow/candidate.json) covers parser/MCP/tool replies and52 observed public-entry refusals across13 independent skills. Invalid input returns nonfinite_json_value, validation / not_executed, retryable=false and correct_plan. Installation/session counters stay zero; original files, runtime caches and output directories remain unchanged. Original RED captures attempted installation; long-literal RED captures lost field paths. Complete source regression and fixed public-copy acceptance are recorded separately.

[Droplet candidate](PhotoCraft-Supervised-Droplet-Candidate.md) is packaged alongside the fix; its native craft.5 runtime is not activated. Public runtime remains craft.1. Task9.6, streaming, nested aggregate internals, public supervisor integration, persistent raw recovery and full V1 remain open.
