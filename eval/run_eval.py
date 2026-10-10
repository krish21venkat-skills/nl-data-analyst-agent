"""Benchmark: compare the agent's answers with ground truth computed by plain pandas."""
import math
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from analyst_agent.agent import answer_question, result_to_text  # noqa: E402
from analyst_agent.llm import DEFAULT_MODEL  # noqa: E402

# (question, function that computes the TRUE answer with plain pandas)
CASES = [
    ("What is the total revenue?", lambda d: d["revenue"].sum()),
    ("Which region has the highest total revenue?",
     lambda d: d.groupby("region")["revenue"].sum().idxmax()),
    ("How many orders are in the Electronics category?",
     lambda d: (d["category"] == "Electronics").sum()),
    ("What is the average unit price?", lambda d: d["unit_price"].mean()),
    ("Which category sells the most units?",
     lambda d: d.groupby("category")["units"].sum().idxmax()),
    ("What is the median revenue per order?", lambda d: d["revenue"].median()),
    ("Which region has the lowest average revenue per order?",
     lambda d: d.groupby("region")["revenue"].mean().idxmin()),
    ("How many orders have more than 5 units?", lambda d: (d["units"] > 5).sum()),
]


def is_correct(got, expected) -> bool:
    if isinstance(expected, str):
        return expected.lower() in result_to_text(got).lower()
    try:
        return math.isclose(float(got), float(expected), rel_tol=1e-3)
    except (TypeError, ValueError):
        return False


if __name__ == "__main__":
    df = pd.read_csv("data/sales.csv")
    correct = retries = 0
    print(f"Model: {DEFAULT_MODEL}\n")
    for question, truth_fn in CASES:
        res = answer_question(df, question)
        ok = res.success and is_correct(res.result, truth_fn(df))
        correct += int(ok)
        retries += len(res.attempts) - 1
        print(f"{'PASS' if ok else 'FAIL'}  {question}")
    total = len(CASES)
    print(f"\nAccuracy: {correct}/{total} = {correct / total:.0%}")
    print(f"Average retries: {retries / total:.1f}")
