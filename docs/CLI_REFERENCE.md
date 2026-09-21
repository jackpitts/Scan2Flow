# Scan2Flow user CLI reference

This is the public command contract. For installation and examples, see [README.md](../README.md). Model creation and training are maintained separately by the developers.

## CLI reference

This section describes **all currently accepted commands and flags**. The tables distinguish parser behavior from intended future execution semantics.

### Invocation and global options

```text
scan2flow [-h | --help] [--version] COMMAND ...
python -m scan2flow [-h | --help] [--version] COMMAND ...
```

| Option / argument | Meaning |
|---|---|
| `-h`, `--help` | Print top-level help and exit `0` |
| `--version` | Print `scan2flow 0.1.0.dev0` and exit `0`; use before a subcommand |
| `COMMAND` | Required unless requesting help/version: `reconstruct`, `prepare-cfd`, or `doctor` |

Use command-specific options after the command. Each command also has `-h`/`--help`. Names are case-sensitive and option abbreviations are disabled. No arguments produces a usage error (`2`). There are no positional file arguments or implicit default commands. `train` and `evaluate` have been removed; both return a usage error (`2`).

### Shared workflow behavior

| Option | Applies to | Meaning |
|---|---|---|
| `--dry-run` | All commands except `doctor` | Boolean, default false. Validate CLI syntax/relationships and print a JSON plan; no inputs/configs/checkpoints are read and no outputs are created |
| `--output PATH` | All commands except `doctor` | Required destination directory in the future backend. Path is only recorded today |
| `--device {auto,cpu,cuda}` | `reconstruct` | Default `auto`. Planned selection: CUDA when supported/available, otherwise CPU; explicit `cuda` must fail if unavailable. No GPU discovery or allocation occurs today |

Relative paths are preserved as supplied and refer to the current working directory. The current parser accepts strings without checking existence, suffix, permissions or contents. Quote spaces. Repeat only `reconstruct --input` to supply multiple files; its order is preserved. For other scalar options repeated values follow argparse's last-value behavior. Globs, directory expansion, stdin assets, URI fetching, environment-based overrides, `--checkpoint`, `--seed`, `--resume`, `--force`, `--verbose` and `--config` on `reconstruct` are not implemented.

Finite positive numeric values are required where listed; `0`, negatives, `NaN` and infinities are rejected for positive-valued settings. Type, choice, required-flag and cross-option errors return `2` before any workflow execution.

### `reconstruct`

```text
scan2flow reconstruct --input PATH [--input PATH ...]
  --input-type {photo,video,lidar} --output PATH [--model PATH]
  [--calibration PATH] [--units {m,cm,mm}] [--known-length NUMBER]
  [--scan-units {m,cm,mm}] [--frame-step N] [--max-frames N]
  [--voxel-size METRES] [--tolerance METRES] [--format {step,stl,both}]
  [--device {auto,cpu,cuda}] [--dry-run] [-h]
```

| Option | Required / default | Definition |
|---|---|---|
| `--input PATH` | Required; repeatable | Explicit files depicting one object; planned modality-specific decoding |
| `--input-type` | Required | `photo`, `video`, or `lidar`; selects one modality for every input |
| `--output PATH` | Required | Planned reconstruction directory |
| `--model PATH` | Optional; omitted/null | Pretrained inference-bundle override. Omission selects the future release model; no model is shipped or loaded today |
| `--calibration PATH` | Optional; omitted/null | Proposed camera/sensor calibration JSON; poses may need estimation when absent |
| `--units` | `m` | `m`, `cm`, `mm`; output coordinates and `--known-length` unit |
| `--known-length NUMBER` | Required for `photo`/`video`; forbidden for `lidar` | Finite positive measured longest oriented-bounding-box side; approximate scale anchor |
| `--scan-units` | Required for `lidar`; forbidden otherwise | `m`, `cm`, `mm`; source point-coordinate units |
| `--frame-step N` | Video default `30`; forbidden otherwise | Positive integer; sample every Nth decoded frame in each clip |
| `--max-frames N` | Video default `300`; forbidden otherwise | Positive integer; planned maximum retained frames across all input clips |
| `--voxel-size METRES` | `0.002` | Finite positive downsampling voxel edge in metres; applies to input or reconstructed point evidence |
| `--tolerance METRES` | `0.0001` | Finite positive requested geometry tolerance in metres; an algorithm parameter, not guaranteed accuracy |
| `--format` | `both` | `step`, `stl`, `both`; planned geometry export selection |
| `--device` | `auto` | Shared compute-device choice |
| `--dry-run` | False | Print a plan instead of returning the unimplemented-backend error |
| `-h`, `--help` | — | Print command help |

For non-video modes, `frame_step` and `max_frames` are `null` in the JSON plan. Providing either flag explicitly in these modes is an error even if its value matches the video default. Changing calibration does not remove the photo/video scale requirement.

