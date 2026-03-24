"""
Integration tests for DataStructure and ComponentSpec.

Tests the complete workflow of creating and using data structures with schema enforcement.
"""

import pytest
import numpy as np

from morpha.components.base import DataComponent
from morpha.components.dimensions import Dimensions, DimensionsSpec
from morpha.components.metadata import MetaDataField
from morpha.components.specs import ComponentSpec
from morpha.structures.base import DataStructure
from morpha.coordinates.base import Coordinate
from morpha.coordinates.attributes import Attribute


# --- Test Fixtures: Define concrete types for testing -----------------------------------------


class Task(Attribute[str], str):
    """Attribute representing task types."""

    OPTIONS = {"CLK": "Clock task", "PTD": "Pattern discrimination"}
    LABELS = {"CLK": "Clock", "PTD": "Pattern"}


class TimeValue(Attribute[float], float):
    """Attribute representing time values (any float is valid)."""

    @classmethod
    def is_valid(cls, value: float) -> bool:
        """All floats are valid time values."""
        return isinstance(value, (int, float, np.floating))


class CoreData(DataComponent):
    """Concrete data component for core values."""

    DIMENSIONS_SPEC = DimensionsSpec(units=True, time=True)
    DTYPE = np.float64
    SENTINEL = np.nan
    METADATA = {"session": MetaDataField(str, None)}


class CoordTime(Coordinate[TimeValue]):
    """Time coordinate component."""

    ATTRIBUTE = TimeValue
    DIMENSIONS_SPEC = DimensionsSpec(time=True)
    DTYPE = np.float64
    SENTINEL = np.nan


class CoordTask(Coordinate[Task]):
    """Task coordinate component."""

    ATTRIBUTE = Task
    DIMENSIONS_SPEC = DimensionsSpec(trials=True)
    DTYPE = str
    SENTINEL = ""


# --- ComponentSpec Tests ----------------------------------------------------------------------


@pytest.mark.integration
class TestComponentSpec:
    """Tests for ComponentSpec validation."""

    def test_creation(self):
        """Test ComponentSpec creation with valid spec."""
        spec = ComponentSpec(data=CoreData, time=CoordTime)
        assert "data" in spec
        assert "time" in spec
        assert "invalid" not in spec

    def test_validate_valid_component(self):
        """Test validation passes for correct type."""
        spec = ComponentSpec(data=CoreData)
        data = CoreData(np.zeros((5, 10)), dims=Dimensions("units", "time"))
        spec.validate("data", data)  # Should not raise

    def test_validate_invalid_name_raises(self):
        """Test validation raises AttributeError for unknown name."""
        spec = ComponentSpec(data=CoreData)
        data = CoreData(np.zeros((5, 10)), dims=Dimensions("units", "time"))
        with pytest.raises(AttributeError, match="Invalid component name"):
            spec.validate("unknown", data)

    def test_validate_wrong_type_raises(self):
        """Test validation raises TypeError for wrong component type."""
        spec = ComponentSpec(data=CoreData, time=CoordTime)
        time_coord = CoordTime(np.arange(10.0), dims=Dimensions("time"))
        with pytest.raises(TypeError, match="Invalid component type"):
            spec.validate("data", time_coord)

    def test_iteration(self):
        """Test iteration over component names."""
        spec = ComponentSpec(data=CoreData, time=CoordTime)
        names = list(spec)
        assert "data" in names
        assert "time" in names

    def test_keys_values_items(self):
        """Test dict-like access methods."""
        spec = ComponentSpec(data=CoreData, time=CoordTime)
        assert set(spec.keys()) == {"data", "time"}
        assert CoreData in spec.values()
        assert ("data", CoreData) in spec.items()


# --- DataStructure Tests ----------------------------------------------------------------------


@pytest.mark.integration
class TestDataStructureSubclassing:
    """Tests for DataStructure subclass schema enforcement."""

    def test_missing_dimensions_spec_raises(self):
        """Test that missing DIMENSIONS_SPEC raises TypeError."""
        with pytest.raises(TypeError, match="Missing class-level attribute.*DIMENSIONS_SPEC"):

            class BadStructure(DataStructure[CoreData]):
                COMPONENTS_SPEC = ComponentSpec(data=CoreData)
                IDENTIFIERS = {}

    def test_missing_components_spec_raises(self):
        """Test that missing COMPONENTS_SPEC raises TypeError."""
        with pytest.raises(TypeError, match="Missing class-level attribute.*COMPONENTS_SPEC"):

            class BadStructure(DataStructure[CoreData]):
                DIMENSIONS_SPEC = DimensionsSpec(units=True, time=True)
                IDENTIFIERS = {}

    def test_missing_identifiers_raises(self):
        """Test that missing IDENTIFIERS raises TypeError."""
        with pytest.raises(TypeError, match="Missing class-level attribute.*IDENTIFIERS"):

            class BadStructure(DataStructure[CoreData]):
                DIMENSIONS_SPEC = DimensionsSpec(units=True, time=True)
                COMPONENTS_SPEC = ComponentSpec(data=CoreData)

    def test_valid_subclass_creation(self):
        """Test that valid subclass can be created."""

        class ValidStructure(DataStructure[CoreData]):
            DIMENSIONS_SPEC = DimensionsSpec(units=True, time=True)
            COMPONENTS_SPEC = ComponentSpec(data=CoreData, time=CoordTime)
            IDENTIFIERS = {"session": MetaDataField(str, None)}

        # Should not raise
        instance = ValidStructure()
        assert instance.dims == Dimensions()
        assert instance.coords == set()


