# npi-datashare — Track A / V1

All Track A code and access-control configuration for the Orion datashare pilot sandbox,
under version control from V1 onward. Backs controls **VCS-1**, **REPRO-1**, **REVIEW-1**
in the Orion Pilot Test Plan, and the **PII-1** access-control runbook.

> **No NPI data, sample rows, or query output is ever committed to this repo.**
> Code, templates, and configuration records only.

## The model in one paragraph

`main.json` is the **contract** and is immutable: it declares which variables exist, which
templates render, and the rules. `variables.json` is the **only file you edit** to point the
same templates at a different environment. Templates use `${VAR}` placeholders and never
contain an account ID, ARN, bucket name, or region literal. `scripts/render.py` substitutes
values into `rendered/` (gitignored). Secrets are **referenced, never stored** — `variables.json`
says where a secret lives (Secrets Manager name, SMUS connection), never what it is.

```
main.json  (immutable contract)  +  variables.json (per-env values)  --render-->  rendered/  (gitignored)
                                     secrets: { store, ref }  never { value }
```

## Why secrets are not in a variables file

A variables file holding credentials — even a gitignored one — is the failure mode this repo
exists to prevent. The GitHub PAT is entered once in the SMUS connection UI and held by AWS.
Database credentials live in AWS Secrets Manager and are reached by name from Glue/Redshift
connections. CI (`check_no_secrets.py`) fails the build on anything that looks like a key,
token, or password literal. If you need a local-only override, `*.local.json` is gitignored —
but it still must not contain a secret value.

## Layout

```
main.json                         contract — DO NOT EDIT (CI enforces; label main-json-change to override)
variables.json                    the file you edit
scripts/render.py                 render templates; refuses unset values and secret leakage
scripts/check_no_secrets.py       credential scan; runs in CI
policies/iam/                     group bucket policy; project-role scoped policy (templates)
policies/lakeformation/           LF-Tag management IAM policy (template)
policies/permission_boundaries/   PROPOSED per-user boundary — versioned, not applied
lakeformation/lf_tags_v1.md       tag definitions, assignments, grants, revocations
s3/bucket_config.md               bucket state record (Option A model)
datazone/blueprints_config.md     blueprint enable/disable record
docs/arn_conditions_reference.md  what conditions are actually in force
docs/runbooks/                    PII-1 and VCS-1 runbooks, versioned with the code
docs/build-log/                   dated build / incident entries (link these from Asana)
ddl/views_v1.sql                  the five late-binding views
glue/snapshot_job_v1.py           daily snapshot job (argument-driven, idempotent)
.github/                          CI validate workflow, PR template
CODEOWNERS                        review routing
```

## Day one

```bash
git init && git add . && git commit -m "Track A V1 — initial scaffold"
git tag -a v1.0.0 -m "NPI Datashare Pilot V1 — initial release"
git remote add origin https://github.com/<org>/npi-datashare.git
git push -u origin main --tags
```

Then in GitHub → Settings → Branches → protect `main`: require PR review, require the
`validate` status check, block force-push and deletion. Then connect SMUS:
Project → Settings → Connections → GitHub (PAT entered there, never here).

## Local checks (same as CI)

```bash
python3 scripts/render.py --check       # contract + templates validate, nothing written
python3 scripts/check_no_secrets.py     # credential scan
python3 scripts/render.py               # write rendered/ for a console/CLI apply
```

## Editing rules

| You want to…                              | Edit                    | Then                                       |
|-------------------------------------------|-------------------------|--------------------------------------------|
| Point at a new bucket / project / region  | `variables.json`        | PR → render → apply                         |
| Add a new variable or template            | `main.json`             | PR **with label `main-json-change`** and a reason |
| Change a policy's logic                   | the `.template.json`    | PR; keep `${VAR}` placeholders, no literals |
| Rotate a secret                           | the secret store        | nothing in this repo changes                |
