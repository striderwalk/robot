from enum import Enum
import json


class TILE_TYPES(Enum):
    NONE = 0
    PATH = 1
    START_POINT = 2
    END_POINT = 3


def get_level(path):

    with open(path, "r") as level:
        data = json.load(level)

    return data


def find_start_point(level):
    for i, row in enumerate(level):
        for j, item in enumerate(row):
            if item == TILE_TYPES.START_POINT:
                return i, j
    raise ValueError("could not find start point")


# def find_next_point(level_data, level, point: tuple[int]) -> tuple[int]:
def find_next_point(level_data, level, point):
    i, j = point
    size = level_data["size"]

    # leff
    if j - 1 >= 0 and level[i][j - 1] != TILE_TYPES.NONE:
        return i, j - 1
    # right
    if j + 1 <= size["width"] and level[i][j + 1] != TILE_TYPES.NONE:
        return i, j + 1
    # up
    if i - 1 >= 0 and level[i - 1][j] != TILE_TYPES.NONE:
        return i - 1, j

    # down
    if i + 1 <= size["height"] and level[i + 1][j] != TILE_TYPES.NONE:
        return i + 1, j

    raise ValueError(f"CAN FIND POINT at {point}\n{convet_level(level, point)}")


class temp:
    def __init__(self):
        self.value = "H"


def convet_level(level, point):

    level[point[0]][point[1]] = temp()
    vals = "\n".join(str([i.value for i in row]) for row in level)
    vals = (
        vals[: vals.index("H") - 1]
        + "\u001b[43;1m \u001b[0m"
        + vals[vals.index("H") + 2 :]
    )
    return vals


def _parse_data(level_data):
    level = level_data["board"]

    return [[TILE_TYPES(j) for j in i] for i in level]


def parse_level_data(level_data):
    level = _parse_data(level_data)

    start_point = find_start_point(level)
    points = [start_point]
    while True:
        last_point = points[-1]
        new_point = find_next_point(level_data, level, last_point)
        points.append(new_point)
        level[last_point[0]][last_point[1]] = TILE_TYPES.NONE
        if level[new_point[0]][new_point[1]] == TILE_TYPES.END_POINT:
            break

    # reset the level from pathfinder
    level = _parse_data(level_data)
    return level, points


class Level:
    def print_board(self):
        for i in self.num_board:
            print(*i, sep=" ")

    @property
    def num_board(self):
        return [[j.value for j in i] for i in self.level]

    def __init__(self, path):
        self.level_data = get_level(path)
        self.level, self.path = parse_level_data(self.level_data)
        self.start_point = self.path[0]
