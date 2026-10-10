"""Thin wrapper around the local Ollama model."""
import os

import ollama

# Change the default here, or set an environment variable:
#   PowerShell:  $env:OLLAMA_MODEL = "qwen2.5-coder:7b"
DEFAULT_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:latest")


def ask_llm(messages: list[dict], model: str | None = None) -> str:
    """Send chat messages to the local Ollama model and return its reply."""
    response = ollama.chat(
        model=model or DEFAULT_MODEL,
        messages=messages,
        options={"temperature": 0},  # 0 = most predictable answers
    )
    return response["message"]["content"]
