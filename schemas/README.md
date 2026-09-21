# Proposed data and artifact schemas

These JSON Schemas use Draft 2020-12 and describe contracts for future backends.
The scaffold CLI does not load or enforce them. Validate each non-empty line of a
JSONL dataset manifest against `dataset-record.schema.json`; the manifest is not a
single JSON array. Other schemas describe individual JSON documents.

| Schema | Intended object |
| --- | --- |
| `dataset-record.schema.json` | One capture of an object and its CAD supervision |
| `calibration.schema.json` | Intrinsics and world-from-sensor transforms keyed by sensor ID |
| `model-bundle.schema.json` | Model provenance and safe artifact references |
| `reconstruction-report.schema.json` | Geometry observations, scale provenance, checks, and review decision |

JSON Schema checks structure and basic ranges, not physical correctness or asset
availability. Future semantic validation must additionally verify file checksums,
relative-path containment, rights metadata, proper rigid transforms, camera
intrinsics, sensor references, CAD units, cross-split grouping, and geometric
metrics. A structurally valid document does not prove the underlying measurements.

## Units and coordinate conventions

- CAD and raw point-cloud coordinates use a dataset record's `length_unit`.
  Preprocessing converts them to metres and saves its inverse transform.
- Reconstruction export uses the CLI's `--units`; the report records that choice
  in `scale.output_unit`. Deviation metrics and fitting tolerances remain metres.
- `known_length` is an optional measured estimate of the object's longest oriented
  bounding-box side, expressed in `length_unit`. It is not a camera baseline or
  the length of an arbitrary visible edge. An object with ambiguous hidden extent
  needs a better calibration method or an explicit review decision.
- Calibration translations are always metres, even when raw geometry uses
  millimetres. The world frame is right-handed with +Z up. Camera image axes are
  +X right, +Y down, and +Z forward.
- Each `world_from_sensor` is a row-major array of four rows acting on a homogeneous
  **column** vector: `p_world = world_from_sensor * p_sensor`. Convert sensor point
  coordinates to metres before applying the transform. The final row is
  `[0, 0, 0, 1]`; a validator must check the rotation is orthonormal with determinant
  +1. Calibration `scale_status` identifies whether translations have measured
  metric scale or only an assumed convention; metre labels alone do not establish
  absolute scale.
- Camera `intrinsics` are `[fx, fy, cx, cy]` in pixels of the stated image size.
  `brown_conrady_5` distortion uses `[k1, k2, p1, p2, k3]`; a `none` model uses an
  empty coefficient array. Resizing/cropping must update intrinsics explicitly.
- A video may use one intrinsics-bearing sensor entry plus per-frame poses in
  `frame_poses`, keyed by input path and time in seconds. A static transform must
  never be silently used for every frame of a moving camera.

## Report semantics

`accepted_for_cfd_preparation` means a future implementation has recorded passing
geometry gates and explicit review. It does not certify dimensional accuracy or
the CFD solution. `needs_review` includes unobserved surfaces, uncertain scale,
missing metrics, and insufficient evidence. `rejected` indicates a failed gate or
unusable input. Null metric values mean **unavailable**, never zero error.

The schema requires all named checks, known scale, and approved human review for
acceptance; semantic validation must additionally connect each check to actual
measurement evidence and the case's tolerance policy. Reported deviations are
relative to the stated reference: observed points cannot establish accuracy on
unobserved surfaces. CFD-domain and meshing acceptance are separate downstream
records.

Schemas have a provisional `0.1.0` contract version. Breaking changes must update
the schema and examples together and include a migration note before real artifacts
are persisted. No model weights, dataset binaries, or computed reports are shipped.
