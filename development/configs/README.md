# Developer experiment configurations

These TOML files are design templates for our own training and model evaluation.
No runner currently reads them. They are not options or setup requirements for
end users and cannot be passed to the public CLI.

- `train.toml`: later-stage hybrid-model experiment, data contract, optimization,
  reproducibility and promotion requirements.
- `evaluate.toml`: held-out evaluation settings and baseline comparisons.

`[execution]` records internal device, seed and run destination; evaluation also
selects an inference bundle and split. A future trainer must specify compatible
resume-state handling before documenting a resume command. Paths in these configs
resolve from the repository working directory; paths in dataset records resolve
from the manifest directory. Shared geometry uses metres.

These are research hypotheses. Automatic promotion is disabled and thresholds are
unset. The first primitive experiment is scoped in [the development plan](../../DOCUMENTATION.md#next-experiment);
it needs a smaller measured configuration when implemented. Preserve the broad
hybrid design as a later option rather than implementing every component at once.
