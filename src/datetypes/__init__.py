# type: ignore

import gc as _gc
from datetime import date as _date
from datetime import datetime as _datetime
from datetime import time as _time

# --- basic symbols ---

Date = _date
Time = _time
DateTime = _datetime

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

    @classmethod
    def _generic_hook(cls, key):
        return Annotated[cls, Timezone(... if key is not None else None)]

except Exception:
    # just alias symbols otherwise
    NaiveTime = Time
    AwareTime = Time

    NaiveDateTime = DateTime
    AwareDateTime = DateTime

    @classmethod
    def _generic_hook(cls, key):
        return cls

# inject support for generic syntax at runtime with minimal work.
#
# NOTE: This may look really hacky - I don't want to resort to an actual
# subclass defining __class_getitem__ + metaclass for isinstance hooks, even if
# I were to return the concrete type on __new__(), because the type would be
# distinct from built-in and it won't play well with Pydantic and other
# libraries relying on runtime annotation introspection.


try:
    _gc.get_referents(_time.__dict__)[0]["__class_getitem__"] = _generic_hook
    _gc.get_referents(_datetime.__dict__)[0]["__class_getitem__"] = (
        _generic_hook
    )
except Exception:
    pass


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
