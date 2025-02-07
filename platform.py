import pygame

BLACK = (0, 0, 0)

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height

    def rotate(self):
        self.width, self.height = self.height, self.width
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))