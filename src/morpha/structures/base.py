"""
Base data structure class.

Classes
-------
DataStructure
    Abstract base class for composite data structures with schema enforcement.
"""

from abc import ABC
import copy
from typing import Tuple, Mapping, Self, Set, TypeVar, Generic, Generator, Any, TYPE_CHECKING

from morpha.components.dimensions import Dimensions, DimensionsSpec
from morpha.components.base import DataComponent
from morpha.components.specs import ComponentSpec
from morpha.components.metadata import MetaDataField

if TYPE_CHECKING:
    from morpha.coordinates.base import Coordinate

AnyCoreData = TypeVar("AnyCoreData", bound=DataComponent)
"""Type variable for the core data component stored in the data structure."""


class DataStructure(ABC, Generic[AnyCoreData]):
    """
    Abstract base class for data structures with schema enforcement.

    Provides a framework for building composite data structures that contain:
    - A core data component (the main data array)
    - Coordinate components (labeled axes)
    - Dimension tracking
    - Schema validation via class attributes

    Class Attributes
    ----------------
    DIMENSIONS_SPEC : DimensionsSpec
        Specification of allowed dimensions (names, order, required/optional).
        Must be defined in subclasses.
    COMPONENTS_SPEC : ComponentSpec
        Specification of allowed data components (names and types).
        Must be defined in subclasses.
    IDENTIFIERS : Mapping[str, MetaDataField]
        Metadata attributes that uniquely identify instances.
        Must be defined in subclasses.
    REQUIRED_IN_SUBCLASSES : Tuple[str, ...]
        Class attributes that must be defined in each subclass.

    Attributes
    ----------
    dims : Dimensions
        Active dimensions in this instance.
    coords : Set[str]
        Names of active coordinates.
    data : AnyCoreData
        Core data values.

    Parameters
    ----------
    data : AnyCoreData, optional
        Core data component.
    **coords : Coordinate
        Coordinate components keyed by attribute name.

    Examples
    --------
    Define a concrete data structure:

    >>> class TimeSeries(DataStructure[CoreData]):
    ...     DIMENSIONS_SPEC = DimensionsSpec(time=True, units=False)
    ...     COMPONENTS_SPEC = ComponentSpec(data=CoreData, time=CoordTime)
    ...     IDENTIFIERS = {"session": MetaDataField(str, None)}

    Create an instance:

    >>> ts = TimeSeries(data=my_data, time=time_coord)
    >>> ts.dims
    Dimensions['time', 'units']

    Notes
    -----
    The `__init_subclass__` hook enforces that subclasses define required
    class attributes, providing compile-time-like checks for schema compliance.
    """

    DIMENSIONS_SPEC: DimensionsSpec
    COMPONENTS_SPEC: ComponentSpec
    IDENTIFIERS: Mapping[str, MetaDataField]
    REQUIRED_IN_SUBCLASSES: Tuple[str, ...] = ("DIMENSIONS_SPEC", "COMPONENTS_SPEC", "IDENTIFIERS")

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """Ensure subclasses define required class attributes."""
        super().__init_subclass__(**kwargs)
        for class_attr in cls.REQUIRED_IN_SUBCLASSES:
            if not hasattr(cls, class_attr):
                raise TypeError(f"<{cls.__name__}> Missing class-level attribute: '{class_attr}'.")

    def __init__(
        self, data: AnyCoreData | None = None, **coords: "Coordinate | None"
    ) -> None:
        """
        Initialize data structure with optional data and coordinates.

        Components can be set at initialization or later via setter methods,
        enabling lazy/incremental construction.
        """
        self.dims: Dimensions = Dimensions()
        self.coords: Set[str] = set()
        self.data: AnyCoreData  # type declaration for lazy initialization

        if data is not None:
            self.set_data(data)
        for name, coord in coords.items():
            if coord is not None:
                self.set_coord(name, coord)

    def __repr__(self) -> str:
        data_status = "empty" if not hasattr(self, "data") else "filled"
        active_coords = ", ".join(self.coords) if self.coords else "none"
        return (
            f"<{self.__class__.__name__}> Dims: {self.dims}, "
            f"Data: {data_status}, Coords: {active_coords}"
        )

    # --- Getter Methods ---------------------------------------------------------------------------

    def has_data(self) -> bool:
        """Check if data is set."""
        return hasattr(self, "data")

    def get_data(self) -> AnyCoreData:
        """
        Get the core data.

        Returns
        -------
        AnyCoreData
            Core data component.

        Raises
        ------
        AttributeError
            If data is not set.
        """
        if not self.has_data():
            raise AttributeError(f"Data not set in {self.__class__.__name__} instance.")
        return self.data

    def get_coord(self, name: str) -> "Coordinate":
        """
        Get a coordinate by name.

        Parameters
        ----------
        name : str
            Coordinate attribute name.

        Returns
        -------
        Coordinate
            The coordinate component.

        Raises
        ------
        AttributeError
            If coordinate is not active.
        """
        if name not in self.coords:
            raise AttributeError(f"Coordinate '{name}' not active in {self.coords}.")
        return getattr(self, name)

    def get_coords_from_dim(self, dim: str) -> Mapping[str, "Coordinate"]:
        """Get all coordinates associated with a dimension."""
        return {name: coord for name, coord in self.iter_coords() if dim in coord.dims}

    def iter_coords(self) -> Generator[Tuple[str, "Coordinate"], None, None]:
        """Iterate over active coordinates."""
        for name in self.coords:
            yield name, getattr(self, name)

    @property
    def shape(self) -> Tuple[int, ...]:
        """Shape of the core data."""
        return self.data.shape

    def get_dim(self, axis: int) -> str:
        """Get dimension name by axis index."""
        return self.dims.get_dim(axis)

    def get_axis(self, name: str) -> int:
        """Get axis index by dimension name."""
        return self.dims.get_axis(name)

    def get_size(self, name: str) -> int:
        """Get size along a dimension."""
        if name not in self.dims:
            raise ValueError(f"Dimension '{name}' not active in {self.dims}.")
        if self.has_data():
            return self.data.get_size(name)
        coords_with_dim = self.get_coords_from_dim(name)
        if coords_with_dim:
            return next(iter(coords_with_dim.values())).get_size(name)
        raise ValueError(f"Dimension '{name}' not found in data structure.")

    @property
    def identifiers(self) -> Set[str]:
        """Names of identifier attributes."""
        return set(self.IDENTIFIERS.keys()) if hasattr(self, "IDENTIFIERS") else set()

    def __getattr__(self, name: str) -> Any:
        """
        Delegate attribute access to nested objects.

        Searches data, dims, coords, and identifiers for the attribute.
        """
        # Avoid recursion during initialization and special methods
        if name.startswith("_") or name in ("coords", "dims", "data", "IDENTIFIERS"):
            raise AttributeError(f"'{self.__class__.__name__}' has no attribute '{name}'")

        nested_attr = (
            getattr(self, "coords", set())
            | {"data", "dims"}
            | getattr(self, "identifiers", set())
        )
        for attr in nested_attr:
            obj = object.__getattribute__(self, attr) if hasattr(self, attr) else None
            if obj is not None and hasattr(obj, name):
                return getattr(obj, name)
        raise AttributeError(
            f"Invalid attribute '{name}' for '{self.__class__.__name__}'. "
            f"Not in any nested object: {nested_attr}"
        )

    # --- Setter Methods ---------------------------------------------------------------------------

    def set_data(self, data: AnyCoreData) -> None:
        """
        Set the core data after validation.

        Parameters
        ----------
        data : AnyCoreData
            Core data component.

        Raises
        ------
        TypeError
            If data type doesn't match COMPONENTS_SPEC.
        ValueError
            If dimensions don't match DIMENSIONS_SPEC or shape is inconsistent.
        """
        self.COMPONENTS_SPEC.validate("data", data)
        self.DIMENSIONS_SPEC.validate(data.dims)
        self.validate_shape(data)
        self.data = data
        self.register_dimensions(data.dims)

    def set_coord(self, name: str, coord: "Coordinate") -> None:
        """
        Set a coordinate after validation.

        Parameters
        ----------
        name : str
            Attribute name for the coordinate.
        coord : Coordinate
            Coordinate component.

        Raises
        ------
        AttributeError
            If name is not in COMPONENTS_SPEC.
        TypeError
            If coord type doesn't match expected type.
        ValueError
            If dimensions or shape are inconsistent.
        """
        self.COMPONENTS_SPEC.validate(name, coord)
        self.DIMENSIONS_SPEC.validate(coord.dims)
        self.validate_shape(coord)
        setattr(self, name, coord)
        self.register_coord(name)
        self.register_dimensions(coord.dims)

    def register_coord(self, name: str) -> None:
        """Register an active coordinate."""
        if name not in self.coords:
            self.coords.add(name)

    def register_dimensions(self, dims: Dimensions) -> None:
        """Register new dimensions."""
        for dim in dims:
            if dim not in self.dims:
                self.dims.add(dim)

    def validate_shape(self, component: DataComponent) -> None:
        """
        Validate component shape against existing components.

        Ensures sizes match along common dimensions.

        Parameters
        ----------
        component : DataComponent
            New component to validate.

        Raises
        ------
        ValueError
            If sizes don't match along common dimensions.
        """
        common_dims = Dimensions.intersection(self.dims, component.dims)
        for dim in common_dims:
            expected_size = self.get_size(dim)
            component_size = component.get_size(dim)
            if component_size != expected_size:
                raise ValueError(
                    f"Invalid shape for component '{component.__class__.__name__}' "
                    f"along dimension '{dim}': {component_size} != {expected_size}"
                )

    # --- Data Manipulations -----------------------------------------------------------------------

    def copy(self) -> Self:
        """Create a deep copy."""
        return copy.deepcopy(self)

    def sel(self, **kwargs: Any) -> Self:
        """
        Select data along coordinates.

        Parameters
        ----------
        **kwargs
            Coordinate names and selection criteria (value, list, or slice).

        Returns
        -------
        DataStructure
            New structure with selected data.

        Note
        ----
        Not yet implemented.
        """
        # TODO: Implement selection logic
        return self
