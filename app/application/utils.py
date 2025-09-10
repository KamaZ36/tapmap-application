from datetime import datetime, timezone


def get_datetime_utc_now() -> datetime:
    datetime_now = datetime.now(tz=timezone.utc)
    return datetime_now.replace(tzinfo=None)
