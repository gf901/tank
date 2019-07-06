import pygame


# 墙壁类
class Wall:
    def __init__(self,img, x, y, type):
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.live = True
        self.type = type
