# datetypes

```python
from datetime import date, time, datetime, timezone
from datetypes import Date, Time, DateTime, NaiveDateTime

t = Time(12, 0)
d = Date(2025, 2, 1)
dt = DateTime.combine(d, t)

# at type-checking, timezone info is carried via generics
assert_type(dt, DateTime[None])
# or, using an alias
assert_type(dt, NaiveDateTime)

# detect timezone incompatible comparisons
Time(12, 0, tzinfo=timezone.utc) < t  # mypy error! cannot compare Time[timezone] with Time[None]

# DateTime doesn't subclass Date
def message(d: Date):
    print(f"Hello, date is: {d}")
message(dt) # mypy error! DateTime is not compatible with Date

# at runtime, built-in types are used, zero overhead
type(d) is date
type(t) is time
type(dt) is datetime
```

An effort to provide type annotated and timezone-aware versions of the built-in
`datetime` module, only for static typing. At runtime the built-in classes from
`datetime` will always be used with zero overhead, including when evaluating
type annotations at runtime (e.g. Pydantic, FastAPI, etc.).

Greatly inspired by [`datetype`](https://github.com/glyph/DateType), but
re-imagined to provide no runtime behaviour changes (the typed symbols are
simply aliases over the built-in types) + clean type information subclassing
types from `datetime`, so that typed counterparts can be used in places where
original types are expected (e.g. existing libraries) without having to manually
cast (as compared to `datetype.concrete()`).

## Caveats

Since at runtime the typed versions are simply aliases to the built-in types,
generics don't work when used in runtime contexts! i.e. don't do
`DateTime[ZoneInfo]` in an expression that can be evaluated at runtime, it will
fail without being caught by your type linter (as the type stubs make this use
legit!). I currently don't have any non-invasive workaround for this, but I
expect this library to be mainly used for static type annotations.

## Documentation

WIP, but for examples simply refer to [tests/test_basic.py](tests/test_basic.py)
and other test files.
