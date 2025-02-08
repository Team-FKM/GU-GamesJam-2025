import pygame

class Projectile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, direction, speed):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = direction
        self.speed = speed
        self.platforms = None

    def update(self):
        self.rect.x += self.direction * self.speed

        # check if projectile is out of bounds
        if self.rect.x < 0 or self.rect.x > 2600:
            self.destroy()

        # check if projectile is colliding with any platforms
        for platform in self.platforms:
            if self.check_collision(platform):
                self.destroy()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def check_collision(self, sprite):
        return self.rect.colliderect(sprite.rect)

    def destroy(self):
        self.kill()

    def set_platforms(self, platforms):
        self.platforms = platforms