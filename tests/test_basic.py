from datetime import date, datetime, time, timedelta, timezone

import pytest
from typing_extensions import assert_type

from datetypes import (
    AwareDateTime,
    AwareTime,
    Date,
    DateTime,
    NaiveDateTime,
    NaiveTime,
    Time,
    as_date,
    is_aware,
    is_naive,
    typed,
)


def native_function(
    d: date, t: time, dt: datetime
) -> tuple[date, time, datetime]:
    return d, t, dt


def typed_function(
    d: Date, t: Time, dt: DateTime
) -> tuple[Date, Time, DateTime]:
    return d, t, dt


def naive_function(t: NaiveTime, dt: NaiveDateTime) -> tuple[Time, DateTime]:
    return t, dt


def aware_function(t: AwareTime, dt: AwareDateTime) -> tuple[Time, DateTime]:
    return t, dt


def test_native_basic():
    d = date(2024, 1, 1)
    t = time(12, 0)
    dt = datetime(2024, 1, 2, 13, 0)

    # check function calls
    native_function(d, t, dt)
    typed_function(as_date(d), typed(t), typed(dt))

    # typing assertions
    assert_type(d, date)
    assert_type(t, time)
    assert_type(dt, datetime)

    # check native assertions
    assert isinstance(d, date)
    assert isinstance(t, time)
    assert isinstance(dt, datetime)

    # check typed assertions
    assert isinstance(d, Date)
    assert isinstance(t, Time)
    assert isinstance(dt, DateTime)


def test_typed_basic():
    d: Date = Date(2024, 1, 1)
    t: Time = Time(12, 0)
    dt: DateTime = DateTime(2024, 1, 2, 13, 0)

    # check function calls
    native_function(d, t, dt)
    typed_function(d, t, dt)

    # check native assertions
    assert isinstance(d, date)
    assert isinstance(t, time)
    assert isinstance(dt, datetime)

    # check typed assertions
    assert isinstance(d, Date)
    assert isinstance(t, Time)
    assert isinstance(dt, DateTime)


def test_naive_versions():
    t: Time = NaiveTime(12, 0)
    dt: DateTime = NaiveDateTime(2024, 1, 1, 15, 0)

    # check function calls
    naive_function(t, dt)
    native_function(dt.date(), t, dt)

    # check strict types # TODO
    # assert isinstance(t, NaiveTime)
    # assert isinstance(dt, NaiveDateTime)
    # assert not isinstance(t, AwareTime)
    # assert not isinstance(dt, AwareDateTime)

    # check lax types
    assert isinstance(t, Time)
    assert isinstance(dt, DateTime)

    # check native types
    assert isinstance(t, time)
    assert isinstance(dt, datetime)


def test_aware_versions():
    t: Time = AwareTime(12, 0, tzinfo=timezone.utc)
    dt: DateTime = AwareDateTime(2024, 1, 1, 15, 0, tzinfo=timezone.utc)

    # check function calls
    aware_function(t, dt)
    native_function(dt.date(), t, dt)

    # check strict types # TODO
    # assert isinstance(t, AwareTime)
    # assert isinstance(dt, AwareDateTime)
    # assert not isinstance(t, NaiveTime)
    # assert not isinstance(dt, NaiveDateTime)

    # check lax types
    assert isinstance(t, Time)
    assert isinstance(dt, DateTime)

    # check native types
    assert isinstance(t, time)
    assert isinstance(dt, datetime)


def test_incompatible_aliases():
    # no timezone provided, should type error
    actually_naive_t = AwareTime(12, 0)  # pyright: ignore[reportArgumentType]
    assert actually_naive_t

    actually_naive_dt = AwareDateTime(2024, 1, 1, 12, 0)  # pyright: ignore[reportArgumentType]
    assert actually_naive_dt

    # timezone provided, should type error
    actually_aware_t = NaiveTime(12, 0, tzinfo=timezone.utc)  # pyright: ignore[reportArgumentType]
    assert actually_aware_t

    actually_aware_dt = NaiveDateTime(2024, 1, 1, 12, 0, tzinfo=timezone.utc)  # pyright: ignore[reportArgumentType]
    assert actually_aware_dt


@pytest.mark.skip(reason="unclear whether we want generics at runtime?")
def test_generic_versions():
    aware_t: AwareTime = Time(12, 0, tzinfo=timezone.utc)
    assert isinstance(aware_t, AwareTime)  # pyright: ignore[reportArgumentType]

    aware_dt: AwareDateTime = DateTime(2024, 1, 1, 15, 0, tzinfo=timezone.utc)
    assert isinstance(aware_dt, AwareDateTime)  # pyright: ignore[reportArgumentType]

    naive_t: NaiveTime = Time(12, 0)
    assert isinstance(naive_t, NaiveTime)  # pyright: ignore[reportArgumentType]

    naive_dt: NaiveDateTime = DateTime(2024, 1, 1, 15, 0)
    assert isinstance(naive_dt, NaiveDateTime)  # pyright: ignore[reportArgumentType]


@pytest.mark.skip(reason="unclear whether we want generics at runtime?")
def test_generic_parameters():
    My_DateTime = DateTime[timezone]
    My_Time = Time[timezone]

    # just alias at runtime
    assert type(My_DateTime(2024, 1, 1, tzinfo=timezone.utc)) == datetime  # noqa: E721
    assert type(My_Time(12, 0, tzinfo=timezone.utc)) == time  # noqa: E721


def test_datetime_is_not_date():
    dt = DateTime(2024, 1, 1, 15, 0)
    assert_type(dt.date(), Date)

    # assert not isinstance(dt, Date) # TODO
    assert isinstance(dt.date(), Date)


def test_today():
    today = Date.today()
    assert_type(today, Date)


def test_replace():
    dt = DateTime(2024, 1, 1, 15, 0)
    assert_type(dt, NaiveDateTime)
    assert is_naive(dt)

    dt_with_tz = dt.replace(tzinfo=timezone.utc)
    assert_type(dt_with_tz, "DateTime[timezone]")
    assert is_aware(dt_with_tz)

    dt_with_tz_removed = dt_with_tz.replace(tzinfo=None)
    assert_type(dt_with_tz_removed, NaiveDateTime)
    assert is_naive(dt_with_tz_removed)

    t = Time(13, 0)
    assert_type(t, NaiveTime)
    assert is_naive(t)

    t_with_tz = t.replace(tzinfo=timezone.utc)
    assert_type(t_with_tz, "Time[timezone]")
    assert is_aware(t_with_tz)

    t_with_tz_removed = t.replace(tzinfo=None)
    assert_type(t_with_tz_removed, NaiveTime)
    assert is_naive(t_with_tz_removed)


def test_maths():
    d = Date(2024, 1, 1)
    t = Time(15, 0)
    dt = DateTime.combine(d, t)

    d_plus_one: Date = d + timedelta(days=1)
    assert d_plus_one

    d_minus_one: Date = d - timedelta(days=1)
    assert d_minus_one

    dt_plus_one: DateTime = dt + timedelta(days=1)
    assert dt_plus_one

    dt_minus_one: DateTime = dt - timedelta(days=1)
    assert dt_minus_one

    diff1: timedelta = d - d
    assert diff1.total_seconds() == 0

    diff2: timedelta = dt - dt
    assert diff2.total_seconds() == 0

    with pytest.raises(TypeError):
        assert d - dt  # pyright: ignore[reportOperatorIssue]

    with pytest.raises(TypeError):
        assert dt - d  # pyright: ignore[reportOperatorIssue]
