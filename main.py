#!/usr/bin/env python3

import os
from sys import argv, exit

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

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
    """Run the Fly-in simulation with parsed configuration.

    Args:
        args (list[str]): Command line arguments containing script name,
            map file path, and optional '--no-gui' flag.

    Returns:
        int: 0 on success, 1 on failure.
    """
    success: bool = False

    try:
        if len(args) < 2 or len(args) > 3:
            raise UsageError()

        map_path: str = args[1]
        enable_gui: bool = False
        statistics: bool = False

        if len(args) == 3:
            if args[2] == "--gui":
                enable_gui = True
            elif args[2] == "--statistics":
                statistics = True
            else:
                raise UsageError()

        print("\n\033[1m1. configuration file parsing:\033[0m", end=" ")
        cfg: Config = MapParser(map_path).cfg
        print("\033[0;32m[OK] ✅\033[0m")

        print("\n\033[1m2. starting engine:\033[0m", end=" ")
        engine = SimulationEngine(
            cfg, enable_gui=enable_gui, statistics=statistics
            )
        print("\033[0;32m[OK] ✅\033[0m")

        print("\n\033[1m3. running engine:\n\033[0m")
        engine.run()
        success = True

    except (ConfigError, SimulationError) as e:
        success = False
        print("[KO] ❌\n"
              f"\n{e}"
              "\n\n\033[1;31mFAILURE!"
              "\nYOU MAKE THE CAT VERY UNHAPPY 😿\033[0m"
              )
        return 1

    except KeyboardInterrupt:
        success = False
        print("\n\033[1;33mSimulation interrupted by user.\033[0m")
        return 1

    except Exception as e:
        success = False
        print(f"\033[1;31m[Unexpected Error]\033[0m {e}")
        return 1

    finally:
        if success:
            print("\n\033[1;38;5;213mSUCCESS!"
                  "\nYOU MAKE THE CAT VERY HAPPY 😻\033[0m")
    return 0


if __name__ == "__main__":
    main(argv)
