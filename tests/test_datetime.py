from datetime import timezone
from zoneinfo import ZoneInfo

import pytest

from datetypes import (
    AwareDateTime,
    AwareTime,
    Date,
    DateTime,
    NaiveDateTime,
    NaiveTime,
    Time,
    is_aware,
    is_naive,
)


def test_now():
    naive_dt = DateTime.now()
    aware_dt = DateTime.now(timezone.utc)
    enforced_naive_dt = DateTime.now(None)

    assert is_naive(naive_dt)
    assert is_aware(aware_dt)
    assert is_naive(enforced_naive_dt)


def test_combine():
    d = Date(2024, 1, 1)
    t = Time(12, 0)
    ttz = Time(12, 0, tzinfo=timezone.utc)

    dt_default_naive: NaiveDateTime = DateTime.combine(d, t)
    assert is_naive(dt_default_naive)

    dt_default_aware: AwareDateTime = DateTime.combine(d, ttz)
    assert is_aware(dt_default_aware)

    dt_tz_added_from_naive: AwareDateTime = DateTime.combine(d, t, timezone.utc)
    assert is_aware(dt_tz_added_from_naive)

    dt_tz_added_from_aware: AwareDateTime = DateTime.combine(
        d, ttz, timezone.utc
    )
    assert is_aware(dt_tz_added_from_aware)

    dt_tz_removed_from_naive: NaiveDateTime = DateTime.combine(d, t, None)
    assert is_naive(dt_tz_removed_from_naive)

    dt_tz_removed_from_aware: NaiveDateTime = DateTime.combine(d, ttz, None)
    assert is_naive(dt_tz_removed_from_aware)


def test_naive_components():
    naive_dt: DateTime = DateTime(2024, 1, 1, 12, 0)

    d: Date = naive_dt.date()
    assert isinstance(d, Date)

    t: NaiveTime = naive_dt.time()
    assert is_naive(t)

    ttz: NaiveTime = naive_dt.timetz()
    assert is_naive(ttz)


def test_aware_components():
    aware_dt: DateTime = DateTime(2024, 1, 1, 12, 0, tzinfo=timezone.utc)

    d: Date = aware_dt.date()
    assert isinstance(d, Date)

    t: NaiveTime = aware_dt.time()
    assert is_naive(t)

    ttz: AwareTime = aware_dt.timetz()
    assert is_aware(ttz)


@pytest.mark.parametrize(
    "dt",
    (
        DateTime(2024, 1, 1, 12, 0),
        DateTime(2024, 1, 1, 12, 0, tzinfo=timezone.utc),
    ),
    ids=("naive", "aware"),
)
def test_astimezone(dt: DateTime):
    local: AwareDateTime = dt.astimezone()
    assert is_aware(local)

    changed: AwareDateTime = dt.astimezone(timezone.utc)
    assert is_aware(changed)

    local_explicit: AwareDateTime = dt.astimezone(None)
    assert is_aware(local_explicit)


def test_comparisons():
    naive_dt: DateTime = DateTime(2024, 1, 1, 12, 0)
    aware_dt: DateTime = DateTime(2024, 1, 1, 12, 0, tzinfo=timezone.utc)
    aware_dt_zone: DateTime = DateTime(
        2024, 1, 1, 12, 0, tzinfo=ZoneInfo("UTC")
    )

    assert aware_dt >= aware_dt <= aware_dt
    assert aware_dt >= aware_dt_zone <= aware_dt
    assert naive_dt >= naive_dt <= naive_dt

    with pytest.raises(TypeError):
        assert aware_dt <= naive_dt  # pyright: ignore[reportOperatorIssue]
        assert naive_dt <= aware_dt  # pyright: ignore[reportOperatorIssue]

    with pytest.raises(TypeError):
        assert aware_dt_zone <= naive_dt  # pyright: ignore[reportOperatorIssue]
        assert naive_dt <= aware_dt_zone  # pyright: ignore[reportOperatorIssue]


def test_difference():
    naive_dt: DateTime = DateTime(2024, 1, 1, 12, 0)
    aware_dt: DateTime = DateTime(2024, 1, 1, 12, 0, tzinfo=timezone.utc)
    aware_dt_zone: DateTime = DateTime(
        2024, 1, 1, 12, 0, tzinfo=ZoneInfo("UTC")
    )

    assert (aware_dt - aware_dt).total_seconds() == 0
    assert (naive_dt - naive_dt).total_seconds() == 0
    assert (aware_dt - aware_dt_zone).total_seconds() == 0

    with pytest.raises(TypeError):
        assert aware_dt - naive_dt  # pyright: ignore[reportOperatorIssue]

    with pytest.raises(TypeError):
        assert naive_dt - aware_dt  # pyright: ignore[reportOperatorIssue]

    with pytest.raises(TypeError):
        assert naive_dt - aware_dt_zone  # pyright: ignore[reportOperatorIssue]


def test_inherited_from_date():
    ts: NaiveDateTime = DateTime.fromtimestamp(1234567890)
    assert isinstance(ts, DateTime)
    # assert not isinstance(ts, Date)

    today: NaiveDateTime = DateTime.today()
    assert isinstance(today, DateTime)
    # assert not isinstance(today, Date)

    ord: NaiveDateTime = DateTime.fromordinal(123)
    assert isinstance(ord, DateTime)
    # assert not isinstance(ord, Date)

    isoform: DateTime = DateTime.fromisoformat("2024-03-01")
    assert isinstance(isoform, DateTime)
    # assert not isinstance(isoform, Date)

    isocal: NaiveDateTime = DateTime.fromisocalendar(2024, 3, 2)
    assert isinstance(isocal, DateTime)
    # assert not isinstance(calendar, Date)
