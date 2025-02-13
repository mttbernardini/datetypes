# type: ignore

from datetime import date as _date
from datetime import datetime as _datetime
from datetime import time as _time

# --- basic symbols ---


class _InstanceCheckMeta(type):
    def __instancecheck__(self, instance):
        return self._subclass_check_hook(instance)


class Date(_date, metaclass=_InstanceCheckMeta):
    def __new__(cls, *args, **kwargs):
        # return an instance of datetime.date, not this proxy class
        return _date.__new__(_date, *args, **kwargs)

    @classmethod
    def _subclass_check_hook(cls, obj):
        # allow Date to be used as base class for instance checks.
        # bonus: reject _datetime instances
        return isinstance(obj, _date) and not isinstance(obj, _datetime)


class Time(_time, metaclass=_InstanceCheckMeta):
    def __new__(cls, *args, **kwargs):
        # return an instance of datetime.time, not this proxy class
        return _time.__new__(_time, *args, **kwargs)

    def __class_getitem__(cls, key):
        # support generic syntax at runtime
        return cls

    @classmethod
    def _subclass_check_hook(cls, obj):
        # allow Time to be used as base class for instance checks
        return isinstance(obj, _time)


class DateTime(_datetime, metaclass=_InstanceCheckMeta):
    def __new__(cls, *args, **kwargs):
        # return an instance of datetime.datetime, not this proxy class
        return _datetime.__new__(_datetime, *args, **kwargs)

    def __class_getitem__(cls, key):
        # support generic syntax at runtime
        return cls

    @classmethod
    def _subclass_check_hook(cls, obj):
        # allow DateTime to be used as base class for instance checks
        return isinstance(obj, _datetime)


# --- naive vs aware ---
try:
    # attach annotate-types for runtime introspection, if available
    from typing import Annotated

    from annotated_types import (
        Timezone,
    )

    NaiveTime = Annotated[Time, Timezone(None)]
    AwareTime = Annotated[Time, Timezone(...)]

    NaiveDateTime = Annotated[DateTime, Timezone(None)]
    AwareDateTime = Annotated[DateTime, Timezone(...)]

except Exception:
    # just alias symbols otherwise
    NaiveTime = Time
    AwareTime = Time

    NaiveDateTime = DateTime
    AwareDateTime = DateTime


# --- utility functions ---


def typed(dt):
    return dt


def is_naive(dt):
    # see: https://docs.python.org/3/library/datetime.html#determining-if-an-object-is-aware-or-naive
    arg = dt if isinstance(dt, _datetime) else None
    return dt.tzinfo is None or dt.tzinfo.utcoffset(arg) is None


def is_aware(dt):
    # see: https://docs.python.org/3/library/datetime.html#determining-if-an-object-is-aware-or-naive
    arg = dt if isinstance(dt, _datetime) else None
    return dt.tzinfo is not None and dt.tzinfo.utcoffset(arg) is not None


def as_naive(dt):
    assert is_naive(dt), f"Expected naive object, received {dt!r}"
    return dt


def as_aware(dt):
    assert is_aware(dt), f"Expected aware object, received {dt!r}"
    return dt


def as_date(dt):
    assert type(dt) is _date, f"Excepted datetime.date object, received {dt!r}"
    return dt
