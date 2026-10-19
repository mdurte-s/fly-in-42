def comment(msg: str) -> str:
    """Format a message as an italicized golden comment.

    Args:
        msg (str): The text message to format.

    Returns:
        str: ANSI formatted string.
    """
    return f"\033[3;38;5;178m\n# {msg}\033[0m"


def error(msg: str) -> str:
    """Format an error message with red prefix.

    Args:
        msg (str): Error description message.

    Returns:
        str: ANSI formatted error string.
    """
    return f"\033[0;31m[Error]\033[0m {msg}"


def m_error(msg: str) -> str:
    """Format a mandatory criteria error message.

    Args:
        msg (str): Mandatory error description message.

    Returns:
        str: ANSI formatted mandatory error string.
    """
    return f"\033[0;31m[Mandatory Criteria Error]\033[0m {msg}"


def op_error(msg: str) -> str:
    """Format an optional criteria error message.

    Args:
        msg (str): Optional error description message.

    Returns:
        str: ANSI formatted optional error string.
    """
    return f"\033[0;31m[Optional Criteria Error]\033[0m {msg}"


def bold(msg: str) -> str:
    """Format a string with bold text style.

    Args:
        msg (str): Text to format in bold.

    Returns:
        str: ANSI bold formatted string.
    """
    return f"\033[1m{msg}\033[0m"
