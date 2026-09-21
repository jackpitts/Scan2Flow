# Model artifacts

This directory holds future trained artifacts, not Python model definitions.
Definitions belong under `src/scan2flow/models/`. No weights or pretrained model are
distributed with this scaffold.

- `checkpoints/`: immutable run checkpoints, optimizer/RNG state, and candidate bundles.
- `exports/`: approved inference bundles and optional interchange exports.
- `MODEL_CARD_TEMPLATE.md`: required evidence and limitations to record per bundle.

The proposed bundle manifest follows
[`model-bundle.schema.json`](../schemas/model-bundle.schema.json). Keep weights,
configuration, preprocessing, environment, dataset references, hashes, and evaluation
evidence together. Prefer non-executable tensor serialization for weights; a safe
format does not establish provenance, and a checksum is useful only when its
expected value comes from a trusted source. Do not load untrusted pickle checkpoints.

Store large bundles in a versioned artifact store outside Git. Reference an immutable
approved bundle for reconstruction; retain the previous approved version for rollback.
Promotion is disabled in the example configurations until case-specific gates exist.
