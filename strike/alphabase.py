from __future__ import annotations

from strike.config import ConfigNode
from strike.dataregister import DataRegister

try:
    import numpy as np
except ModuleNotFoundError:  # pragma: no cover - fallback for lightweight environments
    from strike import npcompat as np


class AlphaBase:
    def __init__(self, alphaid: str, cfg: ConfigNode, dr: DataRegister) -> None:
        self.alphaid = alphaid
        self.cfg = cfg
        self.dr = dr
        self.delay = self.cfg.get_attr_default("delay", 1)
        self.universe = self.dr.get_universe()

    def start_di(self) -> int:
        return self.delay

    def generate(self, alpha_vec: np.ndarray, di: int) -> np.ndarray:
        raise NotImplementedError

    def run(self) -> list[float]:
        output: list[float] = []
        for di in range(self.start_di(), self.dr.n_periods):
            alpha_vec = np.zeros(self.dr.n_assets)
            values = self.generate(alpha_vec, di)
            output.append(float(np.mean(values)))
        return output
