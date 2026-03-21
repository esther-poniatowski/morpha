"""Tests for the I/O module."""

import tempfile
from pathlib import Path

import pytest
import numpy as np

from morpha.io.base import FileExt, IOHandler
from morpha.io.savers import (
    Saver,
    SaverPKL,
    SaverNPY,
    SaverNPZ,
    SaverJSON,
    SaverYAML,
    SaverHDF5,
)
from morpha.io.loaders import (
    Loader,
    LoaderPKL,
    LoaderNPY,
    LoaderNPZ,
    LoaderJSON,
    LoaderYAML,
    LoaderHDF5,
)
import logging


class TestFileExt:
    """Tests for the FileExt class."""

    def test_valid_extension(self):
        """Test creating valid extension."""
        ext = FileExt("pkl")
        assert str(ext) == ".pkl"

    def test_valid_extension_with_period(self):
        """Test extension with leading period."""
        ext = FileExt(".pkl")
        assert str(ext) == ".pkl"

    def test_invalid_extension_raises(self):
        """Test that invalid extension raises error."""
        with pytest.raises(ValueError, match="Invalid file extension"):
            FileExt("xyz")

    def test_is_valid(self):
        """Test is_valid class method."""
        assert FileExt.is_valid(".pkl")
        assert FileExt.is_valid(".npy")
        assert not FileExt.is_valid(".xyz")

    def test_add_period(self):
        """Test add_period static method."""
        assert FileExt.add_period("pkl") == ".pkl"
        assert FileExt.add_period(".pkl") == ".pkl"


class TestIOHandler:
    """Tests for the IOHandler base class."""

    def test_enforce_ext(self):
        """Test extension enforcement."""
        path = IOHandler.enforce_ext("/path/to/file", ".pkl")
        assert path == Path("/path/to/file.pkl")

    def test_enforce_ext_replaces(self):
        """Test that existing extension is replaced."""
        path = IOHandler.enforce_ext("/path/to/file.txt", ".pkl")
        assert path == Path("/path/to/file.pkl")


class TestSaverLoader:
    """Tests for Saver and Loader classes."""

    def test_saver_pkl_loader_pkl(self):
        """Test saving and loading pickle files."""
        data = {"key": "value", "number": 42}

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "data"

            # Save
            saver = SaverPKL(path)
            saver.save(data)
            assert (Path(tmpdir) / "data.pkl").exists()

            # Load
            loader = LoaderPKL(path)
            loaded = loader.load()
            assert loaded == data

    def test_saver_npy_loader_npy(self):
        """Test saving and loading numpy files."""
        data = np.array([[1, 2, 3], [4, 5, 6]])

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "array"

            # Save
            saver = SaverNPY(path)
            saver.save(data)
            assert (Path(tmpdir) / "array.npy").exists()

            # Load
            loader = LoaderNPY(path)
            loaded = loader.load()
            np.testing.assert_array_equal(loaded, data)

    def test_saver_npz_loader_npz(self):
        """Test saving and loading compressed numpy files."""
        data = {
            "arr1": np.array([1, 2, 3]),
            "arr2": np.array([4, 5, 6]),
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "arrays"

            # Save
            saver = SaverNPZ(path)
            saver.save(data)
            assert (Path(tmpdir) / "arrays.npz").exists()

            # Load
            loader = LoaderNPZ(path)
            loaded = loader.load()
            np.testing.assert_array_equal(loaded["arr1"], data["arr1"])
            np.testing.assert_array_equal(loaded["arr2"], data["arr2"])

    def test_saver_yaml_loader_yaml(self):
        """Test saving and loading YAML files."""
        data = {"key": "value", "number": 42}

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "data"

            saver = SaverYAML(path)
            saver.save(data)
            assert (Path(tmpdir) / "data.yaml").exists()

            loader = LoaderYAML(path)
            loaded = loader.load()
            assert loaded == data

    def test_saver_yaml_loader_yml(self):
        """Test saving and loading with .yml extension."""
        data = {"key": "value", "number": 42}

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "data.yml"

            saver = SaverYAML(path)
            saver.save(data)
            assert (Path(tmpdir) / "data.yml").exists()

            loader = LoaderYAML(path)
            loaded = loader.load()
            assert loaded == data

    def test_saver_json_loader_json(self):
        """Test saving and loading JSON files."""
        data = {"key": "value", "number": 42}

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "data"

            saver = SaverJSON(path)
            saver.save(data)
            assert (Path(tmpdir) / "data.json").exists()

            loader = LoaderJSON(path)
            loaded = loader.load()
            assert loaded == data

    def test_saver_hdf5_loader_hdf5(self):
        """Test saving and loading HDF5 files."""
        h5py = pytest.importorskip("h5py")
        data = {"arr1": np.array([1, 2, 3]), "arr2": np.array([4, 5, 6])}

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "data"

            saver = SaverHDF5(path)
            saver.save(data)
            assert (Path(tmpdir) / "data.hdf5").exists() or (Path(tmpdir) / "data.h5").exists()

            loader = LoaderHDF5(path)
            loaded = loader.load()
            np.testing.assert_array_equal(loaded["arr1"], data["arr1"])
            np.testing.assert_array_equal(loaded["arr2"], data["arr2"])

    def test_saver_nonexistent_dir_raises(self):
        """Test that saving to nonexistent directory raises error."""
        with pytest.raises(FileNotFoundError, match="Directory does not exist"):
            SaverPKL("/nonexistent/path/file")

    def test_loader_nonexistent_file_raises(self):
        """Test that loading nonexistent file raises error."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with pytest.raises(FileNotFoundError, match="File does not exist"):
                LoaderPKL(Path(tmpdir) / "nonexistent")

    def test_saver_repr(self):
        """Test saver string representation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            saver = SaverPKL(Path(tmpdir) / "file")
            assert "SaverPKL" in repr(saver)
            assert "file.pkl" in repr(saver)

    def test_loader_logs_on_failure(self, caplog):
        """Test loader logs errors when load fails."""
        data = {"key": "value"}

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "bad.pkl"
            path.write_text("not a pickle", encoding="utf-8")

            loader = LoaderPKL(path)
            caplog.set_level(logging.ERROR)
            with pytest.raises(Exception):
                loader.load()
            assert any("Loader failed" in record.message for record in caplog.records)

    def test_saver_logs_on_failure(self, caplog):
        """Test saver logs errors when save fails."""
        class Unpickleable:
            def __getstate__(self):
                raise ValueError("Cannot pickle")

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "data"
            saver = SaverPKL(path)

            caplog.set_level(logging.ERROR)
            with pytest.raises(Exception):
                saver.save(Unpickleable())
            assert any("Saver failed" in record.message for record in caplog.records)


def test_public_api_exports():
    """Test public API exports for IO classes."""
    import morpha
    from morpha import (
        SaverYAML,
        SaverJSON,
        SaverNPZ,
        SaverHDF5,
        LoaderYAML,
        LoaderJSON,
        LoaderNPZ,
        LoaderHDF5,
    )

    assert morpha.SaverYAML is SaverYAML
    assert morpha.SaverJSON is SaverJSON
    assert morpha.SaverNPZ is SaverNPZ
    assert morpha.SaverHDF5 is SaverHDF5
    assert morpha.LoaderYAML is LoaderYAML
    assert morpha.LoaderJSON is LoaderJSON
    assert morpha.LoaderNPZ is LoaderNPZ
    assert morpha.LoaderHDF5 is LoaderHDF5
