<a id="components-module"></a>

# Components Module

Core data components with dimension annotations.

<a id="module-morpha.components.base"></a>

<a id="datacomponent"></a>

## DataComponent

Base data component class.

<a id="classes"></a>

### Classes

DataComponent
: NumPy ndarray subclass with dimension annotations and metadata propagation.

<a id="morpha.components.base.DataComponent"></a>

### *class* morpha.components.base.DataComponent(values, dims=None, \*\*metadata)

Bases: [`ndarray`](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray)

Core component of a data structure with dimension annotations and metadata.

Subclass of numpy.ndarray that adds:
- Named dimensions via the dims attribute
- Metadata fields defined by subclasses
- Automatic propagation of dimensions and metadata through array operations

* **Parameters:**
  * **values** (*ArrayLike*) – Values for the underlying array.
  * **dims** ([*Dimensions*](#morpha.components.dimensions.Dimensions) *,* *optional*) – Dimension names. If not provided, defaults are used.
  * **\*\*metadata** (*Any*) – Additional metadata attributes.
* **Class Attributes:**
  * **DIMENSIONS_SPEC** (*DimensionsSpec*) – Specification of allowed dimensions (names, order, required/optional).
    Define in subclasses.
  * **METADATA** (*Mapping[str, MetaDataField]*) – Metadata attributes with their types and defaults.
    Define in subclasses.
  * **DTYPE** (*np.dtype*) – Data type for array values.
    Define in subclasses.
  * **SENTINEL** (*int | float | str*) – Value marking missing/unset entries.
    Define in subclasses.
* **Return type:**
  [*Self*](https://docs.python.org/3/library/typing.html#typing.Self)

<a id="morpha.components.base.DataComponent.dims"></a>

#### dims

Names for each array dimension.

* **Type:**
  [Dimensions](#morpha.components.dimensions.Dimensions)

### Notes

Dimension propagation:
- Operations preserving dimensionality: dims transferred from parent
- Operations changing dimensionality: dims reset to defaults

Methods like transpose, swapaxes, moveaxis update dims accordingly.

### Examples

Create a DataComponent with dimension names:

```pycon
>>> data = DataComponent(np.zeros((10, 5)), dims=Dimensions("units", "time"))
>>> data.dims
Dimensions['units', 'time']
```

Get dimension information:

```pycon
>>> data.get_dim(0)
'units'
>>> data.get_axis("time")
1
>>> data.get_size("units")
10
```

<a id="morpha.components.base.DataComponent.DIMENSIONS_SPEC"></a>

#### DIMENSIONS_SPEC *: [DimensionsSpec](#morpha.components.dimensions.DimensionsSpec)*

<a id="id0"></a>

#### dims *: [Dimensions](#morpha.components.dimensions.Dimensions)*

<a id="morpha.components.base.DataComponent.METADATA"></a>

#### METADATA *: [Mapping](https://docs.python.org/3/library/typing.html#typing.Mapping)[[str](https://docs.python.org/3/library/stdtypes.html#str), [MetaDataField](#morpha.components.metadata.MetaDataField)]*

<a id="morpha.components.base.DataComponent.DTYPE"></a>

#### DTYPE *: [dtype](https://numpy.org/doc/stable/reference/generated/numpy.dtype.html#numpy.dtype)[[Any](https://docs.python.org/3/library/typing.html#typing.Any)]*

<a id="morpha.components.base.DataComponent.SENTINEL"></a>

#### SENTINEL *: [int](https://docs.python.org/3/library/functions.html#int) | [float](https://docs.python.org/3/library/functions.html#float) | [str](https://docs.python.org/3/library/stdtypes.html#str)*

<a id="morpha.components.base.DataComponent.validate"></a>

#### *classmethod* validate(values)

Validate input values before array creation.

Override in subclasses for specific validation.

* **Parameters:**
  **values** (*ArrayLike*) – Input values to validate.
* **Return type:**
  None

<a id="morpha.components.base.DataComponent.propagate_dimensions"></a>

#### *classmethod* propagate_dimensions(parent, child)

Propagate dimensions from parent to child array.

If dimensionality is preserved, transfers dims. Otherwise resets to defaults.

* **Parameters:**
  * **parent** (*np.ndarray*) – Source array.
  * **child** (*Self*) – Target array to update.
* **Return type:**
  None

<a id="morpha.components.base.DataComponent.propagate_metadata"></a>

#### *classmethod* propagate_metadata(parent, child)

Propagate metadata from parent to child array.

Transfers metadata attributes defined in METADATA from parent.

* **Parameters:**
  * **parent** (*np.ndarray*) – Source array.
  * **child** (*Self*) – Target array to update.
* **Return type:**
  None

<a id="morpha.components.base.DataComponent.wrap"></a>

#### wrap(obj)

Cast a numpy array to this DataComponent type.

* **Parameters:**
  **obj** (*np.ndarray*) – Array to cast.
* **Returns:**
  Array cast to current class.
* **Return type:**
  Self

<a id="morpha.components.base.DataComponent.from_shape"></a>

#### *classmethod* from_shape(shape, dims=None, \*\*metadata)

Create an empty instance filled with the sentinel value.

* **Parameters:**
  * **shape** ([*int*](https://docs.python.org/3/library/functions.html#int) *or* *Tuple* *[*[*int*](https://docs.python.org/3/library/functions.html#int) *,*  *...* *]*) – Shape of the array. Integer creates 1D array.
  * **dims** ([*Dimensions*](#morpha.components.dimensions.Dimensions) *,* *optional*) – Dimension names.
  * **\*\*metadata** (*Any*) – Additional metadata attributes.
* **Returns:**
  Instance filled with SENTINEL value.
* **Return type:**
  Self

<a id="morpha.components.base.DataComponent.get_dim"></a>

#### get_dim(axis)

Get dimension name by axis index.

* **Parameters:**
  **axis** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Axis index.
* **Returns:**
  Dimension name.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

<a id="morpha.components.base.DataComponent.get_axis"></a>

#### get_axis(dim)

Get axis index by dimension name.

* **Parameters:**
  **dim** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Dimension name.
* **Returns:**
  Axis index.
* **Return type:**
  [int](https://docs.python.org/3/library/functions.html#int)

<a id="morpha.components.base.DataComponent.get_size"></a>

#### get_size(dim)

Get the length of a dimension.

* **Parameters:**
  **dim** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Dimension name.
* **Returns:**
  Size along that dimension.
* **Return type:**
  [int](https://docs.python.org/3/library/functions.html#int)

<a id="morpha.components.base.DataComponent.get_missing"></a>

#### get_missing()

Get boolean mask for missing values (equal to SENTINEL).

* **Returns:**
  Boolean mask with True for missing values.
* **Return type:**
  np.ndarray

<a id="morpha.components.base.DataComponent.transpose"></a>

#### transpose(axes: [SupportsIndex](https://docs.python.org/3/library/typing.html#typing.SupportsIndex) | [Sequence](https://docs.python.org/3/library/typing.html#typing.Sequence)[[SupportsIndex](https://docs.python.org/3/library/typing.html#typing.SupportsIndex)] | [None](https://docs.python.org/3/library/constants.html#None), /) → [Self](https://docs.python.org/3/library/typing.html#typing.Self)

#### transpose(\*axes: [SupportsIndex](https://docs.python.org/3/library/typing.html#typing.SupportsIndex)) → [Self](https://docs.python.org/3/library/typing.html#typing.Self)

Transpose array and update dimension names.

* **Parameters:**
  **\*axes** (*SupportsIndex* *|* *Sequence* *[**SupportsIndex* *]*  *|* *None*) – New axis order. If empty, reverses axes.
* **Returns:**
  Transposed array with updated dims.
* **Return type:**
  Self

<a id="morpha.components.base.DataComponent.T"></a>

#### *property* T *: [Self](https://docs.python.org/3/library/typing.html#typing.Self)*

Return transposed array with updated dims.

* **Returns:**
  Transposed view.
* **Return type:**
  Self

<a id="morpha.components.base.DataComponent.swapaxes"></a>

#### swapaxes(axis1, axis2)

Swap two axes and update dimension names.

* **Parameters:**
  * **axis1** (*SupportsIndex*) – Axes to swap.
  * **axis2** (*SupportsIndex*) – Axes to swap.
* **Returns:**
  Array with swapped axes and updated dims.
* **Return type:**
  Self

<a id="morpha.components.base.DataComponent.moveaxis"></a>

#### moveaxis(source, destination)

Move an axis to a new position and update dimension names.

* **Parameters:**
  * **source** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Original axis position.
  * **destination** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Target axis position.
* **Returns:**
  Array with moved axis and updated dims.
* **Return type:**
  Self

<a id="morpha.components.base.DataComponent.rollaxis"></a>

#### rollaxis(axis, start=0)

Roll the specified axis to a given position.

Not implemented — requires manual dimension update.

* **Parameters:**
  * **axis** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Axis to roll.
  * **start** ([*int*](https://docs.python.org/3/library/functions.html#int) *,* *optional*) – Target position, by default 0.
* **Raises:**
  [**NotImplementedError**](https://docs.python.org/3/library/exceptions.html#NotImplementedError) – Always raised; update dimension names manually.
* **Return type:**
  [*Self*](https://docs.python.org/3/library/typing.html#typing.Self)

<a id="morpha.components.base.DataComponent.flip"></a>

#### flip(axis)

Reverse elements along the given axis.

Not implemented — requires manual dimension update.

* **Parameters:**
  **axis** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Axis to reverse.
* **Raises:**
  [**NotImplementedError**](https://docs.python.org/3/library/exceptions.html#NotImplementedError) – Always raised; update dimension names manually.
* **Return type:**
  [*Self*](https://docs.python.org/3/library/typing.html#typing.Self)

<a id="module-morpha.components.dimensions"></a>

<a id="dimensions"></a>

## Dimensions

Dimension management for data components.

### Classes

Dimensions
: Named dimension labels for array axes.

DimensionsSpec
: Specification for validating dimension names in data structures.

<a id="morpha.components.dimensions.Dimensions"></a>

### *class* morpha.components.dimensions.Dimensions(\*args)

Bases: [`UserList`](https://docs.python.org/3/library/collections.html#collections.UserList)[[`str`](https://docs.python.org/3/library/stdtypes.html#str)]

Dimension names to label the axes of a data component or data structure.

Provides utility methods to examine and manipulate dimensions, which can be
used by wrapper objects via delegation.

* **Parameters:**
  **\*args** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Names of the dimensions.
* **Class Attributes:**
  **DEFAULT** (*str*) – Default dimension name for unlabeled axes.

<a id="morpha.components.dimensions.Dimensions.data"></a>

#### data

Underlying list of dimension names (inherited from UserList).

* **Type:**
  [list](https://docs.python.org/3/library/stdtypes.html#list)[[str](https://docs.python.org/3/library/stdtypes.html#str)]

### Examples

Create dimension names:

```pycon
>>> dims = Dimensions("time", "trials", "units")
>>> dims.ndim
3
```

Get dimension by index:

```pycon
>>> dims.get_dim(0)
'time'
```

Get axis by name:

```pycon
>>> dims.get_axis("trials")
1
```

Check subset relationship:

```pycon
>>> partial = Dimensions("time", "trials")
>>> partial.is_subset(dims)
True
```

<a id="morpha.components.dimensions.Dimensions.DEFAULT"></a>

#### DEFAULT *: [str](https://docs.python.org/3/library/stdtypes.html#str)* *= ''*

<a id="morpha.components.dimensions.Dimensions.default"></a>

#### *classmethod* default(ndim)

Create default dimensions with empty names.

* **Parameters:**
  **ndim** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Number of dimensions.
* **Returns:**
  Dimensions with empty string names.
* **Return type:**
  Self

<a id="morpha.components.dimensions.Dimensions.ndim"></a>

#### *property* ndim *: [int](https://docs.python.org/3/library/functions.html#int)*

Return the number of dimensions.

* **Returns:**
  Number of dimensions.
* **Return type:**
  [int](https://docs.python.org/3/library/functions.html#int)

<a id="morpha.components.dimensions.Dimensions.get_dim"></a>

#### get_dim(axis)

Get dimension name by axis index.

* **Parameters:**
  **axis** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Index of the axis.
* **Returns:**
  Name of the dimension.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)
* **Raises:**
  [**IndexError**](https://docs.python.org/3/library/exceptions.html#IndexError) – If axis is out of bounds.

<a id="morpha.components.dimensions.Dimensions.get_axis"></a>

#### get_axis(name)

Get axis index by dimension name.

* **Parameters:**
  **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Name of the dimension.
* **Returns:**
  Axis number associated with the dimension.
* **Return type:**
  [int](https://docs.python.org/3/library/functions.html#int)
* **Raises:**
  [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError) – If the dimension name is not found.

<a id="morpha.components.dimensions.Dimensions.is_subset"></a>

#### is_subset(other)

Check if dimensions are a subset of another.

* **Parameters:**
  **other** ([*Dimensions*](#morpha.components.dimensions.Dimensions)) – Dimensions to compare against.
* **Returns:**
  True if all names are present in *other*.
* **Return type:**
  [bool](https://docs.python.org/3/library/functions.html#bool)

<a id="morpha.components.dimensions.Dimensions.is_ordered_as"></a>

#### is_ordered_as(other)

Check if common dimensions are in the same order.

Only considers dimensions present in both objects.

* **Parameters:**
  **other** ([*Dimensions*](#morpha.components.dimensions.Dimensions)) – Dimensions to compare against.
* **Returns:**
  True if common dimensions appear in the same relative order.
* **Return type:**
  [bool](https://docs.python.org/3/library/functions.html#bool)

<a id="morpha.components.dimensions.Dimensions.intersection"></a>

#### *classmethod* intersection(\*dims)

Get common dimensions between multiple Dimensions objects.

* **Parameters:**
  **\*dims** ([*Dimensions*](#morpha.components.dimensions.Dimensions)) – Two or more Dimensions objects to intersect.
* **Returns:**
  Dimensions present in all inputs.
* **Return type:**
  [Dimensions](#morpha.components.dimensions.Dimensions)

<a id="morpha.components.dimensions.Dimensions.add"></a>

#### add(name='', axis=-1)

Add a dimension at a specific position.

* **Parameters:**
  * **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* *optional*) – Name of the dimension.
  * **axis** ([*int*](https://docs.python.org/3/library/functions.html#int) *,* *optional*) – Index position, -1 for last position.
* **Raises:**
  * [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError) – If dimension name already exists (except for empty default names).
  * [**IndexError**](https://docs.python.org/3/library/exceptions.html#IndexError) – If axis is out of bounds.
* **Return type:**
  None

<a id="morpha.components.dimensions.Dimensions.transpose"></a>

#### transpose(axes=None)

Reorder dimensions.

* **Parameters:**
  **axes** (*Tuple* *[*[*int*](https://docs.python.org/3/library/functions.html#int) *,*  *...* *] or* [*list*](https://docs.python.org/3/library/stdtypes.html#list) *[*[*int*](https://docs.python.org/3/library/functions.html#int) *]* *,* *optional*) – New axis order. If None, reverses order.
* **Returns:**
  Reordered dimensions.
* **Return type:**
  Self

<a id="morpha.components.dimensions.Dimensions.swap"></a>

#### swap(axis1, axis2)

Swap two dimensions.

* **Parameters:**
  * **axis1** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Indices of dimensions to swap.
  * **axis2** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Indices of dimensions to swap.
* **Returns:**
  New instance with swapped dimensions.
* **Return type:**
  Self

<a id="morpha.components.dimensions.Dimensions.move"></a>

#### move(source, destination)

Move dimensions to new positions.

* **Parameters:**
  * **source** ([*int*](https://docs.python.org/3/library/functions.html#int) *|* [*list*](https://docs.python.org/3/library/stdtypes.html#list) *[*[*int*](https://docs.python.org/3/library/functions.html#int) *]*) – Indices of axes to move.
  * **destination** ([*int*](https://docs.python.org/3/library/functions.html#int) *|* [*list*](https://docs.python.org/3/library/stdtypes.html#list) *[*[*int*](https://docs.python.org/3/library/functions.html#int) *]*) – New positions for the axes.
* **Returns:**
  New instance with moved dimensions.
* **Return type:**
  Self

<a id="morpha.components.dimensions.DimensionsSpec"></a>

### *class* morpha.components.dimensions.DimensionsSpec(\*\*kwargs)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Specification for dimension names in a data structure.

Defines which dimensions are required vs optional, and their expected order.

* **Parameters:**
  **\*\*kwargs** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) – Dimension names as keys, with True for required and False for optional.

<a id="morpha.components.dimensions.DimensionsSpec.spec"></a>

#### spec

Ordered mapping of dimension names to required status.

* **Type:**
  OrderedDict[[str](https://docs.python.org/3/library/stdtypes.html#str), [bool](https://docs.python.org/3/library/functions.html#bool)]

### Examples

```pycon
>>> spec = DimensionsSpec(units=False, trials=True, time=False)
>>> spec.required()
Dimensions['trials']
>>> spec.optional()
Dimensions['units', 'time']
```

<a id="id1"></a>

#### *property* spec

Return read-only ordered mapping of dimension names to required status.

* **Returns:**
  Immutable view of the specification.
* **Return type:**
  MappingProxyType

<a id="morpha.components.dimensions.DimensionsSpec.required"></a>

#### required()

Get required dimensions.

* **Returns:**
  Dimensions marked as required.
* **Return type:**
  [Dimensions](#morpha.components.dimensions.Dimensions)

<a id="morpha.components.dimensions.DimensionsSpec.optional"></a>

#### optional()

Get optional dimensions.

* **Returns:**
  Dimensions marked as optional.
* **Return type:**
  [Dimensions](#morpha.components.dimensions.Dimensions)

<a id="morpha.components.dimensions.DimensionsSpec.validate"></a>

#### validate(dims)

Validate dimensions against the specification.

* **Parameters:**
  **dims** ([*Dimensions*](#morpha.components.dimensions.Dimensions)) – Dimensions to validate.
* **Raises:**
  [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError) – If required dimensions are missing, extra dimensions are present,
      or dimensions are in incorrect order.
* **Return type:**
  None

<a id="module-morpha.components.metadata"></a>

<a id="metadata"></a>

## Metadata

Metadata field specification for data components.

### Classes

MetaDataField
: Specification for a metadata attribute on a DataComponent.

<a id="morpha.components.metadata.MetaDataField"></a>

### *class* morpha.components.metadata.MetaDataField(field_type, default_value)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Metadata field specification for a data component.

Defines the expected type and default value for a metadata attribute
that can be attached to DataComponent subclasses.

* **Parameters:**
  * **field_type** ([*Type*](https://docs.python.org/3/library/typing.html#typing.Type) *[*[*Any*](https://docs.python.org/3/library/typing.html#typing.Any) *]*)
  * **default_value** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any))

<a id="morpha.components.metadata.MetaDataField.field_type"></a>

#### field_type

Expected type of the metadata field.

* **Type:**
  Type[Any]

<a id="morpha.components.metadata.MetaDataField.default_value"></a>

#### default_value

Default value for the field when not provided.

* **Type:**
  Any

### Examples

Define metadata fields for a custom DataComponent:

```pycon
>>> class TimeData(DataComponent):
...     METADATA = {
...         "origin": MetaDataField(str, None),
...         "time_unit": MetaDataField(str, "sec"),
...     }
```

<a id="id2"></a>

#### field_type *: [Type](https://docs.python.org/3/library/typing.html#typing.Type)[[Any](https://docs.python.org/3/library/typing.html#typing.Any)]*

<a id="id3"></a>

#### default_value *: [Any](https://docs.python.org/3/library/typing.html#typing.Any)*

<a id="module-morpha.components.specs"></a>

<a id="specs"></a>

## Specs

Component specification for data structures.

### Classes

ComponentSpec
: Specification of allowed data components in a data structure.

<a id="morpha.components.specs.ComponentSpec"></a>

### *class* morpha.components.specs.ComponentSpec(\*\*kwargs)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Specification of data components allowed in a data structure.

Validates that components assigned to a data structure have the correct
attribute names and types.

* **Parameters:**
  **\*\*kwargs** (*Type* *[*[*DataComponent*](#morpha.components.base.DataComponent) *]*) – Component names as keys and their expected types as values.

<a id="morpha.components.specs.ComponentSpec.spec"></a>

#### spec

Mapping of attribute names to expected component types.

* **Type:**
  Dict[[str](https://docs.python.org/3/library/stdtypes.html#str), Type[[DataComponent](#morpha.components.base.DataComponent)]]

### Examples

Define a specification:

```pycon
>>> spec = ComponentSpec(data=CoreData, time=CoordTime)
```

Validate a component:

```pycon
>>> data = CoreData(np.zeros(10))
>>> spec.validate("data", data)  # OK
```

```pycon
>>> spec.validate("data", time_coord)  # Raises TypeError
```

<a id="id4"></a>

#### *property* spec

Return read-only mapping of attribute names to expected component types.

* **Returns:**
  Immutable view of the specification.
* **Return type:**
  MappingProxyType

<a id="morpha.components.specs.ComponentSpec.validate"></a>

#### validate(name, component)

Validate a component against the specification.

* **Parameters:**
  * **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Attribute name for the component.
  * **component** ([*DataComponent*](#morpha.components.base.DataComponent)) – Component instance to validate.
* **Raises:**
  * [**AttributeError**](https://docs.python.org/3/library/exceptions.html#AttributeError) – If the name is not in the specification.
  * [**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError) – If the component type does not match the expected type.
* **Return type:**
  None

<a id="morpha.components.specs.ComponentSpec.keys"></a>

#### keys()

Return component names.

* **Returns:**
  View of component names.
* **Return type:**
  KeysView

<a id="morpha.components.specs.ComponentSpec.values"></a>

#### values()

Return expected component types.

* **Returns:**
  View of component types.
* **Return type:**
  ValuesView

<a id="morpha.components.specs.ComponentSpec.items"></a>

#### items()

Return (name, type) pairs.

* **Returns:**
  View of (name, type) pairs.
* **Return type:**
  ItemsView
