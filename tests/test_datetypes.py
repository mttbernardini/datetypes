from datetime import date, datetime, time, timezone

from typing_extensions import assert_type

from datetypes import (
    AwareDateTime,
    AwareTime,
    Date,
    DateTime,
    NaiveDateTime,
    NaiveTime,
    Time,
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
    typed_function(d, t, dt)

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
    d = Date(2024, 1, 1)
    t = Time(12, 0)
    dt = DateTime(2024, 1, 2, 13, 0)

    # check function calls
    native_function(d, t, dt)
    typed_function(d, t, dt)

    # typing assertions
    assert_type(d, Date)
    assert_type(t, NaiveTime)
    assert_type(dt, DateTime)

    # check native assertions
    assert isinstance(d, date)
    assert isinstance(t, time)
    assert isinstance(dt, datetime)

    # check typed assertions
    assert isinstance(d, Date)
    assert isinstance(t, Time)
    assert isinstance(dt, DateTime)


def test_naive_versions():
    t = NaiveTime(12, 0)
    dt = NaiveDateTime(2024, 1, 1, 15, 0)

    # check function calls
    naive_function(t, dt)
    native_function(dt.date(), t, dt)

    # typing assertions
    assert_type(t, NaiveTime)
    assert_type(dt, NaiveDateTime)

    # check strict types
    assert isinstance(t, NaiveTime)
    assert isinstance(dt, NaiveDateTime)
    assert not isinstance(t, AwareTime)
    assert not isinstance(dt, AwareDateTime)

    # check lax types
    assert isinstance(t, Time)
    assert isinstance(dt, DateTime)

    # check native types
    assert isinstance(t, time)
    assert isinstance(dt, datetime)


def test_aware_versions():
    t = AwareTime(12, 0, tzinfo=timezone.utc)
    dt = AwareDateTime(2024, 1, 1, 15, 0, tzinfo=timezone.utc)

    # check function calls
    aware_function(t, dt)
    native_function(dt.date(), t, dt)

    # typing assertions
    assert_type(t, AwareTime)
    assert_type(dt, AwareDateTime)

    # check strict types
    assert isinstance(t, AwareTime)
    assert isinstance(dt, AwareDateTime)
    assert not isinstance(t, NaiveTime)
    assert not isinstance(dt, NaiveDateTime)

    # check lax types
    assert isinstance(t, Time)
    assert isinstance(dt, DateTime)

    # check native types
    assert isinstance(t, time)
    assert isinstance(dt, datetime)


def test_generic_versions():
    aware_t = Time(12, 0, tzinfo=timezone.utc)
    assert_type(aware_t, AwareTime)
    assert isinstance(aware_t, AwareTime)

    aware_dt = DateTime(2024, 1, 1, 15, 0, tzinfo=timezone.utc)
    assert_type(aware_dt, AwareDateTime)
    assert isinstance(aware_dt, AwareDateTime)

    naive_t = Time(12, 0)
    assert_type(naive_t, NaiveTime)
    assert isinstance(naive_t, NaiveTime)

    naive_dt = DateTime(2024, 1, 1, 15, 0)
    assert_type(naive_dt, NaiveDateTime)
    assert isinstance(naive_dt, NaiveDateTime)


def test_datetime_is_not_date():
    dt = DateTime(2024, 1, 1, 15, 0)
    assert not isinstance(dt, Date)
    assert isinstance(dt.date(), Date)
    assert_type(dt.date(), Date)
