from __future__ import annotations

from typing import Dict, List

from tool.framework import AlphaBase, DataRegister


def create(alpha_id: str, cfg: Dict[str, str], dr: DataRegister) -> "TxliuMom01":
    return TxliuMom01(alpha_id, cfg, dr)


class TxliuMom01(AlphaBase):
    """Momentum placeholder alpha."""

    def generate(self) -> List[float]:
        closes = self.dr.load_close()
        return [0.0] + [closes[idx] - closes[idx - 1] for idx in range(1, len(closes))]
