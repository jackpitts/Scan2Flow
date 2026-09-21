# Scan2Flow

[![CI](https://github.com/jackpitts/Scan2Flow/actions/workflows/ci.yml/badge.svg)](https://github.com/jackpitts/Scan2Flow/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](pyproject.toml)
[![Status](https://img.shields.io/badge/status-design%20%26%20CLI%20scaffold-orange)](#project-status)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

**From physical objects to CAD geometry prepared for Computational Fluid Dynamics.**

Scan2Flow is a command line project for reconstructing physical objects from photographs, short videos, or LiDAR point clouds. Its intended pipeline combines geometric reconstruction with machine learning to identify CAD features, fit valid solid geometry, and prepare that geometry for CFD meshing.

The interface is strictly a CLI. Training, evaluation, reconstruction, and CFD preparation are designed as local, scriptable jobs. No graphical application or hosted inference service is included.

## Project status

This repository is a **documented architecture and executable CLI scaffold**, version `0.1.0.dev0`. It does not yet reconstruct objects, train models, export CAD, or prepare fluid domains. There are no pretrained weights, datasets, measured accuracy results, or production releases.

| Capability | Available now | Intended backend behavior |
|---|---|---|
| Installable `scan2flow` command | Yes | Stable entry point for all jobs |
| Help, version, argument validation | Yes | Validate commands before execution |
| JSON dry-run plans | Yes | Inspect CLI options without changing files |
| Dependency inventory | Yes, through `doctor` | Help diagnose the local environment |
| Photos, videos, and LiDAR reconstruction | CLI contract only | Reconstruct and fit object geometry |
| Model training and evaluation | CLI contract only | Reproducible supervised training and geometry evaluation |
| STEP/STL output and CFD preparation | CLI contract only | Validated geometry, fluid domains, and quality reports |

Commands with `--dry-run` validate CLI syntax and option relationships, then print a plan. They do **not** read inputs or configuration contents, check checkpoint compatibility, or validate geometry. Execution without `--dry-run` exits with code `3` and explains that the backend is unimplemented. Installing optional libraries does not change that behavior.

## Key features and design goals

- **One object, several capture methods:** one or more photos, one or more video clips, or an exported LiDAR scan.
- **Learned CAD feature recognition:** proposed image and point-cloud encoders predict surfaces and analytic features such as planes, cylinders, holes, and fillets.
- **Hybrid reconstruction:** camera estimation and scan registration supply geometric evidence; a CAD kernel fits and checks boundary representations (B-reps).
- **CFD-oriented outputs:** planned STEP solids, STL surface meshes, dimensional provenance, geometry-quality reports, and a separate fluid-domain preparation stage.
- **Reproducible ML workflows:** object-family data splits, versioned manifests, shared preprocessing, baseline comparisons, and traceable model bundles.
- **Explicit uncertainty:** unsupported surfaces and inferred hidden geometry must be reported. A single photograph cannot establish an object's complete shape or absolute dimensions.

These are implementation goals, except for the CLI functionality identified above. A visually plausible mesh is not automatically accurate CAD, and valid object CAD is not a complete CFD simulation.

## Prerequisites

For the scaffold:

- Python **3.11 or newer**, `pip`, and Git.
- A terminal on Windows, Linux, or macOS. GPU hardware is unnecessary for help, dry runs, and the current tests.
- A virtual environment is recommended. The core package has no third-party runtime dependencies.

For future backend development, the proposed stack is PyTorch for learning, COLMAP for camera reconstruction, FFmpeg for video decoding, Open3D for point clouds, and CadQuery/Open CASCADE for CAD operations. OpenFOAM or Gmsh belongs to the downstream CFD/meshing environment. Their platform, GPU, and binary requirements are separate from the scaffold; see [backend setup](DOCUMENTATION.md#backend-development-environment).

No validated training hardware minimum or backend dependency lock exists yet. These must be established through the first reproducible baseline.

## Installation

Install from this repository; no PyPI release is assumed.

```bash
git clone https://github.com/jackpitts/Scan2Flow.git
cd Scan2Flow
```

### Windows PowerShell

Use the virtual environment's Python directly; activation is optional.

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe -m scan2flow --help
.\.venv\Scripts\python.exe -m scan2flow doctor --json
```

To use the shorter `scan2flow` commands below, activate the environment if your local PowerShell policy allows it:

```powershell
.\.venv\Scripts\Activate.ps1
```

Otherwise replace `scan2flow` with `.\.venv\Scripts\python.exe -m scan2flow`.

### Linux or macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
scan2flow --help
scan2flow doctor --json
```

Use `python -m pip install -e .` if you do not need development tools. `python -m scan2flow` is equivalent to the installed command.

### Development checks

Run these inside the environment, from the repository root:

```bash
python -m pytest
python -m ruff check .
python -m ruff format --check .
python -m build
```

The CI workflow checks the scaffold. Passing CI does not establish reconstruction accuracy or CFD suitability.

### ECC architecture and setup workflow

This foundation was developed using the installed **[affaan-m/ECC](https://github.com/affaan-m/ECC) plugin, version 2.2.2**. Its machine-learning workflow informed the data contracts, reproducibility requirements, evaluation gates, and artifact lifecycle; its Python guidance informed package boundaries and the CLI scaffold. Architecture trade-offs are recorded in the project documentation.

See [ECC_WORKFLOW.md](docs/ECC_WORKFLOW.md) for the applied skills, their architectural consequences, and verified contributor setup instructions. ECC is a development aid and is not required to run Scan2Flow.

## CLI usage

All examples below are **runnable planning examples**. Paths name your future local inputs and model bundle; those assets are not supplied. Each command includes `--dry-run`, so it prints a plan without reading assets or producing output files. Removing that flag currently exits with code `3`.

Repeat `--input` for each file. Every file in one reconstruction must depict the **same rigid object in an unchanged configuration**. Inputs are not separate batch jobs. Quote paths containing spaces and expand file lists yourself; the CLI does not expand globs or scan directories.

### Single photograph

```bash
scan2flow reconstruct --input data/raw/images/front.jpg --input-type photo --known-length 0.25 --units m --checkpoint models/checkpoints/baseline --output artifacts/reconstruction/single-photo --dry-run
```

`--known-length` is the measured longest side of the object's oriented bounding box, expressed in `--units`. It supplies an approximate scale anchor; it does not recover unseen shape. Single-photo reconstruction is an exploratory mode requiring learned priors and dimensional review.

### Multiple photographs of the same object

```bash
scan2flow reconstruct --input data/raw/images/front.jpg --input data/raw/images/side.jpg --input data/raw/images/rear.jpg --input-type photo --known-length 250 --units mm --checkpoint models/checkpoints/baseline --output artifacts/reconstruction/multiview --format both --dry-run
```

Three files demonstrate the syntax, not sufficient coverage. Collect overlapping views around the object at several elevations, with stable focus, exposure, and lighting. Include the underside and important openings where possible. See [capture requirements](DOCUMENTATION.md#capture-and-input-contract).

### One short video

```bash
scan2flow reconstruct --input data/raw/videos/orbit.mp4 --input-type video --frame-step 15 --max-frames 200 --known-length 0.25 --checkpoint models/checkpoints/baseline --output artifacts/reconstruction/video --dry-run
```

The planned decoder samples every 15th decoded frame and retains at most 200 frames in total. Sampling is followed by blur, overlap, and pose-quality checks; recording more near-identical frames does not add useful geometry.

### Multiple videos of the same object

```bash
scan2flow reconstruct --input data/raw/videos/upper-orbit.mp4 --input data/raw/videos/lower-orbit.mp4 --input-type video --frame-step 30 --max-frames 300 --known-length 0.25 --checkpoint models/checkpoints/baseline --output artifacts/reconstruction/multi-video --dry-run
```

Clips need overlapping visible surfaces for registration. The proposed frame limit applies across clips, and calibration must account for each recording's camera settings.

### LiDAR point cloud

```bash
scan2flow reconstruct --input data/raw/lidar/object.ply --input-type lidar --scan-units mm --units m --voxel-size 0.002 --tolerance 0.0001 --checkpoint models/checkpoints/baseline --output artifacts/reconstruction/lidar --dry-run
```

Here scan coordinates are in millimetres and output coordinates are in metres. `--voxel-size` and `--tolerance` are **always in metres**. `--scan-units` is mandatory for LiDAR; `--known-length` is not accepted for LiDAR. A point cloud must be segmented to the target object, or the future preprocessing stage must perform that segmentation.

### Initiate model training

```bash
scan2flow train --config configs/train.toml --output artifacts/training/baseline --device cuda --seed 42 --dry-run
```

This is the training entry-point contract; training itself is unimplemented. The [example configuration](configs/train.toml) describes the intended dataset, model, optimizer, and evaluation settings. Prepare licensed paired CAD/capture data and object-family splits before implementing or running a backend. See the [ML pipeline guide](docs/ML_PIPELINE.md).

The planned resume interface is:

```bash
scan2flow train --config configs/train.toml --output artifacts/training/resumed --resume models/checkpoints/last --device cuda --dry-run
```

### Evaluate a model

```bash
scan2flow evaluate --config configs/evaluate.toml --checkpoint models/checkpoints/baseline --split test --output artifacts/evaluation/baseline --device cpu --dry-run
```

### Prepare an external-flow domain

```bash
scan2flow prepare-cfd --input artifacts/reconstruction/lidar/object.step --output artifacts/cfd/external --flow external --units m --domain configs/cfd-external.toml --tolerance 0.0001 --dry-run
```

For internal flow, use `--flow internal` and [configs/cfd-internal.toml](configs/cfd-internal.toml). Domain examples require case-specific review. Preparation will describe geometry and boundary regions; fluid properties, boundary conditions, volume meshing, turbulence models, and solving remain downstream work.

### Help and diagnostics

```bash
scan2flow --version
scan2flow reconstruct --help
scan2flow train --help
scan2flow doctor --json
```

The [complete CLI reference](DOCUMENTATION.md#cli-reference) defines every argument, default, unit, validation rule, and exit code.

## Output contract

A future successful reconstruction is designed to produce selected geometry files and a provenance/quality report:

```text
artifacts/reconstruction/example/
├── object.step          # CAD B-rep, when STEP fitting and validation succeed
├── object.stl           # Tessellated surface; unit convention recorded separately
├── quality.json         # Geometry checks, uncertainty, and acceptance status
└── provenance.json      # Inputs, hashes, units, transforms, config, model and code versions
```

`--format` controls geometry export. STL carries triangles and no standardized physical-unit metadata; STEP does not guarantee an editable feature history. Outputs must pass geometry checks and independent dimensional review before being used to create a CFD mesh. The scaffold creates none of these files.

## Documentation and layout

- [DOCUMENTATION.md](DOCUMENTATION.md): architecture, setup, input/output contracts, full CLI reference, and troubleshooting.
- [ML_PIPELINE.md](docs/ML_PIPELINE.md): data, model design, training, evaluation, deployment, and rollback.
- [CFD_GUIDE.md](docs/CFD_GUIDE.md): geometry validation, fluid domains, meshing, and simulation verification.
- [PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md): complete tracked directory and file skeleton.
- [ECC_WORKFLOW.md](docs/ECC_WORKFLOW.md): plugin use and contributor setup.
- [CONTRIBUTING.md](CONTRIBUTING.md): development and review expectations.
- [Examples](examples/README.md), [configuration templates](configs/README.md), and [schemas](schemas/README.md): proposed backend contracts.

Source code lives in `src/scan2flow/`, tests in `tests/`, datasets in `data/`, model artifacts in `models/`, and generated job outputs in `artifacts/`. Large/private datasets and model binaries are excluded from Git.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md), create a focused branch, and include checks that demonstrate the behavior you change. Backend work should begin with a reproducible classical baseline and an agreed data contract, then add learned features and CAD fitting against measurable geometry criteria.

Do not describe a backend as supported until it runs on a documented environment with representative regression cases. Report reproducible issues through [GitHub Issues](https://github.com/jackpitts/Scan2Flow/issues).

## License

Scan2Flow's original code and documentation are licensed under the **MIT License**; see [LICENSE](LICENSE). Third-party libraries, datasets, pretrained weights, and generated geometry derived from supplied assets retain their own applicable terms. No third-party dataset or model is redistributed here.
