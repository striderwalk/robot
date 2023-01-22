import logging

import pygame
from game import Game


import setup_logger
from conts import BG_COLOUR, FPS, HEIGHT, WIDTH
from robot import MOVES


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
    win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    # setup game -------------------------------->
    game = Game()
    move = None

    # main loop -------------------------------->
    while True:

        screen = pygame.Surface((32 * 8, 32 * 4))
        game.update(move)
        game.draw(screen)
        w, h = win.get_size()
        screen = pygame.transform.scale(screen, (w, h))
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
