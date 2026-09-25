# ARN and condition reference — what is actually in use (V1)

Only conditions that exist in applied or committed policies are listed. Speculative
entries are omitted so this file can be trusted as an audit record.

| Policy / location                              | Mechanism                        | Scope                                                     |
|------------------------------------------------|----------------------------------|-----------------------------------------------------------|
| `NPI-Pilot-ProjectRole-ScopedPolicy` (project role) | Resource ARNs                | DataZone domain + project; S3 bucket; Athena workgroup; Redshift workgroup |
| same — `DenyAllOtherDataAccess`                | `NotResource` explicit Deny      | S3 Get/Put outside `${BUCKET}`                             |
| `SandboxDataSharePilotBucketAccess` (group)    | Resource ARNs, no conditions     | `${BUCKET}` and objects                                    |
| `SageMakerStudioProjectUserRolePermissionsBoundary` | AWS-managed boundary        | Caps the project role; verified present, never removed     |
| Lake Formation LF-Tag grants                   | Tag expression                   | `data_class=npi` AND `sensitivity=restricted`, per user    |

Deferred (documented, not applied): `aws:ResourceTag` on SageMaker Spaces;
`aws:PrincipalTag/PilotAccess` bucket Deny; per-user permissions boundary (PROPOSED).

