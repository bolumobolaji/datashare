# Build log — SMUS notebook ETL blocker

**Date:** 2026-10-03 · **Track:** A (V1) · **Domain:** `dzd-ccfyu0e7eahzhl` (us-east-2) · **Studio domain:** `d-qtea8valgu8b`
**Status:** BLOCKED — AWS Support case open (System impaired)

## Goal

Run the Track A ETL from a SMUS notebook:

```
Orion datashare (producer) → consumer Redshift Serverless → Glue (unload) 
  → s3://sandbox-datashare-test-bucket-test → sandbox-datashare-test-database-test → Athena (SMUS)
```

## Outcome

Bucket and Glue database still empty. SMUS JupyterLab cannot resolve credentials and offers no
Spark kernel. Nothing has been unloaded.

---

## Phase 0 — Domain user / role setup and first notebook attempt (precedes Phase 1)

| Step | Result |
|---|---|
| Boundary errors on `AmazonSageMakerUserIAMExecutionRole_6d9e76ff` persisted after tagging | Root cause: `AmazonDataZoneDomain` tag value missing the `dzd-` prefix → corrected to `dzd-ccfyu0e7eahzhl` |
| Role not a recognized domain user | Added via DataZone console → User management; showed "Assigned / Session based" → **Activated**; still to be added as project member |
| Q proposed Glue ETL job via `GlueCrawlerRole` and a JDBC connection to `aws-orion-default-workgroup` | Deferred — requirement is to establish the connection **through SMUS** and see the datashare **views** |
| Checked subnets: all three SMUS subnets are default **public** subnets (auto-assign public IP, IGW route); Redshift Serverless workgroup uses the **same** public subnets and is publicly accessible | Confirmed — entire data path is public |
| JupyterLab: "Network issue detected. Your domain may be using a public subnet, which affects IDE functionality." | IDE blocked on public subnets |
| Private-subnet migration (3 private subnets, NAT gateway + EIP, private route table, interface endpoints, update SMUS environment **and** Redshift workgroup, turn off public access) | **Deferred to Track B** — explicit decision |
| Workarounds: presigned URL, Code Editor, Query Editor v2 + `UNLOAD` | Used **SMUS Query Editor** (Data analytics) to query the datashare |
| Subscription approval location | Project profiles tab (or blueprint, or per-asset in the catalog) — recorded |
| Connection access role set to `AmazonSageMakerUserIAMExecutionRole_6d9e76ff` | Rejected — ARN regex disallows the `/service-role/` path |
| Access role set to `datazone_usr_role_di4muxhv53wbvt_…` | `sts:AssumeRole` denied — role attempting to assume **itself** |
| Guidance: leave **Access role blank**, IAM authentication, database `dev`; IAM-mapped DB user format `IAMR:<role>` / `IAMU:<user>` | Led into Phase 1 (`sandbox_connection` password-auth error) |

## Phase 1 — SMUS Redshift connection to `aws-orion-default-workgroup`

| Step | Result |
|---|---|
| `sandbox_connection` failing: password auth for `iam-bolu-mobolaji`; JDBC falling back to username/password | Fail |
| Delete/recreate connection with IAM authentication | Fail |
| Secrets Manager: updated SMUS-created secret, edit-save to force re-read, verified key names | Fail |
| Enabled Redshift Serverless blueprint on the domain | Error changed: provisioning role denied `secretsmanager:DescribeSecret` |
| Root cause: secret missing `AmazonDataZoneProject` / `CreatedBy` tags; secret then not listed → recreated manually with tags | `password authentication failed for user "admin"`; no admin password available |
| Retried IAM auth | Denied `redshift-serverless:GetCredentials` — role conditions require `AmazonDataZoneProject` + `for-use-with-all-datazone-projects` tags on workgroup **and** namespace |
| **Decision:** do not modify the production workgroup/namespace | Path abandoned |

## Phase 2 — Alternative paths to the datashare

| Step | Result |
|---|---|
| Glue catalog over `orion_snapshots` (S3 mirror) | Blocked — project sandboxed to its own S3 path; DB also did not populate (no data source; legacy `IAM_ALLOWED_PRINCIPALS`) |
| Query consumer DB `dev@sandbox` on existing workgroup | `Publicly accessible consumer cannot access object` — workgroup is publicly accessible |
| New workgroup on existing namespace | Not possible — namespace↔workgroup is 1:1 |
| **Created** `sandbox-datashare-test-namespace-test` + `sandbox-datashare-test-workgroup-test` (publicly accessible off) | Success |
| Granted `orion_firm_2` to new namespace; `CREATE DATABASE` denied → `ALTER USER admin CREATEDB` → created DB via console UI | Success — datashare mounted |
| Query Editor v2 showing the new workgroup | **Unresolved** — bypassed, not diagnosed |

## Phase 3 — IAM for the Glue job

