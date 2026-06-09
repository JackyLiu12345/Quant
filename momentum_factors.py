from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
import pandas as pd


REQUIRED_COLUMNS = {"date", "asset", "close"}


@dataclass
class MiningResult:
    factor_scores: pd.DataFrame
    summary: pd.DataFrame


def validate_input(df: pd.DataFrame) -> None:
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")


def _cross_sectional_zscore(df: pd.DataFrame) -> pd.DataFrame:
    by_day = df.groupby("date")
    mean = by_day.transform("mean")
    std = by_day.transform("std").replace(0, np.nan)
    return (df - mean) / std


def build_momentum_factors(
    market_data: pd.DataFrame,
    lookbacks: Iterable[int] = (5, 10, 20, 60),
    forward_window: int = 5,
) -> pd.DataFrame:
    validate_input(market_data)
    df = market_data.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(["asset", "date"]).reset_index(drop=True)

    grouped = df.groupby("asset", group_keys=False)
    for window in lookbacks:
        df[f"mom_{window}"] = grouped["close"].pct_change(window)

    rolling_vol = grouped["close"].pct_change().rolling(20).std().reset_index(level=0, drop=True)
    df["vol_adj_mom_20"] = df["mom_20"] / rolling_vol

    ma_20 = grouped["close"].rolling(20).mean().reset_index(level=0, drop=True)
    ma_60 = grouped["close"].rolling(60).mean().reset_index(level=0, drop=True)
    df["ma_ratio_20_60"] = ma_20 / ma_60 - 1

    delta = grouped["close"].diff()
    gain = delta.clip(lower=0).groupby(df["asset"]).rolling(14).mean().reset_index(level=0, drop=True)
    loss = (-delta.clip(upper=0)).groupby(df["asset"]).rolling(14).mean().reset_index(level=0, drop=True)
    rs = gain / loss.replace(0, np.nan)
    df["rsi_14"] = 100 - (100 / (1 + rs))
    df["rsi_mom_14"] = (df["rsi_14"] - 50) / 50

    df["fwd_ret"] = grouped["close"].shift(-forward_window) / df["close"] - 1

    factor_columns = [c for c in df.columns if c.startswith("mom_")] + [
        "vol_adj_mom_20",
        "ma_ratio_20_60",
        "rsi_mom_14",
    ]
    standardized = _cross_sectional_zscore(df[factor_columns].join(df[["date"]]).set_index("date")).reset_index()
    for c in factor_columns:
        df[f"{c}_z"] = standardized[c]
    return df


def mine_factors(factor_data: pd.DataFrame) -> MiningResult:
    factor_columns = [c for c in factor_data.columns if c.endswith("_z")]
    metrics = []
    series = []

    for factor in factor_columns:
        daily_ic = factor_data.groupby("date").apply(
            lambda x: x[[factor, "fwd_ret"]].corr(method="spearman").iloc[0, 1]
        )
        daily_ic = daily_ic.dropna()
        if daily_ic.empty:
            continue
        mean_ic = float(daily_ic.mean())
        std_ic = float(daily_ic.std())
        ir = mean_ic / std_ic if std_ic and not np.isnan(std_ic) else np.nan
        hit_rate = float((daily_ic > 0).mean())
        metrics.append(
            {
                "factor": factor,
                "mean_ic": mean_ic,
                "ic_std": std_ic,
                "ic_ir": ir,
                "hit_rate": hit_rate,
                "observations": int(daily_ic.shape[0]),
            }
        )
        daily_ic.name = factor
        series.append(daily_ic)

    if not metrics:
        return MiningResult(factor_scores=pd.DataFrame(), summary=pd.DataFrame())

    summary = pd.DataFrame(metrics).sort_values("ic_ir", ascending=False).reset_index(drop=True)
    factor_scores = pd.concat(series, axis=1).sort_index()
    return MiningResult(factor_scores=factor_scores, summary=summary)
