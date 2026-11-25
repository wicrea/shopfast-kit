"""Governance check for the dbt project (run after `dbt parse` or `dbt build`).
Fails (exit code 1) if a model has no description or no owner, or a PII column has no classification.
Prints documentation coverage. Use it in CI: a model without an owner cannot be merged.
"""
import json, sys

m = json.load(open("target/manifest.json"))
models = [n for n in m["nodes"].values() if n["resource_type"] == "model"]
errors, cols_total, cols_doc = [], 0, 0
for n in models:
    meta = n.get("meta") or n.get("config", {}).get("meta", {})
    if not n.get("description") or n["description"].startswith("TODO"):
        errors.append(f"{n['name']}: missing model description")
    if not meta.get("owner"):
        errors.append(f"{n['name']}: missing meta.owner")
    for c in n["columns"].values():
        cols_total += 1
        if c.get("description") and not c["description"].startswith("TODO"):
            cols_doc += 1
        cmeta = c.get("meta") or c.get("config", {}).get("meta", {})
        tags = c.get("tags") or c.get("config", {}).get("tags", [])
        if "pii" in tags and not cmeta.get("classification"):
            errors.append(f"{n['name']}.{c['name']}: PII column without meta.classification")

print(f"Models: {len(models)} | documented columns: {cols_doc}/{cols_total}")
for e in errors:
    print("FAIL", e)
print("GOVERNANCE CHECK:", "PASSED" if not errors else f"FAILED ({len(errors)} problems)")
sys.exit(1 if errors else 0)
