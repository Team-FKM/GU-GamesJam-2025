import pygame

BLACK = (0, 0, 0)
GREY = (100, 100, 100)
BROWN = (139, 69, 19)

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, breakable=False):
        super().__init__()
        self.image = pygame.Surface((width, height))
        if breakable:
            self.image.fill(BROWN)
        else:
            self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        self.breakable = breakable

    def rotate(self):
        self.width, self.height = self.height, self.width
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))

    def broken(self):
        if self.breakable:
            self.kill()
        return self.breakable