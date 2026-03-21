"""
Base I/O classes.

Classes
-------
FileExt
    File extension type with validation.
IOHandler
    Abstract base class for file I/O operations.
"""

from abc import ABC
from pathlib import Path
from typing import Union, Self


class FileExt(str):
    """
    Validated file extension.

    A string subclass that ensures the extension is valid and
    properly formatted with a leading period.

    Class Attributes
    ----------------
    OPTIONS : frozenset[str]
        Valid extension values.

    Parameters
    ----------
    ext : str
        File extension (with or without leading period).

    Examples
    --------
    >>> ext = FileExt("pkl")
    >>> str(ext)
    '.pkl'

    >>> FileExt("xyz")  # Raises ValueError
    """

    OPTIONS = frozenset({".csv", ".npy", ".npz", ".pkl", ".yml", ".yaml", ".json", ".h5", ".hdf5"})

    def __new__(cls, ext: str) -> Self:
        ext = cls.add_period(ext)
        if not cls.is_valid(ext):
            raise ValueError(f"Invalid file extension: {ext} not in {cls.OPTIONS}")
        return super().__new__(cls, ext)

    @classmethod
    def is_valid(cls, ext: str) -> bool:
        """Check if extension is valid."""
        return ext in cls.OPTIONS

    @staticmethod
    def add_period(ext: str) -> str:
        """Add leading period if missing."""
        if not ext.startswith("."):
            ext = "." + ext
        return ext


class IOHandler(ABC):
    """
    Abstract base class for file I/O operations.

    Provides common functionality for Saver and Loader classes:
    - Path handling with extension enforcement
    - Consistent interface for file operations

    Class Attributes
    ----------------
    EXT : FileExt
        File extension for this handler.

    Attributes
    ----------
    path : Path
        File path with enforced extension.

    Parameters
    ----------
    path : str or Path
        Path to the file.

    Examples
    --------
    Subclass to create specific handlers:

    >>> class MyHandler(IOHandler):
    ...     EXT = FileExt("pkl")
    ...     def process(self, data): ...

    >>> handler = MyHandler("data/file")
    >>> handler.path
    PosixPath('data/file.pkl')

    See Also
    --------
    Saver : For saving data to files.
    Loader : For loading data from files.
    """

    EXT: FileExt

    def __init__(self, path: Union[str, Path]) -> None:
        if isinstance(path, str):
            path = Path(path)
        self.path = self.enforce_ext(path, self.EXT)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}> Path: {self.path}"

    @staticmethod
    def enforce_ext(path: Union[str, Path], ext: Union[str, FileExt]) -> Path:
        """
        Enforce a specific extension on a path.

        Parameters
        ----------
        path : str or Path
            File path.
        ext : str or FileExt
            Required extension.

        Returns
        -------
        Path
            Path with the specified extension.
        """
        if isinstance(path, str):
            path = Path(path)
        if isinstance(ext, str):
            ext = FileExt(ext)
        return path.with_suffix(ext)
