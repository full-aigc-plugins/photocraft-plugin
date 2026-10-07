# Fixed public protocol authority

The four domain plugins consume the ArtCraft-owned craft-task/v1 and craft-artifact/v1 contracts. `contracts-reference.json` pins release v0.1.0-dev.109, its commit, and SHA-256 for both specifications and schemas. ArtCraft remains the sole authority; domain plugins do not maintain schema copies.

The documentation gate rejects floating identities, unexpected versions, missing files, and inconsistent URLs. Offline structural validation does not authenticate source bytes. Maintainers separately run the verifier against an ArtCraft checkout containing the pinned tag:

```bash
python3 -I -B scripts/contract_reference.py --authority /path/to/artcraft-plugin
```

This checks the tag commit and all four Git object hashes without reading mutable working-tree files. A protocol update requires an explicit new verified release and regenerated references. This reference does not lock the executable runtime or establish complete task protocol, host, or first-use acceptance. Existing immutable plugin releases retain their previous references until a new release is published.

CI also checks out the exact owner commit and verifies tag identity plus content digests; it does not follow the owner main branch.
