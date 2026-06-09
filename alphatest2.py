from __future__ import annotations

from txliumom01 import create as create_mom
from txliusize01 import create as create_size
from tool.framework import DataRegister


def main() -> None:
    dr = DataRegister()
    mom = create_mom("mom-demo", {}, dr).generate()
    size = create_size("size-demo", {}, dr).generate()
    print(f"momentum points={len(mom)}, size points={len(size)}")


if __name__ == "__main__":
    main()
