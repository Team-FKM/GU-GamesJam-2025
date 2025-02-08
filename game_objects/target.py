import pygame

class Target (pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('sprites/interactive/target.png').convert_alpha()
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
        self.width = 50
        self.height = 50

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def check_collision(self, sprite):
        return self.rect.colliderect(sprite.rect)

    def destroy(self):
        self.kill()