# Morpha

[![Conda](https://img.shields.io/badge/conda-eresthanaconda--channel-blue)](#installation)
[![Maintenance](https://img.shields.io/maintenance/yes/2026)]()
[![Last Commit](https://img.shields.io/github/last-commit/esther-poniatowski/morpha)](https://github.com/esther-poniatowski/morpha/commits/main)
[![Python](https://img.shields.io/badge/python-%3E%3D3.12-blue)](https://www.python.org/)
[![License: GPL](https://img.shields.io/badge/License-GPL-yellow.svg)](https://opensource.org/licenses/GPL-3.0)

Provides reusable data structures for scientific computing in Python.

## Overview

Morpha provides foundational abstractions for building structured data representations in Python. Morpha extracts and generalizes patterns from data analysis projects across specific domains into reusable components.

## Features

- **DataComponent**: NumPy array subclasses with dimension annotations and metadata propagation
- **DataStructure**: Abstract base classes for composite data structures with schema enforcement
- **Coordinates**: Labeled axes with attribute validation
- **Creational Patterns**: Factory and Builder patterns for constructing data objects
- **I/O**: Saver/Loader patterns for multiple file formats (PKL, NPY, NPZ, JSON, YAML)

## Installation

```bash
pip install -e .
```

For development:

```bash
pip install -e ".[dev]"
```

## Quick Start

```python
import numpy as np
from morpha import DataComponent, Dimensions, DimensionsSpec

# Define a custom data component
class NeuralData(DataComponent):
    DIMENSIONS_SPEC = DimensionsSpec(time=True, units=False)
    DTYPE = np.float64
    SENTINEL = np.nan

# Create an instance with dimension labels
data = NeuralData(np.random.randn(100, 50), dims=Dimensions("time", "units"))

# Access dimension information
print(data.get_dim(0))      # 'time'
print(data.get_axis("units"))  # 1
print(data.get_size("time"))   # 100

# Dimensions propagate through operations
transposed = data.T
print(transposed.dims)  # Dimensions['units', 'time']
```

## CLI

```bash
# Display package info
morpha info

# Display version
morpha version
```

## Modules

| Module | Description |
|--------|-------------|
| `components` | NumPy array subclasses with dimensions and metadata |
| `structures` | Abstract base classes for composite data structures |
| `coordinates` | Labeled axes with attribute validation |
| `creational` | Factory and Builder patterns |
| `io` | Saver/Loader for multiple file formats |

## License

GPL-3.0-or-later
