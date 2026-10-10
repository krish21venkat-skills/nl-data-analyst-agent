"""The agent loop: ask -> write code -> run -> (retry on error) -> explain."""
import re
from dataclasses import dataclass, field

import pandas as pd

from analyst_agent.llm import ask_llm
from analyst_agent.prompts import build_messages
from analyst_agent.sandbox import run_code


@dataclass
class AgentResult:
    question: str
    success: bool
    code: str = ""
    result: object = None
    explanation: str = ""
    attempts: list = field(default_factory=list)


def extract_code(reply: str) -> str:
    """Pull the code out of a ```python ... ``` block."""
    match = re.search(r"```(?:python)?\s*(.*?)```", reply, re.DOTALL)
    return (match.group(1) if match else reply).strip()


def result_to_text(result) -> str:
    if isinstance(result, (pd.DataFrame, pd.Series)):
        return result.head(20).to_string()
    return str(result)


def answer_question(df: pd.DataFrame, question: str, max_retries: int = 3) -> AgentResult:
    messages = build_messages(df, question)
    attempts: list[dict] = []

    for attempt in range(1, max_retries + 2):  # first try + retries
        reply = ask_llm(messages)
        code = extract_code(reply)
        try:
            result = run_code(code, df)
        except Exception as exc:
            attempts.append({"attempt": attempt, "code": code, "error": str(exc)})
            messages.append({"role": "assistant", "content": reply})
            messages.append({
                "role": "user",
                "content": f"That code failed with: {exc}\n"
                           "Fix it. Reply with the full corrected code in one ```python block.",
            })
            continue

        attempts.append({"attempt": attempt, "code": code, "error": None})
        explanation = ask_llm([{
            "role": "user",
            "content": f"Question: {question}\nComputed result:\n{result_to_text(result)}\n"
                       "Answer the question in one or two plain-English sentences.",
        }])
        return AgentResult(question, True, code, result, explanation, attempts)

    return AgentResult(question, False, attempts[-1]["code"], None,
                       "I could not produce working code for this question.", attempts)
