"""Tests for the Container class."""

import pytest
from morpha.structures.containers import Container


class TestContainer:
    """Tests for the Container class."""

    def test_creation(self):
        """Test basic container creation."""
        container = Container({1: "a", 2: "b"}, key_type=int, value_type=str)
        assert container[1] == "a"
        assert container[2] == "b"

    def test_missing_key_type_raises(self):
        """Test that missing key_type raises error."""
        with pytest.raises(ValueError, match="key_type"):
            Container({}, value_type=str)

    def test_missing_value_type_raises(self):
        """Test that missing value_type raises error."""
        with pytest.raises(ValueError, match="value_type"):
            Container({}, key_type=int)

    def test_setitem_valid_types(self):
        """Test setting items with valid types."""
        container = Container(key_type=int, value_type=str)
        container[1] = "hello"
        assert container[1] == "hello"

    def test_setitem_invalid_key_type_raises(self):
        """Test that invalid key type raises error."""
        container = Container(key_type=int, value_type=str)
        with pytest.raises(TypeError, match="Invalid key type"):
            container["not_an_int"] = "value"

    def test_setitem_invalid_value_type_raises(self):
        """Test that invalid value type raises error."""
        container = Container(key_type=int, value_type=str)
        with pytest.raises(TypeError, match="Invalid value type"):
            container[1] = 123

    def test_from_keys(self):
        """Test from_keys class method."""
        keys = [1, 2, 3]
        container = Container.from_keys(keys, "default", key_type=int, value_type=str)
        assert container[1] == "default"
        assert container[2] == "default"
        assert container[3] == "default"

    def test_list_keys(self):
        """Test list_keys method."""
        container = Container({1: "a", 2: "b"}, key_type=int, value_type=str)
        keys = container.list_keys()
        assert set(keys) == {1, 2}

    def test_list_values(self):
        """Test list_values method."""
        container = Container({1: "a", 2: "b"}, key_type=int, value_type=str)
        values = container.list_values()
        assert set(values) == {"a", "b"}

    def test_list_values_specific_keys(self):
        """Test list_values with specific keys."""
        container = Container({1: "a", 2: "b", 3: "c"}, key_type=int, value_type=str)
        values = container.list_values([1, 3])
        assert values == ["a", "c"]

    def test_to_dict(self):
        """Test to_dict method."""
        container = Container({1: "a", 2: "b"}, key_type=int, value_type=str)
        d = container.to_dict()
        assert d == {1: "a", 2: "b"}
        assert isinstance(d, dict)

    def test_get_subset(self):
        """Test get_subset method."""
        container = Container({1: "a", 2: "b", 3: "c"}, key_type=int, value_type=str)
        subset = container.get_subset([1, 3])
        assert len(subset) == 2
        assert subset[1] == "a"
        assert subset[3] == "c"
        assert 2 not in subset

    def test_filter_on_keys(self):
        """Test filter_on_keys method."""
        container = Container({1: "a", 2: "b", 3: "c"}, key_type=int, value_type=str)
        filtered = container.filter_on_keys(lambda k: k > 1)
        assert len(filtered) == 2
        assert 1 not in filtered
        assert filtered[2] == "b"
        assert filtered[3] == "c"

    def test_filter_on_values(self):
        """Test filter_on_values method."""
        container = Container({1: "aa", 2: "b", 3: "ccc"}, key_type=int, value_type=str)
        filtered = container.filter_on_values(lambda v: len(v) > 1)
        assert len(filtered) == 2
        assert 2 not in filtered
        assert filtered[1] == "aa"
        assert filtered[3] == "ccc"

    def test_fill(self):
        """Test fill method."""
        container = Container({1: "", 2: ""}, key_type=int, value_type=str)
        container.fill(lambda k: str(k * 10))
        assert container[1] == "10"
        assert container[2] == "20"

    def test_apply(self):
        """Test apply method."""
        container = Container({1: "a", 2: "bb"}, key_type=int, value_type=str)
        result = container.apply(len)
        assert result[1] == 1
        assert result[2] == 2
        assert result.value_type == int

    def test_find_types(self):
        """Test find_types static method."""
        data = {1: "a", 2: "b"}
        key_type, value_type = Container.find_types(data)
        assert key_type == int
        assert value_type == str

    def test_find_types_empty_raises(self):
        """Test that find_types raises on empty dict."""
        with pytest.raises(TypeError, match="empty"):
            Container.find_types({})

    def test_apply_method_broadcast(self):
        """Test broadcasting a method call to values via apply()."""

        class MyValue:
            def __init__(self, x):
                self.x = x

            def double(self):
                return self.x * 2

        container = Container(
            {1: MyValue(10), 2: MyValue(20)}, key_type=int, value_type=MyValue
        )
        result = container.apply(lambda v: v.double())
        assert result[1] == 20
        assert result[2] == 40
