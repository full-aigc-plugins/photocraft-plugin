# PhotoCraft Independent PSD Decode First-use Acceptance

Pinned plugin dev.9 / skill source dev.8 was used. After the previous temporary host directory became unavailable, the five plugins were installed again in isolation from ArtCraft's release lock. Codex 0.153.4 discovered all 58 skills without loading errors. The installed `photocraft-cli-export` was copied alone into `.agents/skills/`; a fresh runtime home downloaded pinned CLI 0.2.0 and produced a poster, text revision and cover.

The native poster retains four separately editable Background, Product, Headline and Caption layers. The product mask hides pixels outside its selected region. Revising the headline to NOVA PLUS preserves the product, background and caption layers and all PNG pixels below the headline region. A 360×440 cover is saved from the revised source, preserving layer IDs/types, product mask and headline content. Every file in both source delivery directories and the input product digest remains unchanged.

Each PSD merged image is independently decoded by the existing Pillow 12.3.0 installation and matches every RGB pixel of its PNG. All three canvases are opaque, with PNG alpha 255; this does not prove transparent PSD merged-alpha fidelity. Editable layer/text/mask semantics are observed through independent native reopen and PhotoCraft's own PSD inspection. Pillow merged-image checks are not another editor's live text/mask editing acceptance.

The actual target test passed once in 5.640 seconds. The default source regression had 53 tests: 36 passed and 17 opt-in tests skipped. Skips do not establish acceptance. All 58 installed skill hashes still match their host receipt after execution. See [PSD evidence](evidence/codex-photo9-independent-psd-first-use-20261006.json) and [reinstallation discovery evidence](evidence/codex-five-plugin-reinstall-discovery-20261006.json).

No additional dependency was installed and no pinned skill/native CLI was changed. Actual Photoshop editing, transparent PSDs, complete effect/blend mappings, model dispatch, creative review and production marketplace acceptance remain outside these fixtures.
