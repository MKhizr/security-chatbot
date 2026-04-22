import os
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel
from typing import List
from src.week2.tools import virustotal_lookup, shodan_lookup, mitre_technique_lookup
from src.week2.prompts import SYSTEM_PROMPT

load_dotenv()


class MITRETechnique(BaseModel):
    id: str
    name: str
    tactic: str


class ThreatReport(BaseModel):
    ioc: str
    ioc_type: str
    severity: str
    verdict: str
    malicious_detections: int
    total_engines: int
    country: str
    isp: str
    open_ports: List[int]
    known_vulns: List[str]
    mitre_techniques: List[MITRETechnique]
    summary: str
    recommendations: List[str]


REPORT_PROMPT = """
Based on all the tool results, produce a final threat report as valid JSON only.
No explanation, no markdown, just a JSON object with these exact fields:
{
  "ioc": "the IOC investigated",
  "ioc_type": "ip|hash|url",
  "severity": "critical|high|medium|low",
  "verdict": "malicious|suspicious|clean",
  "malicious_detections": <number>,
  "total_engines": <number>,
  "country": "country name or unknown",
  "isp": "ISP name or unknown",
  "open_ports": [list of port numbers],
  "known_vulns": [list of CVE strings],
  "mitre_techniques": [{"id": "T1234", "name": "technique name", "tactic": "tactic name"}],
  "summary": "2-3 sentence plain English summary",
  "recommendations": ["recommendation 1", "recommendation 2"]
}
"""


def build_agent():
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY")
    )
    tools = [virustotal_lookup, shodan_lookup, mitre_technique_lookup]
    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=SYSTEM_PROMPT
    )
    return agent, llm


def run_agent(ioc: str) -> dict:
    agent, llm = build_agent()

    print(f"\nInvestigating IOC: {ioc}")
    print("="*60)

    result = agent.invoke({
        "messages": [{"role": "user", "content": f"Investigate this IOC and produce a threat report: {ioc}"}]
    })

    investigation = result["messages"][-1].content
    print(f"Investigation complete. Generating structured report...")

    report_response = llm.invoke(
        f"{investigation}\n\n{REPORT_PROMPT}"
    )

    try:
        raw = report_response.content
        start = raw.find("{")
        end = raw.rfind("}") + 1
        json_str = raw[start:end]
        report = json.loads(json_str)
        return report
    except Exception as e:
        print(f"JSON parsing error: {e}")
        return {"ioc": ioc, "raw_report": investigation, "error": str(e)}


if __name__ == "__main__":
    test_iocs = [
        "185.220.101.45",
    ]

    for ioc in test_iocs:
        report = run_agent(ioc)
        print(f"\nSTRUCTURED THREAT REPORT:")
        print(json.dumps(report, indent=2))
