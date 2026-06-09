from __future__ import annotations

import argparse

from tool.framework import Runner, ensure_paths, parse_config


def main() -> None:
    parser = argparse.ArgumentParser(description="Run demo alpha research jobs")
    parser.add_argument("--config", default="config.xml", help="Path to XML config file")
    args = parser.parse_args()

    ensure_paths()
    jobs = parse_config(args.config)
    runner = Runner(jobs)
    runner.execute()


if __name__ == "__main__":
    main()
