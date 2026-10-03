# Runbooks

Operational procedures for the Track A sandbox. These are versioned here so every change to
how NPI access is controlled has a commit and a reviewer.

| Runbook | Controls | Purpose |
|---------|----------|---------|
| `PII-1_NPI_Access_Control_Runbook.html` | PII-1 | Layered access controls (identity, LF-Tags, scoped IAM, project isolation, subscription approval), Step 0 environment prerequisites, gotchas from the first build pass |
| `VCS-1_Version_Control_Runbook.html`   | VCS-1 · REPRO-1 · REVIEW-1 | Repo model (`main.json` / `variables.json` / secrets-by-reference), GitHub setup, branch protection, SMUS connection, reproducibility check |

Runbooks change only via PR, like everything else. If a control changes in AWS, the runbook
change lands in the same PR.

Build history and open blockers live in `../build-log/` — one dated entry per build pass.