@pytest.mark.integration
class TestDataStructureOperations:
    """Tests for DataStructure instance operations."""

    @pytest.fixture
    def structure_class(self):
        """Create a concrete DataStructure class for testing."""

        class TestStructure(DataStructure[CoreData]):
            # Note: units and time are optional (False) so coordinates with subset dims work
            DIMENSIONS_SPEC = DimensionsSpec(units=False, time=False, trials=False)
            COMPONENTS_SPEC = ComponentSpec(data=CoreData, time=CoordTime, task=CoordTask)
            IDENTIFIERS = {"session": MetaDataField(str, None)}

        return TestStructure

    @pytest.fixture
    def sample_data(self):
        """Create sample data for testing."""
        return CoreData(
            np.random.randn(5, 10), dims=Dimensions("units", "time"), session="test_session"
        )

    @pytest.fixture
    def sample_time_coord(self):
        """Create sample time coordinate."""
        return CoordTime(np.arange(10.0), dims=Dimensions("time"))

    def test_init_empty(self, structure_class):
        """Test creating empty structure."""
        s = structure_class()
        assert not s.has_data()
        assert s.coords == set()
        assert s.dims == Dimensions()

    def test_init_with_data(self, structure_class, sample_data):
        """Test creating structure with data."""
        s = structure_class(data=sample_data)
        assert s.has_data()
        assert np.array_equal(s.data, sample_data)
        assert "units" in s.dims
        assert "time" in s.dims

    def test_init_with_coords(self, structure_class, sample_data, sample_time_coord):
        """Test creating structure with data and coordinates."""
        s = structure_class(data=sample_data, time=sample_time_coord)
        assert s.has_data()
        assert "time" in s.coords
        assert np.array_equal(s.get_coord("time"), sample_time_coord)

    def test_set_data_validates_type(self, structure_class, sample_time_coord):
        """Test that set_data validates component type."""
        s = structure_class()
        with pytest.raises(TypeError):
            s.set_data(sample_time_coord)  # Wrong type

    def test_set_coord_validates_type(self, structure_class, sample_data):
        """Test that set_coord validates component type."""
        s = structure_class()
        with pytest.raises(TypeError):
            s.set_coord("time", sample_data)  # Wrong type

    def test_get_data_when_not_set_raises(self, structure_class):
        """Test that get_data raises when data not set."""
        s = structure_class()
        with pytest.raises(RuntimeError, match="Data not initialised"):
            s.get_data()

    def test_get_coord_when_not_active_raises(self, structure_class, sample_data):
        """Test that get_coord raises for inactive coordinate."""
        s = structure_class(data=sample_data)
        with pytest.raises(AttributeError, match="not active"):
            s.get_coord("time")

    def test_validate_shape_success(self, structure_class, sample_data, sample_time_coord):
        """Test shape validation passes for matching dimensions."""
        s = structure_class(data=sample_data)
        # Should not raise - time dimension size matches (10)
        s.set_coord("time", sample_time_coord)

    def test_validate_shape_mismatch_raises(self, structure_class, sample_data):
        """Test shape validation fails for mismatched dimensions."""
        s = structure_class(data=sample_data)
        wrong_size_coord = CoordTime(np.arange(5.0), dims=Dimensions("time"))  # Size 5, not 10
        with pytest.raises(ValueError, match="Invalid shape"):
            s.set_coord("time", wrong_size_coord)

    def test_get_size(self, structure_class, sample_data):
        """Test getting dimension size."""
        s = structure_class(data=sample_data)
        assert s.get_size("units") == 5
        assert s.get_size("time") == 10

    def test_get_dim_get_axis(self, structure_class, sample_data):
        """Test dimension-axis mapping."""
        s = structure_class(data=sample_data)
        assert s.get_dim(0) == "units"
        assert s.get_dim(1) == "time"
        assert s.get_axis("units") == 0
        assert s.get_axis("time") == 1

    def test_shape_property(self, structure_class, sample_data):
        """Test shape property."""
        s = structure_class(data=sample_data)
        assert s.shape == (5, 10)

    def test_copy(self, structure_class, sample_data, sample_time_coord):
        """Test deep copy."""
        s = structure_class(data=sample_data, time=sample_time_coord)
        s_copy = s.copy()

        # Verify deep copy
        assert s_copy is not s
        assert s_copy.data is not s.data
        assert np.array_equal(s_copy.data, s.data)

    def test_repr(self, structure_class, sample_data, sample_time_coord):
        """Test string representation."""
        s = structure_class(data=sample_data, time=sample_time_coord)
        repr_str = repr(s)
        assert "TestStructure" in repr_str
        assert "filled" in repr_str
        assert "time" in repr_str

    def test_iter_coords(self, structure_class, sample_data, sample_time_coord):
        """Test coordinate iteration."""
        s = structure_class(data=sample_data, time=sample_time_coord)
        coords = dict(s.iter_coords())
        assert "time" in coords
        assert np.array_equal(coords["time"], sample_time_coord)
