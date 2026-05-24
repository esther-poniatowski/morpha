<a id="coordinates-module"></a>

# Coordinates Module

Labeled axes with attribute validation.

<a id="module-morpha.coordinates.base"></a>

<a id="coordinate-base"></a>

## Coordinate Base

Base coordinate class.

<a id="classes"></a>

### Classes

Coordinate
: DataComponent subclass representing labeled axes.

<a id="morpha.coordinates.base.AnyAttribute"></a>

### *class* morpha.coordinates.base.AnyAttribute

Type variable for the attribute type associated with coordinate labels.

alias of TypeVar(‘AnyAttribute’, bound=[`Attribute`](#morpha.coordinates.attributes.Attribute)[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any)])

<a id="morpha.coordinates.base.Coordinate"></a>

### *class* morpha.coordinates.base.Coordinate(values, dims=None, \*\*metadata)

Bases: [`DataComponent`](components.md#morpha.components.base.DataComponent), [`Generic`](https://docs.python.org/3/library/typing.html#typing.Generic)[[`AnyAttribute`](#morpha.coordinates.base.AnyAttribute)]

Base class for coordinates representing labeled axes.

A Coordinate is a DataComponent that holds axis labels, with validation
based on an associated Attribute type.

* **Class Attributes:**
  **ATTRIBUTE** (*Type[Attribute]*) – Attribute type for valid coordinate values.
  Determines data type and valid values for the array.
* **Parameters:**
  * **values** (*ArrayLike*)
  * **dims** ([*Dimensions*](components.md#morpha.components.dimensions.Dimensions))
  * **metadata** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any))
* **Return type:**
  [*Self*](https://docs.python.org/3/library/typing.html#typing.Self)

<a id="morpha.coordinates.base.Coordinate.ATTRIBUTE"></a>

#### ATTRIBUTE

Attribute type for valid coordinate values (set on subclasses).

* **Type:**
  Type[[AnyAttribute](#morpha.coordinates.base.AnyAttribute)]

### Notes

The validate method checks that all values are valid for the
associated ATTRIBUTE type using Attribute.is_valid.

> **See also**
>
> `DataComponent`
> : Base class.
>
> `Attribute`
> : Mixin for coordinate value types.

### Examples

Define a coordinate class:

```pycon
>>> class CoordTask(Coordinate[Task]):
...     ATTRIBUTE = Task
...     DIMENSIONS_SPEC = DimensionsSpec(trials=True)
```

Create coordinate instances:

```pycon
>>> coord = CoordTask(["PTD", "PTD", "CLK"])
>>> coord.get_attribute()
<class 'Task'>
```

<a id="id0"></a>

#### ATTRIBUTE *: [Type](https://docs.python.org/3/library/typing.html#typing.Type)[[AnyAttribute](#morpha.coordinates.base.AnyAttribute)]*

<a id="morpha.coordinates.base.Coordinate.validate"></a>

#### *classmethod* validate(values, \*\*kwargs)

Validate coordinate values against the attribute type.

* **Parameters:**
  * **values** (*ArrayLike*) – Values to validate.
  * **\*\*kwargs** (*Any*) – Additional validation arguments.
* **Raises:**
  [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError) – If any value is not valid for the ATTRIBUTE type.
* **Return type:**
  None

#### NOTE
Override in subclasses for custom validation logic.
The default implementation uses ATTRIBUTE.is_valid for validation.

<a id="morpha.coordinates.base.Coordinate.get_attribute"></a>

#### *classmethod* get_attribute()

Get the associated attribute type.

* **Returns:**
  The ATTRIBUTE class.
* **Return type:**
  Type[[AnyAttribute](#morpha.coordinates.base.AnyAttribute)]

<a id="morpha.coordinates.base.Coordinate.has_attribute"></a>

#### *classmethod* has_attribute(attribute_type)

Check if coordinate is associated with an attribute type.

* **Parameters:**
  **attribute_type** (*Type* *[*[*Attribute*](#morpha.coordinates.attributes.Attribute) *[**Any* *]* *]*) – Attribute type to check for.
* **Returns:**
  True if ATTRIBUTE is the same type or a subclass.
* **Return type:**
  [bool](https://docs.python.org/3/library/functions.html#bool)

<a id="morpha.coordinates.base.Coordinate.are_valid"></a>

#### *classmethod* are_valid(values)

Get boolean mask of valid values.

* **Parameters:**
  **values** (*ArrayLike*) – Values to check.
* **Returns:**
  Boolean array with True for valid values.
* **Return type:**
  np.ndarray

<a id="module-morpha.coordinates.attributes"></a>

<a id="attributes"></a>

## Attributes

Attribute mixin for coordinate values.

### Classes

Attribute
: Mixin providing validation and labeling for coordinate value types.

<a id="morpha.coordinates.attributes.BaseT"></a>

### *class* morpha.coordinates.attributes.BaseT

Type variable for the basic type from which the attribute inherits.

alias of TypeVar(‘BaseT’, int, str, float, bool)

<a id="morpha.coordinates.attributes.Attribute"></a>

### *class* morpha.coordinates.attributes.Attribute

Bases: [`Generic`](https://docs.python.org/3/library/typing.html#typing.Generic)[[`BaseT`](#morpha.coordinates.attributes.BaseT)]

Mixin class for attribute types with validation and labeling.

Provides a common interface for types representing categorical or
constrained values that can be used in coordinates.

* **Class Attributes:**
  * **OPTIONS** (*FrozenSet[BaseT]*) – Valid values for this attribute type.
  * **LABELS** (*Mapping[BaseT, str]*) – Human-readable labels for valid values.

<a id="morpha.coordinates.attributes.Attribute.OPTIONS"></a>

#### OPTIONS

Valid values for this attribute type (set on subclasses).

* **Type:**
  FrozenSet[[BaseT](#morpha.coordinates.attributes.BaseT)]

<a id="morpha.coordinates.attributes.Attribute.LABELS"></a>

#### LABELS

Human-readable labels for valid values (set on subclasses).

* **Type:**
  Mapping[[BaseT](#morpha.coordinates.attributes.BaseT), [str](https://docs.python.org/3/library/stdtypes.html#str)]

### Notes

This mixin doesn’t define \_\_new_\_ or \_\_init_\_. It’s designed to be
combined with a built-in type (int, str, float, bool) via multiple
inheritance. Subclasses should implement their own constructor.

### Examples

Define a categorical attribute:

```pycon
>>> class Task(str, Attribute[str]):
...     OPTIONS = frozenset(["PTD", "CLK"])
...     LABELS = {"PTD": "Pursuit Tracking", "CLK": "Clock Task"}
...
...     def __new__(cls, value: str):
...         if not cls.is_valid(value):
...             raise ValueError(f"Invalid value: {value}")
...         return super().__new__(cls, value)
```

Use the attribute:

```pycon
>>> task = Task("PTD")
>>> task.full_label
'Pursuit Tracking'
```

Check validity:

```pycon
>>> Task.is_valid("PTD")
True
>>> Task.is_valid("INVALID")
False
```

<a id="id1"></a>

#### OPTIONS *: [FrozenSet](https://docs.python.org/3/library/typing.html#typing.FrozenSet)[[BaseT](#morpha.coordinates.attributes.BaseT)]*

<a id="id2"></a>

#### LABELS *: [Mapping](https://docs.python.org/3/library/typing.html#typing.Mapping)[[BaseT](#morpha.coordinates.attributes.BaseT), [str](https://docs.python.org/3/library/stdtypes.html#str)]*

<a id="morpha.coordinates.attributes.Attribute.is_valid"></a>

#### *classmethod* is_valid(value)

Check if a value is valid for this attribute type.

* **Parameters:**
  **value** (*Any*) – Value to check.
* **Returns:**
  True if value is in OPTIONS.
* **Return type:**
  [bool](https://docs.python.org/3/library/functions.html#bool)

#### NOTE
Override in subclasses if validation is more complex than
checking membership in OPTIONS.

<a id="morpha.coordinates.attributes.Attribute.full_label"></a>

#### *property* full_label *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

Return human-readable label for this value.

* **Returns:**
  Label from LABELS, or empty string if not found.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

<a id="morpha.coordinates.attributes.Attribute.get_options"></a>

#### *classmethod* get_options()

Get all valid options.

* **Returns:**
  Set of valid attribute values.
* **Return type:**
  FrozenSet[[BaseT](#morpha.coordinates.attributes.BaseT)]

<a id="morpha.coordinates.attributes.Attribute.get_labels"></a>

#### *classmethod* get_labels()

Get all labels.

* **Returns:**
  Mapping from values to human-readable labels.
* **Return type:**
  Mapping[[BaseT](#morpha.coordinates.attributes.BaseT), [str](https://docs.python.org/3/library/stdtypes.html#str)]

<a id="morpha.coordinates.attributes.Attribute.from_container"></a>

#### *classmethod* from_container(values, container=<class 'list'>)

Create multiple attribute instances from an iterable.

* **Parameters:**
  * **values** (*Iterable* *[*[*BaseT*](#morpha.coordinates.attributes.BaseT) *]*) – Values to convert.
  * **container** (*Type* *[**Union* *[**List* *[**Any* *]* *,* *Tuple* *[**Any* *,*  *...* *]* *,* *Set* *[**Any* *]* *]* *]*) – Container type for results (list, tuple, or set).
* **Returns:**
  Container of attribute instances.
* **Return type:**
  Union[List[[Attribute](#morpha.coordinates.attributes.Attribute)[[BaseT](#morpha.coordinates.attributes.BaseT)]], Tuple[[Attribute](#morpha.coordinates.attributes.Attribute)[[BaseT](#morpha.coordinates.attributes.BaseT)], …], Set[[Attribute](#morpha.coordinates.attributes.Attribute)[[BaseT](#morpha.coordinates.attributes.BaseT)]]]
* **Raises:**
  [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError) – If any value is invalid.
