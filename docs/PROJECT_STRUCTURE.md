# Project directory and file skeleton

This is the complete tracked foundation. Generated datasets, checkpoints, build
outputs, virtual environments and caches are excluded. A directory containing only
`README.md` reserves a location and describes its intended contents; it does not
contain a working backend or bundled assets.

The working code is `src/scan2flow/cli.py` and the package entry points. Each other
source package currently contains only an `__init__.py` role description. Tests
exercise the CLI scaffold, including error paths and absence of processing side
effects. Configurations, schemas and examples are proposed backend contracts.

```text
Scan2Flow/
├── .github/
│   └── workflows/
│       └── ci.yml
├── artifacts/
│   ├── cfd/
│   │   └── README.md
│   ├── evaluation/
│   │   └── README.md
│   ├── reconstruction/
│   │   └── README.md
│   ├── training/
│   │   └── README.md
│   └── README.md
├── configs/
│   ├── cfd-external.toml
│   ├── cfd-internal.toml
│   └── README.md
├── data/
│   ├── annotations/
│   │   └── README.md
│   ├── cad/
│   │   └── README.md
│   ├── manifests/
│   │   └── README.md
│   ├── processed/
│   │   └── README.md
│   ├── raw/
│   │   ├── images/
│   │   │   └── README.md
│   │   ├── lidar/
│   │   │   └── README.md
│   │   └── videos/
│   │       └── README.md
│   └── README.md
├── development/
│   ├── configs/
│   │   ├── evaluate.toml
│   │   ├── README.md
│   │   └── train.toml
│   ├── evaluation/
│   │   └── __init__.py
│   ├── training/
│   │   └── __init__.py
│   ├── ARCHITECTURE.md
│   ├── ECC_WORKFLOW.md
│   └── ML_PIPELINE.md
├── docs/
│   ├── CFD_GUIDE.md
│   ├── CLI_REFERENCE.md
│   └── PROJECT_STRUCTURE.md
├── examples/
│   ├── calibration/
│   │   ├── camera.example.json
│   │   └── lidar.example.json
│   ├── manifests/
│   │   └── dataset.example.jsonl
│   ├── reports/
│   │   └── reconstruction.example.json
│   ├── commands.md
│   └── README.md
├── models/
│   ├── checkpoints/
│   │   └── README.md
│   ├── exports/
│   │   └── README.md
│   ├── MODEL_CARD_TEMPLATE.md
│   └── README.md
├── notebooks/
│   └── README.md
├── schemas/
│   ├── calibration.schema.json
│   ├── dataset-record.schema.json
│   ├── model-bundle.schema.json
│   ├── README.md
│   └── reconstruction-report.schema.json
├── scripts/
│   └── README.md
├── src/
│   └── scan2flow/
│       ├── cad/
│       │   └── __init__.py
│       ├── cfd/
│       │   └── __init__.py
│       ├── data/
│       │   └── __init__.py
│       ├── ingestion/
│       │   └── __init__.py
│       ├── models/
│       │   └── __init__.py
│       ├── pipeline/
│       │   └── __init__.py
│       ├── preprocessing/
│       │   └── __init__.py
│       ├── reconstruction/
│       │   └── __init__.py
│       ├── utils/
│       │   └── __init__.py
│       ├── __init__.py
│       ├── __main__.py
│       └── cli.py
├── tests/
│   ├── e2e/
│   │   └── test_entrypoints.py
│   ├── fixtures/
│   │   └── README.md
│   ├── integration/
│   │   └── test_no_backend_side_effects.py
│   └── unit/
│       └── test_cli.py
├── .gitattributes
├── .gitignore
├── AGENTS.md
├── CONTRIBUTING.md
├── DOCUMENTATION.md
├── LICENSE
├── MANIFEST.in
├── pyproject.toml
└── README.md
```

## Where new implementation belongs

| Location | Responsibility and next files to add when implemented |
| --- | --- |
| `src/scan2flow/ingestion/` | Image/video/point-cloud readers and sensor metadata adapters |
| `src/scan2flow/preprocessing/` | Shared masks, calibration transforms, units, frame selection and normalization |
| `src/scan2flow/data/` | Manifest validation, family split audits, datasets, sampling and synthetic-data generation |
| `src/scan2flow/models/` | Image/point encoders, fusion, surface decoders, CAD-feature heads and bundle interfaces |
| `development/training/` | Training loop, loss composition, checkpoints and exact resume |
| `development/evaluation/` | Surface/dimensional/topology metrics, baseline comparisons, slices and promotion checks |
| `src/scan2flow/reconstruction/` | Pose estimation, scan registration and inference orchestration |
| `src/scan2flow/cad/` | Analytic/freeform fitting, constrained B-rep construction, healing, validation and exporters |
| `src/scan2flow/cfd/` | Fluid-region extraction, enclosure/caps, patch mapping and domain quality checks |
| `src/scan2flow/pipeline/` | Stage contracts, job coordination, immutable caches and output publication |
| `src/scan2flow/utils/` | Small shared path/hash/logging/coordinate utilities |
| `tests/unit/` | Isolated contract and transformation checks |
| `tests/integration/` | Stage boundaries and future native CAD/ML integration |
| `tests/e2e/` | Installed CLI behavior and future capture-to-output regression cases |
| `tests/fixtures/` | Tiny licensed/synthetic fixtures; no private or large capture assets |
| `configs/` | User CFD-domain templates |
| `development/configs/` | Developer-only training/evaluation experiments |
| `development/` | Architecture, ML design, ECC guidance and developer tooling; outside the runtime wheel |
| `schemas/` | Versioned data, calibration, bundle and report contracts |
| `examples/` | Readable CLI examples and deliberately incomplete sample records |
| `data/raw/` | Immutable local image/video/LiDAR captures |
| `data/cad/`, `data/annotations/` | Ground-truth CAD and derived supervision |
| `data/processed/`, `data/manifests/` | Reproducible caches and frozen dataset inventories |
| `models/checkpoints/`, `models/exports/` | External/local model bundles and inference exports, not source modules |
| `artifacts/` | Per-job reconstruction, training, evaluation and CFD outputs |
| `notebooks/` | Optional experiments; production pipelines must run without notebook state |
| `scripts/` | Future repeatable dataset/environment/maintenance utilities |
| `docs/` | User CLI reference, CFD guide and repository layout |
| `.github/workflows/` | Automated scaffold checks; GPU/CAD/solver suites need explicit future environments |

The main [development plan](../DOCUMENTATION.md) defines scope, decisions and next steps
and the [README](../README.md) defines current capabilities. Keep this inventory in
sync when adding or moving files.

## Version control and distribution

`.gitignore` preserves directory guidance while excluding local data, checkpoints
and generated runs. Put large artifacts in an appropriate external store with
checksummed manifests; Git LFS or a dataset registry may be introduced after its
access and retention policy is defined. Neither is configured here.

`pyproject.toml` defines the installable package and development tools.
`MANIFEST.in` includes documentation, templates, schemas, examples and tests in the
source distribution. Wheels contain the runtime Python package and license;
training/evaluation code under `development/` is excluded from wheels. Repository documentation remains available on GitHub and in the source archive.
