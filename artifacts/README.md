# Generated run outputs

Future commands write user-selected output directories here by convention.
Generated content is ignored by Git. This scaffold creates no CAD, reports, weights,
meshes, or solver results when invoked.

| Directory | Intended content |
| --- | --- |
| `reconstruction/` | Object CAD, tessellated surfaces, coordinate provenance, quality reports |
| `training/` | Run configuration, logs, checkpoints, environment and data snapshots |
| `evaluation/` | Baseline comparisons, per-object metrics, slice results, failure examples |
| `cfd/` | Fluid-domain geometry, patch assignments, and geometric validation reports |

Use a unique directory per run and preserve code, config, dataset, and model hashes.
The planned backend rejects existing output paths rather than silently replacing a
run. CAD geometry and a patch map are inputs to a separate meshing and solver process.
