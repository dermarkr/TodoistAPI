import datetime
from zoneinfo import ZoneInfo


def convert_time(time_str: str, user_timezone: str = "UTC") -> datetime:
    user_tz = ZoneInfo(user_timezone)

    time = datetime.datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    time = time.replace(tzinfo=ZoneInfo("UTC"))
    time = time.astimezone(user_tz)

    return time
