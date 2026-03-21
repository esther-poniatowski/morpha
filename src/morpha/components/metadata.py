"""
Metadata field specification for data components.

Classes
-------
MetaDataField
    Specification for a metadata attribute on a DataComponent.
"""

from dataclasses import dataclass
from typing import Any, Type


@dataclass
class MetaDataField:
    """
    Metadata field specification for a data component.

    Defines the expected type and default value for a metadata attribute
    that can be attached to DataComponent subclasses.

    Attributes
    ----------
    field_type : Type[Any]
        Expected type of the metadata field.
    default_value : Any
        Default value for the field when not provided.

    Examples
    --------
    Define metadata fields for a custom DataComponent:

    >>> class TimeData(DataComponent):
    ...     METADATA = {
    ...         "origin": MetaDataField(str, None),
    ...         "time_unit": MetaDataField(str, "sec"),
    ...     }
    """

    field_type: Type[Any]
    default_value: Any
