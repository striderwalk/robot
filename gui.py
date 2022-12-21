import pygame
from level import TILE_TYPES, Level
from conts import FPS, WIDTH, HEIGHT, WHITE, TILE_SIZE
import font


def draw_tile(win, type, pos):
    if type == TILE_TYPES.NONE:
        pygame.draw.rect(
            win, (12, 12, 12), (*pos, TILE_SIZE, TILE_SIZE), border_radius=1
        )
    else:
        return

def draw_level(win, level):
    for i, row in enumerate(level.level):
        for j, item in enumerate(row):
            draw_tile(win, item, (j * TILE_SIZE, i * TILE_SIZE))


class Tile:
    def __init__(self, image, pos):
        self.image = image
        self.pos = pos

    def draw(self, win):
        win.blit(self.image, self.pos)


font = font.get_text_font(10)


class Left(Tile):
    def __init__(self):
        image = font.render("left", False, (0, 0, 0))
        super().__init__(image)


class Right(Tile):
    def __init__(self):
        image = font.render("right", False, (0, 0, 0))
        super(image).__init__()


class Forward(Tile):
    def __init__(self):
        image = font.render("forward", False, (0, 0, 0))
        super().__init__(image, (0, 0))


def main():

    # setup pygame
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    level = Level("./levels/level.json")
    run = True
    f = Forward()
    while run:
        draw_level(win, level)
        surf = pygame.Surface((100, 100))
        surf.fill(WHITE)
        f.draw(surf)
        win.blit(surf, (10, 500))
        for event in pygame.event.get():
            # handle pygame events
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    run = False

        # update frame
        pygame.display.flip()
        win.fill(WHITE)
        clock.tick(FPS)


if __name__ == "__main__":
    main()
