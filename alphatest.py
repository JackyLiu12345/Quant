from __future__ import annotations

from alpha5dr import create
from tool.framework import DataRegister


def main() -> None:
    alpha = create("alpha5dr-demo", {"ndays": "5"}, DataRegister())
    result = alpha.generate()
    print(f"alpha5dr demo generated {len(result)} points")


if __name__ == "__main__":
    main()
