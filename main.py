import logging

import pygame


import setup_logger
from conts import BG_COLOUR, FPS, HEIGHT, TILE_SIZE, WIDTH
from level import Level
from robot import MOVES, Robot


class Game:
    def __init__(self) -> None:
        self.level = Level("./levels/level.json")

        # player group only contains only
        # it uses a sprte group bc the interface is nice to use
        self.player = Robot(self.level.start_point)

    def update(self, move):
        self.player.update(self.level, move)

    def draw(self, win):
        self.level.draw_fg(win)
        self.player.draw(win, self.level)
        self.level.draw_bg(win)


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
    # setup pygame -------------------------------->
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    # setup game -------------------------------->
    game = Game()
    move = None

    # main loop -------------------------------->
    while True:

        screen = pygame.Surface((32 * 8, 32 * 4))
        game.update(move)
        game.draw(screen)
        screen = pygame.transform.scale(screen, (800, 400))
        win.blit(screen, (0, 0))
        # store the player's move
        move = handle_events()
        # update win
        pygame.display.flip()
        pygame.display.set_caption(f"{clock.get_fps()}")
        win.fill(BG_COLOUR)
        clock.tick(FPS)


def nice_exit():
    pygame.quit()
    logging.info("Bye!")
    exit()


if __name__ == "__main__":
    setup_logger.run()
    main()
