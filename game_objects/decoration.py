import pygame

class Decoration(pygame.sprite.Sprite):
    def __init__(self, image, x, y, z_index, scale=1):
        super().__init__()
        self.original_image = image
        self.scale = scale
        self.image = pygame.transform.scale(self.original_image, (int(self.original_image.get_width() * self.scale), int(self.original_image.get_height() * self.scale)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.z_index = z_index
        self.original_x = x

    def set_scale(self, new_scale):
        self.scale = new_scale
        self.image = pygame.transform.scale(self.original_image, (int(self.original_image.get_width() * self.scale), int(self.original_image.get_height() * self.scale)))
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)