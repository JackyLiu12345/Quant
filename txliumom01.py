try:
    import numpy as np
except ModuleNotFoundError:  # pragma: no cover - fallback for lightweight environments
    from strike import npcompat as np

from strike.alphabase import AlphaBase
from strike.config import ConfigNode
from strike.dataregister import DataRegister


def create(id, cfg, dr):
    return TxliuMom01(id, cfg, dr)


class TxliuMom01(AlphaBase):
    """
    1-day momentum
    """

    def __init__(self, alphaid: str, cfg: ConfigNode, dr: DataRegister) -> None:
        super().__init__(alphaid, cfg, dr)
        self.close = self.dr.getdata("close")

    def start_di(self) -> int:
        return self.delay + 1

    def generate(self, alpha_vec: np.ndarray, di: int) -> np.ndarray:
        ix = [flag == 1 for flag in self.universe[di]]
        for ai, active in enumerate(ix):
            if not active:
                continue
            alpha_vec[ai] = self.close[di - self.delay][ai] - self.close[di - self.delay - 1][ai]
        return alpha_vec
