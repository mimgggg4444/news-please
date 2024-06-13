from __future__ import print_function

from datetime import datetime, timedelta, tzinfo

from ..ago import human
from ..ago import delta2dict

# datetime objects
PRESENT = datetime.now()
PAST = PRESENT - timedelta(492, 58711, 45)  # days, secs, microseconds
FUTURE = PRESENT + timedelta(2, 12447, 967742)  # days, secs, microseconds

# timedelta objects
PAST_DELTA = PRESENT - PAST
FUTURE_DELTA = PRESENT - FUTURE
ONE_YEAR_FOUR_HOURS_DELTA = timedelta(365, 14400, 0)


class FixedOffset(tzinfo):
    """Fixed offset in minutes east from UTC.

    Adapted from Python's documentation about tzinfo objects:
    https://docs.python.org/2.7/library/datetime.html#tzinfo-objects
    """

    def __init__(self, offset):
        self._offset = timedelta(minutes=offset)

    def utcoffset(self, dt):
        return self._offset

    def tzname(self, dt):
        return "Test"

    def dst(self, dt):
        return timedelta(0)


def test_human_passed_datetime_is_string():
    assert isinstance(human(PAST), str)


def test_human_passed_timedelta_is_string():
    assert isinstance(human(PAST_DELTA), str)


def test_delta2dict_is_dict():
    assert isinstance(delta2dict(PAST_DELTA), dict)


def test_ago_in_past_human():
    assert "ago" in human(PAST)


def test_in_in_future_human():
    assert "in" in human(FUTURE)


def test_no_coma_in_one_precision():
    assert "," not in human(PAST, precision=1)
    assert "," not in human(FUTURE, precision=1)


def test_coma_in_three_precision():
    assert "," in human(PAST, precision=3)
    assert "," in human(FUTURE, precision=3)


def test_coma_in_out_of_bounds_precision():
    assert "," in human(PAST, precision=10)
    assert "," in human(FUTURE, precision=10)


def test_zero_day_is_skipped_display_hour():
    _result = human(ONE_YEAR_FOUR_HOURS_DELTA, precision=2)
    assert "year" in _result
    # day is 0 so it is skipped, so we should show hours ...
    assert "hour" in _result


def test_one_day_singular():
    assert "s" not in human(timedelta(1))


def test_two_day_plural():
    assert "s" in human(timedelta(2))


def test_abbreviation():
    assert "2d ago" in human(timedelta(2), abbreviate=True)
    assert "3d, 12h ago" in human(timedelta(3.5), abbreviate=True)
    assert "2h, 24m ago" in human(timedelta(.1), abbreviate=True)
    assert "1y, 35d ago" in human(timedelta(400), abbreviate=True)


def test_timestamp_integer():
    result = human(1474485467933 / 1000, precision=6)
    assert "minute" in result
    assert "second" in result
    assert "ago" in result


def test_timestamp_float():
    result = human(1474485467933 / 1000.0, precision=6)
    assert "minute" in result
    assert "second" in result
    assert "ago" in result


def test_past_tense():
    output = human(
        PAST,
        past_tense="titanic sunk {} ago",
        future_tense="titanic will sink in {} from now",
    )
    assert "titanic sunk" in output


def test_future_tense():
    output = human(
        FUTURE,
        past_tense="titanic sunk {} ago",
        future_tense="titanic will sink in {} from now",
    )
    assert "titanic will sink in" in output


def test_valid_past_dict():
    past_dict = delta2dict(PAST_DELTA)
    assert past_dict["year"] == 1
    assert past_dict["day"] == 127
    assert past_dict["hour"] == 16
    assert past_dict["minute"] == 18
    assert past_dict["microsecond"] == 45


def test_valid_future_dict():
    past_dict = delta2dict(FUTURE_DELTA)
    assert past_dict["year"] == 0
    assert past_dict["day"] == 2
    assert past_dict["hour"] == 3
    assert past_dict["minute"] == 27
    assert past_dict["millisecond"] == 967
    assert past_dict["microsecond"] == 742


def test_timezone_support():
    # test a naive datetime with no timezone
    # (add an extra minute to ensure it stays over an hour ahead during test)
    dt = datetime.now() + timedelta(minutes=61)
    output = human(dt)
    assert output.startswith("in 1 hour")

    # test a timezone-aware datetime with a UTC-2 timezone
    dt = datetime.now(tz=FixedOffset(-120)) + timedelta(minutes=61)
    output = human(dt)
    assert output.startswith("in 1 hour")


def example_usage():
    """Test and example usage"""

    print("\nTest past tense:\n")
    print(delta2dict(PAST_DELTA))
    print("Commented " + human(PAST_DELTA, 1))
    print(human(PAST, past_tense="Commented {} ago"))

    print(human(ONE_YEAR_FOUR_HOURS_DELTA, past_tense="Posted {} ago"))

    print("\nTest future tense:\n")
    print(delta2dict(FUTURE_DELTA))
    print("Shutdown " + human(FUTURE_DELTA, 5))
    print(human(FUTURE, future_tense="Shutdown in {} from now"))
    print("")


if __name__ == "__main__":
    example_usage()
