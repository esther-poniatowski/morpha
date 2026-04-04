# Usage

## Creating Dimension-Aware Arrays

`DataComponent` extends `numpy.ndarray` with named dimensions that propagate
through operations.

```python
import numpy as np
from morpha import DataComponent, Dimensions

data = DataComponent(
    np.random.randn(100, 50),
    dims=Dimensions("units", "time"),
)

data.get_dim(0)        # "units"
data.get_axis("time")  # 1
data.get_size("units") # 100
```

Dimensions propagate through transpose, swapaxes, and moveaxis:

```python
transposed = data.T
transposed.dims  # Dimensions['time', 'units']

swapped = data.swapaxes(0, 1)
swapped.dims  # Dimensions['time', 'units']

moved = data.moveaxis(1, 0)
moved.dims  # Dimensions['time', 'units']
```

### Allocating Empty Arrays with `from_shape`

Subclasses that define `DTYPE` and `SENTINEL` can allocate sentinel-filled
arrays without providing values upfront:

```python
class SpikeData(DataComponent):
    DTYPE = np.float64
    SENTINEL = np.nan

empty = SpikeData.from_shape((100, 50), dims=Dimensions("units", "time"))
```

Each element in `empty` equals `np.nan`. The `get_missing()` method returns a
boolean mask over sentinel values:

```python
mask = empty.get_missing()  # all True
```

## Specifying Dimensions and Components

`DimensionsSpec` declares which dimension names a structure requires or permits.
Pass dimension names as keyword arguments: `True` marks required, `False` marks
optional.

```python
from morpha import DimensionsSpec

spec = DimensionsSpec(units=True, time=True, trials=False)
spec.required()  # Dimensions['units', 'time']
spec.optional()  # Dimensions['trials']
```

`DimensionsSpec.validate()` checks that a `Dimensions` object satisfies the
spec (no missing required dimensions, no extra dimensions, correct order).

`ComponentSpec` declares the allowed named components and their expected types:

```python
from morpha import ComponentSpec

spec = ComponentSpec(data=SpikeData, time=CoordTime)
spec.validate("data", spike_instance)  # passes or raises TypeError
```

## Attaching Metadata to Components

`MetaDataField` defines typed metadata attributes on `DataComponent` subclasses.
Each field specifies a type and a default value:

```python
from morpha import MetaDataField

class AnnotatedSpikes(DataComponent):
    DTYPE = np.float64
    SENTINEL = np.nan
    METADATA = {
        "origin": MetaDataField(str, None),
        "time_unit": MetaDataField(str, "sec"),
    }

spikes = AnnotatedSpikes(
    np.zeros((10, 5)),
    dims=Dimensions("units", "time"),
    origin="electrode_array",
)
spikes.origin     # "electrode_array"
spikes.time_unit  # "sec" (default)
```

Metadata propagates automatically through array operations.

## Defining Data Structures

`DataStructure` enforces schemas on composite data objects. Subclasses must
define three class attributes: `DIMENSIONS_SPEC`, `COMPONENTS_SPEC`, and
`IDENTIFIERS`.

```python
from morpha import DataStructure, DimensionsSpec, ComponentSpec, MetaDataField

class NeuralData(DataStructure[SpikeData]):
    DIMENSIONS_SPEC = DimensionsSpec(units=True, time=True, trials=False)
    COMPONENTS_SPEC = ComponentSpec(data=SpikeData, time=CoordTime)
    IDENTIFIERS = {
        "session_id": MetaDataField(str, None),
        "subject_id": MetaDataField(str, None),
    }
```

`IDENTIFIERS` maps identifier names to `MetaDataField` instances, not to bare
strings.

### Setting Data and Coordinates

`DataStructure` supports incremental construction. Pass components at init or
add them later with `set_data()` and `set_coord()`:

```python
nd = NeuralData()

spike_array = SpikeData(
    np.random.randn(100, 50),
    dims=Dimensions("units", "time"),
)
nd.set_data(spike_array)

time_coord = CoordTime(np.linspace(0, 1, 50))
nd.set_coord("time", time_coord)
```

Both setters validate types against `COMPONENTS_SPEC`, dimensions against
`DIMENSIONS_SPEC`, and shape consistency across all registered components.

### Querying a Data Structure

```python
nd.data            # core data array (raises RuntimeError if unset)
nd.has_data()      # True
nd.get_coord("time")
nd.dims            # aggregated Dimensions from all registered components
nd.shape           # shape of the core data
nd.get_size("units")
```

## Labeling Axes with Coordinates

`Coordinate` is a `DataComponent` subclass representing a single labeled axis.
Each `Coordinate` subclass declares an `ATTRIBUTE` type that validates its
values.

