#!/usr/bin/env python3

from sys import argv
from flyin import (
    MapParser,
    Config,
    ConfigError,
    UsageError,
    SimulationEngine,
    SimulationError
    )


def main(args: list[str]) -> int:

    try:
        if len(args) != 2:
            raise UsageError()
        cfg: Config = MapParser(args[1]).cfg
        sim = SimulationEngine(cfg)
        sim.run()

    except ConfigError as e:
        print("\033[1;31mFAILURE!"
              "\nYOU MAKE THE CAT VERY UNHAPPY 😿\033[0m"
              f"\n{e}")
        return (0)

    except SimulationError as e:
        print("\033[1;31mFAILURE!"
              "\nYOU MAKE THE CAT VERY UNHAPPY 😿\033[0m"
              f"\n{e}")
        return (0)

    print("\033[1;38;5;213mSUCCESS!"
          "\nYOU MAKE THE CAT VERY HAPPY 😻\033[0m")
    return (0)


if __name__ == "__main__":
    main(argv)
