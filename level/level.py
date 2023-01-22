import pygame

from conts import TILE_SIZE

from .tile import TILE_TYPES, Tile
from .lift import Lift

WALKABLE_TILES = [TILE_TYPES.PATH, TILE_TYPES.END_POINT, TILE_TYPES.START_POINT]


class Level:
    def __init__(self, path):
        from .level_loader import get_level, parse_level_data

        # level dat
        self.level_data = get_level(path)
        self.level, self.path = parse_level_data(self.level_data)
        self.start_point = (
            self.path[0][1] * TILE_SIZE,
            self.path[0][0] * TILE_SIZE,
        )
        self.walls = []
        # create the groups
        self.fg_tiles = pygame.sprite.Group()
        self.bg_tiles = pygame.sprite.Group()
        self.interatavles = pygame.sprite.Group()
        # fill the groups
        self.create_tiles()

        self.interatavles.add(
            Lift((2 * TILE_SIZE, 1 * TILE_SIZE), (2 * TILE_SIZE, 2 * TILE_SIZE))
        )
        self.make_lighting_map()
        self.make_corners()

    def make_corners(self):
        self.coners = []
        for i in self.fg_tiles.sprites():
            # print(i.tile_corners)
            self.coners.extend(i.tile_corners)

        # width = len(self.level) - 1
        # height = len(self.level[0]) - 1

    # self.coners = []

    # for i, row in enumerate(self.level):
    #     for j, _ in enumerate(row):

    #         down = j < height
    #         up = i > 0
    #         right = i < width
    #         left = j > 0
    #         # TO CHECK WHERE EDGES ARE, IDK WHY CAP LOCKS

    #         if self.level[i][j] in WALKABLE_TILES:
    #             self.coners.append((j, i))

    #         if right and self.level[i + 1][j] in WALKABLE_TILES:
    #             self.coners.append((j, i + 1))

    #         if down and self.level[i][j + 1] in WALKABLE_TILES:
    #             self.coners.append((j + 1, i))

    #         if right and down and self.level[i + 1][j + 1] in WALKABLE_TILES:
    #             self.coners.append((j + 1, i + 1))

    #         if left and self.level[i - 1][j] in WALKABLE_TILES:
    #             self.coners.append((j, i - 1))

    #         if up and self.level[i][j - 1] in WALKABLE_TILES:
    #             self.coners.append((j - 1, i))

    #         if left and up and self.level[i - 1][j - 1] in WALKABLE_TILES:
    #             self.coners.append((j - 1, i - 1))

    # self.coners = [(i[0] * TILE_SIZE, i[1] * TILE_SIZE) for i in self.coners]

    @property
    def size(self):
        return len(self.level[0]) * TILE_SIZE, len(self.level) * TILE_SIZE

    def make_lighting_map(self):

        get_val = lambda i: True if i != TILE_TYPES.NONE else False
        level = [[get_val(i) for i in row] for row in self.level]
        surf = pygame.Surface(self.size, pygame.SRCALPHA)

        for i, row in enumerate(level):
            for j, tile in enumerate(row):
                if not tile:
                    continue
                rect = ((j * TILE_SIZE), (i * TILE_SIZE), TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(surf, (16, 20, 31), rect)
        self.lighting_map = surf

    def create_tiles(self):
        width = len(self.level) - 1
        height = len(self.level[0]) - 1
        for i, row in enumerate(self.level):
            for j, tile in enumerate(row):

                dat = self.find_neighbours(width, height, i, j)
                neighbours, coner_neighbours = dat

                pos = (j * TILE_SIZE, i * TILE_SIZE)

                if tile == TILE_TYPES.NONE:
                    if any(neighbours):
                        self.walls.append(pygame.Rect(*pos, TILE_SIZE, TILE_SIZE))
                    self.bg_tiles.add(Tile(tile, pos, [], []))
                else:
                    self.fg_tiles.add(Tile(tile, pos, neighbours, coner_neighbours))

    def find_neighbours(self, width, height, i, j):

        up = j > 0
        down = j < height
        left = i > 0
        right = i < width

        neighbours = [False] * 4

        # TO CHECK WHERE EDGES ARE, IDK WHY CAP LOCKS
        if left and self.level[i - 1][j] == TILE_TYPES.NONE:
            neighbours[0] = True
        if up and self.level[i][j - 1] == TILE_TYPES.NONE:
            neighbours[1] = True
        if right and self.level[i + 1][j] == TILE_TYPES.NONE:
            neighbours[2] = True
        if down and self.level[i][j + 1] == TILE_TYPES.NONE:
            neighbours[3] = True

        coner_neighbours = [False] * 4

        # if corner are walkable
        if left and down and self.level[i - 1][j + 1] == TILE_TYPES.NONE:
            coner_neighbours[0] = True
        if left and up and self.level[i - 1][j - 1] == TILE_TYPES.NONE:
            coner_neighbours[1] = True

        if right and up and self.level[i + 1][j - 1] == TILE_TYPES.NONE:
            coner_neighbours[2] = True

        if right and down and self.level[i + 1][j + 1] == TILE_TYPES.NONE:
            coner_neighbours[3] = True
        return neighbours, coner_neighbours

    @property
    def num_board(self):
        return [[j.value for j in i] for i in self.level]

    def draw_fg(self, win):
        self.fg_tiles.draw(win)
        self.interatavles.update()
        self.interatavles.draw(win)

    def draw_bg(self, win):
        self.bg_tiles.draw(win)
