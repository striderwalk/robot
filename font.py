import pygame

pygame.font.init()


def get_text_font(size: int) -> pygame.font.Font:
    return pygame.font.SysFont("haventica-bold", size)
