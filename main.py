import pygame
from conts import BG_COLOUR, WIDTH, HEIGHT, WHITE, FPS
from level import Level
from robot import MOVES, Robot


def main():

    # setup pygame
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    players = pygame.sprite.Group()
    level = Level("./levels/level.json")
    players.add(Robot(level.start_point))

    # main loop
    run = True
    while run:

        level.draw(win)
        players.draw(win)
        for event in pygame.event.get():
            # handle pygame events
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    run = False

                elif event.key == pygame.K_RIGHT:
                    players.update(level, MOVES.FD)

        # update frame
        players.update(level)
        pygame.display.flip()
        win.fill(BG_COLOUR)
        clock.tick(FPS)


if __name__ == "__main__":
    main()
