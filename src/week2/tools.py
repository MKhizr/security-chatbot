import os
import requests
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()

VIRUSTOTAL_API_KEY = os.getenv("VIRUSTOTAL_API_KEY")
SHODAN_API_KEY = os.getenv("SHODAN_API_KEY")


@tool
def virustotal_lookup(ioc: str) -> dict:
    """Look up an IP address, file hash, or URL on VirusTotal.
    Returns malicious verdict count and detection ratio."""
    headers = {"x-apikey": VIRUSTOTAL_API_KEY}

    if len(ioc) in [32, 40, 64]:
        url = f"https://www.virustotal.com/api/v3/files/{ioc}"
        ioc_type = "hash"
    elif ioc.startswith("http"):
        import base64
        url_id = base64.urlsafe_b64encode(ioc.encode()).decode().strip("=")
        url = f"https://www.virustotal.com/api/v3/urls/{url_id}"
        ioc_type = "url"
    else:
        url = f"https://www.virustotal.com/api/v3/ip_addresses/{ioc}"
        ioc_type = "ip"

    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        stats = data["data"]["attributes"].get("last_analysis_stats", {})
        malicious = stats.get("malicious", 0)
        total = sum(stats.values()) if stats else 0
        return {
            "ioc": ioc,
            "ioc_type": ioc_type,
            "malicious_detections": malicious,
            "total_engines": total,
            "verdict": "malicious" if malicious > 5 else "suspicious" if malicious > 0 else "clean",
            "source": "VirusTotal"
        }
    except Exception as e:
        return {"ioc": ioc, "error": str(e), "source": "VirusTotal"}


@tool
def shodan_lookup(ip: str) -> dict:
    """Look up an IP address on Shodan.
    Returns open ports, country, ISP, and known vulnerabilities."""
    try:
        url = f"https://api.shodan.io/shodan/host/{ip}?key={SHODAN_API_KEY}"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return {
            "ip": ip,
            "country": data.get("country_name", "unknown"),
            "isp": data.get("isp", "unknown"),
            "open_ports": data.get("ports", []),
            "vulns": list(data.get("vulns", {}).keys())[:5],
            "hostnames": data.get("hostnames", []),
            "source": "Shodan"
        }
    except Exception as e:
        return {"ip": ip, "error": str(e), "source": "Shodan"}


@tool
def mitre_technique_lookup(query: str) -> dict:
    """Search MITRE ATT&CK for techniques related to a threat description.
    Returns top matching techniques with IDs and tactics."""
    try:
        from src.week1.embeddings import build_index, semantic_search
        collection, model = build_index()
        hits = semantic_search(query, collection, model, top_k=3)
        return {
            "query": query,
            "techniques": [
                {
                    "id": h["id"],
                    "name": h["name"],
                    "tactics": h["tactics"],
                    "similarity": h["similarity"]
                }
                for h in hits
            ],
            "source": "MITRE ATT&CK"
        }
    except Exception as e:
        return {"query": query, "error": str(e), "source": "MITRE ATT&CK"}
