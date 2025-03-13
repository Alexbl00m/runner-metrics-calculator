"""
Formatting utilities for the Runner Performance Metrics Calculator.
"""


def format_time(seconds):
    """
    Format seconds into hours:minutes:seconds.

    Args:
        seconds (float): Time in seconds

    Returns:
        str: Formatted time string (e.g., "1:23:45" or "23:45")
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes}:{secs:02d}"


def format_pace(seconds_per_km):
    """
    Format pace in seconds per kilometer to min:sec format.

    Args:
        seconds_per_km (float): Pace in seconds per kilometer

    Returns:
        str: Formatted pace string (e.g., "4:30")
    """
    minutes = int(seconds_per_km // 60)
    seconds = int(seconds_per_km % 60)
    return f"{minutes}:{seconds:02d}"


def format_with_units(value, unit, precision=1):
    """
    Format a value with its units to specified precision.

    Args:
        value (float): The numeric value
        unit (str): The unit string (e.g., "watts", "ml/kg/min")
        precision (int): Number of decimal places

    Returns:
        str: Formatted string with value and units
    """
    return f"{value:.{precision}f} {unit}"