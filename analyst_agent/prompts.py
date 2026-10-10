"""Prompt templates and a short data summary for the model."""
import pandas as pd

SYSTEM_PROMPT = """You are an expert data analyst who writes pandas/NumPy code.
A pandas DataFrame named `df` is already loaded. `pd` and `np` are available.

RULES:
1. Do NOT import anything. Do NOT read or write files.
2. Store the final answer in a variable named `result`.
3. Use only the column names listed in the schema.
4. Date columns may be plain text: convert with pd.to_datetime() before using .dt.
5. Reply with ONE ```python code block and nothing else.
"""


def describe_df(df: pd.DataFrame) -> str:
    """Short text summary of the data so the model knows what columns exist."""
    lines = [f"Rows: {len(df)}", "Columns:"]
    for col in df.columns:
        samples = df[col].dropna().head(3).tolist()
        lines.append(f"- {col} (type: {df[col].dtype}), e.g. {samples}")
    return "\n".join(lines)


def build_messages(df: pd.DataFrame, question: str) -> list[dict]:
    user = f"DataFrame schema:\n{describe_df(df)}\n\nQuestion: {question}"
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user},
    ]
