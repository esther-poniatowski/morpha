<a id="i-o-module"></a>

# I/O Module

Saver and Loader implementations for various file formats.

<a id="module-morpha.io.base"></a>

<a id="base-classes"></a>

## Base Classes

Base I/O classes.

<a id="morpha.io.base.FileExt"></a>

### *class* morpha.io.base.FileExt(ext)

Bases: [`str`](https://docs.python.org/3/library/stdtypes.html#str)

Validated file extension.

A string subclass that ensures the extension is valid and
properly formatted with a leading period.

* **Class Attributes:**
  **OPTIONS** (*frozenset[str]*) – Valid extension values.
* **Parameters:**
  **ext** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – File extension (with or without leading period).
* **Return type:**
  [*Self*](https://docs.python.org/3/library/typing.html#typing.Self)

### Examples

```pycon
>>> ext = FileExt("pkl")
>>> str(ext)
'.pkl'
```

```pycon
>>> FileExt("xyz")  # Raises ValueError
```

<a id="morpha.io.base.FileExt.OPTIONS"></a>

#### OPTIONS *= frozenset({'.csv', '.h5', '.hdf5', '.json', '.npy', '.npz', '.pkl', '.yaml', '.yml'})*

<a id="morpha.io.base.FileExt.is_valid"></a>

#### *classmethod* is_valid(ext)

Check if extension is valid.

* **Parameters:**
  **ext** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – File extension to check.
* **Returns:**
  True if the extension is in OPTIONS.
* **Return type:**
  [bool](https://docs.python.org/3/library/functions.html#bool)

<a id="morpha.io.base.FileExt.add_period"></a>

#### *static* add_period(ext)

Add leading period if missing.

* **Parameters:**
  **ext** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – File extension, with or without leading period.
* **Returns:**
  Extension with a leading period.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

<a id="morpha.io.base.IOHandler"></a>

### *class* morpha.io.base.IOHandler(path)

Bases: [`ABC`](https://docs.python.org/3/library/abc.html#abc.ABC)

Abstract base class for file I/O operations.

Provides common functionality for Saver and Loader classes:
- Path handling with extension enforcement
- Multi-extension format support via frozenset-valued EXT

* **Parameters:**
  **path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *or* *Path*) – Path to the file.
* **Class Attributes:**
  **EXT** (*frozenset[str]*) – Acceptable file extensions for this handler (including aliases).
  The first element (by sort order) is used as the canonical default.

<a id="morpha.io.base.IOHandler.path"></a>

#### path

File path with enforced extension.

* **Type:**
  Path

> **See also**
>
> `Saver`
> : For saving data to files.
>
> `Loader`
> : For loading data from files.

### Examples

Subclass to create specific handlers:

```pycon
>>> class MyHandler(IOHandler):
...     EXT = frozenset({".pkl"})
...     def process(self, data): ...
```

```pycon
>>> handler = MyHandler("data/file")
>>> handler.path
PosixPath('data/file.pkl')
```

<a id="morpha.io.base.IOHandler.EXT"></a>

#### EXT *: [frozenset](https://docs.python.org/3/library/stdtypes.html#frozenset)[[str](https://docs.python.org/3/library/stdtypes.html#str)]*

<a id="morpha.io.base.IOHandler.enforce_ext"></a>

#### *static* enforce_ext(path, ext)

Enforce a specific extension on a path.

* **Parameters:**
  * **path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *or* *Path*) – File path.
  * **ext** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *or* [*FileExt*](#morpha.io.base.FileExt)) – Required extension.
* **Returns:**
  Path with the specified extension.
* **Return type:**
  Path

<a id="module-morpha.io.savers"></a>

<a id="savers"></a>

## Savers

Saver implementations for various file formats.

<a id="morpha.io.savers.Saver"></a>

### *class* morpha.io.savers.Saver(path)

Bases: [`IOHandler`](#morpha.io.base.IOHandler)

Abstract base class for saving data to files.

Separates path specification from data, enabling dependency injection
where the saver is configured before data is available.

* **Parameters:**
  **path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *or* *Path*) – Path to save to.
* **Raises:**
  [**FileNotFoundError**](https://docs.python.org/3/library/exceptions.html#FileNotFoundError) – If parent directory doesn’t exist.
* **Class Attributes:**
  **EXT** (*frozenset[str]*) – Acceptable file extensions for this format (including aliases).

<a id="morpha.io.savers.Saver.path"></a>

#### path

Target file path.

* **Type:**
  Path

### Notes

Uses Template Method pattern: save() handles common logic,
\_save() implements format-specific serialization.

> **See also**
>
> `Loader`
> : For loading saved data.

### Examples

```pycon
>>> saver = SaverPKL("output/data")
>>> saver.save(my_object)  # Saves to output/data.pkl
```

<a id="morpha.io.savers.Saver.save"></a>

#### save(data)

Save data to file.

* **Parameters:**
  **data** (*Any*) – Data to save.
* **Raises:**
  [**Exception**](https://docs.python.org/3/library/exceptions.html#Exception) – Re-raises any exception from \_save with context.
* **Return type:**
  None

<a id="morpha.io.savers.SaverPKL"></a>

### *class* morpha.io.savers.SaverPKL(path)

Bases: [`Saver`](#morpha.io.savers.Saver)

Save Python objects as Pickle files.

Uses Python’s pickle module for serialization.

> **See also**
>
> [`pickle.dump`](https://docs.python.org/3/library/pickle.html#pickle.dump)
> : Underlying serialization function.

* **Parameters:**
  **path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *|* [*Path*](https://docs.python.org/3/library/pathlib.html#pathlib.Path))

<a id="morpha.io.savers.SaverPKL.EXT"></a>

#### EXT *: [frozenset](https://docs.python.org/3/library/stdtypes.html#frozenset)[[str](https://docs.python.org/3/library/stdtypes.html#str)]* *= frozenset({'.pkl'})*

<a id="morpha.io.savers.SaverNPY"></a>

### *class* morpha.io.savers.SaverNPY(path)

Bases: [`Saver`](#morpha.io.savers.Saver)

Save NumPy arrays as .npy files.

Uses NumPy’s binary format for efficient storage of arrays.

> **See also**
>
> [`numpy.save`](https://numpy.org/doc/stable/reference/generated/numpy.save.html#numpy.save)
> : Underlying save function.

* **Parameters:**
  **path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *|* [*Path*](https://docs.python.org/3/library/pathlib.html#pathlib.Path))

<a id="morpha.io.savers.SaverNPY.EXT"></a>

#### EXT *: [frozenset](https://docs.python.org/3/library/stdtypes.html#frozenset)[[str](https://docs.python.org/3/library/stdtypes.html#str)]* *= frozenset({'.npy'})*

<a id="morpha.io.savers.SaverNPZ"></a>

### *class* morpha.io.savers.SaverNPZ(path)

Bases: [`Saver`](#morpha.io.savers.Saver)

Save multiple arrays as compressed .npz files.

Accepts either a single array or a dictionary of arrays.

> **See also**
>
> [`numpy.savez_compressed`](https://numpy.org/doc/stable/reference/generated/numpy.savez_compressed.html#numpy.savez_compressed)
> : Underlying save function.

* **Parameters:**
  **path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *|* [*Path*](https://docs.python.org/3/library/pathlib.html#pathlib.Path))

<a id="morpha.io.savers.SaverNPZ.EXT"></a>

#### EXT *: [frozenset](https://docs.python.org/3/library/stdtypes.html#frozenset)[[str](https://docs.python.org/3/library/stdtypes.html#str)]* *= frozenset({'.npz'})*

<a id="morpha.io.savers.SaverJSON"></a>

### *class* morpha.io.savers.SaverJSON(path)

Bases: [`Saver`](#morpha.io.savers.Saver)

Save data as JSON files.

Suitable for configuration and simple nested structures.

> **See also**
>
> [`json.dump`](https://docs.python.org/3/library/json.html#json.dump)
> : Underlying serialization function.

* **Parameters:**
  **path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *|* [*Path*](https://docs.python.org/3/library/pathlib.html#pathlib.Path))

<a id="morpha.io.savers.SaverJSON.EXT"></a>

#### EXT *: [frozenset](https://docs.python.org/3/library/stdtypes.html#frozenset)[[str](https://docs.python.org/3/library/stdtypes.html#str)]* *= frozenset({'.json'})*

<a id="morpha.io.savers.SaverYAML"></a>

### *class* morpha.io.savers.SaverYAML(path)

Bases: [`Saver`](#morpha.io.savers.Saver)

Save data as YAML files.

Human-readable format for configuration and metadata.

> **See also**
>
> `yaml.safe_dump`
> : Underlying serialization function.

* **Parameters:**
  **path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *|* [*Path*](https://docs.python.org/3/library/pathlib.html#pathlib.Path))

<a id="morpha.io.savers.SaverYAML.EXT"></a>

#### EXT *: [frozenset](https://docs.python.org/3/library/stdtypes.html#frozenset)[[str](https://docs.python.org/3/library/stdtypes.html#str)]* *= frozenset({'.yaml', '.yml'})*

<a id="morpha.io.savers.SaverHDF5"></a>

### *class* morpha.io.savers.SaverHDF5(path)

Bases: [`Saver`](#morpha.io.savers.Saver)

Save data to HDF5 files.

* **Parameters:**
  **path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *|* [*Path*](https://docs.python.org/3/library/pathlib.html#pathlib.Path))

<a id="morpha.io.savers.SaverHDF5.EXT"></a>

#### EXT *: [frozenset](https://docs.python.org/3/library/stdtypes.html#frozenset)[[str](https://docs.python.org/3/library/stdtypes.html#str)]* *= frozenset({'.h5', '.hdf5'})*

<a id="module-morpha.io.loaders"></a>

<a id="loaders"></a>

## Loaders

Loader implementations for various file formats.

<a id="morpha.io.loaders.Loader"></a>

### *class* morpha.io.loaders.Loader(path)

Bases: [`IOHandler`](#morpha.io.base.IOHandler)

Abstract base class for loading data from files.

* **Parameters:**
  **path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *or* *Path*) – Path to load from.
* **Raises:**
  [**FileNotFoundError**](https://docs.python.org/3/library/exceptions.html#FileNotFoundError) – If file doesn’t exist.
* **Class Attributes:**
  **EXT** (*frozenset[str]*) – Acceptable file extensions for this format (including aliases).

<a id="morpha.io.loaders.Loader.path"></a>

#### path

Source file path.

* **Type:**
  Path

### Notes

Uses Template Method pattern: load() handles common logic,
\_load() implements format-specific deserialization.

> **See also**
>
> `Saver`
> : For saving data.

### Examples

```pycon
>>> loader = LoaderPKL("data/file")
>>> obj = loader.load()  # Loads from data/file.pkl
```

<a id="morpha.io.loaders.Loader.load"></a>

#### load()

Load data from file.

* **Returns:**
  Loaded data.
* **Return type:**
  Any
* **Raises:**
  [**Exception**](https://docs.python.org/3/library/exceptions.html#Exception) – Re-raises any exception from \_load with context.

<a id="morpha.io.loaders.LoaderPKL"></a>

### *class* morpha.io.loaders.LoaderPKL(path)

Bases: [`Loader`](#morpha.io.loaders.Loader)

Load Python objects from Pickle files.

> **See also**
>
> [`pickle.load`](https://docs.python.org/3/library/pickle.html#pickle.load)
> : Underlying deserialization function.

* **Parameters:**
  **path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *|* [*Path*](https://docs.python.org/3/library/pathlib.html#pathlib.Path))

<a id="morpha.io.loaders.LoaderPKL.EXT"></a>

#### EXT *: [frozenset](https://docs.python.org/3/library/stdtypes.html#frozenset)[[str](https://docs.python.org/3/library/stdtypes.html#str)]* *= frozenset({'.pkl'})*

<a id="morpha.io.loaders.LoaderNPY"></a>

### *class* morpha.io.loaders.LoaderNPY(path)

Bases: [`Loader`](#morpha.io.loaders.Loader)

Load NumPy arrays from .npy files.

> **See also**
>
> [`numpy.load`](https://numpy.org/doc/stable/reference/generated/numpy.load.html#numpy.load)
> : Underlying load function.

* **Parameters:**
  **path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *|* [*Path*](https://docs.python.org/3/library/pathlib.html#pathlib.Path))

<a id="morpha.io.loaders.LoaderNPY.EXT"></a>

#### EXT *: [frozenset](https://docs.python.org/3/library/stdtypes.html#frozenset)[[str](https://docs.python.org/3/library/stdtypes.html#str)]* *= frozenset({'.npy'})*

<a id="morpha.io.loaders.LoaderNPZ"></a>

### *class* morpha.io.loaders.LoaderNPZ(path)

Bases: [`Loader`](#morpha.io.loaders.Loader)

Load arrays from compressed .npz files.

Returns an NpzFile object that behaves like a dictionary.

> **See also**
>
> [`numpy.load`](https://numpy.org/doc/stable/reference/generated/numpy.load.html#numpy.load)
> : Underlying load function.

* **Parameters:**
  **path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *|* [*Path*](https://docs.python.org/3/library/pathlib.html#pathlib.Path))

<a id="morpha.io.loaders.LoaderNPZ.EXT"></a>

#### EXT *: [frozenset](https://docs.python.org/3/library/stdtypes.html#frozenset)[[str](https://docs.python.org/3/library/stdtypes.html#str)]* *= frozenset({'.npz'})*

<a id="morpha.io.loaders.LoaderJSON"></a>

### *class* morpha.io.loaders.LoaderJSON(path)

Bases: [`Loader`](#morpha.io.loaders.Loader)

Load data from JSON files.

> **See also**
>
> [`json.load`](https://docs.python.org/3/library/json.html#json.load)
> : Underlying deserialization function.

* **Parameters:**
  **path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *|* [*Path*](https://docs.python.org/3/library/pathlib.html#pathlib.Path))

<a id="morpha.io.loaders.LoaderJSON.EXT"></a>

#### EXT *: [frozenset](https://docs.python.org/3/library/stdtypes.html#frozenset)[[str](https://docs.python.org/3/library/stdtypes.html#str)]* *= frozenset({'.json'})*

<a id="morpha.io.loaders.LoaderYAML"></a>

### *class* morpha.io.loaders.LoaderYAML(path)

Bases: [`Loader`](#morpha.io.loaders.Loader)

Load data from YAML files.

> **See also**
>
> `yaml.safe_load`
> : Underlying deserialization function.

* **Parameters:**
  **path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *|* [*Path*](https://docs.python.org/3/library/pathlib.html#pathlib.Path))

<a id="morpha.io.loaders.LoaderYAML.EXT"></a>

#### EXT *: [frozenset](https://docs.python.org/3/library/stdtypes.html#frozenset)[[str](https://docs.python.org/3/library/stdtypes.html#str)]* *= frozenset({'.yaml', '.yml'})*

<a id="morpha.io.loaders.LoaderHDF5"></a>

### *class* morpha.io.loaders.LoaderHDF5(path)

Bases: [`Loader`](#morpha.io.loaders.Loader)

Load data from HDF5 files.

* **Parameters:**
  **path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *|* [*Path*](https://docs.python.org/3/library/pathlib.html#pathlib.Path))

<a id="morpha.io.loaders.LoaderHDF5.EXT"></a>

#### EXT *: [frozenset](https://docs.python.org/3/library/stdtypes.html#frozenset)[[str](https://docs.python.org/3/library/stdtypes.html#str)]* *= frozenset({'.h5', '.hdf5'})*
