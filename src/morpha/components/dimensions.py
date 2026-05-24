"""Dimension management for data components."""

from collections import UserList, OrderedDict
from types import MappingProxyType
from typing import Self, Tuple


class Dimensions(UserList[str]):
    """
    Dimension names to label the axes of a data component or data structure.

    Provides utility methods to examine and manipulate dimensions, which can be
    used by wrapper objects via delegation.

    Parameters
    ----------
    *args : str
        Names of the dimensions.

    Class Attributes
    ----------------
    DEFAULT : str
        Default dimension name for unlabeled axes.

    Attributes
    ----------
    data : list[str]
        Underlying list of dimension names (inherited from UserList).

    Examples
    --------
    Create dimension names:

    >>> dims = Dimensions("time", "trials", "units")
    >>> dims.ndim
    3

    Get dimension by index:

    >>> dims.get_dim(0)
    'time'

    Get axis by name:

    >>> dims.get_axis("trials")
    1

    Check subset relationship:

    >>> partial = Dimensions("time", "trials")
    >>> partial.is_subset(dims)
    True
    """

    DEFAULT: str = ""

    def __init__(self, *args: str) -> None:
        # Allow duplicate empty strings (default values), but not other duplicates
        non_empty = [a for a in args if a != self.DEFAULT]
        if len(set(non_empty)) != len(non_empty):
            raise ValueError(f"Duplicate dimension names: {args}")
        super().__init__(args)

    def __repr__(self) -> str:
        return f"Dimensions{super().__repr__()}"

    @classmethod
    def default(cls, ndim: int) -> Self:
        """
        Create default dimensions with empty names.

        Parameters
        ----------
        ndim : int
            Number of dimensions.

        Returns
        -------
        Self
            Dimensions with empty string names.
        """
        return cls(*[cls.DEFAULT for _ in range(ndim)])

    @property
    def ndim(self) -> int:
        """
        Return the number of dimensions.

        Returns
        -------
        int
            Number of dimensions.
        """
        return len(self)

    def get_dim(self, axis: int) -> str:
        """
        Get dimension name by axis index.

        Parameters
        ----------
        axis : int
            Index of the axis.

        Returns
        -------
        str
            Name of the dimension.

        Raises
        ------
        IndexError
            If axis is out of bounds.
        """
        if axis >= self.ndim:
            raise IndexError(f"Invalid dimension index: {axis} >= ndim {self.ndim}.")
        return self[axis]

    def get_axis(self, name: str) -> int:
        """
        Get axis index by dimension name.

        Parameters
        ----------
        name : str
            Name of the dimension.

        Returns
        -------
        int
            Axis number associated with the dimension.

        Raises
        ------
        ValueError
            If the dimension name is not found.
        """
        if name not in self:
            raise ValueError(f"Invalid dimension name: '{name}' not among the dimensions.")
        return self.index(name)

    def is_subset(self, other: Self) -> bool:
        """
        Check if dimensions are a subset of another.

        Parameters
        ----------
        other : Dimensions
            Dimensions to compare against.

        Returns
        -------
        bool
            True if all names are present in *other*.
        """
        return set(self).issubset(set(other))

    def is_ordered_as(self, other: Self) -> bool:
        """
        Check if common dimensions are in the same order.

        Only considers dimensions present in both objects.

        Parameters
        ----------
        other : Dimensions
            Dimensions to compare against.

        Returns
        -------
        bool
            True if common dimensions appear in the same relative order.
        """
        common_dims = set(self) & set(other)
        order_self = [d for d in self if d in common_dims]
        order_other = [d for d in other if d in common_dims]
        return order_self == order_other

    @classmethod
    def intersection(cls, *dims: Self) -> Self:
        """
        Get common dimensions between multiple Dimensions objects.

        Parameters
        ----------
        *dims : Dimensions
            Two or more Dimensions objects to intersect.

        Returns
        -------
        Dimensions
            Dimensions present in all inputs.
        """
        common = set(dims[0])
        for dim in dims[1:]:
            common &= set(dim)
        return cls(*common)

    def add(self, name: str = DEFAULT, axis: int = -1) -> None:
        """
        Add a dimension at a specific position.

        Parameters
        ----------
        name : str, optional
            Name of the dimension.
        axis : int, optional
            Index position, -1 for last position.

        Raises
        ------
        ValueError
            If dimension name already exists (except for empty default names).
        IndexError
            If axis is out of bounds.
        """
        # Allow adding empty default names, but not duplicate non-empty names
        if name != self.DEFAULT and name in self:
            raise ValueError(f"Duplicate dimension name: '{name}' already exists.")
        if axis < 0:
            axis = self.ndim + axis + 1
        if axis < 0 or axis > self.ndim:
            raise IndexError(f"Invalid axis index: {axis} out of bounds.")
        self.insert(axis, name)

    def transpose(self, axes: Tuple[int, ...] | list[int] | None = None) -> Self:
        """
        Reorder dimensions.

        Parameters
        ----------
        axes : Tuple[int, ...] or list[int], optional
            New axis order. If None, reverses order.

        Returns
        -------
        Self
            Reordered dimensions.
        """
        if axes is None:
            axes = tuple(range(self.ndim - 1, -1, -1))
        elif isinstance(axes, list):
            axes = tuple(axes)
        return self.__class__(*[self[axis] for axis in axes])

    def swap(self, axis1: int, axis2: int) -> Self:
        """
        Swap two dimensions.

        Parameters
        ----------
        axis1, axis2 : int
            Indices of dimensions to swap.

        Returns
        -------
        Self
            New instance with swapped dimensions.
        """
        for axis in [axis1, axis2]:
            if axis < 0 or axis >= self.ndim:
                raise IndexError(f"Invalid axis index for {self.ndim} dimensions: {axis}.")
        new_dims = list(self)
        new_dims[axis1], new_dims[axis2] = new_dims[axis2], new_dims[axis1]
        return self.__class__(*new_dims)

    def move(self, source: int | list[int], destination: int | list[int]) -> Self:
        """
        Move dimensions to new positions.

        Parameters
        ----------
        source : int | list[int]
            Indices of axes to move.
        destination : int | list[int]
            New positions for the axes.

        Returns
        -------
        Self
            New instance with moved dimensions.
        """
        if isinstance(source, int):
            source = [source]
        if isinstance(destination, int):
            destination = [destination]
        new_dims = list(self)
        for src, dest in zip(source, destination):
            new_dims.insert(dest, new_dims.pop(src))
        return self.__class__(*new_dims)


