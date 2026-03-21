"""
Saver implementations for various file formats.

Classes
-------
Saver
    Abstract base class for saving data.
SaverPKL
    Save objects as Pickle files.
SaverNPY
    Save arrays as NumPy files.
SaverNPZ
    Save multiple arrays as compressed NumPy files.
"""

from abc import abstractmethod
from pathlib import Path
from typing import Any, Union, Dict
import pickle

import numpy as np

from morpha.io.base import IOHandler, FileExt
import logging

logger = logging.getLogger(__name__)


class Saver(IOHandler):
    """
    Abstract base class for saving data to files.

    Separates path specification from data, enabling dependency injection
    where the saver is configured before data is available.

    Class Attributes
    ----------------
    EXT : FileExt
        File extension for this format.

    Attributes
    ----------
    path : Path
        Target file path.

    Parameters
    ----------
    path : str or Path
        Path to save to.

    Examples
    --------
    >>> saver = SaverPKL("output/data")
    >>> saver.save(my_object)  # Saves to output/data.pkl

    Raises
    ------
    FileNotFoundError
        If parent directory doesn't exist.

    Notes
    -----
    Uses Template Method pattern: `save()` handles common logic,
    `_save()` implements format-specific serialization.

    See Also
    --------
    Loader : For loading saved data.
    """

    def __init__(self, path: Union[str, Path]) -> None:
        super().__init__(path)
        if not self.path.parent.exists():
            raise FileNotFoundError(f"Directory does not exist: {self.path.parent}")

    def save(self, data: Any) -> None:
        """
        Save data to file.

        Parameters
        ----------
        data : Any
            Data to save.

        Raises
        ------
        Exception
            Re-raises any exception from _save with context.
        """
        try:
            self._save(data)
        except Exception as exc:
            logger.exception(
                "Saver failed",
                extra={"saver": self.__class__.__name__, "path": str(self.path)},
            )
            raise

    @abstractmethod
    def _save(self, data: Any) -> None:
        """Implement format-specific saving logic."""
        ...


class SaverPKL(Saver):
    """
    Save Python objects as Pickle files.

    Uses Python's pickle module for serialization.

    See Also
    --------
    pickle.dump : Underlying serialization function.
    """

    EXT = FileExt("pkl")

    def _save(self, data: Any) -> None:
        with self.path.open("wb") as file:
            pickle.dump(data, file)


class SaverNPY(Saver):
    """
    Save NumPy arrays as .npy files.

    Uses NumPy's binary format for efficient storage of arrays.

    See Also
    --------
    numpy.save : Underlying save function.
    """

    EXT = FileExt("npy")

    def _save(self, data: np.ndarray) -> None:
        np.save(self.path, data)


class SaverNPZ(Saver):
    """
    Save multiple arrays as compressed .npz files.

    Accepts either a single array or a dictionary of arrays.

    Parameters
    ----------
    data : np.ndarray | Dict[str, np.ndarray]
        Single array or dictionary mapping names to arrays.

    See Also
    --------
    numpy.savez_compressed : Underlying save function.
    """

    EXT = FileExt("npz")

    def _save(self, data: Union[np.ndarray, Dict[str, np.ndarray]]) -> None:
        if isinstance(data, dict):
            np.savez_compressed(self.path, **data)  # type: ignore[arg-type]
        else:
            np.savez_compressed(self.path, data=data)


class SaverJSON(Saver):
    """
    Save data as JSON files.

    Suitable for configuration and simple nested structures.

    See Also
    --------
    json.dump : Underlying serialization function.
    """

    EXT = FileExt("json")

    def _save(self, data: Any) -> None:
        import json

        with self.path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)


class SaverYAML(Saver):
    """
    Save data as YAML files.

    Human-readable format for configuration and metadata.

    See Also
    --------
    yaml.safe_dump : Underlying serialization function.
    """

    EXT = FileExt("yaml")

    def _save(self, data: Any) -> None:
        import yaml

        with self.path.open("w", encoding="utf-8") as file:
            yaml.safe_dump(data, file, default_flow_style=False)

    def __init__(self, path: Union[str, Path]) -> None:
        if isinstance(path, str):
            path = Path(path)
        if path.suffix in {".yml", ".yaml"}:
            self.path = path
        else:
            self.path = self.enforce_ext(path, self.EXT)
        if not self.path.parent.exists():
            raise FileNotFoundError(f"Directory does not exist: {self.path.parent}")


class SaverHDF5(Saver):
    """
    Save data to HDF5 files.
    """

    EXT = FileExt("hdf5")

    def _save(self, data: Any) -> None:
        try:
            import h5py
        except ImportError as exc:
            raise RuntimeError("h5py is required for HDF5 support") from exc
        with h5py.File(self.path, "w") as file:
            if isinstance(data, dict):
                for key, value in data.items():
                    file.create_dataset(key, data=value)
            else:
                file.create_dataset("data", data=data)

    def __init__(self, path: Union[str, Path]) -> None:
        if isinstance(path, str):
            path = Path(path)
        if path.suffix in {".h5", ".hdf5"}:
            self.path = path
        else:
            self.path = self.enforce_ext(path, self.EXT)
        if not self.path.parent.exists():
            raise FileNotFoundError(f"Directory does not exist: {self.path.parent}")
