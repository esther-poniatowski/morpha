# Usage

Morpha provides foundational data structures for scientific computing:
dimension-aware arrays, structured containers, coordinate systems, and
multi-format I/O. Each abstraction addresses a specific need in data
representation workflows.

## Creating Dimension-Aware Arrays

`DataComponent` extends NumPy arrays with named dimensions that propagate
through operations:

```python
import numpy as np
from morpha.components import DataComponent, Dimensions

data = DataComponent(
    np.random.randn(100, 50),
    dims=Dimensions("units", "time")
)

# Query dimensions by index or name
print(data.get_dim(0))        # "units"
print(data.get_axis("time"))  # 1
print(data.get_size("units")) # 100

# Dimensions propagate through operations
transposed = data.T
print(transposed.dims)  # Dimensions['time', 'units']
```

## Defining Structured Data Containers

`DataStructure` enforces schemas on composite data objects:

```python
from morpha.structures import DataStructure
from morpha.components import DimensionsSpec, ComponentSpec

class NeuralData(DataStructure):
    DIMENSIONS_SPEC = DimensionsSpec(
        required=["units", "time"],
        optional=["trials"]
    )
    COMPONENTS_SPEC = ComponentSpec(
        spikes=DataComponent,
        rates=DataComponent,
    )
    IDENTIFIERS = ["session_id", "subject_id"]
```

The class-level specifications enforce dimension requirements and component
types at construction time, catching structural errors before they propagate
through an analysis pipeline.

## Working with Coordinates

`Coordinates` label axes with validated attributes:

```python
from morpha.coordinates import Coordinates

coords = Coordinates(
    units=np.arange(100),
    time=np.linspace(0, 1, 50)
)
```

## Saving and Loading Data

Morpha provides Saver/Loader patterns for multiple file formats:

```python
from morpha.io import SaverNPZ, LoaderNPZ

# Save arrays to compressed NumPy format
saver = SaverNPZ("data.npz")
saver.save({"spikes": spike_data, "rates": rate_data})

# Load back
loader = LoaderNPZ("data.npz")
loaded = loader.load()
```

Supported formats include PKL, NPY, NPZ, JSON, YAML, and HDF5. Each
format has a dedicated Saver/Loader pair with a consistent interface.

## Using Creational Patterns

Factory and Builder abstractions standardize object construction across
projects:

```python
from morpha.creational import Builder

builder = Builder(NeuralData)
builder.set("spikes", spike_array)
builder.set("rates", rate_array)
data = builder.build()
```

## Next Steps

- [Concepts](concepts.md) — Core abstractions and design principles.
- [API Reference](../api/index.md) — Python API documentation.
