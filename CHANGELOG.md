# Changelog

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
