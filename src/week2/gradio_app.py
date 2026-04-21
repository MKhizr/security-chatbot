import gradio as gr
import json
from src.week2.agent import run_agent


def investigate(ioc: str):
    if not ioc.strip():
        return "Please enter an IOC."
    report = run_agent(ioc.strip())
    return json.dumps(report, indent=2)


with gr.Blocks(title="Threat Intel Triage Agent") as demo:
    gr.Markdown("""
    # Threat Intel Triage Agent
    **Autonomous IOC investigation** · VirusTotal · Shodan · MITRE ATT&CK
    """)

    with gr.Row():
        with gr.Column(scale=2):
            ioc_input = gr.Textbox(
                label="Enter IOC",
                placeholder="IP address, file hash, or URL...",
                lines=1
            )
            investigate_btn = gr.Button("Investigate", variant="primary")
            gr.Examples(
                examples=[
                    ["185.220.101.45"],
                    ["8.8.8.8"],
                ],
                inputs=ioc_input
            )

        with gr.Column(scale=3):
            output = gr.Code(
                label="Threat Report",
                language="json",
                lines=30
            )

    investigate_btn.click(
        fn=investigate,
        inputs=ioc_input,
        outputs=output
    )
    ioc_input.submit(
        fn=investigate,
        inputs=ioc_input,
        outputs=output
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7861)
