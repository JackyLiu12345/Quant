try:
    import numpy as np
except ModuleNotFoundError:  # pragma: no cover - fallback for lightweight environments
    from strike import npcompat as np

from strike.alphabase import AlphaBase
from strike.config import ConfigNode
from strike.dataregister import DataRegister


def create(id, cfg, dr):
    return TxliuSize01(id, cfg, dr)


class TxliuSize01(AlphaBase):
    """
    size proxy from inverse price level
    """

    def __init__(self, alphaid: str, cfg: ConfigNode, dr: DataRegister) -> None:
        super().__init__(alphaid, cfg, dr)
        self.close = self.dr.getdata("close")

    def generate(self, alpha_vec: np.ndarray, di: int) -> np.ndarray:
        ix = [flag == 1 for flag in self.universe[di]]
        for ai, active in enumerate(ix):
            if not active:
                continue
            price = self.close[di - self.delay][ai]
            alpha_vec[ai] = 0.0 if price == 0 else 1.0 / price
        return alpha_vec
