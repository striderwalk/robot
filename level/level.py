import pygame

from conts import BLACK, TILE_SIZE

from .tile import TILE_TYPES, Tile, Lift


class Level:
    def __init__(self, path):
        from .level_loader import get_level, parse_level_data

        self.level_data = get_level(path)
        self.level, self.path = parse_level_data(self.level_data)
        self.start_point = (
            self.path[0][1] * TILE_SIZE,
            self.path[0][0] * TILE_SIZE,
        )
        self.walls = []
        self.tiles = pygame.sprite.Group()
        self.create_tiles()
        self.make_lighting_map()

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
                rect = (
                    (j * TILE_SIZE) - 10,
                    (i * TILE_SIZE) - 10,
                    TILE_SIZE + 20,
                    TILE_SIZE + 20,
                )
                pygame.draw.rect(surf, BLACK, rect)
        self.lighting_map = surf

    def create_tiles(self):
        width = len(self.level) - 1
        height = len(self.level[0]) - 1
        for i, row in enumerate(self.level):
            for j, tile in enumerate(row):
                if tile == TILE_TYPES.NONE:
                    dat = self.find_neighbours(width, height, i, j)
                    neighbours, coner_neighbours = dat
                else:
                    neighbours, coner_neighbours = [], []

                pos = (j * TILE_SIZE, i * TILE_SIZE)

                self.tiles.add(Tile(tile, pos, neighbours, coner_neighbours))
                if any(neighbours):
                    self.walls.append(pygame.Rect(*pos, TILE_SIZE, TILE_SIZE))

    def find_neighbours(self, width, height, i, j):

        up = j > 0
        down = j < height
        left = i > 0
        right = i < width

        neighbours = [False, False, False, False]

        # TO CHECK WHERE EDGES ARE, IDK WHY CAP LOCKS
        if left and self.level[i - 1][j] != TILE_TYPES.NONE:
            neighbours[0] = True
        if up and self.level[i][j - 1] != TILE_TYPES.NONE:
            neighbours[1] = True
        if right and self.level[i + 1][j] != TILE_TYPES.NONE:
            neighbours[2] = True
        if down and self.level[i][j + 1] != TILE_TYPES.NONE:
            neighbours[3] = True

        coner_neighbours = [False, False, False, False]

        # if corner are walkable
        if left and down and self.level[i - 1][j + 1] != TILE_TYPES.NONE:
            coner_neighbours[0] = True
        if left and up and self.level[i - 1][j - 1] != TILE_TYPES.NONE:
            coner_neighbours[1] = True

        if right and up and self.level[i + 1][j - 1] != TILE_TYPES.NONE:
            coner_neighbours[2] = True

        if right and down and self.level[i + 1][j + 1] != TILE_TYPES.NONE:
            coner_neighbours[3] = True
        return neighbours, coner_neighbours

    @property
    def num_board(self):
        return [[j.value for j in i] for i in self.level]

    def draw(self, win):
        self.tiles.draw(win)
