import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from src.week2.tools import virustotal_lookup, shodan_lookup, mitre_technique_lookup
from src.week2.prompts import SYSTEM_PROMPT

load_dotenv()


def build_agent():
    llm = ChatOllama(
        model="mistral",
        base_url=os.getenv("OLLAMA_HOST", "http://localhost:11434"),
    )

    tools = [virustotal_lookup, shodan_lookup, mitre_technique_lookup]

    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=SYSTEM_PROMPT
    )

    return agent


def run_agent(ioc: str) -> str:
    agent = build_agent()

    print(f"\nInvestigating IOC: {ioc}")
    print("="*60)

    result = agent.invoke({
        "messages": [{"role": "user", "content": f"Investigate this IOC and produce a threat report: {ioc}"}]
    })

    final_message = result["messages"][-1].content
    return final_message


if __name__ == "__main__":
    test_iocs = [
        "185.220.101.45",
    ]

    for ioc in test_iocs:
        report = run_agent(ioc)
        print(f"\nFINAL REPORT:\n{report}")
