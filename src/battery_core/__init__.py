"""Core, solver-independent equations for battery modeling."""

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
__version__ = "0.1.0"
