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
        enable_gui: bool = True

        if len(args) == 3:
            if args[2] in ("--no-gui", "-t", "--cli"):
                enable_gui = False
            else:
                raise UsageError()

        cfg: Config = MapParser(map_path).cfg

        try:
            engine = SimulationEngine(cfg, enable_gui=enable_gui)
        except Exception:
            engine = SimulationEngine(cfg, enable_gui=False)

        engine.run()
        success = True

    except (ConfigError, SimulationError) as e:
        success = False
        print("\033[1;31mFAILURE!"
              "\nYOU MAKE THE CAT VERY UNHAPPY 😿\033[0m"
              f"\n{e}")
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
            print("\033[1;38;5;213mSUCCESS!"
                  "\nYOU MAKE THE CAT VERY HAPPY 😻\033[0m")
    return 0


if __name__ == "__main__":
    main(argv)
