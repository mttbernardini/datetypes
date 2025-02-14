import datetime
from typing import Annotated
from zoneinfo import ZoneInfo

from datetypes import (
    AwareDateTime,
    AwareTime,
    Date,
    DateTime,
    NaiveDateTime,
    NaiveTime,
    Time,
)

try:
    import pydantic
except ImportError:
    pass

else:

    class Event(pydantic.BaseModel):
        day: Date
        time: Time[None]
        fulldate: DateTime[ZoneInfo]

    def test_model_init():
        e = Event(
            day=Date(2024, 1, 1),
            time=Time(23, 0),
            # NOTE: type checking fails here, but pydantic semantics are not
            # influenced at runtime - the type annotation aliases a plain
            # datetime.datetime after all.
            #
            # NOTE: if annotated-types is available, then the alias contains a
            # annotated_types.Timezone(...) attached, but currently pydantic
            # makes no use of it, so validation will still work.
            fulldate=DateTime(2024, 1, 1, 23, 0),  # pyright: ignore[reportArgumentType]
        )
        # concrete types
        assert type(e.day) is datetime.date
        assert type(e.time) is datetime.time
        assert type(e.fulldate) is datetime.datetime

    def test_model_validate():
        e = Event.model_validate(
            {
                "day": "2024-01-01",
                "time": "12:00",
                # NOTE: same as above, this is naive - however a type-checker
                # can't dig anything here, as from a type perspective this is
                # legal.
                "fulldate": "2024-01-01T12:00:00",
            }
        )

        # concrete types
        assert type(e.day) is datetime.date
        assert type(e.time) is datetime.time
        assert type(e.fulldate) is datetime.datetime


def test_annotated_types():
    try:
        from annotated_types import Timezone

    except ImportError:
        # when no annotated-types are available, everything is a flat alias
        assert DateTime == datetime.datetime
        assert AwareDateTime == DateTime[ZoneInfo] == datetime.datetime
        assert NaiveDateTime == DateTime[None] == datetime.datetime

        assert Time == datetime.time
        assert AwareTime == Time[ZoneInfo] == datetime.time
        assert NaiveTime == Time[None] == datetime.time

    else:
        # when annotated-types are available, Timezone annotation is attached at
        # runtime
        assert DateTime == datetime.datetime
        assert (
            AwareDateTime
            == DateTime[ZoneInfo]
            == Annotated[datetime.datetime, Timezone(...)]  # pyright: ignore[reportUnknownArgumentType]
        )
        assert (
            NaiveDateTime
            == DateTime[None]
            == Annotated[datetime.datetime, Timezone(None)]
        )

        assert Time == datetime.time
        assert (
            AwareTime
            == Time[ZoneInfo]
            == Annotated[datetime.time, Timezone(...)]  # pyright: ignore[reportUnknownArgumentType]
        )
        assert (
            NaiveTime == Time[None] == Annotated[datetime.time, Timezone(None)]
        )

    # In either case, instances can be created out of the generic versions!
    assert Time[ZoneInfo](tzinfo=ZoneInfo("UTC"))
    assert DateTime[ZoneInfo](2024, 1, 1, tzinfo=ZoneInfo("UTC"))
    assert Time[None]()
    assert DateTime[None](2024, 1, 1)
