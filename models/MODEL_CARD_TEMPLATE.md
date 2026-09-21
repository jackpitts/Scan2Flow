# Model card: <model ID>

Status: candidate / approved / rejected / retired. This is an unfilled template,
not evidence that a model has been trained or approved.

## Intended use

Describe supported object classes, input modalities, capture conditions, scale
requirements, compute profile, and the engineering decisions the output may support.
List unsupported materials, hidden geometry, cavities, thin features, and assemblies.

## Training provenance

Record code revision, environment, architecture, license, data source and snapshot
hash, grouping policy, label provenance, seed, preprocessing version, hyperparameters,
training budget, and any base-model origin. State relevant missing-label assumptions.

## Evaluation evidence

Record the frozen validation/test snapshots, classical baseline, metric definitions,
units, alignment policy, sample counts, family-group confidence intervals, and results
by modality, geometry family, sensor, coverage, and material. Include failure and
abstention rates, dimensional error, topology validity, latency, and peak memory.

## Acceptance and limitations

State case-specific tolerance policy, promotion decision, reviewers, uncertainty
calibration, observed versus inferred surface behavior, and known failure examples.
Identify whether values are measurements, assumptions, or unavailable. Explain why
geometry acceptance does not validate CFD boundary conditions or solution accuracy.

## Reproduction and rollback

Provide exact CLI/config references, artifact hashes, safe loading format, supported
dependency versions, nondeterminism caveats, and the prior approved bundle. Describe
the condition that withdraws this version and how existing results can be traced.
