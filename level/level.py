import pygame

from conts import TILE_SIZE

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
