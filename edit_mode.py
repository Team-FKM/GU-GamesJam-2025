import pygame
import json
from platform import Platform

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Button dimensions
BUTTON_WIDTH = 50
BUTTON_HEIGHT = 50

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Edit Mode")

# Clock for controlling frame rate
clock = pygame.time.Clock()

def load_platforms(filename):
    with open(filename, 'r') as file:
        platforms_data = json.load(file)
    return platforms_data

def save_platforms(filename, platforms):
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

    # Button positions
    add_button_rect = add_button_image.get_rect(topleft=(SCREEN_WIDTH - BUTTON_WIDTH - 10, 10))
    minus_button_rect = remove_button_image.get_rect(topleft=(SCREEN_WIDTH - BUTTON_WIDTH - 10, BUTTON_HEIGHT + 20))

    # Main edit loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if add_button_rect.collidepoint(event.pos):
                    # Add a new platform
                    new_platform = Platform(100, 100, 200, 20)
                    platforms.add(new_platform)
                    all_sprites.add(new_platform)
                else:
                    for platform in platforms:
                        if platform.rect.collidepoint(event.pos):
                            selected_platform = platform
                            offset_x = platform.rect.x - event.pos[0]
                            offset_y = platform.rect.y - event.pos[1]
                            break
                # check right click if so rotate
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
                    selected_platform.rect.x = event.pos[0] + offset_x
                    selected_platform.rect.y = event.pos[1] + offset_y
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
        all_sprites.draw(screen)

        # Draw buttons
        screen.blit(add_button_image, add_button_rect.topleft)
        screen.blit(remove_button_image, minus_button_rect.topleft)

        # Highlight selected platform
        if selected_platform:
            pygame.draw.rect(screen, RED, selected_platform.rect, 2)

        # Flip the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    # Save updated platforms to JSON file
    save_platforms('room.json', platforms)

    pygame.quit()

if __name__ == '__main__':
    main()