"""
Generic typed container.

Classes
-------
Container
    Type-checked dictionary-like container.
"""

from collections import UserDict
from typing import (
    List,
    Callable,
    Any,
    Iterable,
    Tuple,
    Dict,
    Self,
    TypeVar,
    Generic,
    Type,
)


K = TypeVar("K")
"""Type variable for container keys."""

V = TypeVar("V")
"""Type variable for container values."""

Q = TypeVar("Q")
"""Type variable for input dictionary keys."""

R = TypeVar("R")
"""Type variable for function return types."""

C = TypeVar("C", bound="Container")
"""Type variable for Container subclasses."""


class Container(UserDict[K, V], Generic[K, V]):
    """
    Type-checked dictionary container with utility methods.

    Extends UserDict with type validation and functional operations.

    Parameters
    ----------
    *args
        Arguments passed to UserDict.
    key_type : Type[K]
        Expected type for keys.
    value_type : Type[V]
        Expected type for values.
    **kwargs
        Keyword arguments passed to UserDict.

    Attributes
    ----------
    key_type : Type[K]
        Type constraint for keys.
    value_type : Type[V]
        Type constraint for values.

    Examples
    --------
    Create a container with type constraints:

    >>> container = Container({1: "a", 2: "b"}, key_type=int, value_type=str)
    >>> container[1]
    'a'

    Type validation on assignment:

    >>> container[3] = 123  # Raises TypeError - expected str value
    """

    def __init__(
        self,
        *args: Any,
        key_type: Type[K] | None = None,
        value_type: Type[V] | None = None,
        **kwargs: Any,
    ) -> None:
        if key_type is None:
            raise ValueError(f"Missing argument: `key_type` for {self.__class__.__name__}")
        if value_type is None:
            raise ValueError(f"Missing argument: `value_type` for {self.__class__.__name__}")
        self.key_type: Type[K] = key_type
        self.value_type: Type[V] = value_type
        super().__init__(*args, **kwargs)

    def __setitem__(self, key: K, value: V) -> None:
        """Set item with type checking."""
        if not isinstance(key, self.key_type):
            raise TypeError(
                f"Invalid key type: {type(key).__name__} instead of {self.key_type.__name__}"
            )
        if not isinstance(value, self.value_type):
            raise TypeError(
                f"Invalid value type: {type(value).__name__} instead of {self.value_type.__name__}"
            )
        super().__setitem__(key, value)

    @classmethod
    def from_keys(
        cls: Type[C],
        keys: Iterable[K],
        fill_value: V,
        *,
        key_type: Type[K] | None = None,
        value_type: Type[V] | None = None,
    ) -> C:
        """
        Create container from keys with a fill value.

        Parameters
        ----------
        keys : Iterable[K]
            Keys to initialize.
        fill_value : V
            Default value for all keys.
        key_type : Type[K]
            Expected type for keys.
        value_type : Type[V]
            Expected type for values.

        Returns
        -------
        Container
            New container with specified keys and fill value.
        """
        if key_type is None:
            raise ValueError("Missing argument: `key_type`")
        if value_type is None:
            raise ValueError("Missing argument: `value_type`")
        return cls({key: fill_value for key in keys}, key_type=key_type, value_type=value_type)

    def list_keys(self) -> List[K]:
        """Get list of keys."""
        return list(self.data.keys())

    def list_values(self, keys: Iterable[K] | None = None) -> List[V]:
        """
        Get list of values, optionally for specific keys.

        Parameters
        ----------
        keys : Iterable[K], optional
            Keys to get values for. If None, returns all values.

        Returns
        -------
        List[V]
            List of values.
        """
        if keys is None:
            return list(self.data.values())
        return [self.data[k] for k in keys]

    def to_dict(self) -> Dict[K, V]:
        """Convert to plain dictionary."""
        return dict(self.data)

    def get_subset(self, keys: Iterable[K]) -> Self:
        """
        Get a subset by keys.

        Parameters
        ----------
        keys : Iterable[K]
            Keys to include.

        Returns
        -------
        Container
            New container with subset of data.
        """
        subset_data = {k: v for k, v in self.data.items() if k in keys}
        return self.__class__(subset_data, key_type=self.key_type, value_type=self.value_type)

    def filter_on_keys(self, predicate: Callable[[K], bool]) -> Self:
        """
        Filter by key predicate.

        Parameters
        ----------
        predicate : Callable[[K], bool]
            Function returning True for keys to keep.

        Returns
        -------
        Container
            Filtered container.
        """
        return self.get_subset([k for k in self.data.keys() if predicate(k)])

    def filter_on_values(self, predicate: Callable[[V], bool]) -> Self:
        """
        Filter by value predicate.

        Parameters
        ----------
        predicate : Callable[[V], bool]
            Function returning True for values to keep.

        Returns
        -------
        Container
            Filtered container.
        """
        return self.get_subset([k for k, v in self.data.items() if predicate(v)])

    def fill(self, func: Callable[[K], V], **kwargs: Any) -> None:
        """
        Generate values from keys using a function.

        Parameters
        ----------
        func : Callable[[K], V]
            Function taking key and returning value.
        **kwargs
            Additional arguments for func.
        """
        for key in self.data.keys():
            self[key] = func(key, **kwargs)

    def apply(self, func: Callable[[V], R], **kwargs: Any) -> "Container[K, R]":
        """
        Apply function to all values.

        Parameters
        ----------
        func : Callable[[V], R]
            Function to apply.
        **kwargs
            Additional arguments for func.

        Returns
        -------
        Container[K, R]
            New container with transformed values.
        """
        result_data = {k: func(v, **kwargs) for k, v in self.data.items()}
        _, result_type = self.find_types(result_data)
        return self.__class__(result_data, key_type=self.key_type, value_type=result_type)

    @staticmethod
    def find_types(data: Dict[Q, R]) -> Tuple[Type[Q], Type[R]]:
        """
        Determine types from dictionary contents.

        Parameters
        ----------
        data : Dict[Q, R]
            Dictionary to analyze.

        Returns
        -------
        Tuple[Type[Q], Type[R]]
            Key and value types.

        Raises
        ------
        TypeError
            If data is empty.
        """
        if data:
            first_key = next(iter(data.keys()))
            key_type = type(first_key)
            first_value = next(iter(data.values()))
            value_type = type(first_value)
        else:
            raise TypeError("Cannot determine types for an empty dictionary")
        return key_type, value_type
