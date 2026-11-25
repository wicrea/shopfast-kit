"""Export a data dictionary (CSV) from the dbt manifest: documentation as code -> a file business users can open."""
import csv, json

m = json.load(open("target/manifest.json"))
with open("data_dictionary_from_dbt.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["model", "column", "description", "pii", "classification", "model_owner", "domain", "tier"])
    for n in m["nodes"].values():
        if n["resource_type"] != "model":
            continue
        meta = n.get("meta") or n.get("config", {}).get("meta", {})
        for c in n["columns"].values():
            cmeta = c.get("meta") or c.get("config", {}).get("meta", {})
            tags = c.get("tags") or c.get("config", {}).get("tags", [])
            w.writerow([n["name"], c["name"], c.get("description", ""), "pii" in tags, cmeta.get("classification", ""),
                        meta.get("owner", ""), meta.get("domain", ""), meta.get("tier", "")])
print("Written: data_dictionary_from_dbt.csv")
