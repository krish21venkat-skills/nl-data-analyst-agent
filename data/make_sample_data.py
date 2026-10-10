"""Create a reproducible sample sales dataset at data/sales.csv."""
from pathlib import Path

import numpy as np
import pandas as pd

if __name__ == "__main__":
    rng = np.random.default_rng(42)  # fixed seed = same data every time
    n = 1000

    df = pd.DataFrame({
        "order_id": np.arange(1, n + 1),
        "order_date": pd.to_datetime("2025-01-01")
        + pd.to_timedelta(rng.integers(0, 365, n), unit="D"),
        "region": rng.choice(["North", "South", "East", "West"], n),
        "category": rng.choice(["Electronics", "Clothing", "Home", "Sports"], n),
        "units": rng.integers(1, 10, n),
        "unit_price": rng.uniform(5, 500, n).round(2),
    })
    df["revenue"] = (df["units"] * df["unit_price"]).round(2)

    out = Path(__file__).resolve().parent / "sales.csv"
    df.to_csv(out, index=False)
    print(f"Created {out} with {len(df)} rows")
