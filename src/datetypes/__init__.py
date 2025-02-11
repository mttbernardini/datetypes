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


# --- utility functions ---


def typed(dt):
    return dt


def is_naive(dt):
    # TODO: check utcoffset too, according to spec
    return dt.tzinfo is None


def is_aware(dt):
    # TODO: check utcoffset too, according to spec
    return dt.tzinfo is not None


def as_naive(dt):
    assert is_naive(dt), f"Expected naive object, received {dt}"
    return dt


def as_aware(dt):
    assert is_aware(dt), f"Expected aware object, received {dt}"
    return dt
