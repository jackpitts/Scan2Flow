# Local datasets

Store licensed data here or in an explicitly configured external dataset tree.
Large and private assets are excluded from Git; only these directory guides are
tracked. No sample media or CAD supervision is supplied.

| Directory | Intended content |
| --- | --- |
| `raw/images/` | Original object photographs and capture metadata |
| `raw/videos/` | Original video clips, timestamps, and capture metadata |
| `raw/lidar/` | Original scans with sensor scale and coordinate conventions |
| `cad/` | Paired ground-truth STEP geometry and native CAD provenance |
| `annotations/` | Feature labels, segmentation, dimensional measurements, and quality review |
| `manifests/` | Frozen JSONL train, validation, and test records |
| `processed/` | Reproducible frames, masks, registered points, targets, and transform records |

Record source rights, hashes, sensor calibration, object identity, and dataset
version before processing. Keep raw assets immutable. Manifest asset paths resolve
relative to the manifest's directory; for example, `../raw/images/object/front.jpg`
inside `data/manifests/train.jsonl`. See the
[dataset contract](../schemas/dataset-record.schema.json) and
[text-only examples](../examples/README.md).

Splits must isolate all shared object, design-family, and capture-session groups,
including synthetic renders and augmented derivatives. Cached preprocessing must
include the data hash and transform version so a stale cache cannot silently alter
evaluation. Use external versioned storage for real data snapshots; adding a path
to this directory does not make that storage reproducible.
