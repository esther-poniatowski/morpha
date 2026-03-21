# Quickstart

## Installation

```bash
pip install morpha
```

## DataComponent

Create arrays with named dimensions:

```python
import numpy as np
from morpha.components import DataComponent, Dimensions

# Create with dimension names
data = DataComponent(
    np.random.randn(100, 50),
    dims=Dimensions("units", "time")
)

# Query dimensions
print(data.get_dim(0))       # "units"
print(data.get_axis("time")) # 1
print(data.get_size("units")) # 100

# Dimensions propagate through operations
transposed = data.T
print(transposed.dims)  # Dimensions['time', 'units']
```

## DataStructure

Define structured data with schema enforcement:

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

## I/O Operations

Save and load data:

```python
from morpha.io import SaverNPZ, LoaderNPZ

# Save
saver = SaverNPZ("data.npz")
saver.save({"array1": data1, "array2": data2})

# Load
loader = LoaderNPZ("data.npz")
loaded = loader.load()
```
