"""Quick terminal test of the agent (no UI)."""
import pandas as pd

from analyst_agent.agent import answer_question

if __name__ == "__main__":  # required on Windows because the sandbox spawns a process
    df = pd.read_csv("data/sales.csv")
    res = answer_question(df, "Which region has the highest total revenue?")
    print("CODE:\n", res.code)
    print("RESULT:", res.result)
    print("ANSWER:", res.explanation)
    print("ATTEMPTS:", len(res.attempts))
