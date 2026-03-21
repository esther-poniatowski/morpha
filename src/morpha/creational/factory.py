"""
Factory pattern for creating data components.

Classes
-------
Factory
    Abstract base class for creating data components.
"""

from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Type, Tuple, Any

from morpha.components.base import DataComponent


Products = TypeVar("Products", bound="DataComponent | Tuple[DataComponent, ...]")
"""Type variable for products created by a factory."""


class Factory(Generic[Products], ABC):
    """
    Abstract base class for creating data components.

    Factories encapsulate the logic for creating one or more coupled
    DataComponent instances from raw inputs.

    Class Attributes
    ----------------
    PRODUCT_CLASSES : Type[DataComponent] | Tuple[Type[DataComponent], ...]
        Class(es) of products this factory creates.

    Examples
    --------
    Define a concrete factory:

    >>> class TimeCoordFactory(Factory[CoordTime]):
    ...     PRODUCT_CLASSES = CoordTime
    ...
    ...     def create(self, timestamps: np.ndarray, unit: str) -> CoordTime:
    ...         return CoordTime(timestamps, time_unit=unit)

    Use the factory:

    >>> factory = TimeCoordFactory()
    >>> coord = factory.create(np.arange(100), unit="ms")

    Notes
    -----
    Factories are useful when:
    - Creating a component requires complex processing of inputs
    - Multiple related components must be created together
    - The creation logic should be reusable and testable

    See Also
    --------
    Builder : For step-by-step construction of DataStructures.
    """

    PRODUCT_CLASSES: Type[DataComponent] | Tuple[Type[DataComponent], ...]

    @abstractmethod
    def create(self, *args: Any, **kwargs: Any) -> Products:
        """
        Create one or more data components.

        Parameters
        ----------
        *args
            Inputs required to create the products.
        **kwargs
            Additional options for creation.

        Returns
        -------
        Products
            Created component(s).

        Note
        ----
        Subclasses must implement this method with appropriate
        parameters for their specific product types.
        """
        ...
