from enum import Enum
import numpy as np
import pygame

from conts import TILE_SIZE
from level import TILE_TYPES


class MOVES(Enum):
    LEFT = 1
    RIGHT = -1
    FD = 2
    INTERACT = 3


class Robot(pygame.sprite.Sprite):
    """
    facing  left = 1, right = -1
    """

    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("./assets/robot.png")
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.x = pos[0] + (TILE_SIZE - self.image.get_width()) / 2
        self.y = pos[1] + TILE_SIZE
        self.y -= self.image.get_height()
        self.facing = 1
        self.rect = pygame.Rect(
            (self.x, self.y, self.image.get_width(), self.image.get_height())
        )
        self.next_pos = []
        self.next_facing = []

    @property
    def level_pos(self):
        return int(self.x // TILE_SIZE), int(self.y // TILE_SIZE)

    @property
    def pos(self):
        return self.x, self.y

    def update_rect(self):
        self.rect = pygame.Rect(
            (self.x, self.y, self.image.get_width(), self.image.get_height())
        )

    def check_fd(self, level):
        x, y = self.level_pos
        x += self.facing
        if level.level[x][y] != TILE_TYPES.NONE:
            return True

    def handle_move(self, level, move):
        if move == MOVES.FD:
            if not self.check_fd(level):
                return
            self.next_pos = list(
                np.linspace(self.pos, [self.x + TILE_SIZE * self.facing, self.y], 10)
            )
        if move == MOVES.INTERACT:
            # level.interactables.
            ...

    def update(self, level, move=None):
        if level.level[self.level_pos[1]][self.level_pos[0]] == TILE_TYPES.NONE:
            self.kill()

        self.update_rect()
        if self.next_pos:
            self.x, self.y = self.next_pos.pop(0)
        if self.next_facing:
            self.facing = self.next_facing.pop(0)

        if self.next_pos or self.next_facing or not move:
            return

        self.handle_move(level, move)
