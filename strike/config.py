from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Generic, TypeVar, cast

T = TypeVar("T")


@dataclass
class ConfigNode:
    data: Dict[str, str] = field(default_factory=dict)

    def get_attr_default(self, key: str, default: T) -> T:
        value = self.data.get(key)
        if value is None:
            return default

        if isinstance(default, bool):
            return cast(T, value.lower() in {"1", "true", "yes", "on"})
        if isinstance(default, int):
            return cast(T, int(value))
        if isinstance(default, float):
            return cast(T, float(value))
        return cast(T, value)
