#!/usr/bin/env python3

from sys import argv
from parser import parser, Config, ConfigError, UsageError


def main(args: list[str]) -> int:

    try:
        if len(args) != 2:
            raise UsageError()
        cfg: Config = parser(args[1])

    except ConfigError as e:
        print("\033[1;31mFAILURE!"
              "\nYOU MAKE THE CAT VERY UNHAPPY 😿\033[0m"
              f"\n{e}")
        return (0)

    print("\033[1;38;5;213mSUCCESS!"
          "\nYOU MAKE THE CAT VERY HAPPY 😻\033[0m")

    print(f"\nnb_drones = {cfg._nb_drones}\n")
    for i, item in enumerate(cfg._hubs):
        print(f"hub[{i}]: {item._name}")
    print()
    for i, item in enumerate(cfg._connections):
        print(f"connection[{i}]: {item._hub1}-{item._hub2}")

    return (0)


if __name__ == "__main__":
    main(argv)
