import pygame

class Decoration(pygame.sprite.Sprite):
    def __init__(self, image, x, y, z_index):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.z_index = z_index
        self.original_x = x

    def draw(self, screen):
        screen.blit(self.image, self.rect)