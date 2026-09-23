"""Timezone and local-time formatting."""

from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from utils.api_helpers import APIError


def get_local_time(timezone_name: str) -> dict[str, str]:
    """Return a timezone label and current local time without another API key."""
    try:
        local_time = datetime.now(ZoneInfo(timezone_name))
    except (ZoneInfoNotFoundError, ValueError) as exc:
        raise APIError("Local time is unavailable for this destination.") from exc
    return {
        "timezone": timezone_name,
        "local_time": local_time.strftime("%A, %B %d, %Y at %I:%M %p"),
        "utc_offset": local_time.strftime("UTC%z"),
    }