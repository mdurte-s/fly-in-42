#!/usr/bin/env python3

from sys import argv
from flyin import (
    MapParser,
    Config,
    ConfigError,
    UsageError,
    Simulation
    )


def main(args: list[str]) -> int:

    try:
        if len(args) != 2:
            raise UsageError()
        cfg: Config = MapParser(args[1]).parser

    except ConfigError as e:
        print("\033[1;31mFAILURE!"
              "\nYOU MAKE THE CAT VERY UNHAPPY 😿\033[0m"
              f"\n{e}")
        return (0)

    print("\033[1;38;5;213mSUCCESS!"
          "\nYOU MAKE THE CAT VERY HAPPY 😻\033[0m")

    fly = Simulation(cfg=cfg)
    fly.solver()
    path = fly._path
    print("path: ", end="")
    for hub in path:
        print(f"{hub._name} ", end="")
    return (0)


if __name__ == "__main__":
    main(argv)