| Step | Result |
|---|---|
| `Redshift-S3-Access` attached to the new namespace | Done |
| `Redshift-S3-Access` + inline `SandboxDatashareS3Access` (bucket write) | Done |
| `GlueCrawlerRole` + `SandboxDatashareS3Access` + `RedshiftServerlessAccess` | Done |
| Tagged sandbox namespace + workgroup with `AmazonDataZoneProject` / `for-use-with-all-datazone-projects` to satisfy the `GetCredentials` conditions | Applied — **connection still failed** |

## Phase 4 — SMUS notebook cannot run

| Step | Result |
|---|---|
| `datazone:ListNotebooks` explicit deny from permissions boundary; error referenced the **us-east-1** domain | Launched from wrong portal → switched to us-east-2 portal |
| `Network is unreachable` → `datazone.us-east-2.api.aws` | Studio domains are **VpcOnly** in `vpc-06030b1e27835cd9d`; created DataZone interface endpoint (private DNS, 3 subnets, default SG) → **timeout** |
| Kernel restart; shutdown; space delete/recreate (×3+) | Timeout persists |
| Added `sg-051819d9aac896734` to Studio domain private + shared spaces (had to delete InService app first) | Timeout persists |
| Verified SG, route tables, endpoint ENIs in CIDR, VPC DNS attrs, endpoint policy | All correct |
| Created endpoints: `sagemaker.api`, `sts`, `s3`, `glue`, `logs`, `sagemaker.runtime`, `sagemaker.studio` | All Available; error changed to `%idle_timeout` not found + `CredentialsError: Missing credentials in config` |
| No PySpark kernel; only JupyterLab spaces | `serverless.spark` connection has **no backing EMR Serverless app** |
| Created EMR Serverless app `00g97qv2dmfsjj0d` (Spark, emr-7.x, same VPC/subnets/SG, Livy on) | STARTED |
| Link app to `serverless.spark` | Blocked — default connection, non-deletable, no application field |
| Inline `EMRServerlessAccess` on `datazone_usr_role_di4muxhv53wbvt_48rtbx1rft5fhl`; trust policy verified | No change |
| VSCode via Livy | Blocked — private subnets, no VPN/bastion |
| **AWS Support case opened** | Open |

---

## Standing infrastructure (as of this entry)

- Consumer: `sandbox-datashare-test-namespace-test` / `sandbox-datashare-test-workgroup-test`, `orion_firm_2` mounted, DataZone tags applied (did not unblock the SMUS connection)
- Storage: `sandbox-datashare-test-bucket-test` (empty), `sandbox-datashare-test-database-test` (empty)
- IAM: `Redshift-S3-Access`, `GlueCrawlerRole` scoped to the bucket; `EMRServerlessAccess` on the project user role
- Network: 10 interface endpoints in `vpc-06030b1e27835cd9d`
- Compute: EMR Serverless `00g97qv2dmfsjj0d`

## Open blockers

1. SMUS JupyterLab credential resolution / no Spark kernel — with Support.
2. `serverless.spark` default connection cannot be re-pointed.
3. Query Editor v2 does not list the new workgroup.
4. `AmazonSageMakerUserIAMExecutionRole_6d9e76ff` is a domain user but not yet a **project member**; confirm whether it is still needed given the project role is the executing principal.

## Follow-ups

- **Sandbox namespace/workgroup tagging — tried during the trial, did not resolve it.** `sandbox-datashare-test-namespace-test` / `-workgroup-test` carry `AmazonDataZoneProject=di4muxhv53wbvt` and `for-use-with-all-datazone-projects=true`; the SMUS connection still failed. So the tag conditions are not the only gate on `GetCredentials` from SMUS. **Give Support this fact explicitly** — it rules out the most common cause and points at the connection/credential layer.
- **Role sprawl:** `GlueCrawlerRole` now has NPI-bucket write + Redshift credentials; `Redshift-S3-Access` broadened. Neither is on the IT Security approval sheet — add as line items or consolidate onto one job role.
- **Cost:** ten interface endpoints bill hourly; flag for the sandbox cost review.
- **Track B — private network migration.** SMUS environment and the production Redshift workgroup share three default public subnets; the workgroup is publicly accessible. Track B scope: private subnets ×3, NAT gateway + EIP, private route table, endpoints re-homed, SMUS environment subnets updated, Redshift workgroup moved and public access turned off. This also lifts the JupyterLab public-subnet block. Needs its own line items on the IT Security sheet (NAT/EIP are new billable resources; workgroup network change touches production).
- Add this entry's gotchas to the PII-1 runbook (done — v1.3).

## Variables touched

`variables.json` should gain: `REDSHIFT_WORKGROUP_ID` → the new sandbox workgroup; `EMR_SERVERLESS_APP_ID` → `00g97qv2dmfsjj0d` (new variable — requires a `main-json-change` PR).
