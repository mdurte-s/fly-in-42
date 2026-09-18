from .config import Config, ConfigError, StructError, hub
from .utils import to_int, bold, comment, error, m_error, op_error


def to_name(info: str) -> str:

    if " " in info or "-" in info:
        raise ConfigError(
            m_error('''Zone names can use any valid characters except:'''
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
                            f'''{(", ").join(Config.zones)}.'''))

    return info


def to_color(info: str) -> str:

    if info not in Config.colors:
        raise ConfigError(
            op_error('''String must be a color.'''
                     f'''\nInput: "{info}"\n''') +
            comment('''Colors available: ''') +
            comment(f'''{(", ").join(Config.colors)}.'''))

    return info


def to_hub(config: str) -> dict[str, tuple[int, int, str, str, int]]:

    new_hub: dict[str, tuple[int, int, str, str, int]] = {}
    info = config.split("[")

    if len(info) > 2 or (len(info) == 2 and info[1][-1] != "]"):
        raise StructError(error(hub))

    mandatory = info[0].split()
    optional = (info[1][:-1].split() if len(info) == 2 else "")

    if len(mandatory) != 3:
        raise ConfigError(m_error("EXPECTED: 'NAME X Y'"))

    zone = ""
    color = ""
    max_drones = 0

    for item in optional:
        items = item.split("=")
        if len(items) == 2:
            if items[0] == "zone" and not zone:
                zone = to_zone(items[1])
            elif items[0] == "color" and not color:
                color = to_color(items[1])
            elif items[0] == "max_drones" and not max_drones:
                max_drones = to_int(items[1], 1, True)
            else:
                raise ConfigError(op_error("EXPECTED: '[criteria=CRITERIA]'"))
        else:
            raise ConfigError(
                op_error("EXPECTED: "
                         "'[zone=ZONE color=COLOR max_drones=MAX_DRONES]'"))

    new_hub[to_name(mandatory[0])] = (
        to_int(mandatory[1], 0, False),
        to_int(mandatory[2], 0, False),
        zone,
        color,
        max_drones
        )

    return new_hub
