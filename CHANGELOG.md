# Changelog

## v1.0.1 — 2026-10-03 (unreleased)
- Build log: added Phase 0 (domain-user activation, public-subnet IDE block, access-role regex/self-assume); sandbox consumer tagged; Track B private-network migration scoped.
- PII-1 runbook v1.4: four more gotchas.
- Build log: `docs/build-log/2026-10-03_smus-notebook-blocker.md` — SMUS notebook ETL blocked; AWS Support case open.
- PII-1 runbook v1.3: nine new gotchas (Redshift consumer tagging, secret tags, VpcOnly endpoints, EMR app prerequisite, namespace 1:1).
- `main.json` (**main-json-change**): declared `EMR_SERVERLESS_APP_ID`, `CONSUMER_NAMESPACE`.
- `variables.json`: filled project ID, project role, consumer workgroup/namespace, EMR app ID.


## v1.0.0 — Track A initial release
- Repo scaffold: immutable `main.json` contract, `variables.json` values, render + secret-scan scripts, CI.
- Policy templates: group bucket access, project-role scoped policy, LF-Tag management, proposed user boundary.
- Records: LF tags, S3 bucket config, blueprint state, ARN/condition reference.
- Code placeholders: five late-binding view DDL, Glue snapshot job skeleton.

## Versioning convention
| Version | Trigger                                              | Action                                              |
|---------|------------------------------------------------------|-----------------------------------------------------|
| v1.0.0  | Initial pilot setup                                  | Tag on first commit                                 |
| v1.x.x  | Fixes, helper scripts, doc updates                   | Patch on main via PR                                |
| v2.0.0  | Schema change or major Glue job change               | New tag **and** a DataZone asset revision → approval |
