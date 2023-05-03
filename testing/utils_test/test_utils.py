from src.todoistAPI.utils import convert_time
import datetime
import zoneinfo
import pytest


@pytest.mark.parametrize("time_str, user_timezone, expected", [
    ("2022-04-19T12:34:56.789Z", "America/Los_Angeles", datetime.datetime(2022, 4, 19, 12, 34, 56, 789000, tzinfo=zoneinfo.ZoneInfo("UTC"))),
    ("2022-01-01T00:00:00.000Z", "Europe/Paris", datetime.datetime(2022, 1, 1, 1, 0, 0, tzinfo=zoneinfo.ZoneInfo("UTC"))),
    ("2021-12-31T23:59:59.999Z", "Asia/Tokyo", datetime.datetime(2022, 1, 1, 8, 59, 59, 999000, tzinfo=zoneinfo.ZoneInfo("UTC"))),
    ("2021-06-01T12:34:56.000Z", "UTC", datetime.datetime(2021, 6, 1, 12, 34, 56, tzinfo=zoneinfo.ZoneInfo("UTC"))),
])
def test_convert_time(time_str, user_timezone, expected):
    result = convert_time(time_str, user_timezone)

    expected = expected.astimezone(zoneinfo.ZoneInfo(user_timezone))
    assert result == expected

