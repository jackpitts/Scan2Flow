# Scan2Flow

[![CI](https://github.com/jackpitts/Scan2Flow/actions/workflows/ci.yml/badge.svg)](https://github.com/jackpitts/Scan2Flow/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](pyproject.toml)
[![Status](https://img.shields.io/badge/status-CLI%20scaffold-orange)](#project-status)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

**Turn captures of physical objects into CAD geometry for CFD preparation.**

Scan2Flow is a command line tool being developed to reconstruct objects from
photographs, short videos or LiDAR scans, generate CAD, and prepare fluid-domain
geometry. The intended workflow uses a pretrained model supplied by the project.
Users do not need to create a dataset or train a model.

## Project status

This is an **executable CLI scaffold**, version `0.1.0.dev0`.

| Capability | Current status |
| --- | --- |
| Installation, help and version | Working |
| Argument checks and JSON dry-run plans | Working |
| Environment inventory with `doctor` | Working |
| Input decoding, model inference and CAD export | Not implemented |
| CFD-domain preparation | Not implemented |
| Pretrained model | Not yet supplied |

A dry-run validates command syntax and option relationships only. It does not read
files, load a model, inspect geometry or produce CAD. Without `--dry-run`, processing
commands exit with code `3` because their backends are not implemented.

## Intended features

- Reconstruct one rigid object from one or several photos, video clips or LiDAR scans.
- Export checked STEP geometry and/or an STL surface mesh.
- Record physical scale, uncertainty and geometry-quality evidence.
- Prepare external or internal fluid regions with explicit boundary definitions.

A single photo cannot establish all hidden geometry. A CAD file also needs dimensional
review, fluid-domain definition, meshing and solver setup before meaningful CFD analysis.

## Installation

The scaffold requires Python **3.11+** and Git. No GPU or third-party runtime
packages are needed for its current commands. Install from this repository:

```bash
git clone https://github.com/jackpitts/Scan2Flow.git
cd Scan2Flow
```

### Windows PowerShell

Use the environment's Python directly; activation is optional:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m scan2flow --help
```

For the short `scan2flow` command, activate the environment:

```powershell
.\.venv\Scripts\Activate.ps1
scan2flow --help
```

If activation is blocked, replace `scan2flow` in the examples below with
`.\.venv\Scripts\python.exe -m scan2flow`. No global execution-policy change is needed.

### Windows Git Bash

Use forward slashes and the Bash activation script:

```bash
python -m venv .venv
source .venv/Scripts/activate
python -m pip install -e .
scan2flow --help
```

Without activation, use `./.venv/Scripts/python.exe -m scan2flow --help`.

### Linux or macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
scan2flow --help
```

## Commands

The public CLI has three commands:

| Command | Purpose |
| --- | --- |
| `reconstruct` | Plan reconstruction and CAD export from your captures |
| `prepare-cfd` | Plan fluid-domain preparation from object geometry |
| `doctor` | Inspect the local environment |

All processing examples below are **dry-run plans**. Their input files do not need
to exist. Removing `--dry-run` currently reports the unavailable backend.

### Single photo

```bash
scan2flow reconstruct --input front.jpg --input-type photo --known-length 0.25 --units m --output artifacts/reconstruction/photo --dry-run
```

`--known-length` is the measured longest side of the object's oriented bounding box,
expressed in `--units`. It anchors scale approximately; unseen shape still needs review.

### Multiple photos of the same object

```bash
scan2flow reconstruct --input front.jpg --input side.jpg --input rear.jpg --input-type photo --known-length 250 --units mm --output artifacts/reconstruction/photos --dry-run
```

Repeat `--input` for each file. All captures must show the same rigid object in an
unchanged configuration. Three filenames illustrate syntax, not sufficient coverage;
use overlapping views around important surfaces and openings. Directory/glob expansion
is not provided by the CLI.

### One video or several clips

```bash
scan2flow reconstruct --input orbit.mp4 --input-type video --known-length 0.25 --frame-step 15 --max-frames 200 --output artifacts/reconstruction/video --dry-run
scan2flow reconstruct --input upper.mp4 --input lower.mp4 --input-type video --known-length 0.25 --output artifacts/reconstruction/videos --dry-run
```

The planned sampler selects every Nth frame in each clip. The maximum retained frame
count applies across all clips; useful overlap and viewpoint changes are still required.

### LiDAR scan

```bash
scan2flow reconstruct --input object.ply --input-type lidar --scan-units mm --units m --output artifacts/reconstruction/lidar --dry-run
```

`--scan-units` declares source point units; `--units` declares output units. Both
`--voxel-size` and `--tolerance` always use metres. LiDAR does not accept `--known-length`.

### Prepare a fluid domain

```bash
scan2flow prepare-cfd --input artifacts/reconstruction/lidar/object.step --output artifacts/cfd/external --flow external --units m --domain configs/cfd-external.toml --dry-run
```

For internal flow, use `--flow internal` and `configs/cfd-internal.toml`. Adapt the
domain template to your object. This stage is intended to prepare geometry; it does
not select fluid properties, boundary conditions, mesh settings or run a solver.

### Help and diagnostics

```bash
scan2flow --version
scan2flow reconstruct --help
scan2flow prepare-cfd --help
scan2flow doctor --json
```

`doctor` inventories optional packages and executables without importing native
libraries or testing GPU/backend compatibility. Missing optional entries are expected.

The [CLI reference](docs/CLI_REFERENCE.md) covers every option, default and exit code.
`--model PATH` is an optional pretrained-model override. No checkpoint argument is
required; no release model is supplied or automatically downloaded today.

## Planned output

```text
artifacts/reconstruction/example/
├── object.step          # CAD geometry when fitting and validation succeed
├── object.stl           # Triangulated surface, if requested
├── quality.json         # Geometry checks, limitations and review decision
└── provenance.json      # Source, units, model and processing versions
```

`--format step`, `stl` or `both` selects planned geometry exports. STL requires an
explicit unit convention; STEP does not guarantee editable feature history. These
files are not generated by the current scaffold.

## Documentation

- [CLI reference](docs/CLI_REFERENCE.md): public commands and troubleshooting.
- [CFD guide](docs/CFD_GUIDE.md): using and checking geometry for fluid simulation.
- [Examples](examples/commands.md): additional planning commands.

For contributors, [DOCUMENTATION.md](DOCUMENTATION.md) is the shared development
plan: scope, current state, decisions and next steps. Detailed engineering material
lives under `development/`; it is not part of the end-user setup.

## Contributing and license

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup, checks and review.

Original code and documentation use the [MIT License](LICENSE). Third-party libraries,
models and datasets retain their own terms; none are redistributed here.
