import pandas as pd

from analyst_agent.agent import extract_code, result_to_text
from analyst_agent.prompts import describe_df


def test_extract_code_from_fenced_block():
    reply = "Sure!\n```python\nresult = 1 + 1\n```\nDone."
    assert extract_code(reply) == "result = 1 + 1"


def test_extract_code_without_fence():
    assert extract_code("result = 5") == "result = 5"


def test_result_to_text_scalar():
    assert result_to_text(42) == "42"


def test_describe_df_lists_columns():
    text = describe_df(pd.DataFrame({"x": [1, 2], "y": ["a", "b"]}))
    assert "x" in text and "y" in text and "Rows: 2" in text
