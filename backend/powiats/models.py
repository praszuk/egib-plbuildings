from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict


@dataclass(frozen=True)
class Powiat:
    name: str
    data_parser: Callable  # type: ignore
    url_builder: Callable  # type: ignore
    url_extras: Dict[str, Any]

    def build_url(self, lat: float, lon: float) -> str:
        return self.url_builder(self, lat=lat, lon=lon)  # type: ignore
