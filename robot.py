from itertools import cycle
import logging
from enum import Enum

import numpy as np
import pygame

import lighting
from conts import HEIGHT, TILE_SIZE, WHITE, WIDTH
from level import TILE_TYPES


class MOVES(Enum):
    LEFT = 1
    RIGHT = -1
    FD = 2
    INTERACT = 3


class Robot:
    """
    facing  left = 1, right = -1
    """

    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("./assets/robot.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.load_images()
        self.x = pos[0] + (TILE_SIZE - self.image.get_width()) / 2
        self.y = pos[1] + TILE_SIZE
        self.y -= self.image.get_height()
        self.facing = 1
        self.rect = pygame.Rect(
            (self.x, self.y, self.image.get_width(), self.image.get_height())
        )
        self.next_pos = []
        self.next_facing = []
        self.last_ploy = None
        self.dtime = 0  # time since last move

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
        logging.debug(f"{move=}")

        if move == MOVES.FD:
            if not self.check_fd(level):
                return
            _next_pos = [self.x + TILE_SIZE * self.facing, self.y]
            self.next_pos = np.linspace(self.pos, _next_pos, 10)
            self.next_pos = list(self.next_pos)

        if move == MOVES.INTERACT:

            ...

    def load_images(self):
        # es muy malo
        self.images = []
        for i in range(24):

            self.images.append(
                pygame.image.load(
                    f"./assets/robot_{str(i).zfill(3)}.png"
                ).convert_alpha()
            )

        self.images = cycle(self.images)

    def image_update(self):
        self.image = next(self.images)

    def update(self, level, move=None):
        if self.dtime > 8:
            self.image_update()
        if self.dtime > 8 + 25:
            self.dtime = 0

        if level.level[self.level_pos[1]][self.level_pos[0]] == TILE_TYPES.NONE:
            self.kill()

        self.update_rect()
        if self.next_pos:
            self.x, self.y = self.next_pos.pop(0)
        if self.next_facing:
            self.facing = self.next_facing.pop(0)

        if self.next_pos or self.next_facing or not move:
            self.dtime += 1

            return
        else:
            self.dtime = 0

        self.handle_move(level, move)

    def draw(self, win, level):
        surf = level.lighting_map.copy()
        pos = self.pos
        pos = pos[0] + 14, pos[1] + 18
        if len(self.next_facing) == 0 and self.last_ploy:
            ploy = self.last_ploy
        else:

            ploy = lighting.get_rays(pos, level.walls, level.coners)

            # ploy.extend(ploy[1:3])

        pygame.draw.polygon(surf, (214, 183, 26), ploy)

        surf.convert_alpha()
        surf.set_alpha(100)

        win.blit(surf, (0, 0))
        win.blit(self.image, self.pos)
        _temp_win = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.polygon(_temp_win, WHITE, ploy)
        for i in ploy:
            pygame.draw.circle(_temp_win, (12, 111, 255), i, 2)
        for i in level.coners:
            pygame.draw.circle(_temp_win, (255, 111, 31), i, 2)
        return _temp_win


def palette_swap(surf, old_c, new_c):
    img_copy = pygame.Surface(surf.get_size())
    img_copy.fill(new_c)
    surf.set_colorkey(old_c)
    img_copy.blit(surf, (0, 0))
    return img_copy
