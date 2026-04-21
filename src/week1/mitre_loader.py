import json
import requests
from typing import List, Dict

MITRE_URL = (
    "https://raw.githubusercontent.com/mitre/cti/master/"
    "enterprise-attack/enterprise-attack.json"
)

def load_mitre_techniques(max_techniques: int = 200) -> List[Dict]:
    print("Downloading MITRE ATT&CK data...")
    resp = requests.get(MITRE_URL, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    techniques = []
    for obj in data["objects"]:
        if obj.get("type") != "attack-pattern":
            continue
        if obj.get("revoked") or obj.get("x_mitre_deprecated"):
            continue

        ext_refs = obj.get("external_references", [])
        technique_id = next(
            (r["external_id"] for r in ext_refs
             if r.get("source_name") == "mitre-attack"),
            "unknown"
        )

        techniques.append({
            "id": technique_id,
            "name": obj.get("name", ""),
            "description": obj.get("description", "")[:500],
            "tactics": [
                phase["phase_name"]
                for phase in obj.get("kill_chain_phases", [])
            ],
        })

        if len(techniques) >= max_techniques:
            break

    print(f"Loaded {len(techniques)} techniques")
    return techniques
