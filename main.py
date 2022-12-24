import logging

import pygame

import lighting
import setup_logger
from conts import BG_COLOUR, FPS, HEIGHT, TILE_SIZE, WIDTH
from level import Level
from robot import MOVES, Robot


class Game:
    def __init__(self) -> None:
        self.level = Level("./levels/level.json")

        # player group only contains only
        # it uses a sprte group bc the interface is nice to use
        self.player = pygame.sprite.Group()
        self.player.add(Robot(self.level.start_point))

    def update(self, move):
        self.player.update(self.level, move)

    def draw(self, win):
        self.level.draw(win)
        surf = self.level.lighting_map.copy()
        pos = self.player.sprites()[0].pos
        pos = pos[0] + TILE_SIZE / 2, pos[1] + TILE_SIZE / 2

        ploy = lighting.get_rays(pos, self.level.walls, start_angle=270, end_angle=450)
        if ploy:
            pygame.draw.polygon(surf, (255, 255, 0), ploy)
            # for i in ploy:
            # pygame.draw.line(win, (0, 0, 255), pos, i, width=3)

        surf.convert_alpha()
        surf.set_alpha(200)
        win.blit(surf, (0, 0))
        self.player.draw(win)


def handle_events():
    move = None
    for event in pygame.event.get():
        # handle pygame events
        if event.type == pygame.QUIT:
            nice_exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                nice_exit()

            elif event.key == pygame.K_RIGHT:
                move = MOVES.FD
    return move


def main():

    # setup pygame
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    game = Game()
    # main loop
    move = None

    while True:

        screen = pygame.Surface((800, 400))
        game.update(move)
        game.draw(screen)
        win.blit(screen, (0, 0))
        # store the player's move
        move = handle_events()

        # update win
        pygame.display.flip()
        win.fill(BG_COLOUR)
        clock.tick(FPS)


def nice_exit():
    pygame.quit()
    logging.info("Bye!")
    exit()


if __name__ == "__main__":
    setup_logger.run()
    main()
