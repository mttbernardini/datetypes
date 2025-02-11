# type: ignore

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

except Exception:
    # just alias symbols otherwise
    NaiveTime = Time
    AwareTime = Time

    NaiveDateTime = DateTime
    AwareDateTime = DateTime

# attach support for generic syntax at runtime with minimal work.
#
# NOTE: This doesn't seem to work - I don't want to resort to an actual subclass
# using Generic (as done in the stubs), even if I were to return the concrete
# type on __new__(), otherwise the type may not play well with Pydantic and
# other libraries relying on runtime type annotations.
#
# Time.__class_getitem__ = lambda cls, _: cls
# DateTime.__class_getitem__ = lambda cls, _: cls


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
