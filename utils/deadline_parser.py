from datetime import datetime
from typing import Optional

import dateparser


def parse_deadline(deadline: Optional[str]) -> Optional[datetime]:
    """
    Parse an explicit contractual deadline into a datetime.

    Returns:
        datetime if the deadline can be directly interpreted.
        None if the deadline is missing or cannot be directly resolved.
    """

    if deadline is None:
        return None

    if not isinstance(deadline, str):
        raise ValueError("Deadline must be a string or None")

    deadline = deadline.strip()

    if not deadline:
        return None

    parsed_date = dateparser.parse(
        deadline,
        settings={
            "PREFER_DATES_FROM": "future",
            "RETURN_AS_TIMEZONE_AWARE": False,
        },
    )

    return parsed_date