```python
from morpha import Coordinate, Attribute, DimensionsSpec

class Task(str, Attribute[str]):
    OPTIONS = frozenset({"PTD", "CLK"})
    LABELS = {"PTD": "Pursuit Tracking", "CLK": "Clock Task"}

    def __new__(cls, value: str):
        if not cls.is_valid(value):
            raise ValueError(f"Invalid task: {value}")
        return super().__new__(cls, value)

class CoordTask(Coordinate[Task]):
    ATTRIBUTE = Task
    DIMENSIONS_SPEC = DimensionsSpec(trials=True)

coord = CoordTask(["PTD", "PTD", "CLK"], dims=Dimensions("trials"))
```

`Attribute` is a mixin that pairs with a built-in type (`int`, `str`, `float`,
`bool`) via multiple inheritance. Subclasses define `OPTIONS` (valid values) and
`LABELS` (human-readable names):

```python
Task.is_valid("PTD")      # True
Task("PTD").full_label    # "Pursuit Tracking"
Task.get_options()        # frozenset({"PTD", "CLK"})
```

## Using Typed Containers

`Container` extends `UserDict` with type checking on keys and values:

```python
from morpha import Container

c = Container({"spike_rates": data_a, "lfp": data_b}, key_type=str, value_type=DataComponent)
c["spike_rates"]  # data_a
```

Assigning a value of the wrong type raises `TypeError`.

`Container` provides functional operations:

```python
subset = c.get_subset(["spike_rates"])
filtered = c.filter_on_keys(lambda k: k.startswith("spike"))
transformed = c.apply(lambda v: v.mean(axis=0))
```

`Container.from_keys` initializes a container from an iterable of keys with a
fill value:

```python
c = Container.from_keys(["a", "b"], fill_value=0.0, key_type=str, value_type=float)
```

## Building Data Structures (Creational Patterns)

### Factory

`Factory` is an abstract base class for creating `DataComponent` instances.
Subclasses define `PRODUCT_CLASSES` and implement `create()`:

```python
from morpha import Factory

class TimeCoordFactory(Factory[CoordTime]):
    PRODUCT_CLASSES = CoordTime

    def create(self, timestamps: np.ndarray, unit: str) -> CoordTime:
        return CoordTime(timestamps, time_unit=unit)

factory = TimeCoordFactory()
coord = factory.create(np.arange(100), unit="ms")
```

### Builder

`Builder` is an abstract base class for step-by-step construction of
`DataStructure` objects. Subclasses define `PRODUCT_CLASS`, `TMP_DATA`, and
implement `build()`:

```python
from morpha import Builder

class NeuralDataBuilder(Builder[NeuralData]):
    PRODUCT_CLASS = NeuralData
    TMP_DATA = ("raw_data", "timestamps")

    def build(self, raw: np.ndarray, times: np.ndarray) -> NeuralData:
        self.product = NeuralData()
        data = SpikeData(raw, dims=Dimensions("units", "time"))
        self.product.set_data(data)
        coord = CoordTime(times, dims=Dimensions("time"))
        self.product.set_coord("time", coord)
        return self.get_product()

builder = NeuralDataBuilder()
result = builder.build(raw_data, timestamps)
```

`get_product()` returns the finished structure and resets the builder for reuse.

Neither `Factory` nor `Builder` can be instantiated directly -- both require
concrete subclasses.

## Saving and Loading Data

Morpha pairs each file format with a `Saver` and `Loader` class. All savers and
loaders accept a path (string or `Path`) and append the correct extension
automatically.

| Format           | Saver       | Loader       | Extensions       |
| ---------------- | ----------- | ------------ | ---------------- |
| Pickle           | `SaverPKL`  | `LoaderPKL`  | `.pkl`           |
| NumPy            | `SaverNPY`  | `LoaderNPY`  | `.npy`           |
| NumPy compressed | `SaverNPZ`  | `LoaderNPZ`  | `.npz`           |
| JSON             | `SaverJSON` | `LoaderJSON` | `.json`          |
| YAML             | `SaverYAML` | `LoaderYAML` | `.yaml`, `.yml`  |
| HDF5             | `SaverHDF5` | `LoaderHDF5` | `.hdf5`, `.h5`   |

```python
from morpha import SaverNPZ, LoaderNPZ

saver = SaverNPZ("output/data")
saver.save({"spikes": spike_array, "rates": rate_array})

loader = LoaderNPZ("output/data.npz")
loaded = loader.load()  # dict of arrays
```

`SaverNPZ` accepts a single array or a `dict` of arrays. `SaverHDF5` and
`LoaderHDF5` require the `h5py` package; a `RuntimeError` signals when the
dependency is missing.

### File Extension Validation

`FileExt` validates and normalizes file extensions:

```python
from morpha import FileExt

ext = FileExt("pkl")   # ".pkl"
ext = FileExt(".npz")  # ".npz"
FileExt("xyz")         # raises ValueError
```

`IOHandler.enforce_ext` forces a specific extension onto a path:

```python
from morpha import IOHandler

path = IOHandler.enforce_ext("data/file", "npz")  # Path('data/file.npz')
```

## Next Steps

- [Concepts](concepts.md) -- Core abstractions and design principles.
- [API Reference](../api/index.md) -- Full Python API documentation.
