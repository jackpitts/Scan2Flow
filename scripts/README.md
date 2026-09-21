# Developer scripts

Future maintenance scripts belong here: dataset integrity checks, reproducible
synthetic-data generation, benchmark orchestration, and artifact packaging.
User operations belong in the `scan2flow` CLI, and reusable processing belongs in
`src/scan2flow/`. No data downloader, trainer, or backend installer is supplied.

Scripts must document dependencies and inputs, use explicit output paths, and avoid
hidden notebook state. Test geometry and metric logic in the package rather than
duplicating it inside a script.
