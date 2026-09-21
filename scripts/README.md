# Maintenance scripts

Future shared maintenance scripts belong here: asset integrity checks and artifact
packaging. Model training and evaluation are developer work under `development/`;
there is no trainer or evaluator to run yet. End-user operations belong to the
`scan2flow` CLI; reusable inference and geometry code belongs in `src/scan2flow/`.

Scripts must document dependencies, input/output paths and reproducibility.
Personal scratch work belongs in ignored `.local-notes/`. Update the shared
[development plan](../DOCUMENTATION.md) when an experiment changes a decision.
