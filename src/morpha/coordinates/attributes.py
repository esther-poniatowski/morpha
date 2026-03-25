"""
Attribute mixin for coordinate values.

Classes
-------
Attribute
    Mixin providing validation and labeling for coordinate value types.
"""

from typing import (
    Generic,
    TypeVar,
    Mapping,
    FrozenSet,
    Any,
    cast,
    Iterable,
    Union,
    List,
    Tuple,
    Type,
    Set,
)


BaseT = TypeVar("BaseT", int, str, float, bool)
"""Type variable for the basic type from which the attribute inherits."""


class Attribute(Generic[BaseT]):
    """
    Mixin class for attribute types with validation and labeling.

    Provides a common interface for types representing categorical or
    constrained values that can be used in coordinates.

    Class Attributes
    ----------------
    OPTIONS : FrozenSet[BaseT]
        Valid values for this attribute type.
    LABELS : Mapping[BaseT, str]
        Human-readable labels for valid values.

    Examples
    --------
    Define a categorical attribute:

    >>> class Task(str, Attribute[str]):
    ...     OPTIONS = frozenset(["PTD", "CLK"])
    ...     LABELS = {"PTD": "Pursuit Tracking", "CLK": "Clock Task"}
    ...
    ...     def __new__(cls, value: str):
    ...         if not cls.is_valid(value):
    ...             raise ValueError(f"Invalid value: {value}")
    ...         return super().__new__(cls, value)

    Use the attribute:

    >>> task = Task("PTD")
    >>> task.full_label
    'Pursuit Tracking'

    Check validity:

    >>> Task.is_valid("PTD")
    True
    >>> Task.is_valid("INVALID")
    False

    Notes
    -----
    This mixin doesn't define __new__ or __init__. It's designed to be
    combined with a built-in type (int, str, float, bool) via multiple
    inheritance. Subclasses should implement their own constructor.
    """

    OPTIONS: FrozenSet[BaseT]
    LABELS: Mapping[BaseT, str]

    @classmethod
    def is_valid(cls, value: Any) -> bool:
        """
        Check if a value is valid for this attribute type.

        Parameters
        ----------
        value : Any
            Value to check.

        Returns
        -------
        bool
            True if value is in OPTIONS.

        Note
        ----
        Override in subclasses if validation is more complex than
        checking membership in OPTIONS.
        """
        return value in cls.OPTIONS

    @property
    def full_label(self) -> str:
        """Human-readable label for this value."""
        return self.LABELS.get(cast(BaseT, self), "")

    @classmethod
    def get_options(cls) -> FrozenSet[BaseT]:
        """Get all valid options."""
        return cls.OPTIONS

    @classmethod
    def get_labels(cls) -> Mapping[BaseT, str]:
        """Get all labels."""
        return cls.LABELS

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>({super().__repr__()})"

    @classmethod
    def from_container(
        cls,
        values: Iterable[BaseT],
        container: Type[Union[List[Any], Tuple[Any, ...], Set[Any]]] = list,
    ) -> Union[List["Attribute[BaseT]"], Tuple["Attribute[BaseT]", ...], Set["Attribute[BaseT]"]]:
        """
        Create multiple attribute instances from an iterable.

        Parameters
        ----------
        values : Iterable[BaseT]
            Values to convert.
        container : Type
            Container type for results (list, tuple, or set).

        Returns
        -------
        Union[List[BaseT], Tuple[BaseT, ...], Set[BaseT]]
            Container of attribute instances.

        Raises
        ------
        ValueError
            If any value is invalid.
        """
        instances: List[Attribute[BaseT]] = []
        for value in values:
            if not cls.is_valid(value):
                raise ValueError(f"Invalid value for {cls.__name__}: {value}")
            instances.append(cast(Attribute[BaseT], cls(value)))
        return container(instances)
