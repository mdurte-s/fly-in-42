#!/usr/bin/env python3

from sys import argv, exit

try:
    from flyin import (
        MapParser,
        Config,
        ConfigError,
        UsageError,
        SimulationEngine,
        SimulationError
        )
except ImportError as e:
    print(f"\033[0;31m[Import Error]\033[0m {e}"
          "\n\033[3;38;5;178m# Usage:"
          "\n# make install"
          "\n# make run MAP=path/config-file.txt\033[0m")
    exit(1)


def main(args: list[str]) -> int:

    success: bool = True

    try:
        if len(args) != 2:
            raise UsageError()
        cfg: Config = MapParser(args[1]).cfg
        engine = SimulationEngine(cfg)
        engine.run()

    except (ConfigError, SimulationError) as e:
        success = False
        print("\033[1;31mFAILURE!"
              "\nYOU MAKE THE CAT VERY UNHAPPY 😿\033[0m"
              f"\n{e}")
        return (1)

    finally:
        if success:
            print("\033[1;38;5;213mSUCCESS!"
                  "\nYOU MAKE THE CAT VERY HAPPY 😻\033[0m")
    return (0)


if __name__ == "__main__":
    main(argv)
