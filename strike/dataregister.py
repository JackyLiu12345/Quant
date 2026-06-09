from __future__ import annotations

from dataclasses import dataclass
import math
from typing import List


@dataclass
class DataRegister:
    symbol: str = "DEMO"
    periods: int = 60
    assets: int = 4

    def getdata(self, name: str) -> List[List[float]]:
        if name != "close":
            raise KeyError(f"Unsupported dataset: {name}")

        close: List[List[float]] = []
        for di in range(self.periods):
            row = []
            for ai in range(self.assets):
                price = 100.0 + 0.2 * di + 0.5 * ai + math.sin((di + ai) / 4.0)
                row.append(price)
            close.append(row)
        return close

    def get_universe(self) -> List[List[int]]:
        return [[1 for _ in range(self.assets)] for _ in range(self.periods)]

    @property
    def n_assets(self) -> int:
        return self.assets

    @property
    def n_periods(self) -> int:
        return self.periods
