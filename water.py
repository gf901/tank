import pygame


# water类
class Water:
    def __init__(self, x, y):
        self.image = pygame.image.load("img/wall/water.gif")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
