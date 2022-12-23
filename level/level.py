from enum import Enum

import pygame

from conts import TILE_SIZE


class TILE_TYPES(Enum):
    NONE = 0
    PATH = 1
    START_POINT = 2
    END_POINT = 3
    LIFT = 4


TILE_PATH_MAP = {
    TILE_TYPES.NONE: "./assets/tiles/tile.png",
    TILE_TYPES.PATH: "./assets/tiles/empty.png",
    TILE_TYPES.START_POINT: "./assets/tiles/empty.png",
    TILE_TYPES.END_POINT: "./assets/tiles/empty.png",
    TILE_TYPES.LIFT: "./assets/tiles/empty.png",
}
TILE_SIDE_MAP = {
    0: "./assets/tiles/tile_000.png",  # center
    1: "./assets/tiles/tile_001.png",  # edge
    2: "./assets/tiles/tile_002.png",  # corner
    3: "./assets/tiles/tile_003.png",  # 3 sides
    4: "./assets/tiles/tile_004.png",  # 4 sides
}


class Lift(pygame.sprite.Sprite):
    def __init__(self, pos):

        self.image = pygame.image.load("./assets/tiles/lift.png")
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.rect = pygame.Rect(*pos, TILE_SIZE, TILE_SIZE)
        self.x, self.y = pos
        self.moveing = False

    @property
    def tile_pos(self):
        return int(self.x // TILE_SIZE), int(self.y // TILE_SIZE)

    @property
    def pos(self):
        return self.x, self.y

    def update_rect(self):
        self.rect = pygame.Rect((self.x, self.y, TILE_SIZE, TILE_SIZE))

    def update(self, players):
        if self.moveing:
            self.x, self.y = self.next_pos.pop(0)
            self.update_rect()


nub = pygame.image.load("./assets/tiles/tile_nub.png")


def add_nubs(image, coner_neighbours):

    for index, i in enumerate(coner_neighbours):
        if not i:
            continue

        this_nub = pygame.transform.rotate(nub.copy(), index * 90)
        image.blit(this_nub, (0, 0))

    return image


class Tile(pygame.sprite.Sprite):
    """
    Tile represents a level tile not in path
    """

    def __init__(self, tile, pos, neighbours, coner_neighbours):
        super().__init__()
        if tile == TILE_TYPES.NONE:
            self.image = pygame.image.load(TILE_SIDE_MAP[neighbours.count(True)])
            if any(neighbours):
                self.image = pygame.transform.rotate(
                    self.image, 90 * neighbours.index(True)
                )
            else:  # inner
                self.image = add_nubs(self.image, coner_neighbours)

        elif tile in TILE_PATH_MAP:
            self.image = pygame.image.load(TILE_PATH_MAP[tile])
        else:
            self.image = pygame.image.load("./assets/fail.png")
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.rect = pygame.Rect(*pos, TILE_SIZE, TILE_SIZE)


class Level:
    def __init__(self, path):
        from .level_loader import get_level, parse_level_data

        self.level_data = get_level(path)
        self.level, self.path = parse_level_data(self.level_data)
        self.start_point = (
            self.path[0][1] * TILE_SIZE,
            self.path[0][0] * TILE_SIZE,
        )
        self.tiles = pygame.sprite.Group()
        self.create_tiles()

    def create_tiles(self):
        width = len(self.level) - 1
        height = len(self.level[0]) - 1
        for i, row in enumerate(self.level):
            for j, tile in enumerate(row):
                # TO CHECK WHERE EDGES ARE, IDK WHY CAP LOCKS
                neighbours = [False, False, False, False]
                if tile == TILE_TYPES.NONE:
                    up = j > 0
                    down = j < height
                    left = i > 0
                    right = i < width

                    if left and self.level[i - 1][j] != TILE_TYPES.NONE:
                        neighbours[0] = True
                    if up and self.level[i][j - 1] != TILE_TYPES.NONE:
                        neighbours[1] = True
                    if right and self.level[i + 1][j] != TILE_TYPES.NONE:
                        neighbours[2] = True
                    if down and self.level[i][j + 1] != TILE_TYPES.NONE:
                        neighbours[3] = True

                    coner_neighbours = [False, False, False, False]

                    if left and down and self.level[i - 1][j + 1] != TILE_TYPES.NONE:
                        coner_neighbours[0] = True
                    if left and up and self.level[i - 1][j - 1] != TILE_TYPES.NONE:
                        coner_neighbours[1] = True

                    if right and up and self.level[i + 1][j - 1] != TILE_TYPES.NONE:
                        coner_neighbours[2] = True

                    if right and down and self.level[i + 1][j + 1] != TILE_TYPES.NONE:
                        coner_neighbours[3] = True

                self.tiles.add(
                    Tile(
                        tile,
                        (j * TILE_SIZE, i * TILE_SIZE),
                        neighbours,
                        coner_neighbours,
                    )
                )

    @property
    def num_board(self):
        return [[j.value for j in i] for i in self.level]

    def draw(self, win):
        self.tiles.draw(win)
