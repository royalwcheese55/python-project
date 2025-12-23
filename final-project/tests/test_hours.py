from datetime import datetime

from store_locator.services.hours import is_open_now, validate_hours


def test_validate_hours_accepts_range():
    assert validate_hours("08:00-17:00")
    assert not validate_hours("25:00-26:00")
    assert not validate_hours("09:00-09:00")


def test_is_open_now():
    morning = datetime(2024, 1, 1, 9, 30)
    evening = datetime(2024, 1, 1, 21, 30)
    assert is_open_now("08:00-17:00", now=morning)
    assert not is_open_now("08:00-17:00", now=evening)
