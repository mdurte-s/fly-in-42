def comment(msg: str) -> str:
    return f"\033[3;38;5;178m{msg}\033[0m"


def error(msg: str) -> str:
    return f"\033[3;31m[Error]\033[0m {msg}"


def bold(msg: str) -> str:
    return f"\033[1m{msg}\033[0m"
