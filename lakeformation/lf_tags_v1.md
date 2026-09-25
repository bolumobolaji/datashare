# Lake Formation tags — Track A / V1

Tag names match the PII-1 runbook and the IT Security approval sheet. Do not introduce
alternate casings (e.g. `DataClass=NPI`) — one vocabulary only.

## Tag definitions

| Key           | Values                          | Purpose                          |
|---------------|---------------------------------|----------------------------------|
| `data_class`  | `npi`, `standard`               | Classification                   |
| `environment` | `pilot`, `prod`                 | Environment                      |
| `sensitivity` | `restricted`, `internal`, `public` | Handling level                |

## Assignments (database level — tables and columns inherit)

| Resource                        | Tags                                        |
|---------------------------------|---------------------------------------------|
| NPI database (Glue catalog)     | `data_class=npi`, `sensitivity=restricted`  |
| `${GLUE_DATABASE}` (snapshots)  | `data_class=npi`, `environment=pilot`, `sensitivity=restricted` |

## Grants (per IAM user — IAM groups are not valid LF principals on this domain)

| Principal                 | Expression                                   | Database | Table              |
|---------------------------|----------------------------------------------|----------|--------------------|
| `iam-sandbox-bolu`        | `data_class=npi` AND `sensitivity=restricted` | DESCRIBE | SELECT, DESCRIBE   |
| phase-2 users (4)         | same                                          | DESCRIBE | SELECT, DESCRIBE   |

`iam-bolu-mobolaji` is Data Lake Administrator; it needs no data grant.

## Revocations (required for the tag model to hold)
- Remove any `SELECT` granted to `IAMAllowedPrincipals` or broad roles on the NPI database.

## Track B
- Replace per-user grants with one grant to an IAM Identity Center group on the new IDC-based domain.
