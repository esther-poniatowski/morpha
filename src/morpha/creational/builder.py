"""Builder pattern for constructing data structures."""

from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Type, Tuple, Any, Optional

from morpha.structures.base import DataStructure


Product = TypeVar("Product", bound=DataStructure[Any])
"""Type variable for the data structure produced by a builder."""


class Builder(Generic[Product], ABC):
    """
    Abstract base class for building data structures.

    Builders encapsulate the step-by-step construction of complex
    DataStructure objects, separating construction logic from the
    data structure class itself.

    Class Attributes
    ----------------
    PRODUCT_CLASS : Type[Product]
        Class of the data structure to build.
    TMP_DATA : Tuple[str, ...]
        Names of temporary data attributes used during building.

    Attributes
    ----------
    product : Optional[Product]
        The data structure being constructed.

    Notes
    -----
    The Builder pattern separates concerns:
    - Constructor: Store static configuration
    - build(): Receive dynamic inputs, orchestrate construction
    - Helper methods: Process specific aspects of construction
    - reset(): Clear state for reuse

    After `get_product()` is called, the builder resets and can be
    reused to build another instance.

    See Also
    --------
    Factory : For simpler component creation without step-by-step logic.

    Examples
    --------
    Define a concrete builder:

    >>> class TimeSeriesBuilder(Builder[TimeSeries]):
    ...     PRODUCT_CLASS = TimeSeries
    ...     TMP_DATA = ("raw_data", "timestamps")
    ...
    ...     def build(self, raw: np.ndarray, times: np.ndarray) -> TimeSeries:
    ...         self.product = TimeSeries()
    ...         self._process_data(raw)
    ...         self._create_time_coord(times)
    ...         return self.get_product()
    ...
    ...     def _process_data(self, raw: np.ndarray) -> None:
    ...         # Processing logic...
    ...         self.product.set_data(CoreData(raw))
    ...
    ...     def _create_time_coord(self, times: np.ndarray) -> None:
    ...         # Coordinate creation logic...
    ...         self.product.set_coord("time", CoordTime(times))

    Use the builder:

    >>> builder = TimeSeriesBuilder()
    >>> ts = builder.build(raw_data, timestamps)
    """

    PRODUCT_CLASS: Type[Product]
    TMP_DATA: Tuple[str, ...]

    def __init__(self) -> None:
        """Initialize the builder with no product."""
        self.product: Optional[Product] = None
        self.reset()

    def reset(self) -> None:
        """Reset builder state for reuse."""
        self.product = None
        if hasattr(self, "TMP_DATA"):
            for attr in self.TMP_DATA:
                setattr(self, attr, None)

    def get_product(self) -> Product:
        """
        Return the built product and reset the builder.

        Returns
        -------
        Product
            The completed data structure.

        Raises
        ------
        AssertionError
            If product is None (build not complete).
        """
        assert self.product is not None, "Product not built"
        product = self.product
        self.reset()
        return product

    @abstractmethod
    def build(self, *args: Any, **kwargs: Any) -> Product:
        """
        Build a data structure step-by-step.

        Parameters
        ----------
        *args : Any
            Input objects required for building.
        **kwargs : Any
            Additional options for building.

        Returns
        -------
        Product
            The completed data structure.

        Note
        ----
        Implementations should:
        1. Initialize `self.product`
        2. Call helper methods to build components
        3. Return via `self.get_product()`
        """
        ...
