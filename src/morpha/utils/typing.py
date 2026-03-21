"""
Type variables and aliases for Morpha.

This module centralizes type definitions used across the package to ensure
consistency and enable proper generic type checking.
"""

from typing import TypeVar, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from morpha.components.base import DataComponent
    from morpha.structures.base import DataStructure


# --- Attribute Types ------------------------------------------------------------------------------

BaseT = TypeVar("BaseT", int, str, float, bool)
"""Type variable for the basic type from which an Attribute inherits."""


# --- Creational Pattern Types ---------------------------------------------------------------------

Products = TypeVar("Products", bound="DataComponent | Tuple[DataComponent, ...]")
"""Type variable for product class(es) created by a Factory."""

Product = TypeVar("Product", bound="DataStructure")
"""Type variable for the DataStructure class produced by a Builder."""


# --- Container Types ------------------------------------------------------------------------------

K = TypeVar("K")
"""Type variable for keys in a Container."""

V = TypeVar("V")
"""Type variable for values in a Container."""

Q = TypeVar("Q")
"""Type variable for keys in an input dictionary."""

R = TypeVar("R")
"""Type variable for return type of a function applied to container values."""

C = TypeVar("C", bound="Container")  # type: ignore[name-defined]
"""Type variable for Container and its subclasses."""


# --- Data Types -----------------------------------------------------------------------------------

AnyCoreData = TypeVar("AnyCoreData")
"""Type variable for the core data component stored in a DataStructure."""
