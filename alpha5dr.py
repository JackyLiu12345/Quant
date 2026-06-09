from __future__ import annotations

from typing import Dict, List

from tool.framework import AlphaBase, DataRegister


def create(alpha_id: str, cfg: Dict[str, str], dr: DataRegister) -> "Alpha5DR":
    return Alpha5DR(alpha_id, cfg, dr)


class Alpha5DR(AlphaBase):
    """5-day mean reversion alpha example."""

    def __init__(self, alpha_id: str, cfg: Dict[str, str], dr: DataRegister):
        super().__init__(alpha_id=alpha_id, cfg=cfg, dr=dr)
        self.ndays = int(cfg.get("ndays", "5"))
        self.close = dr.load_close()

    def generate(self) -> List[float]:
        if len(self.close) < self.ndays:
            return []

        output: List[float] = []
        for idx, value in enumerate(self.close):
            start = max(0, idx - self.ndays + 1)
            window = self.close[start : idx + 1]
            rolling_mean = sum(window) / len(window)
            output.append(rolling_mean - value)
        return output
