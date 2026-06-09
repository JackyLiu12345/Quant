"""Tiny numpy-compatible subset used when numpy is unavailable."""

from __future__ import annotations

from typing import List

ndarray = List[float]


def zeros(size: int) -> ndarray:
    return [0.0 for _ in range(size)]


def mean(values: List[float], axis: int | None = None) -> float:
    del axis
    if not values:
        return 0.0
    return float(sum(values) / len(values))
