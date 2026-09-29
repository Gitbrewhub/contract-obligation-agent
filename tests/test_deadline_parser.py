from datetime import datetime

from utils.deadline_parser import parse_deadline


def test_parse_explicit_date():
    result = parse_deadline("30 September 2026")

    assert isinstance(result, datetime)
    assert result.year == 2026
    assert result.month == 9
    assert result.day == 30


def test_parse_another_explicit_date_format():
    result = parse_deadline("September 30, 2026")

    assert isinstance(result, datetime)
    assert result.year == 2026
    assert result.month == 9
    assert result.day == 30


def test_missing_deadline():
    result = parse_deadline(None)

    assert result is None


def test_empty_deadline():
    result = parse_deadline("")

    assert result is None


def test_relative_deadline_requires_context():
    result = parse_deadline("within 30 days of signing")

    assert result is None


def test_invalid_deadline():
    result = parse_deadline("banana deadline xyz")

    assert result is None