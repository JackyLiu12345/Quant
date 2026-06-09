from alpha5dr import create
from strike.config import ConfigNode
from strike.dataregister import DataRegister


def main() -> None:
    alpha = create("alpha5dr-demo", ConfigNode({"ndays": "5"}), DataRegister())
    result = alpha.run()
    print(f"alpha5dr demo generated {len(result)} points")


if __name__ == "__main__":
    main()
