from enum import Enum

import pygame

from conts import TILE_SIZE

from paths import TILE_SIDE_MAP, TILE_PATH_MAP


class TILE_TYPES(Enum):
    NONE = 0
    PATH = 1
    START_POINT = 2
    END_POINT = 3
    LIFT = 4


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

    def __init__(self, tile_type, pos, neighbours, coner_neighbours):
        self.image = get_tile_image(tile_type, neighbours, coner_neighbours)
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        super().__init__()
        self.rect = pygame.Rect(*pos, TILE_SIZE, TILE_SIZE)


def get_tile_image(tile_type, neighbours, coner_neighbours):
    if tile_type == TILE_TYPES.NONE:
        image = pygame.image.load(TILE_SIDE_MAP[neighbours.count(True)])
        if any(neighbours):
            image = pygame.transform.rotate(image, 90 * neighbours.index(True))
        else:  # inner
            image = add_nubs(image, coner_neighbours)

    elif tile_type in TILE_PATH_MAP:
        image = pygame.image.load(TILE_PATH_MAP[tile_type])
    else:

        image = pygame.image.load("./assets/fail.png")

    return image
