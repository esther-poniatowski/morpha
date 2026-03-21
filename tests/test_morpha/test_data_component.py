"""Tests for the DataComponent class."""

import pytest
import numpy as np
from morpha.components.base import DataComponent
from morpha.components.dimensions import Dimensions, DimensionsSpec
from morpha.components.metadata import MetaDataField


class SimpleData(DataComponent):
    """Simple DataComponent subclass for testing."""

    DIMENSIONS_SPEC = DimensionsSpec(time=True, units=False)
    DTYPE = np.float64
    SENTINEL = np.nan


class DataWithMetadata(DataComponent):
    """DataComponent with metadata for testing."""

    DIMENSIONS_SPEC = DimensionsSpec(time=True)
    METADATA = {
        "origin": MetaDataField(str, None),
        "unit": MetaDataField(str, "ms"),
    }
    DTYPE = np.float64
    SENTINEL = np.nan


class TestDataComponent:
    """Tests for the DataComponent class."""

    def test_creation_with_dims(self):
        """Test basic creation with dimensions."""
        values = np.zeros((10, 5))
        dims = Dimensions("time", "units")
        data = SimpleData(values, dims=dims)

        assert data.shape == (10, 5)
        assert list(data.dims) == ["time", "units"]

    def test_creation_without_dims(self):
        """Test creation with default dimensions."""
        values = np.zeros((10, 5))
        data = SimpleData(values)

        assert data.shape == (10, 5)
        assert data.dims.ndim == 2
        assert all(d == "" for d in data.dims)

    def test_dtype_enforcement(self):
        """Test that DTYPE is enforced."""
        values = np.array([1, 2, 3])  # int array
        data = SimpleData(values)

        assert data.dtype == np.float64

    def test_dims_length_mismatch_raises(self):
        """Test that mismatched dims length raises error."""
        values = np.zeros((10, 5))
        dims = Dimensions("time")  # Only 1 dim for 2D array

        with pytest.raises(ValueError, match="len\\(dims\\)"):
            SimpleData(values, dims=dims)

    def test_get_dim(self):
        """Test get_dim method."""
        values = np.zeros((10, 5))
        dims = Dimensions("time", "units")
        data = SimpleData(values, dims=dims)

        assert data.get_dim(0) == "time"
        assert data.get_dim(1) == "units"

    def test_get_axis(self):
        """Test get_axis method."""
        values = np.zeros((10, 5))
        dims = Dimensions("time", "units")
        data = SimpleData(values, dims=dims)

        assert data.get_axis("time") == 0
        assert data.get_axis("units") == 1

    def test_get_size(self):
        """Test get_size method."""
        values = np.zeros((10, 5))
        dims = Dimensions("time", "units")
        data = SimpleData(values, dims=dims)

        assert data.get_size("time") == 10
        assert data.get_size("units") == 5

    def test_from_shape(self):
        """Test from_shape class method."""
        dims = Dimensions("time", "units")
        data = SimpleData.from_shape((10, 5), dims=dims)

        assert data.shape == (10, 5)
        assert np.all(np.isnan(data))
        assert list(data.dims) == ["time", "units"]

    def test_get_missing(self):
        """Test get_missing method."""
        dims = Dimensions("time")
        data = SimpleData.from_shape(5, dims=dims)
        data[2] = 1.0

        missing = data.get_missing()
        expected = np.array([True, True, False, True, True])
        np.testing.assert_array_equal(missing, expected)

    def test_transpose_updates_dims(self):
        """Test that transpose updates dimensions."""
        values = np.zeros((10, 5))
        dims = Dimensions("time", "units")
        data = SimpleData(values, dims=dims)

        transposed = data.transpose()
        assert transposed.shape == (5, 10)
        assert list(transposed.dims) == ["units", "time"]

    def test_T_updates_dims(self):
        """Test that T property updates dimensions."""
        values = np.zeros((10, 5))
        dims = Dimensions("time", "units")
        data = SimpleData(values, dims=dims)

        transposed = data.T
        assert transposed.shape == (5, 10)
        assert list(transposed.dims) == ["units", "time"]

    def test_swapaxes_updates_dims(self):
        """Test that swapaxes updates dimensions."""
        values = np.zeros((10, 5, 3))
        dims = Dimensions("time", "units", "trials")
        # Use base DataComponent directly to avoid spec validation
        data = DataComponent(values, dims=dims)

        swapped = data.swapaxes(0, 2)
        assert swapped.shape == (3, 5, 10)
        assert list(swapped.dims) == ["trials", "units", "time"]

    def test_moveaxis_updates_dims(self):
        """Test that moveaxis updates dimensions."""
        values = np.zeros((10, 5, 3))
        dims = Dimensions("time", "units", "trials")
        data = DataComponent(values, dims=dims)

        moved = data.moveaxis(0, 2)
        assert moved.shape == (5, 3, 10)
        assert list(moved.dims) == ["units", "trials", "time"]

    def test_slicing_preserves_type(self):
        """Test that slicing returns DataComponent."""
        values = np.zeros((10, 5))
        dims = Dimensions("time", "units")
        data = SimpleData(values, dims=dims)

        sliced = data[:5]
        assert isinstance(sliced, SimpleData)
        assert sliced.shape == (5, 5)

    def test_arithmetic_preserves_type(self):
        """Test that arithmetic returns DataComponent."""
        values = np.ones((10, 5))
        dims = Dimensions("time", "units")
        data = SimpleData(values, dims=dims)

        result = data + 1
        assert isinstance(result, SimpleData)
        np.testing.assert_array_equal(result, 2.0)

    def test_metadata_propagation(self):
        """Test that metadata is set and propagated."""
        values = np.zeros(10)
        dims = Dimensions("time")
        data = DataWithMetadata(values, dims=dims, origin="test", unit="s")

        assert data.origin == "test"
        assert data.unit == "s"

    def test_metadata_default_values(self):
        """Test metadata default values."""
        values = np.zeros(10)
        dims = Dimensions("time")
        data = DataWithMetadata(values, dims=dims)

        assert data.origin is None
        # Note: default_value in MetaDataField is not automatically applied
        # It's available for reference, but __new__ sets None if not provided

    def test_dims_preserved_on_same_ndim_operation(self):
        """Test dimensions preserved when ndim unchanged."""
        values = np.zeros((10, 5))
        dims = Dimensions("time", "units")
        data = SimpleData(values, dims=dims)

        # Addition preserves shape and dims
        result = data + 0
        assert list(result.dims) == ["time", "units"]

    def test_dims_reset_on_reduce_operation(self):
        """Test dimensions reset when ndim changes."""
        values = np.zeros((10, 5))
        dims = Dimensions("time", "units")
        data = SimpleData(values, dims=dims)

        # Sum reduces dimensions
        result = data.sum(axis=1)
        assert result.ndim == 1
        assert result.dims.ndim == 1
        assert all(d == "" for d in result.dims)

    def test_array_ufunc_tuple_output(self):
        """Test __array_ufunc__ handles tuple outputs."""
        values = np.array([1.5, 2.25, 3.75])
        dims = Dimensions("time")
        data = SimpleData(values, dims=dims)

        frac, whole = np.modf(data)
        assert isinstance(frac, SimpleData)
        assert isinstance(whole, SimpleData)
        assert list(frac.dims) == ["time"]
        assert list(whole.dims) == ["time"]
