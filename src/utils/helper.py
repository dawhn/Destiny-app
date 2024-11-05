import re


def parse_time(time_str):
    pattern = r"(?:(\d+)h)?\s*(?:(\d+)m)?\s*(?:(\d+)s)?"
    match = re.match(pattern, time_str)

    if match:
        hours = int(match.group(1)) if match.group(1) else 0
        minutes = int(match.group(2)) if match.group(2) else 0
        seconds = int(match.group(3)) if match.group(3) else 0

        total_seconds = seconds + 60 * minutes + 3600 * hours
        return total_seconds
    else:
        raise ValueError(f"Invalid time format: {time_str}")
