import pandas as pd
import pytest

from analyst_agent.sandbox import UnsafeCodeError, run_code

DF = pd.DataFrame({"a": [1, 2, 3], "b": [10, 20, 30]})


def test_runs_valid_code():
    assert run_code("result = df['b'].sum()", DF) == 60


def test_blocks_imports():
    with pytest.raises(UnsafeCodeError):
        run_code("import os\nresult = 1", DF)


def test_blocks_file_access():
    with pytest.raises(UnsafeCodeError):
        run_code("result = open('secret.txt').read()", DF)


def test_blocks_dunder_tricks():
    with pytest.raises(UnsafeCodeError):
        run_code("result = df.__class__", DF)


def test_blocks_file_write_methods():
    with pytest.raises(UnsafeCodeError):
        run_code("df.to_csv('x.csv')\nresult = 1", DF)


def test_original_dataframe_untouched():
    run_code("df['a'] = 0\nresult = 1", DF)
    assert DF["a"].tolist() == [1, 2, 3]


def test_missing_result_variable():
    with pytest.raises(RuntimeError):
        run_code("x = 1", DF)


def test_timeout():
    with pytest.raises(TimeoutError):
        run_code("while True:\n    pass\nresult = 1", DF, timeout=2)
