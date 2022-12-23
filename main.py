import pygame
from conts import BG_COLOUR, TILE_SIZE, WIDTH, HEIGHT, WHITE, FPS
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
        self.player.draw(win)


def main():

    # setup pygame
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    game = Game()
    # main loop
    run = True
    move = None

    while run:

        screen = pygame.Surface((800, 400))
        game.update(move)
        game.draw(screen)
        win.blit(screen, (0, 0))
        # store the player's move
        move = None
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
                    move = MOVES.FD

        # update win
        pygame.display.flip()
        win.fill(BG_COLOUR)
        clock.tick(FPS)


if __name__ == "__main__":
    main()
