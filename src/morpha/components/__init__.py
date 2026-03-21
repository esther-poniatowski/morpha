"""
Data components module.

Provides NumPy array subclasses with dimension annotations and metadata propagation.
"""

from morpha.components.base import DataComponent
from morpha.components.dimensions import Dimensions, DimensionsSpec
from morpha.components.metadata import MetaDataField
from morpha.components.specs import ComponentSpec

__all__ = [
    "DataComponent",
    "Dimensions",
    "DimensionsSpec",
    "MetaDataField",
    "ComponentSpec",
]
