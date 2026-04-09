"""
Base data component class.

Classes
-------
DataComponent
    NumPy ndarray subclass with dimension annotations and metadata propagation.
"""

from typing import Tuple, Self, Mapping, Any, SupportsIndex, Sequence, overload

import numpy as np
from numpy.typing import ArrayLike

from morpha.components.dimensions import Dimensions, DimensionsSpec
from morpha.components.metadata import MetaDataField


class DataComponent(np.ndarray):
    """
    Core component of a data structure with dimension annotations and metadata.

    Subclass of numpy.ndarray that adds:
    - Named dimensions via the `dims` attribute
    - Metadata fields defined by subclasses
    - Automatic propagation of dimensions and metadata through array operations

    Parameters
    ----------
    values : ArrayLike
        Values for the underlying array.
    dims : Dimensions, optional
        Dimension names. If not provided, defaults are used.
    **metadata : Any
        Additional metadata attributes.

    Class Attributes
    ----------------
    DIMENSIONS_SPEC : DimensionsSpec
        Specification of allowed dimensions (names, order, required/optional).
        Define in subclasses.
    METADATA : Mapping[str, MetaDataField]
        Metadata attributes with their types and defaults.
        Define in subclasses.
    DTYPE : np.dtype
        Data type for array values.
        Define in subclasses.
    SENTINEL : int | float | str
        Value marking missing/unset entries.
        Define in subclasses.

    Attributes
    ----------
    dims : Dimensions
        Names for each array dimension.

    Notes
    -----
    Dimension propagation:
    - Operations preserving dimensionality: dims transferred from parent
    - Operations changing dimensionality: dims reset to defaults

    Methods like transpose, swapaxes, moveaxis update dims accordingly.

    Examples
    --------
    Create a DataComponent with dimension names:

    >>> data = DataComponent(np.zeros((10, 5)), dims=Dimensions("units", "time"))
    >>> data.dims
    Dimensions['units', 'time']

    Get dimension information:

    >>> data.get_dim(0)
    'units'
    >>> data.get_axis("time")
    1
    >>> data.get_size("units")
    10
    """

    DIMENSIONS_SPEC: DimensionsSpec
    dims: Dimensions
    METADATA: Mapping[str, MetaDataField]
    DTYPE: np.dtype[Any]
    SENTINEL: int | float | str

    def __repr__(self) -> str:
        if hasattr(self, "METADATA"):
            metadata = ", ".join(f"{attr}={getattr(self, attr, None)}" for attr in self.METADATA)
        else:
            metadata = ""
        return (
            f"{self.__class__.__name__}("
            f"shape={self.shape}, "
            f"dims={getattr(self, 'dims', None)}, "
            f"{metadata})"
        )

    # --- Creation Methods -------------------------------------------------------------------------

    def __new__(cls, values: ArrayLike, dims: Dimensions | None = None, **metadata: Any) -> Self:
        """
        Create a new DataComponent instance.

        Parameters
        ----------
        values : ArrayLike
            Values to store.
        dims : Dimensions, optional
            Dimension names.
        **metadata : Any
            Additional metadata attributes.

        Returns
        -------
        Self
            New instance.

        Raises
        ------
        ValueError
            If dims length doesn't match array dimensions, or
            if dimension names violate DIMENSIONS_SPEC.
        """
        cls.validate(values)

        # Convert to array with optional dtype
        if hasattr(cls, "DTYPE"):
            values = np.asarray(values, dtype=cls.DTYPE)
        else:
            values = np.asarray(values)

        obj = values.view(cls)

        # Set dimensions
        if dims is None:
            dims = Dimensions.default(obj.ndim)
        else:
            if hasattr(cls, "DIMENSIONS_SPEC"):
                cls.DIMENSIONS_SPEC.validate(dims)

        if len(dims) != obj.ndim:
            raise ValueError(f"len(dims) = {len(dims)} != array.ndim = {obj.ndim}")

        obj.dims = dims

        # Set metadata with type validation and default values
        if hasattr(cls, "METADATA"):
            for attr, field in cls.METADATA.items():
                value = metadata.get(attr, field.default_value)
                if value is not None and not isinstance(value, field.field_type):
                    raise TypeError(
                        f"Metadata '{attr}' expects type {field.field_type.__name__}, "
                        f"got {type(value).__name__}"
                    )
                setattr(obj, attr, value)
        else:
            for attr, value in metadata.items():
                setattr(obj, attr, value)

        return obj

    def __array_finalize__(self, obj: np.ndarray | None) -> None:
        """
        Finalize creation by propagating dimensions and metadata.

        Parameters
        ----------
        obj : np.ndarray or None
            Source array from which this instance was created.
        """
        if obj is None:
            return
        self.propagate_dimensions(obj, self)
        self.propagate_metadata(obj, self)

    @classmethod
    def validate(cls, values: ArrayLike) -> None:
        """
        Validate input values before array creation.

        Override in subclasses for specific validation.

        Parameters
        ----------
        values : ArrayLike
            Input values to validate.
        """

    @classmethod
    def propagate_dimensions(cls, parent: np.ndarray, child: Self) -> None:
        """
        Propagate dimensions from parent to child array.

        If dimensionality is preserved, transfers dims. Otherwise resets to defaults.

        Parameters
        ----------
        parent : np.ndarray
            Source array.
        child : Self
            Target array to update.
        """
        if parent.ndim == child.ndim:
            dims = getattr(parent, "dims", Dimensions.default(parent.ndim))
        else:
            dims = Dimensions.default(child.ndim)
        setattr(child, "dims", dims)

    @classmethod
    def propagate_metadata(cls, parent: np.ndarray, child: Self) -> None:
        """
        Propagate metadata from parent to child array.

        Transfers metadata attributes defined in METADATA from parent.

        Parameters
        ----------
        parent : np.ndarray
            Source array.
        child : Self
            Target array to update.
        """
        if hasattr(cls, "METADATA"):
            for attr in cls.METADATA:
                setattr(child, attr, getattr(parent, attr, None))

    def wrap(self, obj: np.ndarray) -> Self:
        """
        Cast a numpy array to this DataComponent type.

        Parameters
        ----------
        obj : np.ndarray
            Array to cast.

        Returns
        -------
        Self
            Array cast to current class.
        """
        if isinstance(obj, np.ndarray):
            return obj.view(type(self))
        return obj

    @classmethod
    def from_shape(
        cls, shape: int | Tuple[int, ...], dims: Dimensions | None = None, **metadata: Any
    ) -> Self:
        """
        Create an empty instance filled with the sentinel value.

        Parameters
        ----------
        shape : int or Tuple[int, ...]
            Shape of the array. Integer creates 1D array.
        dims : Dimensions, optional
            Dimension names.
        **metadata : Any
            Additional metadata attributes.

        Returns
        -------
        Self
            Instance filled with SENTINEL value.
        """
        if isinstance(shape, int):
            shape = (shape,)
        values = np.full(shape=shape, fill_value=cls.SENTINEL, dtype=cls.DTYPE)
        return cls(values, dims=dims, **metadata)

    # --- Getter Methods ---------------------------------------------------------------------------

    def get_dim(self, axis: int) -> str:
        """
        Get dimension name by axis index.

        Parameters
        ----------
        axis : int
            Axis index.

        Returns
        -------
        str
            Dimension name.
        """
        return self.dims.get_dim(axis)

    def get_axis(self, dim: str) -> int:
        """
        Get axis index by dimension name.

        Parameters
        ----------
        dim : str
            Dimension name.

        Returns
        -------
        int
            Axis index.
        """
        return self.dims.get_axis(dim)

    def get_size(self, dim: str) -> int:
        """
        Get the length of a dimension.

        Parameters
        ----------
        dim : str
            Dimension name.

        Returns
        -------
        int
            Size along that dimension.
        """
        return self.shape[self.get_axis(dim)]

    def get_missing(self) -> np.ndarray:
        """
        Get boolean mask for missing values (equal to SENTINEL).

        Returns
        -------
        np.ndarray
            Boolean mask with True for missing values.
        """
        # Handle NaN sentinel specially since NaN != NaN
        if isinstance(self.SENTINEL, float) and np.isnan(self.SENTINEL):
            return np.isnan(self)
        return self == self.SENTINEL

    # --- Overridden NumPy Methods -----------------------------------------------------------------

    def __getitem__(self, index: Any) -> Self:
        """
        Get subset with DataComponent type and propagated attributes.

        Parameters
        ----------
        index : Any
            Array index or slice.

        Returns
        -------
        Self
            Subset with propagated dimensions and metadata.
        """
        result = super().__getitem__(index)
        if isinstance(result, np.ndarray) and not isinstance(result, DataComponent):
            result = self.wrap(result)
            self.propagate_dimensions(self, result)
            self.propagate_metadata(self, result)
        return result

    def __array_ufunc__(
        self,
        ufunc: np.ufunc,
        method: str,
        *inputs: np.ndarray,
        **kwargs: Any,
    ) -> Any:
        """
        Apply ufunc and maintain DataComponent type.

        Converts inputs to plain arrays, applies ufunc, then wraps result.

        Parameters
        ----------
        ufunc : np.ufunc
            Universal function to apply.
        method : str
            Ufunc method name (e.g. ``"__call__"``, ``"reduce"``).
        *inputs : np.ndarray
            Input arrays.
        **kwargs : Any
            Additional keyword arguments forwarded to the ufunc.

        Returns
        -------
        Any
            Result with DataComponent type when applicable.
        """
        args = [i.view(np.ndarray) if isinstance(i, DataComponent) else i for i in inputs]
        result = getattr(ufunc, method)(*args, **kwargs)

        if result is NotImplemented:
            return NotImplemented
        if isinstance(result, np.ndarray):
            result = self.wrap(result)
            self.propagate_dimensions(self, result)
            self.propagate_metadata(self, result)
            return result
        if isinstance(result, tuple):
            wrapped = []
            for item in result:
                if isinstance(item, np.ndarray):
                    item = self.wrap(item)
                    self.propagate_dimensions(self, item)
                    self.propagate_metadata(self, item)
                wrapped.append(item)
            return tuple(wrapped)
        return result

    @overload
    def transpose(self, axes: SupportsIndex | Sequence[SupportsIndex] | None, /) -> Self: ...
    @overload
    def transpose(self, *axes: SupportsIndex) -> Self: ...

    def transpose(
        self, *axes: SupportsIndex | Sequence[SupportsIndex] | None
    ) -> Self:
        """
        Transpose array and update dimension names.

        Parameters
        ----------
        *axes : SupportsIndex | Sequence[SupportsIndex] | None
            New axis order. If empty, reverses axes.

        Returns
        -------
        Self
            Transposed array with updated dims.
        """
        result = super().transpose(*axes)  # type: ignore[arg-type]
        # Handle the case when numpy passes a single list as axes
        if axes and len(axes) == 1 and isinstance(axes[0], (list, tuple)):
            dim_axes: tuple[int, ...] | None = tuple(int(a) for a in axes[0])  # type: ignore[union-attr]
        elif axes:
            dim_axes = tuple(int(a) for a in axes if a is not None)  # type: ignore[arg-type]
        else:
            dim_axes = None
        result.dims = self.dims.transpose(dim_axes)
        return result

    @property
    def T(self) -> Self:
        """
        Return transposed array with updated dims.

        Returns
        -------
        Self
            Transposed view.
        """
        return self.transpose()

    def swapaxes(self, axis1: SupportsIndex, axis2: SupportsIndex) -> Self:
        """
        Swap two axes and update dimension names.

        Parameters
        ----------
        axis1, axis2 : SupportsIndex
            Axes to swap.

        Returns
        -------
        Self
            Array with swapped axes and updated dims.
        """
        result = super().swapaxes(axis1, axis2)
        result = self.wrap(result)
        result.dims = self.dims.swap(int(axis1), int(axis2))
        return result

    def moveaxis(self, source: int, destination: int) -> Self:
        """
        Move an axis to a new position and update dimension names.

        Parameters
        ----------
        source : int
            Original axis position.
        destination : int
            Target axis position.

        Returns
        -------
        Self
            Array with moved axis and updated dims.
        """
        result = np.moveaxis(self, source, destination)
        result = self.wrap(result)
        result.dims = self.dims.move(source, destination)
        return result

    def rollaxis(self, axis: int, start: int = 0) -> Self:
        """
        Roll the specified axis to a given position.

        Not implemented — requires manual dimension update.

        Parameters
        ----------
        axis : int
            Axis to roll.
        start : int, optional
            Target position, by default 0.

        Raises
        ------
        NotImplementedError
            Always raised; update dimension names manually.
        """
        raise NotImplementedError("Update dimension names manually after rollaxis.")

    def flip(self, axis: int) -> Self:
        """
        Reverse elements along the given axis.

        Not implemented — requires manual dimension update.

        Parameters
        ----------
        axis : int
            Axis to reverse.

        Raises
        ------
        NotImplementedError
            Always raised; update dimension names manually.
        """
        raise NotImplementedError("Update dimension names manually after flip.")
