"""
Drop-in replacements for `datetime` objects with better typing information.

Note: at runtime, actual `datetime` classes are used directly for minimum
performance overhead.
"""

__all__ = [
    "AwareDateTime",
    "AwareTime",
    "Date",
    "DateTime",
    "NaiveDateTime",
    "NaiveTime",
    "Time",
]

import sys
from datetime import date as _date
from datetime import datetime as _datetime
from datetime import time as _time
from datetime import timedelta as _timedelta
from datetime import tzinfo as _tzinfo
from typing import (
    ClassVar,
    Generic,
    SupportsIndex,
    overload,
)

from typing_extensions import Self, TypeAlias, TypeIs, TypeVar

_MaybeTZ = TypeVar(
    "_MaybeTZ",
    bound=_tzinfo | None,
    default=_tzinfo | None,
    covariant=True,
)
_OptionalTZ = TypeVar("_OptionalTZ", bound=_tzinfo | None)
_TZ = TypeVar("_TZ", bound=_tzinfo)

#
# === Date ===

# subclass _date to allow Date to be used in places where _date is expected
class Date(_date):
    """
    Date object with no time associated.
    """

    # restrict `datetime.date -> Self` to prevent comparisons with `DateTime`
    def __le__(self, value: Self, /) -> bool: ...
    def __lt__(self, value: Self, /) -> bool: ...
    def __ge__(self, value: Self, /) -> bool: ...
    def __gt__(self, value: Self, /) -> bool: ...
    #
    @overload
    def __sub__(self, value: Self, /) -> _timedelta: ...
    @overload
    def __sub__(self, value: _timedelta, /) -> Self: ...

#
# === Time & co. ===

class Time(_time, Generic[_MaybeTZ]):
    """
    Generic Time object with optional timezone attached.
    """

    # replace `datetime.time -> Time`
    min: ClassVar[Time]
    max: ClassVar[Time]

    def __new__(
        cls,
        hour: SupportsIndex = ...,
        minute: SupportsIndex = ...,
        second: SupportsIndex = ...,
        microsecond: SupportsIndex = ...,
        tzinfo: _MaybeTZ = None,
        *,
        fold: int = ...,
    ) -> Time[_MaybeTZ]: ...
    #
    # fix inherited stubs to consider generic timezone
    @property
    def tzinfo(self) -> _MaybeTZ: ...

    if sys.version_info >= (3, 13):
        def __replace__(
            self,
            /,
            *,
            hour: SupportsIndex = ...,
            minute: SupportsIndex = ...,
            second: SupportsIndex = ...,
            microsecond: SupportsIndex = ...,
            tzinfo: _OptionalTZ = ...,
            fold: int = ...,
        ) -> Time[_OptionalTZ]: ...

    def replace(
        self,
        hour: SupportsIndex = ...,
        minute: SupportsIndex = ...,
        second: SupportsIndex = ...,
        microsecond: SupportsIndex = ...,
        tzinfo: _OptionalTZ = None,
        *,
        fold: int = ...,
    ) -> Time[_OptionalTZ]: ...
    #
    # prevent aware-vs-naive comparisons
    @overload
    def __le__(self: NaiveTime, value: NaiveTime, /) -> bool: ...
    @overload
    def __le__(self: AwareTime, value: AwareTime, /) -> bool: ...
    @overload
    def __lt__(self: NaiveTime, value: NaiveTime, /) -> bool: ...
    @overload
    def __lt__(self: AwareTime, value: AwareTime, /) -> bool: ...
    @overload
    def __ge__(self: NaiveTime, value: NaiveTime, /) -> bool: ...
    @overload
    def __ge__(self: AwareTime, value: AwareTime, /) -> bool: ...
    @overload
    def __gt__(self: NaiveTime, value: NaiveTime, /) -> bool: ...
    @overload
    def __gt__(self: AwareTime, value: AwareTime, /) -> bool: ...

NaiveTime: TypeAlias = Time[None]
"""Alias for Time with no timezone associated."""
AwareTime: TypeAlias = Time[_tzinfo]
"""Alias for Time with timezone associated."""

#
# === DateTime & co. ===

