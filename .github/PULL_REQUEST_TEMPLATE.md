## What changed
<!-- One or two sentences. Small PRs only. -->

## Control mapping
- [ ] **VCS-1** — code is in this repo, not only in AWS
- [ ] **REPRO-1** — no hardcoded credentials, account IDs, or ARNs in templates; values live in `variables.json`
- [ ] **REVIEW-1** — this PR is small enough to review in one sitting

## Checklist
- [ ] `python scripts/render.py --check` passes locally
- [ ] `python scripts/check_no_secrets.py` passes locally
- [ ] `main.json` untouched (or PR carries the `main-json-change` label with a reason below)
- [ ] If a policy changed: the equivalent change is described for the console/CLI apply step
- [ ] No NPI data, sample rows, or query output in this PR

## Reason for main.json change (if any)
<!-- Leave blank if main.json was not modified. -->
