"""
Drop-in replacements for `datetime` objects with better typing information.

Note: at runtime, `datetime` classes are used directly for minimum performance
overhead.
"""

from __future__ import annotations

__all__ = []

from datetime import date as _date
from datetime import datetime as _datetime
from datetime import time as _time
from datetime import timedelta
from datetime import tzinfo as _tzinfo
from typing import (
    TYPE_CHECKING,
    ClassVar,
    Generic,
    Optional,
    SupportsIndex,
    overload,
)

from typing_extensions import Self, TypeAlias, TypeVar

if TYPE_CHECKING:
    import sys

_MaybeTZ = TypeVar(
    "_MaybeTZ",
    bound="Optional[_tzinfo]",
    default="Optional[_tzinfo]",
    covariant=True,
)
_OptionalTZ = TypeVar("_OptionalTZ", bound="Optional[_tzinfo]")
_TZ = TypeVar("_TZ", bound=_tzinfo)


class _InstanceCheckMeta(type):
    def __instancecheck__(self, instance: object) -> bool:
        return self._instance_check_hook(instance)  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType, reportAttributeAccessIssue]


#
# === Date ===


class Date(_date, metaclass=_InstanceCheckMeta):
    """
    Date object with no time associated. Note that `datetime` won't match
    against this class.
    """

    if TYPE_CHECKING:
        pass

    else:

        def __new__(cls, *args, **kwargs):
            return _date(*args, **kwargs)

    @classmethod
    def _instance_check_hook(cls, instance: object):
        return isinstance(instance, _date) and not isinstance(
            instance, _datetime
        )


#
# === Time & co. ===


class Time(_time, Generic[_MaybeTZ], metaclass=_InstanceCheckMeta):
    """
    Generic time object with optional timezone attached.
    """

    if TYPE_CHECKING:
        min: ClassVar[Time]  # pyright: ignore[reportIncompatibleVariableOverride]
        max: ClassVar[Time]  # pyright: ignore[reportIncompatibleVariableOverride]

        def __new__(
            cls,
            hour: SupportsIndex = ...,
            minute: SupportsIndex = ...,
            second: SupportsIndex = ...,
            microsecond: SupportsIndex = ...,
            tzinfo: _OptionalTZ = None,
            *,
            fold: int = ...,
        ) -> Time[_OptionalTZ]: ...

        # TODO: parametrize on timezone
        # def utcoffset(self) -> timedelta | None: ...
        # def tzname(self) -> str | None: ...
        # def dst(self) -> timedelta | None: ...

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

        def replace(  # pyright: ignore[reportIncompatibleMethodOverride]
            self,
            hour: SupportsIndex = ...,
            minute: SupportsIndex = ...,
            second: SupportsIndex = ...,
            microsecond: SupportsIndex = ...,
            tzinfo: _OptionalTZ = None,
            *,
            fold: int = ...,
        ) -> Time[_OptionalTZ]: ...

    else:

        def __new__(cls, *args, **kwargs):
            return _time(*args, **kwargs)

    @classmethod
    def _instance_check_hook(cls, instance: object):
        return isinstance(instance, _time)
        # TODO: check timezone!


if TYPE_CHECKING:
    NaiveTime: TypeAlias = Time[None]
    AwareTime: TypeAlias = Time[_tzinfo]
else:
    # at runtime, isinstance() can't be done against a generic type
    class NaiveTime(Time[None]): ...

    class AwareTime(Time[_tzinfo]): ...


#
# === DateTime & co. ===


class DateTime(_datetime, Generic[_MaybeTZ], metaclass=_InstanceCheckMeta):
    """
    Generic datetime object with optional timezone attached.
    """

    if TYPE_CHECKING:
        min: ClassVar[DateTime]  # pyright: ignore[reportIncompatibleVariableOverride]
        max: ClassVar[DateTime]  # pyright: ignore[reportIncompatibleVariableOverride]

        def __new__(
            cls,
            year: SupportsIndex,
            month: SupportsIndex,
            day: SupportsIndex,
            hour: SupportsIndex = ...,
            minute: SupportsIndex = ...,
            second: SupportsIndex = ...,
            microsecond: SupportsIndex = ...,
            tzinfo: _OptionalTZ = None,
            *,
            fold: int = ...,
        ) -> DateTime[_OptionalTZ]: ...

        if sys.version_info >= (3, 12):

            @classmethod
            def fromtimestamp(
                cls, timestamp: float, tz: _OptionalTZ = None
            ) -> DateTime[_OptionalTZ]: ...
        else:

            @classmethod
            def fromtimestamp(  # pyright: ignore[reportIncompatibleMethodOverride]
                cls, timestamp: float, /, tz: _OptionalTZ = None
            ) -> DateTime[_OptionalTZ]: ...

        @classmethod
        def utcfromtimestamp(cls, t: float, /) -> DateTime[None]: ...  # pyright: ignore[reportIncompatibleMethodOverride]

        @classmethod
        def now(cls, tz: _OptionalTZ = None) -> DateTime[_OptionalTZ]: ...  # pyright: ignore[reportIncompatibleMethodOverride]

        @classmethod
        def utcnow(cls) -> DateTime[None]: ...  # pyright: ignore[reportIncompatibleMethodOverride]

        @overload
        @classmethod
        def combine(  # pyright: ignore[reportNoOverloadImplementation]
            cls, date: Date, time: Time[_OptionalTZ], tzinfo: None = ...
        ) -> DateTime[_OptionalTZ]: ...

        @overload
        @classmethod
        def combine(  # pyright: ignore[reportIncompatibleMethodOverride]
            cls, date: Date, time: Time, tzinfo: _TZ
        ) -> DateTime[_TZ]: ...

        def date(self) -> Date: ...
        def time(self) -> Time[None]: ...
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

        def replace(  # pyright: ignore[reportIncompatibleMethodOverride]
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

        @overload
        def astimezone(self) -> DateTime[_tzinfo]: ...  # pyright: ignore[reportNoOverloadImplementation]

        @overload
        def astimezone(  # pyright: ignore[reportIncompatibleMethodOverride]
            self, tz: _OptionalTZ = None
        ) -> DateTime[_OptionalTZ]: ...

        # TODO: be conditional on timezone
        # def tzname(self) -> str | None: ...
        # def dst(self) -> timedelta | None: ...

        def __le__(self, value: Self, /) -> bool: ...  # pyright: ignore[reportIncompatibleMethodOverride]
        def __lt__(self, value: Self, /) -> bool: ...  # pyright: ignore[reportIncompatibleMethodOverride]
        def __ge__(self, value: Self, /) -> bool: ...  # pyright: ignore[reportIncompatibleMethodOverride]
        def __gt__(self, value: Self, /) -> bool: ...  # pyright: ignore[reportIncompatibleMethodOverride]

    else:

        def __new__(cls, *args, **kwargs):
            return _datetime(*args, **kwargs)

    @classmethod
    def _instance_check_hook(cls, instance: object):
        return isinstance(instance, _datetime)
        # TODO: check timezone!


if TYPE_CHECKING:
    NaiveDateTime: TypeAlias = DateTime[None]
    AwareDateTime: TypeAlias = DateTime[_tzinfo]
else:
    # at runtime, isinstance() can't be done against a generic type
    class NaiveDateTime(DateTime[None]): ...

    class AwareDateTime(DateTime[_tzinfo]): ...
