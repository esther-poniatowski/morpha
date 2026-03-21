"""Tests for the Dimensions and DimensionsSpec classes."""

import pytest
from morpha.components.dimensions import Dimensions, DimensionsSpec


class TestDimensions:
    """Tests for the Dimensions class."""

    def test_creation(self):
        """Test basic dimension creation."""
        dims = Dimensions("time", "units", "trials")
        assert dims.ndim == 3
        assert list(dims) == ["time", "units", "trials"]

    def test_duplicate_names_raises(self):
        """Test that duplicate names raise an error."""
        with pytest.raises(ValueError, match="Duplicate"):
            Dimensions("time", "time", "units")

    def test_default_creation(self):
        """Test default dimension creation."""
        dims = Dimensions.default(3)
        assert dims.ndim == 3
        assert all(d == "" for d in dims)

    def test_get_dim(self):
        """Test getting dimension by index."""
        dims = Dimensions("time", "units")
        assert dims.get_dim(0) == "time"
        assert dims.get_dim(1) == "units"

    def test_get_dim_out_of_bounds(self):
        """Test that out-of-bounds index raises error."""
        dims = Dimensions("time")
        with pytest.raises(IndexError):
            dims.get_dim(5)

    def test_get_axis(self):
        """Test getting axis by name."""
        dims = Dimensions("time", "units", "trials")
        assert dims.get_axis("time") == 0
        assert dims.get_axis("units") == 1
        assert dims.get_axis("trials") == 2

    def test_get_axis_invalid_name(self):
        """Test that invalid name raises error."""
        dims = Dimensions("time", "units")
        with pytest.raises(ValueError, match="Invalid dimension name"):
            dims.get_axis("invalid")

    def test_is_subset(self):
        """Test subset checking."""
        full = Dimensions("time", "units", "trials")
        partial = Dimensions("time", "units")
        assert partial.is_subset(full)
        assert not full.is_subset(partial)

    def test_is_ordered_as(self):
        """Test order checking."""
        dims1 = Dimensions("time", "units", "trials")
        dims2 = Dimensions("time", "trials")
        dims3 = Dimensions("trials", "time")
        assert dims1.is_ordered_as(dims2)
        assert not dims1.is_ordered_as(dims3)

    def test_intersection(self):
        """Test dimension intersection."""
        dims1 = Dimensions("time", "units")
        dims2 = Dimensions("time", "trials")
        common = Dimensions.intersection(dims1, dims2)
        assert "time" in common
        assert "units" not in common
        assert "trials" not in common

    def test_add(self):
        """Test adding a dimension."""
        dims = Dimensions("time", "units")
        dims.add("trials", axis=1)
        assert list(dims) == ["time", "trials", "units"]

    def test_add_duplicate_raises(self):
        """Test that adding duplicate raises error."""
        dims = Dimensions("time", "units")
        with pytest.raises(ValueError, match="Duplicate"):
            dims.add("time")

    def test_transpose_reverse(self):
        """Test transposing (reversing) dimensions."""
        dims = Dimensions("time", "units", "trials")
        transposed = dims.transpose()
        assert list(transposed) == ["trials", "units", "time"]

    def test_transpose_with_axes(self):
        """Test transposing with specific axes."""
        dims = Dimensions("time", "units", "trials")
        transposed = dims.transpose((2, 0, 1))
        assert list(transposed) == ["trials", "time", "units"]

    def test_swap(self):
        """Test swapping two dimensions."""
        dims = Dimensions("time", "units", "trials")
        swapped = dims.swap(0, 2)
        assert list(swapped) == ["trials", "units", "time"]

    def test_move(self):
        """Test moving a dimension."""
        dims = Dimensions("time", "units", "trials")
        moved = dims.move(0, 2)
        assert list(moved) == ["units", "trials", "time"]


class TestDimensionsSpec:
    """Tests for the DimensionsSpec class."""

    def test_creation(self):
        """Test spec creation."""
        spec = DimensionsSpec(time=True, units=False)
        assert "time" in spec.required()
        assert "units" in spec.optional()

    def test_required(self):
        """Test getting required dimensions."""
        spec = DimensionsSpec(time=True, units=False, trials=True)
        required = spec.required()
        assert "time" in required
        assert "trials" in required
        assert "units" not in required

    def test_optional(self):
        """Test getting optional dimensions."""
        spec = DimensionsSpec(time=True, units=False)
        optional = spec.optional()
        assert "units" in optional
        assert "time" not in optional

    def test_validate_success(self):
        """Test successful validation."""
        spec = DimensionsSpec(time=True, units=False)
        dims = Dimensions("time", "units")
        spec.validate(dims)  # Should not raise

    def test_validate_required_only(self):
        """Test validation with only required dimensions."""
        spec = DimensionsSpec(time=True, units=False)
        dims = Dimensions("time")
        spec.validate(dims)  # Should not raise

    def test_validate_missing_required(self):
        """Test that missing required dimension raises error."""
        spec = DimensionsSpec(time=True, units=True)
        dims = Dimensions("time")
        with pytest.raises(ValueError, match="Missing required"):
            spec.validate(dims)

    def test_validate_extra_dimension(self):
        """Test that extra dimension raises error."""
        spec = DimensionsSpec(time=True)
        dims = Dimensions("time", "extra")
        with pytest.raises(ValueError, match="Extra dimensions"):
            spec.validate(dims)

    def test_validate_wrong_order(self):
        """Test that wrong order raises error."""
        spec = DimensionsSpec(time=True, units=True)
        dims = Dimensions("units", "time")
        with pytest.raises(ValueError, match="Incorrect order"):
            spec.validate(dims)
