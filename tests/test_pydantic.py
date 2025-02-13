import datetime
from zoneinfo import ZoneInfo

import pydantic

from datetypes import Date, DateTime, Time


class Event(pydantic.BaseModel):
    day: Date
    time: Time[None]
    fulldate: DateTime[ZoneInfo]


def test_model_init():
    e = Event(
        day=Date(2024, 1, 1),
        time=Time(23, 0),
        # NOTE: type checking fails here, but pydantic semantics are not
        # influenced at runtime - it's just a plain datetime.datetime after all
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
            # NOTE: this is actually naive, pydantic semantics are not
            # influenced
            "fulldate": "2024-01-01T12:00:00",
        }
    )

    # concrete types
    assert type(e.day) is datetime.date
    assert type(e.time) is datetime.time
    assert type(e.fulldate) is datetime.datetime
