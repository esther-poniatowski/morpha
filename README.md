# Morpha

[![Conda](https://img.shields.io/badge/conda-eresthanaconda--channel-blue)](docs/guide/installation.md)
[![Maintenance](https://img.shields.io/maintenance/yes/2026)]()
[![Last Commit](https://img.shields.io/github/last-commit/esther-poniatowski/morpha)](https://github.com/esther-poniatowski/morpha/commits/main)
[![Python](https://img.shields.io/badge/python-%E2%89%A53.12-blue)](https://www.python.org/)
[![License: GPL](https://img.shields.io/badge/License-GPL-yellow.svg)](https://opensource.org/licenses/GPL-3.0)

Provides reusable data structures for scientific computing in Python.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

## Overview

### Motivation

Data analysis projects across scientific domains repeatedly implement the same
structural patterns: arrays with named dimensions, composite data containers with
schema enforcement, labeled coordinate axes, and serialization to multiple file
formats. Without shared abstractions, each project re-invents these patterns with
inconsistent interfaces.

### Advantages

Morpha extracts and generalizes these recurring patterns into a reusable library:

- **Dimension-aware arrays** — NumPy array subclasses that carry dimension names and
  propagate them through operations.
- **Structured containers** — abstract base classes for composite data with schema
  enforcement.
- **Creational patterns** — Factory and Builder abstractions for constructing data
  objects consistently.
- **Multi-format I/O** — Saver/Loader patterns for PKL, NPY, NPZ, JSON, YAML, and
  HDF5 formats.

---

## Features

- [x] **DataComponent**: NumPy array subclasses with dimension annotations and
  metadata propagation.
- [x] **DataStructure**: Abstract base classes for composite data structures with
  schema enforcement.
- [x] **Coordinates**: Labeled axes with attribute validation.
- [x] **Creational Patterns**: Factory and Builder abstractions for object creation.
- [x] **I/O**: Saver/Loader patterns for multiple file formats.

---

## Quick Start

```python
import numpy as np
from morpha import DataComponent, Dimensions

data = DataComponent(np.random.randn(100, 50), dims=Dimensions("time", "units"))
print(data.get_dim(0))        # 'time'
print(data.get_axis("units")) # 1
```

---

## Documentation

| Guide | Content |
| ----- | ------- |
| [Installation](docs/guide/installation.md) | Prerequisites, pip setup |
| [Usage](docs/guide/usage.md) | DataComponent, DataStructure, coordinates, I/O |
| [Concepts](docs/guide/concepts.md) | Core abstractions and design |

Full API documentation and rendered guides are also available at
[esther-poniatowski.github.io/morpha](https://esther-poniatowski.github.io/morpha/).

---

## Contributing

Contribution guidelines are described in [CONTRIBUTING.md](CONTRIBUTING.md).

---

## License

This project is licensed under the terms of the
[GNU General Public License v3.0](LICENSE).
