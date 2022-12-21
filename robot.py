from enum import Enum
import numpy as np
import pygame

from conts import TILE_SIZE
from level import TILE_TYPES


class MOVES(Enum):
    LEFT = 1
    RIGHT = -1
    FD = 2


class Robot(pygame.sprite.Sprite):
    """
    facing  left = 1, right = -1
    """

    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface([40, 70])
        self.image.fill((255, 251, 16))
        self.x = pos[0] + TILE_SIZE / 2 - 20
        self.y = pos[1] + TILE_SIZE
        self.y -= 70
        self.facing = 1
        self.rect = pygame.Rect((self.x, self.y, 40, 70))
        self.next_pos = []
        self.next_facing = []

    @property
    def level_pos(self):
        return int(self.x // TILE_SIZE), int(self.y // TILE_SIZE)

    @property
    def pos(self):
        return self.x, self.y

    def update_rect(self):
        self.rect = pygame.Rect((self.x, self.y, 40, 70))

    def update(self, level, move=None):
        if level.level[self.level_pos[1]][self.level_pos[0]] == TILE_TYPES.NONE:
            self.kill()

        self.update_rect()
        print(f"hi {self.next_pos=}")
        if self.next_pos:
            self.x, self.y = self.next_pos.pop(0)
        if self.next_facing:
            self.facing = self.next_facing.pop(0)

        if self.next_pos or self.next_facing or not move:
            return
        if move == MOVES.FD:

            self.next_pos = list(
                np.linspace(self.pos, [self.x + TILE_SIZE * self.facing, self.y], 10)
            )
