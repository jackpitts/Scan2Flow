# ECC architecture and contributor workflow

Scan2Flow's architecture and setup were developed using the installed
[affaan-m/ECC](https://github.com/affaan-m/ECC) plugin, version **2.2.2**.
ECC is contributor tooling for AI-assisted engineering. It is not a Python package
dependency, a reconstruction model, or a requirement for running the Scan2Flow CLI.
Installing Scan2Flow does not install ECC or change an assistant's configuration.

## What was used

The installed `VERSION`, `README.md`, `.codex-plugin/README.md`, skill files,
`scripts/ecc.js`, `scripts/install-guided.js`, and `scripts/install-apply.js`
were inspected when producing this scaffold. The applicable guidance resulted in
concrete repository contracts:

| ECC source | Applied guidance | Scan2Flow result |
| --- | --- | --- |
| [`ecc-guide`](https://github.com/affaan-m/ECC/blob/main/skills/ecc-guide/SKILL.md) | Read the installed catalog and installer; prefer supported managed setup | Version-specific, verified Codex dry-run below; no copying plugin internals into this project |
| [`mle-workflow`](https://github.com/affaan-m/ECC/blob/main/skills/mle-workflow/SKILL.md) | Define input, label, split, and unit contracts before training | [`dataset-record.schema.json`](../schemas/dataset-record.schema.json), grouped split policy, explicit scale provenance |
| [`mle-workflow`](https://github.com/affaan-m/ECC/blob/main/skills/mle-workflow/SKILL.md) | Share preprocessing; capture reproducibility and artifact provenance | Versioned preprocessing configuration and [`model-bundle.schema.json`](../schemas/model-bundle.schema.json) |
| [`mle-workflow`](https://github.com/affaan-m/ECC/blob/main/skills/mle-workflow/SKILL.md) | Compare a baseline; use explicit metrics and fail closed on missing evidence | [`train.toml`](../configs/train.toml), [`evaluate.toml`](../configs/evaluate.toml), promotion disabled until case-specific thresholds exist |
| [`mle-workflow`](https://github.com/affaan-m/ECC/blob/main/skills/mle-workflow/SKILL.md) | Make fallback and limitations explicit | No invented weights, no fabricated reconstruction; unimplemented execution exits with code 3 |
| [`python-patterns`](https://github.com/affaan-m/ECC/blob/main/skills/python-patterns/SKILL.md) | Use a `src/` package, explicit dependencies, and clear module responsibilities | CLI isolated from data, reconstruction, ML, CAD, and CFD backend packages |

The links above identify upstream sources; the observed local version is 2.2.2.
Upstream `main` may subsequently change. The workflow is applied selectively:
Scan2Flow is a local CLI, so this design does not add a web server, feature store,
online traffic routing, or browser automation to the reconstruction pipeline.

## Optional setup for contributors using Codex

Use Node.js 18 or newer and an available Codex CLI for ECC's guided native-plugin
path. Preview the supported installation before applying it:

```shell
npx ecc-universal@2.2.2 install --guided --harness codex --dry-run
```

For an existing reviewed ECC checkout, the equivalent command is:

```shell
node scripts/ecc.js install --guided --harness codex --dry-run
```

Run the second command from the **ECC checkout**, not from Scan2Flow. The command
was executed against the installed 2.2.2 source when creating this project and
returned `Codex / native-plugin` followed by `Dry run complete. No changes were
made.` No installation or global configuration changes were applied for this task.

If ECC is not already installed, continue through the guided installer after
reviewing its preview:

```shell
npx ecc-universal@2.2.2 install --guided --harness codex
codex plugin list --json
```

The installer uses Codex's native marketplace/plugin lifecycle. Codex owns hook
trust. Check the installed plugin in Codex and review any trust requests there.
For native-plugin verification from an ECC checkout, use:

```shell
node scripts/codex/check-plugin-cache.js
```

If ECC already appears in the Codex plugin list, use the installed skills directly.
Do not stack a legacy sync or a second manual installation on top of that plugin.
In particular, the generic managed plan
`--profile minimal --target codex --with capability:machine-learning` skips the
`machine-learning` module in the inspected 2.2.2 manifests. It is not a substitute
for the native Codex plugin used here. See ECC's
[native plugin notes](https://github.com/affaan-m/ECC/blob/main/.codex-plugin/README.md)
for lifecycle details.

## Engineering workflow

1. State the desired object class, capture conditions, permitted reconstruction
   error, and CFD decision the output will inform. Record unknown scale, unseen
   surfaces, and inaccessible cavities as limitations.
2. Freeze a licensed, checksummed dataset snapshot. Keep physical objects, related
   design families, capture sessions, and synthetic derivatives together across
   splits. Validate the schema and geometric meaning of units and transforms.
3. Establish a measured classical reconstruction baseline before increasing neural
   model complexity. Use shared preprocessing and save every coordinate transform.
4. Evaluate geometric deviation, engineering dimensions, topology, uncertainty,
   and performance by capture modality and failure-prone slices. Missing metrics
   cannot count as passing promotion gates; test data is reserved for final review.
5. Package approved weights with their model card, config, preprocessing version,
   dataset reference, environment, and evaluation report. Retain a known previous
   bundle for rollback; reconstructing an older run should not require retraining.
6. Review CAD validity and fluid-region construction separately. A watertight solid
   alone does not establish correct boundary patches or a trustworthy CFD solution.
7. Ship changes with tests for the capability actually implemented and documentation
   that distinguishes measured evidence, proposed behavior, and unsupported cases.

## Initial MLE experiment contract

| Item | Initial proposal |
| --- | --- |
| User action | Convert observations of one physical object into reviewable geometry and a quality report |
| Baseline | Classical multi-view or point-cloud reconstruction followed by deterministic primitive fitting |
| Candidate | Image/point encoders, feature fusion, implicit surface prediction, and explicit CAD fitting |
| Primary comparison | Symmetric surface distance in metres and dimension errors at known scale |
| Guardrails | B-rep validity, watertightness, observed-surface coverage, slice performance, uncertainty, runtime |
| Unacceptable error | Silently presenting invented geometry or unknown-scale geometry as engineering-validated output |
| Fallback | Reject or require review with reasons and provenance; preserve observations |
| Labels | Paired CAD and calibrated captures; license, source, split, and transforms recorded per object |
| Current evidence | Documentation and CLI contract scaffold only; no trained model or benchmark result exists |
| Next experiment | Build and measure one reproducible paired-data baseline, then calibrate acceptance thresholds |

Provisional values in configuration files are experiment hypotheses. They must not
be described as achieved accuracy, universal CFD tolerances, or automatic approval
criteria before validation evidence exists.
