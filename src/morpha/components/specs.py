"""Component specification for data structures."""

from types import MappingProxyType
from typing import Dict, Type, TYPE_CHECKING

if TYPE_CHECKING:
    from morpha.components.base import DataComponent


class ComponentSpec:
    """
    Specification of data components allowed in a data structure.

    Validates that components assigned to a data structure have the correct
    attribute names and types.

    Parameters
    ----------
    **kwargs : Type[DataComponent]
        Component names as keys and their expected types as values.

    Examples
    --------
    Define a specification:

    >>> spec = ComponentSpec(data=CoreData, time=CoordTime)

    Validate a component:

    >>> data = CoreData(np.zeros(10))
    >>> spec.validate("data", data)  # OK

    >>> spec.validate("data", time_coord)  # Raises TypeError
    """

    def __init__(self, **kwargs: Type["DataComponent"]) -> None:
        if len(set(kwargs.keys())) != len(kwargs):
            raise ValueError("Duplicate component names in the specification.")
        self._spec: Dict[str, Type["DataComponent"]] = dict(kwargs)

    @property
    def spec(self):
        """
        Return read-only mapping of attribute names to expected component types.

        Returns
        -------
        MappingProxyType
            Immutable view of the specification.
        """
        return MappingProxyType(self._spec)

    def validate(self, name: str, component: "DataComponent") -> None:
        """
        Validate a component against the specification.

        Parameters
        ----------
        name : str
            Attribute name for the component.
        component : DataComponent
            Component instance to validate.

        Raises
        ------
        AttributeError
            If the name is not in the specification.
        TypeError
            If the component type does not match the expected type.
        """
        if name not in self._spec:
            raise AttributeError(f"Invalid component name: '{name}' not in {self._spec.keys()}.")
        if not isinstance(component, self._spec[name]):
            raise TypeError(
                f"Invalid component type for '{name}': {type(component)} != {self._spec[name]}"
            )

    def __contains__(self, name: str) -> bool:
        """
        Check if a name is in the specification.

        Parameters
        ----------
        name : str
            Component name to look up.

        Returns
        -------
        bool
            True if the name is registered.
        """
        return name in self._spec

    def __iter__(self):
        """
        Return an iterator over registered component names.

        Returns
        -------
        Iterator[str]
            Iterator yielding component names.
        """
        return iter(self._spec)

    def keys(self):
        """
        Return component names.

        Returns
        -------
        KeysView
            View of component names.
        """
        return self._spec.keys()

    def values(self):
        """
        Return expected component types.

        Returns
        -------
        ValuesView
            View of component types.
        """
        return self._spec.values()

    def items(self):
        """
        Return (name, type) pairs.

        Returns
        -------
        ItemsView
            View of (name, type) pairs.
        """
        return self._spec.items()
