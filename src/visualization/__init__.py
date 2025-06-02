"""
Visualization Package
---------------------

This package contains modules for different components of the environmental
simulation and visualization system. Each module typically defines a class
representing a specific environmental or visual element (e.g., Atmosphere, WaterBody).

The `__all__` variable lists the primary classes intended for import from this package.
"""

from .atmosphere import Atmosphere
from .water_body import WaterBody
from .ecosystem import Ecosystem

__all__ = [
    "Atmosphere",
    "WaterBody",
    "Ecosystem"
]
# Removed: print("src.visualization package initialized.")