class DateTime(_datetime, Generic[_MaybeTZ]):
    """
    Generic DateTime object with optional timezone attached.
    """

    # replace `datetime.date -> DateTime`
    min: ClassVar[DateTime]
    max: ClassVar[DateTime]

    def __new__(
        cls,
        year: SupportsIndex,
        month: SupportsIndex,
        day: SupportsIndex,
        hour: SupportsIndex = ...,
        minute: SupportsIndex = ...,
        second: SupportsIndex = ...,
        microsecond: SupportsIndex = ...,
        tzinfo: _MaybeTZ = None,
        *,
        fold: int = ...,
    ) -> DateTime[_MaybeTZ]: ...
    #
    # fix inherited stubs to consider generic timezone
    @property
    def tzinfo(self) -> _MaybeTZ: ...

    if sys.version_info >= (3, 12):
        @classmethod
        def fromtimestamp(
            cls, timestamp: float, tz: _OptionalTZ = None
        ) -> DateTime[_OptionalTZ]: ...
    else:
        @classmethod
        def fromtimestamp(
            cls, timestamp: float, /, tz: _OptionalTZ = None
        ) -> DateTime[_OptionalTZ]: ...

    @classmethod
    def utcfromtimestamp(cls, t: float, /) -> NaiveDateTime: ...
    #
    @classmethod
    def now(cls, tz: _OptionalTZ = None) -> DateTime[_OptionalTZ]: ...
    #
    @classmethod
    def utcnow(cls) -> NaiveDateTime: ...
    #
    @overload
    @classmethod
    def combine(
        cls, date: Date, time: Time[_OptionalTZ]
    ) -> DateTime[_OptionalTZ]: ...
    @overload
    @classmethod
    def combine(
        cls, date: Date, time: Time, tzinfo: _OptionalTZ
    ) -> DateTime[_OptionalTZ]: ...
    #
    def date(self) -> Date: ...
    def time(self) -> NaiveTime: ...
    def timetz(self) -> Time[_MaybeTZ]: ...

    if sys.version_info >= (3, 13):
        def __replace__(
            self,
            /,
            *,
            year: SupportsIndex = ...,
            month: SupportsIndex = ...,
            day: SupportsIndex = ...,
            hour: SupportsIndex = ...,
            minute: SupportsIndex = ...,
            second: SupportsIndex = ...,
            microsecond: SupportsIndex = ...,
            tzinfo: _OptionalTZ = None,
            fold: int = ...,
        ) -> DateTime[_OptionalTZ]: ...

    def replace(
        self,
        year: SupportsIndex = ...,
        month: SupportsIndex = ...,
        day: SupportsIndex = ...,
        hour: SupportsIndex = ...,
        minute: SupportsIndex = ...,
        second: SupportsIndex = ...,
        microsecond: SupportsIndex = ...,
        tzinfo: _OptionalTZ = None,
        *,
        fold: int = ...,
    ) -> DateTime[_OptionalTZ]: ...
    #
    @overload
    def astimezone(self, tz: None = None) -> AwareDateTime: ...
    @overload
    def astimezone(self, tz: _TZ) -> DateTime[_TZ]: ...
    #
    # prevent aware-vs-naive comparisons
    @overload
    def __le__(self: NaiveDateTime, value: NaiveDateTime, /) -> bool: ...
    @overload
    def __le__(self: AwareDateTime, value: AwareDateTime, /) -> bool: ...
    @overload
    def __lt__(self: NaiveDateTime, value: NaiveDateTime, /) -> bool: ...
    @overload
    def __lt__(self: AwareDateTime, value: AwareDateTime, /) -> bool: ...
    @overload
    def __ge__(self: NaiveDateTime, value: NaiveDateTime, /) -> bool: ...
    @overload
    def __ge__(self: AwareDateTime, value: AwareDateTime, /) -> bool: ...
    @overload
    def __gt__(self: NaiveDateTime, value: NaiveDateTime, /) -> bool: ...
    @overload
    def __gt__(self: AwareDateTime, value: AwareDateTime, /) -> bool: ...
    #
    @overload
    def __sub__(self: NaiveDateTime, value: NaiveDateTime, /) -> _timedelta: ...
    @overload
    def __sub__(self: AwareDateTime, value: AwareDateTime, /) -> _timedelta: ...
    @overload
    def __sub__(self, value: _timedelta, /) -> Self: ...
    #
    # fix stubs iherited from datetime.date that don't encode time
    @classmethod
    def today(cls) -> NaiveDateTime: ...
    @classmethod
    def fromordinal(cls, n: int, /) -> NaiveDateTime: ...
    @classmethod
    def fromisocalendar(
        cls, year: int, week: int, day: int
    ) -> NaiveDateTime: ...

NaiveDateTime: TypeAlias = DateTime[None]
"""Alias for DateTime with no timezone associated."""
AwareDateTime: TypeAlias = DateTime[_tzinfo]
"""Alias for DateTime with timezone associated."""

#
# === Utility functions ===

# typed()
@overload
def typed(dt: _time) -> Time: ...
@overload
def typed(dt: _datetime) -> DateTime: ...

# is_naive()
@overload
def is_naive(dt: _time) -> TypeIs[NaiveTime]: ...
@overload
def is_naive(dt: _datetime) -> TypeIs[NaiveDateTime]: ...

# is_aware()
@overload
def is_aware(dt: _time) -> TypeIs[AwareTime]: ...
@overload
def is_aware(dt: _datetime) -> TypeIs[AwareDateTime]: ...

# as_naive()
@overload
def as_naive(dt: _time) -> NaiveTime: ...
@overload
def as_naive(dt: _datetime) -> NaiveDateTime: ...

# as_aware()
@overload
def as_aware(dt: _time) -> AwareTime: ...
@overload
def as_aware(dt: _datetime) -> AwareDateTime: ...

# as_date()
def as_date(dt: _date) -> Date: ...
