try:
    import numpy as np
except ModuleNotFoundError:  # pragma: no cover - fallback for lightweight environments
    from strike import npcompat as np

from strike.alphabase import AlphaBase
from strike.config import ConfigNode
from strike.dataregister import DataRegister


def create(id, cfg, dr):
    return Alpha5DR(id, cfg, dr)


class Alpha5DR(AlphaBase):
    """
    5-days reversion
    """

    def __init__(self, alphaid: str, cfg: ConfigNode, dr: DataRegister) -> None:
        super().__init__(alphaid, cfg, dr)
        self.ndays = self.cfg.get_attr_default("ndays", 5)
        self.close = self.dr.getdata("close")

    def start_di(self) -> int:
        return max(self.delay, self.ndays + self.delay - 1)

    def generate(self, alpha_vec: np.ndarray, di: int) -> np.ndarray:
        ix = [flag == 1 for flag in self.universe[di]]
        window = self.close[di - self.ndays - self.delay + 1 : di - self.delay + 1]

        for ai, active in enumerate(ix):
            if not active:
                continue
            hist = [row[ai] for row in window]
            alpha_vec[ai] = -self.close[di - self.delay][ai] + np.mean(hist)
        return alpha_vec
