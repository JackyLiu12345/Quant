from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from momentum_factors import build_momentum_factors, mine_factors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Momentum factor mining (alpha5dr style).")
    parser.add_argument("--input", required=True, help="Path to CSV with date,asset,close columns.")
    parser.add_argument("--output-dir", default="outputs", help="Directory to save mining outputs.")
    parser.add_argument("--forward-window", type=int, default=5, help="Forward return horizon.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    data = pd.read_csv(args.input)
    factor_data = build_momentum_factors(data, forward_window=args.forward_window)
    result = mine_factors(factor_data)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    summary_path = output_dir / "momentum_factor_summary.csv"
    ic_path = output_dir / "momentum_factor_daily_ic.csv"
    full_factor_path = output_dir / "momentum_factor_panel.csv"

    result.summary.to_csv(summary_path, index=False)
    result.factor_scores.to_csv(ic_path, index=True)
    factor_data.to_csv(full_factor_path, index=False)

    print(f"Saved summary: {summary_path}")
    print(f"Saved daily IC: {ic_path}")
    print(f"Saved factor panel: {full_factor_path}")
    if not result.summary.empty:
        print("\nTop factors by IC-IR:")
        print(result.summary.head(5).to_string(index=False))


if __name__ == "__main__":
    main()
