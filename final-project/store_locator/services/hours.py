from __future__ import annotations

import re
from datetime import datetime, time
from typing import Optional

HOURS_PATTERN = re.compile(r"^(closed|[0-2]\d:[0-5]\d-[0-2]\d:[0-5]\d)$")


def validate_hours(value: str) -> bool:
    if not HOURS_PATTERN.match(value):
        return False
    if value == "closed":
        return True
    try:
        start_str, end_str = value.split("-")
        start = _parse_time(start_str)
        end = _parse_time(end_str)
    except ValueError:
        return False
    return start < end


def _parse_time(value: str) -> time:
    hour, minute = [int(x) for x in value.split(":")]
    return time(hour=hour, minute=minute)


def is_open_now(hours_value: str, now: Optional[datetime] = None) -> bool:
    if hours_value == "closed":
        return False
    now = now or datetime.now()
    start_str, end_str = hours_value.split("-")
    start = _parse_time(start_str)
    end = _parse_time(end_str)
    return start <= now.time() <= end
