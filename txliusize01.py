from __future__ import annotations

from typing import Dict, List

from tool.framework import AlphaBase, DataRegister


def create(alpha_id: str, cfg: Dict[str, str], dr: DataRegister) -> "TxliuSize01":
    return TxliuSize01(alpha_id, cfg, dr)


class TxliuSize01(AlphaBase):
    """Size placeholder alpha."""

    def generate(self) -> List[float]:
        closes = self.dr.load_close()
        scale = max(closes) if closes else 1.0
        return [value / scale for value in closes]
