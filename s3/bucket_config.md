# S3 — `${BUCKET}` configuration record (V1)

| Setting                         | State (V1)                                   |
|---------------------------------|----------------------------------------------|
| Block Public Access             | All four settings **enabled**                |
| Object Ownership                | Bucket owner enforced (ACLs disabled)        |
| Versioning                      | **Enable before the V1 tag** — prerequisite for the DataZone subscription flow |
| Encryption                      | AWS-managed keys (decided for this phase)    |
| Bucket policy                   | **Empty** — Option A model                   |
| Access                          | `${PILOT_GROUP}` via `SandboxDataSharePilotBucketAccess` inline policy |
| Snapshot layout                 | `s3://${BUCKET}/${SNAPSHOT_PREFIX}/<view>/year=YYYY/month=MM/day=DD/` |

## Why no bucket policy
S3 bucket policies cannot reference IAM groups, and an explicit `Deny` + `ArnNotLike`
overrides any group `Allow`. Option A (group Allow + Block Public Access, no Deny) was
chosen for Track A. Its guarantee depends on no broad S3 `Allow` existing elsewhere —
inventory `AdministratorAccess`-style groups before phase 2.

If a Deny is reintroduced later, use `aws:PrincipalTag/PilotAccess` rather than ARN lists.
