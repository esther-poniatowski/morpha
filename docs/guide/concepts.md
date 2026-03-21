# Concepts

## DataComponent

`DataComponent` is a NumPy ndarray subclass that adds:

- **Dimension names**: Each axis has a string label
- **Metadata propagation**: Custom attributes survive array operations
- **Type enforcement**: Optional dtype constraints

Dimensions are automatically updated through operations like `transpose()`,
`swapaxes()`, and `moveaxis()`.

## Dimensions and DimensionsSpec

`Dimensions` stores ordered dimension names:

```python
dims = Dimensions("units", "time", "trials")
dims.get_axis("time")  # 1
dims.get_dim(0)        # "units"
```

`DimensionsSpec` validates dimensions against requirements:

```python
spec = DimensionsSpec(
    required=["units", "time"],
    optional=["trials"]
)
spec.validate(dims)  # Passes
```

## DataStructure

`DataStructure` is an abstract base class for composite data:

- **Schema enforcement**: `__init_subclass__` validates class definitions
- **Component management**: Type-checked data components
- **Coordinate handling**: Labeled axes with validation

Subclasses must define:

- `DIMENSIONS_SPEC`: Required and optional dimensions
- `COMPONENTS_SPEC`: Named components with types
- `IDENTIFIERS`: Required metadata keys

## Container

`Container[K, V]` is a typed dictionary with runtime checking:

```python
from morpha.structures import Container

class StringIntContainer(Container[str, int]):
    pass

c = StringIntContainer()
c["key"] = 42      # OK
c["key"] = "str"   # Raises TypeError
```

## Creational Patterns

**Factory**: Creates families of related objects

```python
from morpha.creational import Factory

class DataFactory(Factory[DataComponent]):
    def create(self, name: str) -> DataComponent:
        ...
```

**Builder**: Constructs complex objects step-by-step

```python
from morpha.creational import Builder

class DataBuilder(Builder[DataStructure]):
    def set_dimensions(self, dims): ...
    def add_component(self, name, data): ...
    def build(self) -> DataStructure: ...
```

## I/O Handlers

Saver/Loader pairs handle serialization:

- `SaverPKL` / `LoaderPKL`: Python pickle
- `SaverNPY` / `LoaderNPY`: Single NumPy array
- `SaverNPZ` / `LoaderNPZ`: Multiple arrays (compressed)
- `SaverYAML` / `LoaderYAML`: YAML configuration
- `SaverJSON` / `LoaderJSON`: JSON data
- `SaverHDF5` / `LoaderHDF5`: HDF5 hierarchical data
