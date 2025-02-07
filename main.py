import pygame
import sys
import json
from player import Player
from platform import Platform

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
START_COLOR = (0, 128, 255)
END_COLOR = (255, 255, 255)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Platformer")

# Clock for controlling frame rate
clock = pygame.time.Clock()

def draw_gradient(screen, start_color, end_color):
    """Draw a vertical gradient from start_color to end_color."""
    for y in range(SCREEN_HEIGHT):
        color = [
            start_color[i] + (end_color[i] - start_color[i]) * y // SCREEN_HEIGHT
            for i in range(3)
        ]
        pygame.draw.line(screen, color, (0, y), (SCREEN_WIDTH, y))

def load_platforms(filename):
    with open(filename, 'r') as file:
        platforms_data = json.load(file)
    return platforms_data

def main():
    # Create sprite groups
    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()

    # Load and scale background image
    background = pygame.image.load('backgrounds/middle_ground.png').convert_alpha()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, background.get_height()))
    background_rect = background.get_rect()
    background_rect.bottom = SCREEN_HEIGHT

    # Create player
    player = Player()
    player.rect.x = SCREEN_WIDTH // 2
    player.rect.y = SCREEN_HEIGHT // 2
    player.set_platforms(platforms)
    all_sprites.add(player)

    # Load platforms from JSON file
    platforms_data = load_platforms('room.json')
    for platform_data in platforms_data:
        platform = Platform(platform_data['x'], platform_data['y'], platform_data['width'], platform_data['height'])
        platforms.add(platform)
        all_sprites.add(platform)

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player.go_left()
                elif event.key == pygame.K_d:
                    player.go_right()
                elif event.key == pygame.K_w:
                    player.jump()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a and player.change_x < 0:
                    player.stop()
                elif event.key == pygame.K_d and player.change_x > 0:
                    player.stop()

        # Update sprites
        all_sprites.update()

        # Draw everything
        draw_gradient(screen, START_COLOR, END_COLOR)
        screen.blit(background, background_rect.topleft)
        all_sprites.draw(screen)

        # Flip the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()