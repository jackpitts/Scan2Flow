# Text-only examples

These files illustrate proposed data formats. No photographs, video, LiDAR scans,
CAD labels, model weights, or computed results are included. The all-zero hashes
are deliberate placeholders and must never be accepted as verified asset hashes.
The illustrative license and rights-holder values do not grant rights to any data.

| Example | Intended use |
| --- | --- |
| [`manifests/dataset.example.jsonl`](manifests/dataset.example.jsonl) | Three independent object captures showing photo, video, and LiDAR records |
| [`calibration/camera.example.json`](calibration/camera.example.json) | Two camera poses with explicit pixel intrinsics and metre translations |
| [`calibration/lidar.example.json`](calibration/lidar.example.json) | A raw point cloud in millimetres transformed in metres |
| [`reports/reconstruction.example.json`](reports/reconstruction.example.json) | A report that honestly requires review with missing measurements |
| [`commands.md`](commands.md) | Runnable CLI argument dry-runs using nonexistent example assets |

Each JSONL record is validated separately against
[`dataset-record.schema.json`](../schemas/dataset-record.schema.json). Asset paths
resolve against `examples/manifests/`, while its calibration paths resolve to
`examples/calibration/`. A future loader must verify the resolved files remain in
an explicitly authorized dataset tree. The sample contains one row from each split
only to show the format; real train, validation, and test manifests must be separate.

The two photo sensors in the camera calibration are synthetic numeric examples,
with cameras looking along world +Y from `y = -1 m`, at `z = 0.2 m`. Camera +Y
points down in the image, hence maps to world -Z. The camera orientations are proper
rotations, but none of their values was measured from an actual photograph. Video
has no example calibration because moving-camera poses must be estimated or supplied
per frame rather than copied from a still-camera example.

Replace identifiers, paths, license evidence, checksums, measured scale, intrinsics,
extrinsics, and annotations with your own validated data before implementing any
training run. Run `scan2flow ... --dry-run` only to inspect parsed arguments; it does
not read these files or establish that the assets or backends exist.
