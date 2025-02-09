import pygame
import random


class Particle(pygame.sprite.Sprite):
    def __init__(self, color, x, y, width, height, dx, dy):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Movement variables
        self.x = float(x)  # Store precise positions as floats
        self.y = float(y)
        self.dx = dx  # Horizontal velocity
        self.dy = dy  # Vertical velocity

        # Particle properties
        self.gravity = 0.5
        self.lifetime = 60  # Number of frames the particle will live
        self.alpha = 255  # Start fully opaque
        self.fade_rate = 255 / self.lifetime  # How quickly to fade out

        # Make background transparent
        self.image.set_colorkey((0, 0, 0))

    def update(self):
        # Update position
        self.x += self.dx
        self.y += self.dy
        self.dy += self.gravity  # Apply gravity

        # Update rect position
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        # Update lifetime and alpha
        self.lifetime -= 1
        self.alpha = max(0, self.alpha - self.fade_rate)
        self.image.set_alpha(int(self.alpha))

        # Kill the particle if its lifetime is over
        if self.lifetime <= 0:
            self.kill()