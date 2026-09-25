#!/usr/bin/env python3
"""
Render templates listed in main.json using values from variables.json.

Rules enforced (from main.json):
  - main.json is the contract; variables.json must define every variable it declares.
  - A value beginning with the unset marker ('<') fails the render. No placeholder ever ships.
  - Secrets are reference-only. Any 'value' key under secrets, or any variable flagged
    secret:true, fails the render.
  - Output goes to rendered/ which is gitignored.

Usage:  python scripts/render.py            # render all
        python scripts/render.py --check    # validate only, write nothing
"""
import json, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
MAIN = json.loads((ROOT / "main.json").read_text())
VARS = json.loads((ROOT / "variables.json").read_text())
CHECK_ONLY = "--check" in sys.argv
UNSET = MAIN["rules"]["unset_value_marker"]
PLACEHOLDER = re.compile(r"\$\{([A-Z0-9_]+)\}")

def fail(msg):
    print(f"RENDER FAIL: {msg}", file=sys.stderr)
    sys.exit(1)

# 1. Contract: every declared variable is present.
declared = set(MAIN["variables"].keys())
provided = set(VARS.get("values", {}).keys())
missing = declared - provided
if missing:
    fail(f"variables.json missing declared variables: {sorted(missing)}")
extra = provided - declared
if extra:
    fail(f"variables.json defines undeclared variables (add to main.json via a labeled PR): {sorted(extra)}")

# 2. No secret-flagged variable may carry a value here.
for k, meta in MAIN["variables"].items():
    if meta.get("secret"):
        fail(f"variable {k} is flagged secret in main.json — secrets are reference-only, remove it from variables.json values")

# 3. Secrets block: reference-only, never a value.
for name, entry in VARS.get("secrets", {}).items():
    if "value" in entry or set(entry.keys()) - {"store", "ref"}:
        fail(f"secrets.{name} must contain only 'store' and 'ref' — no literal value")

# 4. Unset values block the render.
values = VARS["values"]
unset = [k for k, v in values.items() if str(v).startswith(UNSET)]

# 5. Render each template.
rendered = 0
pending = []
for t in MAIN["templates"]:
    src = ROOT / t["src"]
    if not src.exists():
        fail(f"template not found: {t['src']}")
    text = src.read_text()
    needed = set(PLACEHOLDER.findall(text))
    unknown = needed - declared
    if unknown:
        fail(f"{t['src']} references undeclared variables {sorted(unknown)}")
    blocked = [v for v in needed if v in unset]
    if blocked:
        if CHECK_ONLY:
            pending.append((t["src"], sorted(blocked)))
            continue
        fail(f"{t['src']} needs unset variables {sorted(blocked)} — set them in variables.json first")
    out_text = PLACEHOLDER.sub(lambda m: str(values[m.group(1)]), text)
    if src.suffix == ".json":
        json.loads(out_text)  # rendered policy must be valid JSON
    if not CHECK_ONLY:
        out = ROOT / t["out"]
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(out_text)
    rendered += 1

mode = "validated" if CHECK_ONLY else "rendered"
print(f"OK: {rendered} template(s) {mode}.")
for src, vars_ in pending:
    print(f"PENDING (not an error in --check): {src} waits on {vars_}")
if unset:
    print(f"Unset variables in variables.json: {sorted(set(unset))}")
