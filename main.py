# *************************************************************************** #
#                                                                             #
#                                                         :::      ::::::::   #
#   main.py                                             :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#   By: mdurte-s <mdurte-s@student.42porto.com>     +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#   Created: 2026/09/11 10:38:28 by mdurte-s           #+#    #+#             #
#   Updated: 2026/09/18 13:19:16 by mdurte-s          ###   ########.fr       #
#                                                                             #
# *************************************************************************** #

from sys import argv
from parser import parser, ConfigError


def main(args: list[str]) -> int:

    if len(args) != 2:
        return (0)

    try:
        cfg = parser(args[1])
        print("\033[1;38;5;213mSUCCESS!"
              "\nYOU MAKE THE CAT VERY HAPPY 😻\033[0m")
    except ConfigError as e:
        print("\033[1;31mFAILURE!"
              "\nYOU MAKE THE CAT VERY UNHAPPY 😿\033[0m\n"
              f"\n{e}")
        return (0)

    print(f"\nnb_drones = {cfg.nb_drones}")
    print()
    for i, item in enumerate(cfg.hubs):
        print(f"hub[{i}]: {item}")
    print()
    for i, item in enumerate(cfg.connections):
        print(f"connection[{i}]: {item}")

    return (0)


if __name__ == "__main__":
    main(argv)
