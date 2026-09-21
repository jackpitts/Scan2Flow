# Dataset manifests

Create immutable `train.jsonl`, `validation.jsonl`, and `test.jsonl` snapshots after
semantic data validation and grouped splitting are implemented. Each line follows
`schemas/dataset-record.schema.json`. Record asset paths relative to this directory.
Real manifests are intentionally absent and ignored by Git; use a versioned dataset
registry or external storage to preserve snapshots and their hashes.
