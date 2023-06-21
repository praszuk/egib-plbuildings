from dataclasses import dataclass
from typing import Any, Callable, Dict


@dataclass(frozen=True)
class Powiat:
    name: str
    data_parser: Callable
    url_builder: Callable
    url_extras: Dict[str, Any]

    def build_url(self, lat: float, lon: float) -> str:
        return self.url_builder(self, lat=lat, lon=lon)
