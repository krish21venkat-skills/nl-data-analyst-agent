"""Safely run LLM-written pandas/NumPy code.

NOTE: This is a learning-grade sandbox, not a hardened security boundary.
For production, run generated code in a locked-down container.
"""
import ast
import builtins
import multiprocessing as mp
import queue

import numpy as np
import pandas as pd


class UnsafeCodeError(Exception):
    """Raised when generated code breaks a safety rule."""


BLOCKED_NAMES = {
    "eval", "exec", "compile", "open", "__import__", "input", "globals",
    "locals", "vars", "getattr", "setattr", "delattr", "breakpoint",
    "exit", "quit",
}
BLOCKED_ATTRS = {
    "read_csv", "read_excel", "read_json", "read_pickle", "read_sql",
    "read_parquet", "to_csv", "to_excel", "to_json", "to_pickle", "to_sql",
    "to_parquet", "system", "popen", "eval",
}
ALLOWED_BUILTINS = [
    "abs", "all", "any", "bool", "dict", "enumerate", "filter", "float",
    "int", "isinstance", "len", "list", "map", "max", "min", "print",
    "range", "reversed", "round", "set", "sorted", "str", "sum", "tuple", "zip",
]
SAFE_BUILTINS = {name: getattr(builtins, name) for name in ALLOWED_BUILTINS}


def validate_code(code: str) -> None:
    """Raise UnsafeCodeError if the code contains anything risky."""
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            raise UnsafeCodeError("Imports are not allowed. pd, np and df are already available.")
        if isinstance(node, ast.Name) and node.id in BLOCKED_NAMES:
            raise UnsafeCodeError(f"Use of '{node.id}' is not allowed.")
        if isinstance(node, ast.Attribute):
            if node.attr.startswith("_"):
                raise UnsafeCodeError(f"Access to '{node.attr}' is not allowed.")
            if node.attr in BLOCKED_ATTRS:
                raise UnsafeCodeError(f"Use of '.{node.attr}' is not allowed.")


def _worker(code: str, df: pd.DataFrame, out) -> None:
    """Runs inside a separate process."""
    try:
        namespace = {"__builtins__": SAFE_BUILTINS, "df": df.copy(), "pd": pd, "np": np}
        exec(code, namespace)
        if "result" not in namespace:
            out.put(("error", "Code did not create a variable named 'result'."))
        else:
            out.put(("ok", namespace["result"]))
    except Exception as exc:
        out.put(("error", f"{type(exc).__name__}: {exc}"))


def run_code(code: str, df: pd.DataFrame, timeout: int = 10):
    """Validate, then execute code in a child process with a time limit."""
    validate_code(code)
    ctx = mp.get_context("spawn")
    out = ctx.Queue()
    proc = ctx.Process(target=_worker, args=(code, df, out))
    proc.start()
    try:
        status, payload = out.get(timeout=timeout)
    except queue.Empty:
        proc.terminate()
        raise TimeoutError(f"Code took longer than {timeout} seconds.") from None
    finally:
        proc.join(1)
    if status == "error":
        raise RuntimeError(payload)
    return payload
