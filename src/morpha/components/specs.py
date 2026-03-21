"""
Component specification for data structures.

Classes
-------
ComponentSpec
    Specification of allowed data components in a data structure.
"""

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

    Attributes
    ----------
    spec : Dict[str, Type[DataComponent]]
        Mapping of attribute names to expected component types.

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
        self.spec: Dict[str, Type["DataComponent"]] = kwargs

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
        if name not in self.spec:
            raise AttributeError(f"Invalid component name: '{name}' not in {self.spec.keys()}.")
        if not isinstance(component, self.spec[name]):
            raise TypeError(
                f"Invalid component type for '{name}': {type(component)} != {self.spec[name]}"
            )

    def __contains__(self, name: str) -> bool:
        """Check if a name is in the specification."""
        return name in self.spec

    def __iter__(self):
        """Iterate over component names."""
        return iter(self.spec)

    def keys(self):
        """Return component names."""
        return self.spec.keys()

    def values(self):
        """Return expected component types."""
        return self.spec.values()

    def items(self):
        """Return (name, type) pairs."""
        return self.spec.items()
