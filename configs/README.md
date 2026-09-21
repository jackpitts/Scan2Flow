# Configuration contracts

These TOML files describe the proposed backend configuration. They are valid TOML,
but no training, evaluation, or CFD backend consumes them in this scaffold.
`--dry-run` validates CLI arguments only: it does not read these files, resolve
paths, check schemas, inspect assets, or test hardware. A command without
`--dry-run` exits with code 3 because its backend is not implemented.

| File | Intended consumer | Purpose |
| --- | --- | --- |
| `train.toml` | `scan2flow train --config` | Dataset contract, baseline model, optimization, reproducibility, promotion policy |
| `evaluate.toml` | `scan2flow evaluate --config` | Frozen evaluation preprocessing, metrics, slices, and acceptance criteria |
| `cfd-external.toml` | `scan2flow prepare-cfd --domain` | External fluid enclosure and geometric patch selection |
| `cfd-internal.toml` | `scan2flow prepare-cfd --domain` | Explicit internal fluid-region extraction and opening definitions |

The planned parser will reject unknown keys, invalid units, missing assets, and
inconsistent configuration versions. Relative asset paths will resolve against the
working directory from which the command is invoked; examples assume the repository
root. Paths inside dataset records resolve against their manifest's directory. CFD coordinate
values and all fields ending in `_m` use metres after input-unit conversion.

CLI arguments will govern execution placement and reproducibility: `--output`,
`--device`, `--seed`, `--resume`, and `--split` are deliberately absent where the
CLI already owns them. In evaluation, the checkpoint's saved preprocessing contract
must match the evaluation configuration; an override must never silently replace it.

Numerical settings are initial experiment proposals, not measured performance or
validated engineering limits. Both example evaluation policies leave promotion
thresholds unset and explicitly disable promotion until limits have been calibrated on representative
objects and reviewed. Domain extents and patch coordinates require case-specific
editing; they are not universal CFD recommendations.
