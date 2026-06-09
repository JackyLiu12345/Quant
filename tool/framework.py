from __future__ import annotations

from dataclasses import dataclass, field
from importlib import import_module
from pathlib import Path
from typing import Dict, Iterable, List
import xml.etree.ElementTree as ET

from strike.config import ConfigNode
from strike.dataregister import DataRegister


@dataclass
class Job:
    name: str
    module: str
    options: Dict[str, str] = field(default_factory=dict)


def parse_config(config_path: str) -> List[Job]:
    root = ET.parse(config_path).getroot()
    jobs: List[Job] = []
    for node in root.findall("job"):
        options = {opt.get("name", ""): opt.get("value", "") for opt in node.findall("option")}
        jobs.append(
            Job(
                name=node.get("name", node.get("module", "job")),
                module=node.get("module", "alpha5dr"),
                options={k: v for k, v in options.items() if k},
            )
        )
    return jobs


class Runner:
    def __init__(self, jobs: Iterable[Job]):
        self.jobs = list(jobs)

    def execute(self) -> None:
        print(f"Loaded {len(self.jobs)} job(s)")
        for job in self.jobs:
            module = import_module(job.module)
            create = getattr(module, "create")
            cfg = ConfigNode(job.options)
            dr = DataRegister(symbol=job.options.get("symbol", "DEMO"))
            alpha = create(job.name, cfg, dr)
            output = alpha.run()
            sample = ", ".join(f"{value:.6f}" for value in output[-3:]) if output else "<empty>"
            print(f"[{job.name}] module={job.module} points={len(output)} tail=[{sample}]")


def ensure_paths() -> None:
    for folder in ("pnl", "source_ref"):
        Path(folder).mkdir(parents=True, exist_ok=True)


__all__ = ["Runner", "parse_config", "ensure_paths"]
