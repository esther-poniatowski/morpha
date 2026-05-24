<a id="structures-module"></a>

# Structures Module

Abstract base classes for composite data structures.

<a id="module-morpha.structures.base"></a>

<a id="datastructure"></a>

## DataStructure

Base data structure class.

<a id="morpha.structures.base.AnyCoreData"></a>

### *class* morpha.structures.base.AnyCoreData

Type variable for the core data component stored in the data structure.

alias of TypeVar(‘AnyCoreData’, bound=[`DataComponent`](components.md#morpha.components.base.DataComponent))

<a id="morpha.structures.base.DataStructure"></a>

### *class* morpha.structures.base.DataStructure(data=None, \*\*coords)

Bases: [`ABC`](https://docs.python.org/3/library/abc.html#abc.ABC), [`Generic`](https://docs.python.org/3/library/typing.html#typing.Generic)[[`AnyCoreData`](#morpha.structures.base.AnyCoreData)]

Abstract base class for data structures with schema enforcement.

Provides a framework for building composite data structures that contain:
- A core data component (the main data array)
- Coordinate components (labeled axes)
- Dimension tracking
- Schema validation via class attributes

* **Parameters:**
  * **data** ([*AnyCoreData*](#morpha.structures.base.AnyCoreData) *,* *optional*) – Core data component.
  * **\*\*coords** ([*Coordinate*](coordinates.md#morpha.coordinates.base.Coordinate)) – Coordinate components keyed by attribute name.
* **Class Attributes:**
  * **DIMENSIONS_SPEC** (*DimensionsSpec*) – Specification of allowed dimensions (names, order, required/optional).
    Must be defined in subclasses.
  * **COMPONENTS_SPEC** (*ComponentSpec*) – Specification of allowed data components (names and types).
    Must be defined in subclasses.
  * **IDENTIFIERS** (*Mapping[str, MetaDataField]*) – Metadata attributes that uniquely identify instances.
    Must be defined in subclasses.
  * **REQUIRED_IN_SUBCLASSES** (*Tuple[str, …]*) – Class attributes that must be defined in each subclass.

<a id="morpha.structures.base.DataStructure.dims"></a>

#### dims

Active dimensions in this instance.

* **Type:**
  [Dimensions](components.md#morpha.components.dimensions.Dimensions)

<a id="morpha.structures.base.DataStructure.coords"></a>

#### coords

Names of active coordinates.

* **Type:**
  Set[[str](https://docs.python.org/3/library/stdtypes.html#str)]

### Notes

The \_\_init_subclass_\_ hook enforces that subclasses define required
class attributes, providing compile-time-like checks for schema compliance.

### Examples

Define a concrete data structure:

```pycon
>>> class TimeSeries(DataStructure[CoreData]):
...     DIMENSIONS_SPEC = DimensionsSpec(time=True, units=False)
...     COMPONENTS_SPEC = ComponentSpec(data=CoreData, time=CoordTime)
...     IDENTIFIERS = {"session": MetaDataField(str, None)}
```

Create an instance:

```pycon
>>> ts = TimeSeries(data=my_data, time=time_coord)
>>> ts.dims
Dimensions['time', 'units']
```

<a id="morpha.structures.base.DataStructure.DIMENSIONS_SPEC"></a>

#### DIMENSIONS_SPEC *: [DimensionsSpec](components.md#morpha.components.dimensions.DimensionsSpec)*

<a id="morpha.structures.base.DataStructure.COMPONENTS_SPEC"></a>

#### COMPONENTS_SPEC *: [ComponentSpec](components.md#morpha.components.specs.ComponentSpec)*

<a id="morpha.structures.base.DataStructure.IDENTIFIERS"></a>

#### IDENTIFIERS *: [Mapping](https://docs.python.org/3/library/typing.html#typing.Mapping)[[str](https://docs.python.org/3/library/stdtypes.html#str), [MetaDataField](components.md#morpha.components.metadata.MetaDataField)]*

<a id="morpha.structures.base.DataStructure.REQUIRED_IN_SUBCLASSES"></a>

#### REQUIRED_IN_SUBCLASSES *: [Tuple](https://docs.python.org/3/library/typing.html#typing.Tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ('DIMENSIONS_SPEC', 'COMPONENTS_SPEC', 'IDENTIFIERS')*

<a id="morpha.structures.base.DataStructure.__init__"></a>

#### \_\_init_\_(data=None, \*\*coords)

Initialize data structure with optional data and coordinates.

Components can be set at initialization or later via setter methods,
enabling lazy/incremental construction.

* **Parameters:**
  * **data** ([*AnyCoreData*](#morpha.structures.base.AnyCoreData) *|* *None*)
  * **coords** ([*Coordinate*](coordinates.md#morpha.coordinates.base.Coordinate) *|* *None*)
* **Return type:**
  None

<a id="morpha.structures.base.DataStructure.has_data"></a>

#### has_data()

Check if data has been set.

* **Returns:**
  True if data has been assigned.
* **Return type:**
  [bool](https://docs.python.org/3/library/functions.html#bool)

<a id="morpha.structures.base.DataStructure.data"></a>

#### *property* data *: [AnyCoreData](#morpha.structures.base.AnyCoreData)*

Core data component.

* **Returns:**
  The core data.
* **Return type:**
  [AnyCoreData](#morpha.structures.base.AnyCoreData)
* **Raises:**
  [**RuntimeError**](https://docs.python.org/3/library/exceptions.html#RuntimeError) – If data has not been set yet.

<a id="morpha.structures.base.DataStructure.get_data"></a>

#### get_data()

Get the core data.

* **Returns:**
  Core data component.
* **Return type:**
  [AnyCoreData](#morpha.structures.base.AnyCoreData)
* **Raises:**
  [**RuntimeError**](https://docs.python.org/3/library/exceptions.html#RuntimeError) – If data is not set.

<a id="morpha.structures.base.DataStructure.get_coord"></a>

#### get_coord(name)

Get a coordinate by name.

* **Parameters:**
  **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Coordinate attribute name.
* **Returns:**
  The coordinate component.
* **Return type:**
  [Coordinate](coordinates.md#morpha.coordinates.base.Coordinate)
* **Raises:**
  [**AttributeError**](https://docs.python.org/3/library/exceptions.html#AttributeError) – If coordinate is not active.

<a id="morpha.structures.base.DataStructure.get_coords_from_dim"></a>

#### get_coords_from_dim(dim)

Get all coordinates associated with a dimension.

* **Parameters:**
  **dim** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Dimension name.
* **Returns:**
  Coordinates whose dims include *dim*.
* **Return type:**
  Mapping[[str](https://docs.python.org/3/library/stdtypes.html#str), [Coordinate](coordinates.md#morpha.coordinates.base.Coordinate)]

<a id="morpha.structures.base.DataStructure.iter_coords"></a>

#### iter_coords()

Iterate over active coordinates.

* **Yields:**
  *Tuple[str, Coordinate]* – Name and coordinate instance.
* **Return type:**
  [*Generator*](https://docs.python.org/3/library/typing.html#typing.Generator)[[*Tuple*](https://docs.python.org/3/library/typing.html#typing.Tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Coordinate](coordinates.md#morpha.coordinates.base.Coordinate)], None, None]

<a id="morpha.structures.base.DataStructure.shape"></a>

#### *property* shape *: [Tuple](https://docs.python.org/3/library/typing.html#typing.Tuple)[[int](https://docs.python.org/3/library/functions.html#int), ...]*

Return the shape of the core data.

* **Returns:**
  Shape tuple.
* **Return type:**
  Tuple[[int](https://docs.python.org/3/library/functions.html#int), …]

<a id="morpha.structures.base.DataStructure.get_dim"></a>

#### get_dim(axis)

Get dimension name by axis index.

* **Parameters:**
  **axis** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Axis index.
* **Returns:**
  Dimension name.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

<a id="morpha.structures.base.DataStructure.get_axis"></a>

#### get_axis(name)

Get axis index by dimension name.

* **Parameters:**
  **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Dimension name.
* **Returns:**
  Axis index.
* **Return type:**
  [int](https://docs.python.org/3/library/functions.html#int)

<a id="morpha.structures.base.DataStructure.get_size"></a>

#### get_size(name)

Get size along a dimension.

* **Parameters:**
  **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Dimension name.
* **Returns:**
  Size along that dimension.
* **Return type:**
  [int](https://docs.python.org/3/library/functions.html#int)
* **Raises:**
  [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError) – If the dimension is not active or not found.

<a id="morpha.structures.base.DataStructure.identifiers"></a>

#### *property* identifiers *: [Set](https://docs.python.org/3/library/typing.html#typing.Set)[[str](https://docs.python.org/3/library/stdtypes.html#str)]*

Return names of identifier attributes.

* **Returns:**
  Identifier attribute names from IDENTIFIERS.
* **Return type:**
  Set[[str](https://docs.python.org/3/library/stdtypes.html#str)]

<a id="morpha.structures.base.DataStructure.ndim"></a>

#### *property* ndim *: [int](https://docs.python.org/3/library/functions.html#int)*

Return the number of dimensions of the core data.

* **Returns:**
  Dimensionality.
* **Return type:**
  [int](https://docs.python.org/3/library/functions.html#int)

<a id="morpha.structures.base.DataStructure.dtype"></a>

#### *property* dtype *: np.dtype[Any]*

Return the data type of the core data.

* **Returns:**
  NumPy data type.
* **Return type:**
  np.dtype[Any]

<a id="morpha.structures.base.DataStructure.size"></a>

#### *property* size *: [int](https://docs.python.org/3/library/functions.html#int)*

Return the total number of elements in the core data.

* **Returns:**
  Total element count.
* **Return type:**
  [int](https://docs.python.org/3/library/functions.html#int)

<a id="morpha.structures.base.DataStructure.set_data"></a>

#### set_data(data)

Set the core data after validation.

* **Parameters:**
  **data** ([*AnyCoreData*](#morpha.structures.base.AnyCoreData)) – Core data component.
* **Raises:**
  * [**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError) – If data type doesn’t match COMPONENTS_SPEC.
  * [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError) – If dimensions don’t match DIMENSIONS_SPEC or shape is inconsistent.
* **Return type:**
  None

<a id="morpha.structures.base.DataStructure.set_coord"></a>

#### set_coord(name, coord)

Set a coordinate after validation.

* **Parameters:**
  * **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Attribute name for the coordinate.
  * **coord** ([*Coordinate*](coordinates.md#morpha.coordinates.base.Coordinate)) – Coordinate component.
* **Raises:**
  * [**AttributeError**](https://docs.python.org/3/library/exceptions.html#AttributeError) – If name is not in COMPONENTS_SPEC.
  * [**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError) – If coord type doesn’t match expected type.
  * [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError) – If dimensions or shape are inconsistent.
* **Return type:**
  None

<a id="morpha.structures.base.DataStructure.register_coord"></a>

#### register_coord(name)

Register an active coordinate.

* **Parameters:**
  **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Coordinate attribute name.
* **Return type:**
  None

<a id="morpha.structures.base.DataStructure.register_dimensions"></a>

#### register_dimensions(dims)

Register new dimensions.

* **Parameters:**
  **dims** ([*Dimensions*](components.md#morpha.components.dimensions.Dimensions)) – Dimensions to add if not already present.
* **Return type:**
  None

<a id="morpha.structures.base.DataStructure.validate_shape"></a>

#### validate_shape(component)

Validate component shape against existing components.

Ensures sizes match along common dimensions.

* **Parameters:**
  **component** ([*DataComponent*](components.md#morpha.components.base.DataComponent)) – New component to validate.
* **Raises:**
  [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError) – If sizes don’t match along common dimensions.
* **Return type:**
  None

<a id="morpha.structures.base.DataStructure.copy"></a>

#### copy()

Create a deep copy.

* **Returns:**
  Independent copy of this data structure.
* **Return type:**
  Self

<a id="morpha.structures.base.DataStructure.sel"></a>

#### sel(\*\*kwargs)

Select data along coordinates.

* **Parameters:**
  **\*\*kwargs** (*Any*) – Coordinate names and selection criteria (value, list, or slice).
* **Returns:**
  New structure with selected data.
* **Return type:**
  Self
* **Raises:**
  [**NotImplementedError**](https://docs.python.org/3/library/exceptions.html#NotImplementedError) – Always raised; selection is not yet available.

<a id="module-morpha.structures.containers"></a>

<a id="containers"></a>

## Containers

Generic typed container.

<a id="morpha.structures.containers.K"></a>

### *class* morpha.structures.containers.K

Type variable for container keys.

alias of TypeVar(‘K’)

<a id="morpha.structures.containers.V"></a>

### *class* morpha.structures.containers.V

Type variable for container values.

alias of TypeVar(‘V’)

<a id="morpha.structures.containers.Q"></a>

### *class* morpha.structures.containers.Q

Type variable for input dictionary keys.

alias of TypeVar(‘Q’)

<a id="morpha.structures.containers.R"></a>

### *class* morpha.structures.containers.R

Type variable for function return types.

alias of TypeVar(‘R’)

<a id="morpha.structures.containers.C"></a>

### *class* morpha.structures.containers.C

Type variable for Container subclasses.

alias of TypeVar(‘C’, bound=[`Container`](#morpha.structures.containers.Container))

<a id="morpha.structures.containers.Container"></a>

### *class* morpha.structures.containers.Container(\*args, key_type=None, value_type=None, \*\*kwargs)

Bases: [`UserDict`](https://docs.python.org/3/library/collections.html#collections.UserDict)[[`K`](#morpha.structures.containers.K), [`V`](#morpha.structures.containers.V)], [`Generic`](https://docs.python.org/3/library/typing.html#typing.Generic)[[`K`](#morpha.structures.containers.K), [`V`](#morpha.structures.containers.V)]

Type-checked dictionary container with utility methods.

Extends UserDict with type validation and functional operations.

* **Parameters:**
  * **\*args** (*Any*) – Arguments passed to UserDict.
  * **key_type** (*Type* *[*[*K*](#morpha.structures.containers.K) *]*) – Expected type for keys.
  * **value_type** (*Type* *[*[*V*](#morpha.structures.containers.V) *]*) – Expected type for values.
  * **\*\*kwargs** (*Any*) – Keyword arguments passed to UserDict.

<a id="morpha.structures.containers.Container.key_type"></a>

#### key_type

Type constraint for keys.

* **Type:**
  Type[[K](#morpha.structures.containers.K)]

<a id="morpha.structures.containers.Container.value_type"></a>

#### value_type

Type constraint for values.

* **Type:**
  Type[[V](#morpha.structures.containers.V)]

### Examples

Create a container with type constraints:

```pycon
>>> container = Container({1: "a", 2: "b"}, key_type=int, value_type=str)
>>> container[1]
'a'
```

Type validation on assignment:

```pycon
>>> container[3] = 123  # Raises TypeError - expected str value
```

<a id="morpha.structures.containers.Container.from_keys"></a>

#### *classmethod* from_keys(keys, fill_value, \*, key_type=None, value_type=None)

Create container from keys with a fill value.

* **Parameters:**
  * **keys** (*Iterable* *[*[*K*](#morpha.structures.containers.K) *]*) – Keys to initialize.
  * **fill_value** ([*V*](#morpha.structures.containers.V)) – Default value for all keys.
  * **key_type** (*Type* *[*[*K*](#morpha.structures.containers.K) *]*) – Expected type for keys.
  * **value_type** (*Type* *[*[*V*](#morpha.structures.containers.V) *]*) – Expected type for values.
* **Returns:**
  New container with specified keys and fill value.
* **Return type:**
  [C](#morpha.structures.containers.C)

<a id="morpha.structures.containers.Container.list_keys"></a>

#### list_keys()

Get list of keys.

* **Returns:**
  Keys in insertion order.
* **Return type:**
  List[[K](#morpha.structures.containers.K)]

<a id="morpha.structures.containers.Container.list_values"></a>

#### list_values(keys=None)

Get list of values, optionally for specific keys.

* **Parameters:**
  **keys** (*Iterable* *[*[*K*](#morpha.structures.containers.K) *]* *,* *optional*) – Keys to get values for. If None, returns all values.
* **Returns:**
  List of values.
* **Return type:**
  List[[V](#morpha.structures.containers.V)]

<a id="morpha.structures.containers.Container.to_dict"></a>

#### to_dict()

Convert to plain dictionary.

* **Returns:**
  Shallow copy of the underlying data.
* **Return type:**
  Dict[[K](#morpha.structures.containers.K), [V](#morpha.structures.containers.V)]

<a id="morpha.structures.containers.Container.get_subset"></a>

#### get_subset(keys)

Get a subset by keys.

* **Parameters:**
  **keys** (*Iterable* *[*[*K*](#morpha.structures.containers.K) *]*) – Keys to include.
* **Returns:**
  New container with subset of data.
* **Return type:**
  Self

<a id="morpha.structures.containers.Container.filter_on_keys"></a>

#### filter_on_keys(predicate)

Filter by key predicate.

* **Parameters:**
  **predicate** (*Callable* *[* *[*[*K*](#morpha.structures.containers.K) *]* *,* [*bool*](https://docs.python.org/3/library/functions.html#bool) *]*) – Function returning True for keys to keep.
* **Returns:**
  Filtered container.
* **Return type:**
  Self

<a id="morpha.structures.containers.Container.filter_on_values"></a>

#### filter_on_values(predicate)

Filter by value predicate.

* **Parameters:**
  **predicate** (*Callable* *[* *[*[*V*](#morpha.structures.containers.V) *]* *,* [*bool*](https://docs.python.org/3/library/functions.html#bool) *]*) – Function returning True for values to keep.
* **Returns:**
  Filtered container.
* **Return type:**
  Self

<a id="morpha.structures.containers.Container.fill"></a>

#### fill(func, \*\*kwargs)

Generate values from keys using a function.

* **Parameters:**
  * **func** (*Callable* *[* *[*[*K*](#morpha.structures.containers.K) *]* *,* [*V*](#morpha.structures.containers.V) *]*) – Function taking key and returning value.
  * **\*\*kwargs** (*Any*) – Additional arguments for func.
* **Return type:**
  None

<a id="morpha.structures.containers.Container.apply"></a>

#### apply(func, \*\*kwargs)

Apply function to all values.

* **Parameters:**
  * **func** (*Callable* *[* *[*[*V*](#morpha.structures.containers.V) *]* *,* [*R*](#morpha.structures.containers.R) *]*) – Function to apply.
  * **\*\*kwargs** (*Any*) – Additional arguments for func.
* **Returns:**
  New container with transformed values.
* **Return type:**
  [Container](#morpha.structures.containers.Container)[[K](#morpha.structures.containers.K), [R](#morpha.structures.containers.R)]

<a id="morpha.structures.containers.Container.find_types"></a>

#### *static* find_types(data)

Determine types from dictionary contents.

* **Parameters:**
  **data** (*Dict* *[*[*Q*](#morpha.structures.containers.Q) *,* [*R*](#morpha.structures.containers.R) *]*) – Dictionary to analyze.
* **Returns:**
  Key and value types.
* **Return type:**
  Tuple[Type[[Q](#morpha.structures.containers.Q)], Type[[R](#morpha.structures.containers.R)]]
* **Raises:**
  [**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError) – If data is empty.
