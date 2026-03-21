"""
Data structures module.

Provides abstract base classes for composite data structures with schema enforcement.
"""

from morpha.structures.base import DataStructure
from morpha.structures.containers import Container

__all__ = ["DataStructure", "Container"]
