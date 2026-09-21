# CLI argument examples

Run these commands from the repository root after installing the local package.
They parse and print the requested operation only. All media paths and model
checkpoints below are illustrative and are not included in the repository.

```shell
scan2flow reconstruct --checkpoint models/checkpoints/baseline --input data/raw/images/object/front.jpg --input-type photo --known-length 0.2 --units m --output artifacts/reconstruction/single-photo --dry-run
scan2flow reconstruct --checkpoint models/checkpoints/baseline --input data/raw/images/object/front.jpg --input data/raw/images/object/back.jpg --input-type photo --known-length 20 --units cm --output artifacts/reconstruction/multiple-photos --dry-run
scan2flow reconstruct --checkpoint models/checkpoints/baseline --input data/raw/videos/object/orbit.mp4 --input-type video --known-length 0.2 --units m --output artifacts/reconstruction/single-video --dry-run
scan2flow reconstruct --checkpoint models/checkpoints/baseline --input data/raw/videos/object/orbit.mp4 --input data/raw/videos/object/top.mp4 --input-type video --known-length 0.2 --units m --output artifacts/reconstruction/multiple-videos --dry-run
scan2flow reconstruct --checkpoint models/checkpoints/baseline --input data/raw/lidar/object/scan.ply --input-type lidar --scan-units mm --output artifacts/reconstruction/lidar --dry-run
scan2flow train --config configs/train.toml --output artifacts/training/baseline --device auto --seed 42 --dry-run
scan2flow evaluate --config configs/evaluate.toml --checkpoint models/checkpoints/best --split validation --output artifacts/evaluation/baseline --dry-run
scan2flow prepare-cfd --input artifacts/reconstruction/lidar/object.step --output artifacts/cfd/external --flow external --units m --domain configs/cfd-external.toml --dry-run
```

`--known-length` is the measured estimate of the object's longest oriented
bounding-box side; choosing an arbitrary visible edge changes its meaning and can
silently set the wrong scale in a future backend. `--scan-units` specifies units
already present in LiDAR coordinates. CAD fitting tolerance and voxel size use
metres regardless of either unit flag.

Commands without `--dry-run` return exit code 3: execution backends are not yet
implemented. Syntax examples are not instructions for producing real CAD today.
