<a id="creational-module"></a>

# Creational Module

Factory and Builder patterns for object creation.

<a id="module-morpha.creational.factory"></a>

<a id="factory"></a>

## Factory

Factory pattern for creating data components.

<a id="classes"></a>

### Classes

Factory
: Abstract base class for creating data components.

<a id="morpha.creational.factory.Products"></a>

### *class* morpha.creational.factory.Products

Type variable for products created by a factory.

alias of TypeVar(‘Products’, bound=`DataComponent | Tuple[DataComponent, ...]`)

<a id="morpha.creational.factory.Factory"></a>

### *class* morpha.creational.factory.Factory

Bases: [`Generic`](https://docs.python.org/3/library/typing.html#typing.Generic)[[`Products`](#morpha.creational.factory.Products)], [`ABC`](https://docs.python.org/3/library/abc.html#abc.ABC)

Abstract base class for creating data components.

Factories encapsulate the logic for creating one or more coupled
DataComponent instances from raw inputs.

* **Class Attributes:**
  **PRODUCT_CLASSES** (*Type[DataComponent] | Tuple[Type[DataComponent], …]*) – Class(es) of products this factory creates.

<a id="morpha.creational.factory.Factory.PRODUCT_CLASSES"></a>

#### PRODUCT_CLASSES

Class(es) of products this factory creates (set on subclasses).

* **Type:**
  Type[[DataComponent](components.md#morpha.components.base.DataComponent)] | Tuple[Type[[DataComponent](components.md#morpha.components.base.DataComponent)], …]

### Notes

Factories are useful when:
- Creating a component requires complex processing of inputs
- Multiple related components must be created together
- The creation logic should be reusable and testable

> **See also**
>
> `Builder`
> : For step-by-step construction of DataStructures.

### Examples

Define a concrete factory:

```pycon
>>> class TimeCoordFactory(Factory[CoordTime]):
...     PRODUCT_CLASSES = CoordTime
...
...     def create(self, timestamps: np.ndarray, unit: str) -> CoordTime:
...         return CoordTime(timestamps, time_unit=unit)
```

Use the factory:

```pycon
>>> factory = TimeCoordFactory()
>>> coord = factory.create(np.arange(100), unit="ms")
```

<a id="id0"></a>

#### PRODUCT_CLASSES *: [Type](https://docs.python.org/3/library/typing.html#typing.Type)[[DataComponent](components.md#morpha.components.base.DataComponent)] | [Tuple](https://docs.python.org/3/library/typing.html#typing.Tuple)[[Type](https://docs.python.org/3/library/typing.html#typing.Type)[[DataComponent](components.md#morpha.components.base.DataComponent)], ...]*

<a id="morpha.creational.factory.Factory.create"></a>

#### *abstractmethod* create(\*args, \*\*kwargs)

Create one or more data components.

* **Parameters:**
  * **\*args** (*Any*) – Inputs required to create the products.
  * **\*\*kwargs** (*Any*) – Additional options for creation.
* **Returns:**
  Created component(s).
* **Return type:**
  [Products](#morpha.creational.factory.Products)

#### NOTE
Subclasses must implement this method with appropriate
parameters for their specific product types.

<a id="module-morpha.creational.builder"></a>

<a id="builder"></a>

## Builder

Builder pattern for constructing data structures.

### Classes

Builder
: Abstract base class for step-by-step data structure construction.

<a id="morpha.creational.builder.Product"></a>

### *class* morpha.creational.builder.Product

Type variable for the data structure produced by a builder.

alias of TypeVar(‘Product’, bound=[`DataStructure`](structures.md#morpha.structures.base.DataStructure)[[`Any`](https://docs.python.org/3/library/typing.html#typing.Any)])

<a id="morpha.creational.builder.Builder"></a>

### *class* morpha.creational.builder.Builder

Bases: [`Generic`](https://docs.python.org/3/library/typing.html#typing.Generic)[[`Product`](#morpha.creational.builder.Product)], [`ABC`](https://docs.python.org/3/library/abc.html#abc.ABC)

Abstract base class for building data structures.

Builders encapsulate the step-by-step construction of complex
DataStructure objects, separating construction logic from the
data structure class itself.

* **Class Attributes:**
  * **PRODUCT_CLASS** (*Type[Product]*) – Class of the data structure to build.
  * **TMP_DATA** (*Tuple[str, …]*) – Names of temporary data attributes used during building.

<a id="morpha.creational.builder.Builder.product"></a>

#### product

The data structure being constructed.

* **Type:**
  Optional[[Product](#morpha.creational.builder.Product)]

### Notes

The Builder pattern separates concerns:
- Constructor: Store static configuration
- build(): Receive dynamic inputs, orchestrate construction
- Helper methods: Process specific aspects of construction
- reset(): Clear state for reuse

After get_product() is called, the builder resets and can be
reused to build another instance.

> **See also**
>
> `Factory`
> : For simpler component creation without step-by-step logic.

### Examples

Define a concrete builder:

```pycon
>>> class TimeSeriesBuilder(Builder[TimeSeries]):
...     PRODUCT_CLASS = TimeSeries
...     TMP_DATA = ("raw_data", "timestamps")
...
...     def build(self, raw: np.ndarray, times: np.ndarray) -> TimeSeries:
...         self.product = TimeSeries()
...         self._process_data(raw)
...         self._create_time_coord(times)
...         return self.get_product()
...
...     def _process_data(self, raw: np.ndarray) -> None:
...         # Processing logic...
...         self.product.set_data(CoreData(raw))
...
...     def _create_time_coord(self, times: np.ndarray) -> None:
...         # Coordinate creation logic...
...         self.product.set_coord("time", CoordTime(times))
```

Use the builder:

```pycon
>>> builder = TimeSeriesBuilder()
>>> ts = builder.build(raw_data, timestamps)
```

<a id="morpha.creational.builder.Builder.PRODUCT_CLASS"></a>

#### PRODUCT_CLASS *: [Type](https://docs.python.org/3/library/typing.html#typing.Type)[[Product](#morpha.creational.builder.Product)]*

<a id="morpha.creational.builder.Builder.TMP_DATA"></a>

#### TMP_DATA *: [Tuple](https://docs.python.org/3/library/typing.html#typing.Tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]*

<a id="morpha.creational.builder.Builder.__init__"></a>

#### \_\_init_\_()

Initialize the builder with no product.

* **Return type:**
  None

<a id="morpha.creational.builder.Builder.reset"></a>

#### reset()

Reset builder state for reuse.

* **Return type:**
  None

<a id="morpha.creational.builder.Builder.get_product"></a>

#### get_product()

Return the built product and reset the builder.

* **Returns:**
  The completed data structure.
* **Return type:**
  [Product](#morpha.creational.builder.Product)
* **Raises:**
  [**AssertionError**](https://docs.python.org/3/library/exceptions.html#AssertionError) – If product is None (build not complete).

<a id="morpha.creational.builder.Builder.build"></a>

#### *abstractmethod* build(\*args, \*\*kwargs)

Build a data structure step-by-step.

* **Parameters:**
  * **\*args** (*Any*) – Input objects required for building.
  * **\*\*kwargs** (*Any*) – Additional options for building.
* **Returns:**
  The completed data structure.
* **Return type:**
  [Product](#morpha.creational.builder.Product)

#### NOTE
Implementations should:
1. Initialize self.product
2. Call helper methods to build components
3. Return via self.get_product()