### `prepare-cfd`

```text
scan2flow prepare-cfd --input PATH --output PATH --flow {external,internal}
  --units {m,cm,mm} --domain PATH [--tolerance METRES] [--dry-run] [-h]
```

| Option | Required / default | Definition |
|---|---|---|
| `--input PATH` | Required; one file | Planned source CAD or validated surface mesh; STEP/STL adapters remain unimplemented |
| `--output PATH` | Required | Planned fluid-geometry and boundary-report directory |
| `--flow` | Required | `external` enclosure-minus-object or `internal` connected fluid-region construction |
| `--units` | Required | `m`, `cm`, `mm`; input coordinate unit; unlike reconstruction, no default |
| `--domain PATH` | Required | Proposed TOML enclosure or opening/region definition; see [external](../configs/cfd-external.toml) and [internal](../configs/cfd-internal.toml) templates |
| `--tolerance METRES` | `0.0001` | Finite positive geometry tolerance in metres |
| `--dry-run` | False | Record a plan; no CAD is read and no regions are generated |
| `-h`, `--help` | — | Print command help |

The future backend must reject a mismatch between CLI `--flow` and the domain config. This cannot be checked by today's dry-run because it does not read the config. No `--solver`, `--mesh-size`, `--yplus`, or solver execution flag is provided. STL input can follow a surface workflow; it must not silently acquire claims of analytic STEP reconstruction.

### `doctor`

```text
scan2flow doctor [--json] [-h]
```

| Option | Default | Definition |
|---|---|---|
| `--json` | False | Print discovery results as JSON instead of human-readable text |
| `-h`, `--help` | — | Print command help |

Reports the Scan2Flow/Python versions, Python executable, discoverable `ffmpeg` and `colmap` paths, and installed distribution versions for `torch`, `open3d`, and `cadquery`. Missing entries are `null` in JSON or `not found` in text. It returns `0` for a successful inventory even when optional components are absent, with `status: scaffold_available` and `backend: unimplemented`.

### JSON plans, output and exit codes

A dry-run prints an object with `status: "planned"`, `backend: "unimplemented"`,
`command`, `options`, and a `validation` explanation. For reconstruction, `options.model` is `null`
when no custom model is selected. Paths are recorded without opening files.
The flag does not prove that a model, input or backend is available.

JSON uses snake_case option names and preserves path strings. Plans, diagnostic reports and help go to stdout; errors go to stderr. Do not parse human-readable error text as a stable machine API.

| Exit code | Current meaning |
|---|---|
| `0` | Help/version printed, syntactically valid dry-run plan, or completed doctor inventory |
| `2` | CLI syntax, missing required flag, invalid value, or incompatible options |
| `3` | Requested reconstruction/CFD backend is unimplemented |
| `130` | Keyboard interruption caught by the entry point |

Unexpected interpreter/OS failures are outside this application-code contract and may have other nonzero codes. A dry-run's `0` is not success for processing an input, and the future runtime error taxonomy must be defined when execution is implemented.

## Troubleshooting

| Symptom | Explanation and action |
|---|---|
| `scan2flow` is not found | Use the installed environment's `python -m scan2flow`, or activate its environment |
| PowerShell activation is blocked | Use `.\.venv\Scripts\python.exe -m scan2flow`; changing global execution policy is unnecessary |
| Backend is unimplemented / exit `3` | Expected for processing commands in this foundation; use `--dry-run` to inspect the contract |
| A dry-run succeeds for a nonexistent file | Expected: paths and configuration contents are not inspected |
| `--known-length` or `--scan-units` error | Photo/video needs a known length; LiDAR needs scan units and forbids known length |
| `--frame-step` fails for photos | Frame sampling flags are video-only |
| `doctor` shows packages but reconstruction fails | Discovery does not install or enable a Scan2Flow backend |
| Native CAD/ML package installation fails | Check the upstream supported Python/platform/build combination in a separate environment |
| Future result has the wrong scale | Check source units, scale-anchor meaning, metadata and transforms before changing a mesher |
| Future STEP export or topology validation fails | Inspect invalid fits/trim boundaries and missing observations; do not rename STL to STEP |
| Future mesh loses a flow passage | Compare against source evidence and feature size before healing/defeaturing or increasing tolerances |


## Model selection

The intended user workflow uses an approved pretrained model supplied with a
release. Users do not prepare a dataset or run training. `--model PATH` is an
optional override for a compatible exported inference bundle, not optimizer or
training-resume state. A distribution mechanism and model loader have not been
implemented, so omission and override both remain planning-only today.

## Migrating from the initial scaffold

The initial development commands `train` and `evaluate` are no longer public.
Reconstruction no longer requires `--checkpoint`; remove that argument, or replace
it with `--model` only when selecting a pretrained inference bundle explicitly.
`--seed` is no longer public. No automatic training or implicit download occurs.
