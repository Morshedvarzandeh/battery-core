"""Core, solver-independent equations for battery modeling."""

from importlib.metadata import PackageNotFoundError, version

from battery_core.capacity import (
    c_rate_from_current,
    current_from_c_rate,
    ideal_duration_hours,
)
from battery_core.diffusion import ficks_first_law_flux

__all__ = [
    "c_rate_from_current",
    "current_from_c_rate",
    "ficks_first_law_flux",
    "ideal_duration_hours",
]

try:
    __version__ = version("battery-core")
except PackageNotFoundError:  # pragma: no cover - package not installed
    __version__ = "0.0.0"
