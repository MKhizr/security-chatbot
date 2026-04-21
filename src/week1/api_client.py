import os
import openai
from dotenv import load_dotenv
from dataclasses import dataclass
from typing import Optional

load_dotenv()

@dataclass
class APIResponse:
    provider: str
    model: str
    content: str
    input_tokens: int
    output_tokens: int

    def summary(self) -> str:
        return (
            f"[{self.provider}] {self.model}\n"
            f"Tokens: {self.input_tokens} in / {self.output_tokens} out\n"
            f"Response: {self.content[:200]}"
        )


def call_ollama(prompt: str, system: str = "") -> Optional[APIResponse]:
    client = openai.OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama"
    )
    try:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        resp = client.chat.completions.create(
            model="llama3.2",
            max_tokens=512,
            messages=messages
        )
        return APIResponse(
            provider="Ollama",
            model=resp.model,
            content=resp.choices[0].message.content,
            input_tokens=resp.usage.prompt_tokens,
            output_tokens=resp.usage.completion_tokens,
        )
    except Exception as e:
        print(f"Error: {e}")
        return None
