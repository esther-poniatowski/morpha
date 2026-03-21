"""
Morpha: Domain-agnostic data representation patterns for scientific computing.

This package provides foundational abstractions for building structured data representations:

- **Components**: NumPy array subclasses with dimension annotations and metadata propagation
- **Structures**: Abstract base classes for composite data structures with schema enforcement
- **Coordinates**: Labeled axes with attribute validation
- **Creational**: Factory and Builder patterns for constructing data objects
- **I/O**: Saver/Loader patterns for multiple file formats

Example
-------
>>> from morpha import DataComponent, Dimensions, DataStructure
>>> import numpy as np
>>>
>>> class MyData(DataComponent):
...     DIMENSIONS_SPEC = DimensionsSpec(time=True, units=False)
...     DTYPE = np.float64
...     SENTINEL = np.nan
...
>>> data = MyData(np.zeros((10, 5)), dims=Dimensions("time", "units"))
"""

__version__ = "0.0.0"

# Core components
from morpha.components.base import DataComponent
from morpha.components.dimensions import Dimensions, DimensionsSpec
from morpha.components.metadata import MetaDataField
from morpha.components.specs import ComponentSpec

# Structures
from morpha.structures.base import DataStructure
from morpha.structures.containers import Container

# Coordinates
from morpha.coordinates.base import Coordinate
from morpha.coordinates.attributes import Attribute

# Creational patterns
from morpha.creational.factory import Factory
from morpha.creational.builder import Builder

# I/O
from morpha.io.base import IOHandler, FileExt
from morpha.io.savers import (
    Saver,
    SaverPKL,
    SaverNPY,
    SaverNPZ,
    SaverJSON,
    SaverYAML,
    SaverHDF5,
)
from morpha.io.loaders import (
    Loader,
    LoaderPKL,
    LoaderNPY,
    LoaderNPZ,
    LoaderJSON,
    LoaderYAML,
    LoaderHDF5,
)

__all__ = [
    # Components
    "DataComponent",
    "Dimensions",
    "DimensionsSpec",
    "MetaDataField",
    "ComponentSpec",
    # Structures
    "DataStructure",
    "Container",
    # Coordinates
    "Coordinate",
    "Attribute",
    # Creational
    "Factory",
    "Builder",
    # I/O
    "IOHandler",
    "FileExt",
    "Saver",
    "SaverPKL",
    "SaverNPY",
    "SaverNPZ",
    "SaverJSON",
    "SaverYAML",
    "SaverHDF5",
    "Loader",
    "LoaderPKL",
    "LoaderNPY",
    "LoaderNPZ",
    "LoaderJSON",
    "LoaderYAML",
    "LoaderHDF5",
]
