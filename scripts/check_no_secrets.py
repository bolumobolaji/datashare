#!/usr/bin/env python3
"""
Fail loud if any tracked file contains something that looks like a credential.
Runs in CI on every PR and can run locally: python scripts/check_no_secrets.py
Exits non-zero on the first finding.
"""
import re, sys, pathlib, subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
PATTERNS = {
    "AWS access key":        re.compile(r"\b(AKIA|ASIA)[0-9A-Z]{16}\b"),
    "AWS secret key":        re.compile(r"(?i)aws_secret_access_key\s*[:=]\s*['\"]?[A-Za-z0-9/+=]{40}"),
    "GitHub PAT":            re.compile(r"\b(ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{36,}\b"),
    "GitHub fine-grained":   re.compile(r"\bgithub_pat_[A-Za-z0-9_]{60,}\b"),
    "Private key block":     re.compile(r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "Password literal":      re.compile(r"(?i)\"?(password|passwd|pwd)\"?\s*[:=]\s*\"[^\"<$][^\"]{3,}\""),
    "Secret 'value' key":    re.compile(r"(?i)\"value\"\s*:\s*\"[^\"]+\""),
}
SKIP_DIRS = {".git", "rendered", "__pycache__"}
SKIP_FILES = {"check_no_secrets.py"}

def tracked_files():
    try:
        out = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True).stdout
        return [ROOT / p for p in out.split()]
    except Exception:
        return [p for p in ROOT.rglob("*") if p.is_file()]

findings = 0
for path in tracked_files():
    if any(part in SKIP_DIRS for part in path.parts) or path.name in SKIP_FILES:
        continue
    try:
        text = path.read_text(errors="ignore")
    except Exception:
        continue
    for label, rx in PATTERNS.items():
        for m in rx.finditer(text):
            line = text.count("\n", 0, m.start()) + 1
            print(f"SECRET SCAN FAIL: {label} in {path.relative_to(ROOT)}:{line}", file=sys.stderr)
            findings += 1

if findings:
    sys.exit(1)
print("OK: no credential-like strings found in tracked files.")
