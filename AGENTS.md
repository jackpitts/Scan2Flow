# Working on Scan2Flow

- Read `DOCUMENTATION.md` first for the product scope, implemented state, current
  milestone, open decisions and next step. Read the relevant development guide
  before changing geometry, model or data contracts.
- The public CLI serves end users: reconstruction, CFD preparation and diagnostics.
  Training and model evaluation belong to developer tooling under `development/`.
  Do not add them to the public CLI or require users to train a model.
- Keep claims aligned with working code. A dry-run is argument planning, not
  reconstruction, model loading or geometry validation.
- After a material change, update the state and next step in `DOCUMENTATION.md`.
  Update public help, `docs/CLI_REFERENCE.md`, README and examples when the interface
  changes. Keep detailed research in `development/` and personal scratch notes in
  ignored `.local-notes/`.
- Run relevant tests and the checks in `CONTRIBUTING.md`. Do not claim measured
  CAD accuracy or CFD readiness without representative evidence.
