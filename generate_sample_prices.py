from __future__ import annotations

import argparse

import numpy as np
import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate sample price panel for factor mining.")
    parser.add_argument("--assets", type=int, default=30)
    parser.add_argument("--days", type=int, default=400)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", default="sample_prices.csv")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rng = np.random.default_rng(args.seed)
    dates = pd.bdate_range(end=pd.Timestamp.today().normalize(), periods=args.days)
    asset_ids = [f"A{i:03d}" for i in range(args.assets)]

    rows = []
    for asset in asset_ids:
        drift = rng.normal(0.0003, 0.0002)
        shocks = rng.normal(drift, 0.02, len(dates))
        close = 100 * np.exp(np.cumsum(shocks))
        rows.append(pd.DataFrame({"date": dates, "asset": asset, "close": close}))

    df = pd.concat(rows, ignore_index=True).sort_values(["asset", "date"])
    df.to_csv(args.output, index=False)
    print(f"Saved sample data to {args.output} ({len(df)} rows)")


if __name__ == "__main__":
    main()
