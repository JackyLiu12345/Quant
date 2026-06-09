from strike.config import ConfigNode
from strike.dataregister import DataRegister
from txliumom01 import create as create_mom
from txliusize01 import create as create_size


def main() -> None:
    dr = DataRegister()
    mom = create_mom("mom-demo", ConfigNode({}), dr).run()
    size = create_size("size-demo", ConfigNode({}), dr).run()
    print(f"momentum points={len(mom)}, size points={len(size)}")


if __name__ == "__main__":
    main()
