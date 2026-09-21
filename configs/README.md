# User CFD-domain templates

These files describe proposed fluid-domain settings for `scan2flow prepare-cfd`:

| File | Purpose |
| --- | --- |
| `cfd-external.toml` | Enclosure around the object and boundary-region selection |
| `cfd-internal.toml` | Internal fluid region, explicit openings and caps |

All coordinate values and fields ending in `_m` use metres after input-unit
conversion. Relative paths resolve from the command's working directory. Domain
extents and patch coordinates require case-specific editing; the supplied numbers
are illustrative and are not validated for your object.

The scaffold records `--domain` but does not read TOML or create geometry.
A future backend must reject unknown keys, incompatible units and disagreement
between the configuration and `--flow`.

Training and model-evaluation templates belong to [developer tooling](../development/configs/README.md),
not this user configuration directory.
