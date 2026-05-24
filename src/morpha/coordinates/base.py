"""Base coordinate class."""

from typing import Type, TypeVar, Generic, Any

import numpy as np
from numpy.typing import ArrayLike

from morpha.components.base import DataComponent
from morpha.coordinates.attributes import Attribute


AnyAttribute = TypeVar("AnyAttribute", bound=Attribute[Any])
"""Type variable for the attribute type associated with coordinate labels."""


class Coordinate(DataComponent, Generic[AnyAttribute]):
    """
    Base class for coordinates representing labeled axes.

    A Coordinate is a DataComponent that holds axis labels, with validation
    based on an associated Attribute type.

    Notes
    -----
    The `validate` method checks that all values are valid for the
    associated ATTRIBUTE type using `Attribute.is_valid`.

    See Also
    --------
    DataComponent : Base class.
    Attribute : Mixin for coordinate value types.

    Examples
    --------
    Define a coordinate class:

    >>> class CoordTask(Coordinate[Task]):
    ...     ATTRIBUTE = Task
    ...     DIMENSIONS_SPEC = DimensionsSpec(trials=True)

    Create coordinate instances:

    >>> coord = CoordTask(["PTD", "PTD", "CLK"])
    >>> coord.get_attribute()
    <class 'Task'>
    """

    ATTRIBUTE: Type[AnyAttribute]
    """Attribute type for valid coordinate values. Set on subclasses;
    determines the data type and valid values for the array."""

    @classmethod
    def validate(cls, values: ArrayLike, **kwargs: Any) -> None:
        """
        Validate coordinate values against the attribute type.

        Parameters
        ----------
        values : ArrayLike
            Values to validate.
        **kwargs : Any
            Additional validation arguments.

        Raises
        ------
        ValueError
            If any value is not valid for the ATTRIBUTE type.

        Note
        ----
        Override in subclasses for custom validation logic.
        The default implementation uses ATTRIBUTE.is_valid for validation.
        """
        if hasattr(cls, "ATTRIBUTE"):
            mask = cls.are_valid(values)
            if not np.all(mask):
                raise ValueError(f"Invalid values for {cls.__name__}")

    @classmethod
    def get_attribute(cls) -> Type[AnyAttribute]:
        """
        Get the associated attribute type.

        Returns
        -------
        Type[AnyAttribute]
            The ATTRIBUTE class.
        """
        return cls.ATTRIBUTE

    @classmethod
    def has_attribute(cls, attribute_type: Type[Attribute[Any]]) -> bool:
        """
        Check if coordinate is associated with an attribute type.

        Parameters
        ----------
        attribute_type : Type[Attribute[Any]]
            Attribute type to check for.

        Returns
        -------
        bool
            True if ATTRIBUTE is the same type or a subclass.
        """
        return issubclass(cls.get_attribute(), attribute_type)

    @classmethod
    def are_valid(cls, values: ArrayLike) -> np.ndarray:
        """
        Get boolean mask of valid values.

        Parameters
        ----------
        values : ArrayLike
            Values to check.

        Returns
        -------
        np.ndarray
            Boolean array with True for valid values.
        """
        values = np.asarray(values)
        return np.vectorize(cls.ATTRIBUTE.is_valid)(values)
