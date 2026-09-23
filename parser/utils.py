def to_int(info: str, criteria: int, positive: bool) -> int:

    try:
        value = int(info)
        if positive and value <= 0:
            raise ValueError()
        return value

    except ValueError:
        from .config import ConfigError

        if criteria and positive:
            raise ConfigError(
                op_error('''Value must be a postive integer above zero.'''
                         f'''\nInput: "{info}"'''))
        elif criteria and not positive:
            raise ConfigError(
                op_error('''Value must be an integer.'''
                         f'''\nInput: "{info}"'''))

        elif not criteria and positive:
            raise ConfigError(
                m_error('''Value must be a postive integer above zero.'''
                        f'''\nInput: "{info}"'''))
        else:
            raise ConfigError(
                m_error('''Value must be an integer.'''
                        f'''\nInput: "{info}"'''))


def comment(msg: str) -> str:
    return f"\033[3;38;5;178m# {msg}\033[0m"


def error(msg: str) -> str:
    return f"\033[3;31m[Error]\033[0m {msg}"


def m_error(msg: str) -> str:
    return f"\033[3;31m[Mandatory Criteria Error]\033[0m {msg}"


def op_error(msg: str) -> str:
    return f"\033[3;31m[Optional Criteria Error]\033[0m {msg}"


def bold(msg: str) -> str:
    return f"\033[1m{msg}\033[0m"
