import pygame
import json
from platform import Platform

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 600

# Zoom factor (0.5 means zoomed out by double)
ZOOM_FACTOR = 0.5

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Button dimensions
BUTTON_WIDTH = 50
BUTTON_HEIGHT = 50

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Edit Mode (Zoomed Out)")

# Clock for controlling frame rate
clock = pygame.time.Clock()

def load_platforms(filename):
    with open(filename, 'r') as file:
        platforms_data = json.load(file)
    return platforms_data

def save_platforms(filename, platforms):
    # Save platforms with their original (unscaled) positions
    platforms_data = [{'x': p.rect.x, 'y': p.rect.y, 'width': p.width, 'height': p.height} for p in platforms]
    with open(filename, 'w') as file:
        json.dump(platforms_data, file, indent=4)

def main():
    # Create sprite groups
    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()

    # Load platforms from JSON file
    platforms_data = load_platforms('room.json')
    for platform_data in platforms_data:
        platform = Platform(platform_data['x'], platform_data['y'], platform_data['width'], platform_data['height'])
        platforms.add(platform)
        all_sprites.add(platform)

    selected_platform = None
    offset_x = 0
    offset_y = 0

    # Load button images
    add_button_image = pygame.image.load('sprites/edit_mode/add_button.png').convert_alpha()
    remove_button_image = pygame.image.load('sprites/edit_mode/remove_button.png').convert_alpha()

    # Button positions (not scaled)
    add_button_rect = add_button_image.get_rect(topleft=(SCREEN_WIDTH - BUTTON_WIDTH - 10, 10))
    minus_button_rect = remove_button_image.get_rect(topleft=(SCREEN_WIDTH - BUTTON_WIDTH - 10, BUTTON_HEIGHT + 20))

    # Main edit loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Scale mouse position to account for zoom
                scaled_mouse_pos = (event.pos[0] / ZOOM_FACTOR, event.pos[1] / ZOOM_FACTOR)

                if add_button_rect.collidepoint(event.pos):
                    # Add a new platform at a default position (unscaled)
                    new_platform = Platform(100, 100, 200, 20)
                    platforms.add(new_platform)
                    all_sprites.add(new_platform)
                else:
                    for platform in platforms:
                        # Check collision with scaled platform rect
                        scaled_platform_rect = pygame.Rect(
                            platform.rect.x * ZOOM_FACTOR,
                            platform.rect.y * ZOOM_FACTOR,
                            platform.rect.width * ZOOM_FACTOR,
                            platform.rect.height * ZOOM_FACTOR
                        )
                        if scaled_platform_rect.collidepoint(event.pos):
                            selected_platform = platform
                            offset_x = platform.rect.x - scaled_mouse_pos[0]
                            offset_y = platform.rect.y - scaled_mouse_pos[1]
                            break
                # Check right click to rotate
                if event.button == 3:
                    if selected_platform:
                        selected_platform.rotate()

            elif event.type == pygame.MOUSEBUTTONUP:
                if selected_platform and minus_button_rect.collidepoint(event.pos):
                    # Remove the platform
                    platforms.remove(selected_platform)
                    all_sprites.remove(selected_platform)
                selected_platform = None
            elif event.type == pygame.MOUSEMOTION:
                if selected_platform:
                    # Scale mouse position for movement
                    scaled_mouse_pos = (event.pos[0] / ZOOM_FACTOR, event.pos[1] / ZOOM_FACTOR)
                    selected_platform.rect.x = scaled_mouse_pos[0] + offset_x
                    selected_platform.rect.y = scaled_mouse_pos[1] + offset_y
            elif event.type == pygame.KEYDOWN:
                if selected_platform:
                    if event.key == pygame.K_w:
                        selected_platform.rect.width += 10
                    elif event.key == pygame.K_s:
                        selected_platform.rect.width = max(10, selected_platform.rect.width - 10)
                    # Update the platform's image to reflect the new width
                    selected_platform.image = pygame.Surface((selected_platform.rect.width, selected_platform.rect.height))
                    selected_platform.width, selected_platform.height = selected_platform.rect.width, selected_platform.rect.height
                    selected_platform.image.fill(BLACK)

        # Draw everything
        screen.fill(WHITE)

        # Draw platforms with scaling
        for sprite in all_sprites:
            scaled_rect = pygame.Rect(
                sprite.rect.x * ZOOM_FACTOR,
                sprite.rect.y * ZOOM_FACTOR,
                sprite.rect.width * ZOOM_FACTOR,
                sprite.rect.height * ZOOM_FACTOR
            )
            scaled_image = pygame.transform.scale(sprite.image, (scaled_rect.width, scaled_rect.height))
            screen.blit(scaled_image, scaled_rect.topleft)

        # Draw buttons (not scaled)
        screen.blit(add_button_image, add_button_rect.topleft)
        screen.blit(remove_button_image, minus_button_rect.topleft)

        # Highlight selected platform
        if selected_platform:
            scaled_selected_rect = pygame.Rect(
                selected_platform.rect.x * ZOOM_FACTOR,
                selected_platform.rect.y * ZOOM_FACTOR,
                selected_platform.rect.width * ZOOM_FACTOR,
                selected_platform.rect.height * ZOOM_FACTOR
            )
            pygame.draw.rect(screen, RED, scaled_selected_rect, 2)

        # Flip the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    # Save updated platforms to JSON file
    save_platforms('room.json', platforms)

    pygame.quit()

if __name__ == '__main__':
    main()