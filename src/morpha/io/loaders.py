"""Loader implementations for various file formats."""

from abc import abstractmethod
from pathlib import Path
from typing import Any, Union, Dict
import pickle

import numpy as np

from morpha.io.base import IOHandler
import logging

logger = logging.getLogger(__name__)


class Loader(IOHandler):
    """
    Abstract base class for loading data from files.

    Parameters
    ----------
    path : str or Path
        Path to load from.

    Raises
    ------
    FileNotFoundError
        If file doesn't exist.

    Class Attributes
    ----------------
    EXT : frozenset[str]
        Acceptable file extensions for this format (including aliases).

    Attributes
    ----------
    path : Path
        Source file path.

    Notes
    -----
    Uses Template Method pattern: `load()` handles common logic,
    `_load()` implements format-specific deserialization.

    See Also
    --------
    Saver : For saving data.

    Examples
    --------
    >>> loader = LoaderPKL("data/file")
    >>> obj = loader.load()  # Loads from data/file.pkl
    """

    def __init__(self, path: Union[str, Path]) -> None:
        super().__init__(path)
        if not self.path.exists():
            raise FileNotFoundError(f"File does not exist: {self.path}")

    def load(self) -> Any:
        """
        Load data from file.

        Returns
        -------
        Any
            Loaded data.

        Raises
        ------
        Exception
            Re-raises any exception from _load with context.
        """
        try:
            data = self._load()
        except Exception as exc:
            logger.exception(
                "Loader failed",
                extra={"loader": self.__class__.__name__, "path": str(self.path)},
            )
            raise
        return data

    @abstractmethod
    def _load(self) -> Any:
        """Implement format-specific loading logic."""
        ...


class LoaderPKL(Loader):
    """
    Load Python objects from Pickle files.

    See Also
    --------
    pickle.load : Underlying deserialization function.
    """

    EXT = frozenset({".pkl"})

    def _load(self) -> Any:
        with self.path.open("rb") as file:
            return pickle.load(file)


class LoaderNPY(Loader):
    """
    Load NumPy arrays from .npy files.

    See Also
    --------
    numpy.load : Underlying load function.
    """

    EXT = frozenset({".npy"})

    def _load(self) -> np.ndarray:
        return np.load(self.path)


class LoaderNPZ(Loader):
    """
    Load arrays from compressed .npz files.

    Returns an NpzFile object that behaves like a dictionary.

    See Also
    --------
    numpy.load : Underlying load function.
    """

    EXT = frozenset({".npz"})

    def _load(self) -> Dict[str, np.ndarray]:
        npz = np.load(self.path)
        return dict(npz)


class LoaderJSON(Loader):
    """
    Load data from JSON files.

    See Also
    --------
    json.load : Underlying deserialization function.
    """

    EXT = frozenset({".json"})

    def _load(self) -> Any:
        import json

        with self.path.open("r", encoding="utf-8") as file:
            return json.load(file)


class LoaderYAML(Loader):
    """
    Load data from YAML files.

    See Also
    --------
    yaml.safe_load : Underlying deserialization function.
    """

    EXT = frozenset({".yaml", ".yml"})

    def _load(self) -> Any:
        import yaml

        with self.path.open("r", encoding="utf-8") as file:
            return yaml.safe_load(file)


class LoaderHDF5(Loader):
    """
    Load data from HDF5 files.
    """

    EXT = frozenset({".hdf5", ".h5"})

    def _load(self) -> Any:
        try:
            import h5py
        except ImportError as exc:
            raise RuntimeError("h5py is required for HDF5 support") from exc
        with h5py.File(self.path, "r") as file:
            data: Dict[str, np.ndarray] = {}
            def _visit(name, obj):
                if isinstance(obj, h5py.Dataset):
                    data[name] = obj[()]
            file.visititems(_visit)
            return data
