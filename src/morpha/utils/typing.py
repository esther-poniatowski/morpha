"""
Type variable re-exports for Morpha.

Type variables are defined in their canonical modules (where they are used
as generic parameters). This module re-exports them for convenience.

Canonical locations
-------------------
BaseT : morpha.coordinates.attributes
Products : morpha.creational.factory
Product : morpha.creational.builder
K, V, Q, R, C : morpha.structures.containers
AnyCoreData : morpha.structures.base
AnyAttribute : morpha.coordinates.base
"""

from morpha.coordinates.attributes import BaseT
from morpha.creational.factory import Products
from morpha.creational.builder import Product
from morpha.structures.containers import K, V
from morpha.structures.base import AnyCoreData
