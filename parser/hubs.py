from dataclasses import dataclass
from .config import Config, ConfigError, StructError, hub
from .utils import to_int, bold, comment, error, m_error, op_error

@dataclass
class Hub():
    _name: str
    _x: int
    _y: int
    _zone: str = ""
    _color: str = ""
    _max_drones: int = 0


def to_name(info: str) -> str:

    if " " in info or "-" in info:
        raise ConfigError(
            m_error('''Hub names can use any valid characters except:'''
                    f'''\n  • {bold("dashes('-')")};'''
                    f'''\n  • {bold("spaces(' ')")}.'''
                    f'''\nInput: "{info}"'''))

    return info


def to_zone(info: str) -> str:

    if info not in Config.zones:
        raise ConfigError(
                    op_error('''String must be a zone type.'''
                             f'''\nInput: "{info}"\n''') +
                    comment(f'''Zone types available: '''
                            f'''\n{", ".join(Config.zones)}.'''))

    return info


def to_color(info: str) -> str:

    if info not in Config.colors:
        raise ConfigError(
            op_error('''String must be a color.'''
                     f'''\nInput: "{info}"\n''') +
            comment('''Colors available: ''') +
            comment(f'''\n{", ".join(Config.colors)}.'''))

    return info


OPTIONAL_PARSERS = {
    "zone": to_zone,
    "color": to_color,
    "max_drones": lambda val: to_int(val, 1, True)
}


def parse_optional_params(optional: list[str]) -> dict:
    params = {}
    for item in optional:
        if "=" not in item:
            raise ConfigError(op_error(hub))

        key, value = item.split("=", 1)
        if key not in OPTIONAL_PARSERS or key in params:
            raise ConfigError(op_error(hub))

        params[key] = OPTIONAL_PARSERS[key](value)
    return params


def to_hub(config: str) -> Hub:

    if "[" in config:
        if not config.endswith("]"):
            raise StructError(error(hub))
        mandatory_part, optional_part = config[:-1].split("[", 1)
        optional = optional_part.split()
    else:
        mandatory_part = config
        optional = []

    mandatory = mandatory_part.split()
    if len(mandatory) != 3:
        raise ConfigError(m_error(hub))

    opts = parse_optional_params(optional)

    return Hub(
        _name=to_name(mandatory[0]),
        _x=to_int(mandatory[1], 0, False),
        _y=to_int(mandatory[2], 0, False),
        _zone=opts.get("zone", ""),
        _color=opts.get("color", ""),
        _max_drones=opts.get("max_drones", "")
        )