class DimensionsSpec:
    """
    Specification for dimension names in a data structure.

    Defines which dimensions are required vs optional, and their expected order.

    Parameters
    ----------
    **kwargs : bool
        Dimension names as keys, with True for required and False for optional.

    Examples
    --------
    >>> spec = DimensionsSpec(units=False, trials=True, time=False)
    >>> spec.required()
    Dimensions['trials']
    >>> spec.optional()
    Dimensions['units', 'time']
    """

    def __init__(self, **kwargs: bool) -> None:
        if len(set(kwargs.keys())) != len(kwargs):
            raise ValueError("Duplicate dimension names in the specification.")
        self._spec: OrderedDict[str, bool] = OrderedDict(kwargs)

    @property
    def spec(self):
        """
        Return read-only ordered mapping of dimension names to required status.

        Returns
        -------
        MappingProxyType
            Immutable view of the specification.
        """
        return MappingProxyType(self._spec)

    def required(self) -> Dimensions:
        """
        Get required dimensions.

        Returns
        -------
        Dimensions
            Dimensions marked as required.
        """
        return Dimensions(*[dim for dim, req in self._spec.items() if req])

    def optional(self) -> Dimensions:
        """
        Get optional dimensions.

        Returns
        -------
        Dimensions
            Dimensions marked as optional.
        """
        return Dimensions(*[dim for dim, req in self._spec.items() if not req])

    def validate(self, dims: Dimensions) -> None:
        """
        Validate dimensions against the specification.

        Parameters
        ----------
        dims : Dimensions
            Dimensions to validate.

        Raises
        ------
        ValueError
            If required dimensions are missing, extra dimensions are present,
            or dimensions are in incorrect order.
        """
        dims_set = set(dims)
        spec_set = set(self._spec.keys())

        # Check for missing required and extra dimensions
        missing = [dim for dim, req in self._spec.items() if req and dim not in dims_set]
        extra = [dim for dim in dims_set if dim not in spec_set]

        if missing:
            raise ValueError(f"Missing required dimensions: {missing}")
        if extra:
            raise ValueError(f"Extra dimensions not allowed: {extra}")

        # Check order
        spec_order = [dim for dim in self._spec.keys() if dim in dims]
        actual_order = list(dims)
        if spec_order != actual_order:
            raise ValueError(f"Incorrect order: {actual_order} instead of {spec_order}.")
