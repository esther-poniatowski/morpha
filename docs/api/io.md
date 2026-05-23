# I/O Module

Saver and Loader implementations for various file formats.

## Base Classes

Base I/O classes.

### Classes

FileExt
: File extension type with validation.

IOHandler
: Abstract base class for file I/O operations.

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

#### OPTIONS *= frozenset({'.csv', '.h5', '.hdf5', '.json', '.npy', '.npz', '.pkl', '.yaml', '.yml'})*

#### *classmethod* is_valid(ext)

Check if extension is valid.

* **Parameters:**
  **ext** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – File extension to check.
* **Returns:**
  True if the extension is in OPTIONS.
* **Return type:**
  [bool](https://docs.python.org/3/library/functions.html#bool)

#### *static* add_period(ext)

Add leading period if missing.

* **Parameters:**
  **ext** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – File extension, with or without leading period.
* **Returns:**
  Extension with a leading period.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

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

#### EXT *: [frozenset](https://docs.python.org/3/library/stdtypes.html#frozenset)[[str](https://docs.python.org/3/library/stdtypes.html#str)]*

#### *static* enforce_ext(path, ext)

Enforce a specific extension on a path.

* **Parameters:**
  * **path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *or* *Path*) – File path.
  * **ext** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *or* [*FileExt*](#morpha.io.base.FileExt)) – Required extension.
* **Returns:**
  Path with the specified extension.
* **Return type:**
  Path

## Savers

Saver implementations for various file formats.

### Classes

Saver
: Abstract base class for saving data.

SaverPKL
: Save objects as Pickle files.

SaverNPY
: Save arrays as NumPy files.

SaverNPZ
: Save multiple arrays as compressed NumPy files.

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

#### save(data)

Save data to file.

* **Parameters:**
  **data** (*Any*) – Data to save.
* **Raises:**
  [**Exception**](https://docs.python.org/3/library/exceptions.html#Exception) – Re-raises any exception from \_save with context.
* **Return type:**
  None

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

#### EXT *: [frozenset](https://docs.python.org/3/library/stdtypes.html#frozenset)[[str](https://docs.python.org/3/library/stdtypes.html#str)]* *= frozenset({'.pkl'})*

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

#### EXT *: [frozenset](https://docs.python.org/3/library/stdtypes.html#frozenset)[[str](https://docs.python.org/3/library/stdtypes.html#str)]* *= frozenset({'.npy'})*

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

#### EXT *: [frozenset](https://docs.python.org/3/library/stdtypes.html#frozenset)[[str](https://docs.python.org/3/library/stdtypes.html#str)]* *= frozenset({'.npz'})*

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

#### EXT *: [frozenset](https://docs.python.org/3/library/stdtypes.html#frozenset)[[str](https://docs.python.org/3/library/stdtypes.html#str)]* *= frozenset({'.json'})*

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

#### EXT *: [frozenset](https://docs.python.org/3/library/stdtypes.html#frozenset)[[str](https://docs.python.org/3/library/stdtypes.html#str)]* *= frozenset({'.yaml', '.yml'})*

### *class* morpha.io.savers.SaverHDF5(path)

Bases: [`Saver`](#morpha.io.savers.Saver)

Save data to HDF5 files.

* **Parameters:**
  **path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *|* [*Path*](https://docs.python.org/3/library/pathlib.html#pathlib.Path))

#### EXT *: [frozenset](https://docs.python.org/3/library/stdtypes.html#frozenset)[[str](https://docs.python.org/3/library/stdtypes.html#str)]* *= frozenset({'.h5', '.hdf5'})*

## Loaders

Loader implementations for various file formats.

### Classes

Loader
: Abstract base class for loading data.

LoaderPKL
: Load objects from Pickle files.

LoaderNPY
: Load arrays from NumPy files.

LoaderNPZ
: Load multiple arrays from compressed NumPy files.

### *class* morpha.io.loaders.Loader(path)

Bases: [`IOHandler`](#morpha.io.base.IOHandler)

Abstract base class for loading data from files.

* **Parameters:**
  **path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *or* *Path*) – Path to load from.
* **Raises:**
  [**FileNotFoundError**](https://docs.python.org/3/library/exceptions.html#FileNotFoundError) – If file doesn’t exist.
* **Class Attributes:**
  **EXT** (*frozenset[str]*) – Acceptable file extensions for this format (including aliases).

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

#### load()

Load data from file.

* **Returns:**
  Loaded data.
* **Return type:**
  Any
* **Raises:**
  [**Exception**](https://docs.python.org/3/library/exceptions.html#Exception) – Re-raises any exception from \_load with context.

### *class* morpha.io.loaders.LoaderPKL(path)

Bases: [`Loader`](#morpha.io.loaders.Loader)

Load Python objects from Pickle files.

> **See also**
>
> [`pickle.load`](https://docs.python.org/3/library/pickle.html#pickle.load)
> : Underlying deserialization function.

* **Parameters:**
  **path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *|* [*Path*](https://docs.python.org/3/library/pathlib.html#pathlib.Path))

#### EXT *: [frozenset](https://docs.python.org/3/library/stdtypes.html#frozenset)[[str](https://docs.python.org/3/library/stdtypes.html#str)]* *= frozenset({'.pkl'})*

### *class* morpha.io.loaders.LoaderNPY(path)

Bases: [`Loader`](#morpha.io.loaders.Loader)

Load NumPy arrays from .npy files.

> **See also**
>
> [`numpy.load`](https://numpy.org/doc/stable/reference/generated/numpy.load.html#numpy.load)
> : Underlying load function.

* **Parameters:**
  **path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *|* [*Path*](https://docs.python.org/3/library/pathlib.html#pathlib.Path))

#### EXT *: [frozenset](https://docs.python.org/3/library/stdtypes.html#frozenset)[[str](https://docs.python.org/3/library/stdtypes.html#str)]* *= frozenset({'.npy'})*

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

#### EXT *: [frozenset](https://docs.python.org/3/library/stdtypes.html#frozenset)[[str](https://docs.python.org/3/library/stdtypes.html#str)]* *= frozenset({'.npz'})*

### *class* morpha.io.loaders.LoaderJSON(path)

Bases: [`Loader`](#morpha.io.loaders.Loader)

Load data from JSON files.

> **See also**
>
> [`json.load`](https://docs.python.org/3/library/json.html#json.load)
> : Underlying deserialization function.

* **Parameters:**
  **path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *|* [*Path*](https://docs.python.org/3/library/pathlib.html#pathlib.Path))

#### EXT *: [frozenset](https://docs.python.org/3/library/stdtypes.html#frozenset)[[str](https://docs.python.org/3/library/stdtypes.html#str)]* *= frozenset({'.json'})*

### *class* morpha.io.loaders.LoaderYAML(path)

Bases: [`Loader`](#morpha.io.loaders.Loader)

Load data from YAML files.

> **See also**
>
> `yaml.safe_load`
> : Underlying deserialization function.

* **Parameters:**
  **path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *|* [*Path*](https://docs.python.org/3/library/pathlib.html#pathlib.Path))

#### EXT *: [frozenset](https://docs.python.org/3/library/stdtypes.html#frozenset)[[str](https://docs.python.org/3/library/stdtypes.html#str)]* *= frozenset({'.yaml', '.yml'})*

### *class* morpha.io.loaders.LoaderHDF5(path)

Bases: [`Loader`](#morpha.io.loaders.Loader)

Load data from HDF5 files.

* **Parameters:**
  **path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *|* [*Path*](https://docs.python.org/3/library/pathlib.html#pathlib.Path))

#### EXT *: [frozenset](https://docs.python.org/3/library/stdtypes.html#frozenset)[[str](https://docs.python.org/3/library/stdtypes.html#str)]* *= frozenset({'.h5', '.hdf5'})*
