# Morpha Documentation

**Morpha** is a domain-agnostic data representation library for scientific computing.
It provides reusable patterns for structured arrays, typed containers, and I/O operations.

```{toctree}
:maxdepth: 2
:caption: "Contents:"

guide/quickstart
guide/concepts
api/index
```

```{toctree}
:maxdepth: 1
:caption: Architecture Decisions

adr/adr-template
```

## Features

- **DataComponent**: NumPy array subclass with dimension annotations and metadata propagation
- **DataStructure**: Abstract base for composite data structures with schema enforcement
- **Coordinates**: Labeled axes with attribute validation
- **Creational patterns**: Factory and Builder abstractions for object creation
- **I/O handlers**: Saver/Loader for PKL, NPY, NPZ, YAML, JSON, HDF5 formats
- **Typed containers**: Generic containers with runtime type checking

## Quick Example

```python
import numpy as np
from morpha.components import DataComponent, Dimensions

# Create array with named dimensions
data = DataComponent(
    np.random.randn(100, 50),
    dims=Dimensions("units", "time")
)

# Dimension-aware operations
print(data.get_axis("time"))  # 1
print(data.get_size("units"))  # 100

# Metadata propagates through operations
subset = data[:10, :25]
print(subset.dims)  # Dimensions['units', 'time']
```

# Indices and tables

* {ref}`genindex`
* {ref}`modindex`
* {ref}`search`
