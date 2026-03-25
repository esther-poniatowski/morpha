"""Tests for the Attribute class."""

import pytest
from morpha.coordinates.attributes import Attribute


class Task(str, Attribute[str]):
    """Example attribute for testing."""

    OPTIONS = frozenset(["PTD", "CLK"])
    LABELS = {"PTD": "Pursuit Tracking", "CLK": "Clock Task"}

    def __new__(cls, value: str):
        if not cls.is_valid(value):
            raise ValueError(f"Invalid value: {value}")
        return super().__new__(cls, value)


class Priority(int, Attribute[int]):
    """Example integer attribute for testing."""

    OPTIONS = frozenset([1, 2, 3])
    LABELS = {1: "Low", 2: "Medium", 3: "High"}

    def __new__(cls, value: int):
        if not cls.is_valid(value):
            raise ValueError(f"Invalid value: {value}")
        return super().__new__(cls, value)


class TestAttribute:
    """Tests for the Attribute class."""

    def test_creation_valid(self):
        """Test creating attribute with valid value."""
        task = Task("PTD")
        assert task == "PTD"

    def test_creation_invalid_raises(self):
        """Test that invalid value raises error."""
        with pytest.raises(ValueError, match="Invalid value"):
            Task("INVALID")

    def test_is_valid(self):
        """Test is_valid class method."""
        assert Task.is_valid("PTD")
        assert Task.is_valid("CLK")
        assert not Task.is_valid("INVALID")

    def test_full_label(self):
        """Test full_label property."""
        task = Task("PTD")
        assert task.full_label == "Pursuit Tracking"

    def test_full_label_missing(self):
        """Test full_label with no label defined."""

        class NoLabels(str, Attribute[str]):
            OPTIONS = frozenset(["A", "B"])
            LABELS = {}

            def __new__(cls, value):
                if not cls.is_valid(value):
                    raise ValueError(f"Invalid: {value}")
                return super().__new__(cls, value)

        obj = NoLabels("A")
        assert obj.full_label == ""

    def test_get_options(self):
        """Test get_options class method."""
        options = Task.get_options()
        assert options == frozenset(["PTD", "CLK"])

    def test_get_labels(self):
        """Test get_labels class method."""
        labels = Task.get_labels()
        assert labels == {"PTD": "Pursuit Tracking", "CLK": "Clock Task"}

    def test_int_attribute(self):
        """Test integer-based attribute."""
        priority = Priority(2)
        assert priority == 2
        assert priority.full_label == "Medium"

    def test_from_container_list(self):
        """Test from_container returning list."""
        values = ["PTD", "CLK", "PTD"]
        result = Task.from_container(values, container=list)
        assert result == ["PTD", "CLK", "PTD"]
        assert isinstance(result, list)
        assert all(isinstance(item, Task) for item in result)

    def test_from_container_set(self):
        """Test from_container returning set."""
        values = ["PTD", "CLK", "PTD"]
        result = Task.from_container(values, container=set)
        assert result == {"PTD", "CLK"}
        assert isinstance(result, set)

    def test_from_container_invalid_raises(self):
        """Test from_container with invalid value raises."""
        with pytest.raises(ValueError, match="Invalid value"):
            Task.from_container(["PTD", "INVALID"])

    def test_repr(self):
        """Test string representation - uses base type's repr due to MRO."""
        task = Task("PTD")
        # Note: When inheriting from str first (str, Attribute), str's __repr__ is used
        # This is expected Python MRO behavior for mixins
        assert "PTD" in repr(task)

    def test_behaves_like_base_type(self):
        """Test that attribute behaves like its base type."""
        task = Task("PTD")

        # String operations
        assert task.upper() == "PTD"
        assert task + "_suffix" == "PTD_suffix"

        priority = Priority(2)

        # Integer operations
        assert priority + 1 == 3
        assert priority * 2 == 4
