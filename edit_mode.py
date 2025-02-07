import pygame
import json
from game_objects.platform import Platform
from game_objects.goal import Goal  # Import the Goal class

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

# List of room filenames
ROOMS = [
    'levels/room1A.json',
    'levels/room1B.json',
    'levels/room2A.json',
    'levels/room2B.json',
    'levels/room3A.json',
    'levels/room3B.json',
]

def load_level(filename):
    """Load level data from a JSON file."""
    try:
        with open(filename, 'r') as file:
            level_data = json.load(file)
        return level_data
    except FileNotFoundError:
        return {'platforms': [], 'goal': {'x': 100, 'y': 100, 'width': 50, 'height': 50}}  # Default level data

def save_level(filename, platforms, goal):
    """Save level data to a JSON file."""
    level_data = {
        'platforms': [{'x': p.rect.x, 'y': p.rect.y, 'width': p.width, 'height': p.height} for p in platforms],
        'goal': {'x': goal.rect.x, 'y': goal.rect.y, 'width': goal.width, 'height': goal.height}
    }
    with open(filename, 'w') as file:
        json.dump(level_data, file, indent=4)

def main():
    # Create sprite groups
    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()

    # Current room index
    current_room_index = 0

    # Load level data for the current room
    level_data = load_level(ROOMS[current_room_index])

    # Load platforms
    for platform_data in level_data['platforms']:
        platform = Platform(platform_data['x'], platform_data['y'], platform_data['width'], platform_data['height'])
        platforms.add(platform)
        all_sprites.add(platform)

    # Load goal
    goal_data = level_data['goal']
    goal = Goal(goal_data['x'], goal_data['y'], goal_data['width'], goal_data['height'])
    all_sprites.add(goal)

    selected_object = None
    offset_x = 0
    offset_y = 0

    # Load button images
    add_button_image = pygame.image.load('sprites/edit_mode/add_button.png').convert_alpha()
    remove_button_image = pygame.image.load('sprites/edit_mode/remove_button.png').convert_alpha()
    prev_button_image = pygame.image.load('sprites/edit_mode/prev_button.png').convert_alpha()
    next_button_image = pygame.image.load('sprites/edit_mode/next_button.png').convert_alpha()

    # Button positions (not scaled)
    add_button_rect = add_button_image.get_rect(topleft=(SCREEN_WIDTH - BUTTON_WIDTH - 10, 10))
    minus_button_rect = remove_button_image.get_rect(topleft=(SCREEN_WIDTH - BUTTON_WIDTH - 10, BUTTON_HEIGHT + 20))
    prev_button_rect = prev_button_image.get_rect(topleft=(10, 10))
    next_button_rect = next_button_image.get_rect(topleft=(10 + BUTTON_WIDTH + 10, 10))

    # Font for displaying room name
    font = pygame.font.Font(None, 36)

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
                elif prev_button_rect.collidepoint(event.pos):
                    # Switch to the previous room
                    save_level(ROOMS[current_room_index], platforms, goal)  # Save current room
                    current_room_index = (current_room_index - 1) % len(ROOMS)
                    level_data = load_level(ROOMS[current_room_index])
                    platforms.empty()
                    all_sprites.empty()
                    for platform_data in level_data['platforms']:
                        platform = Platform(platform_data['x'], platform_data['y'], platform_data['width'], platform_data['height'])
                        platforms.add(platform)
                        all_sprites.add(platform)
                    goal_data = level_data['goal']
                    goal = Goal(goal_data['x'], goal_data['y'], goal_data['width'], goal_data['height'])
                    all_sprites.add(goal)
                elif next_button_rect.collidepoint(event.pos):
                    # Switch to the next room
                    save_level(ROOMS[current_room_index], platforms, goal)  # Save current room
                    current_room_index = (current_room_index + 1) % len(ROOMS)
                    level_data = load_level(ROOMS[current_room_index])
                    platforms.empty()
                    all_sprites.empty()
                    for platform_data in level_data['platforms']:
                        platform = Platform(platform_data['x'], platform_data['y'], platform_data['width'], platform_data['height'])
                        platforms.add(platform)
                        all_sprites.add(platform)
                    goal_data = level_data['goal']
                    goal = Goal(goal_data['x'], goal_data['y'], goal_data['width'], goal_data['height'])
                    all_sprites.add(goal)
                else:
                    for obj in all_sprites:
                        # Check collision with scaled object rect
                        scaled_rect = pygame.Rect(
                            obj.rect.x * ZOOM_FACTOR,
                            obj.rect.y * ZOOM_FACTOR,
                            obj.rect.width * ZOOM_FACTOR,
                            obj.rect.height * ZOOM_FACTOR
                        )
                        if scaled_rect.collidepoint(event.pos):
                            selected_object = obj
                            offset_x = obj.rect.x - scaled_mouse_pos[0]
                            offset_y = obj.rect.y - scaled_mouse_pos[1]
                            break
                # Check right click to rotate (only for platforms)
                if event.button == 3 and isinstance(selected_object, Platform):
                    selected_object.rotate()

            elif event.type == pygame.MOUSEBUTTONUP:
                if selected_object and minus_button_rect.collidepoint(event.pos):
                    # Remove the selected object
                    if isinstance(selected_object, Platform):
                        platforms.remove(selected_object)
                    all_sprites.remove(selected_object)
                selected_object = None
            elif event.type == pygame.MOUSEMOTION:
                if selected_object:
                    # Scale mouse position for movement
                    scaled_mouse_pos = (event.pos[0] / ZOOM_FACTOR, event.pos[1] / ZOOM_FACTOR)
                    selected_object.rect.x = scaled_mouse_pos[0] + offset_x
                    selected_object.rect.y = scaled_mouse_pos[1] + offset_y
            elif event.type == pygame.KEYDOWN:
                if selected_object and isinstance(selected_object, Platform):
                    if event.key == pygame.K_w:
                        selected_object.rect.width += 10
                    elif event.key == pygame.K_s:
                        selected_object.rect.width = max(10, selected_object.rect.width - 10)
                    # Update the platform's image to reflect the new width
                    selected_object.image = pygame.Surface((selected_object.rect.width, selected_object.rect.height))
                    selected_object.width, selected_object.height = selected_object.rect.width, selected_object.rect.height
                    selected_object.image.fill(BLACK)

        # Draw everything
        screen.fill(WHITE)

        # Draw objects with scaling
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
        screen.blit(prev_button_image, prev_button_rect.topleft)
        screen.blit(next_button_image, next_button_rect.topleft)

        # Highlight selected object
        if selected_object:
            scaled_selected_rect = pygame.Rect(
                selected_object.rect.x * ZOOM_FACTOR,
                selected_object.rect.y * ZOOM_FACTOR,
                selected_object.rect.width * ZOOM_FACTOR,
                selected_object.rect.height * ZOOM_FACTOR
            )
            pygame.draw.rect(screen, RED, scaled_selected_rect, 2)

        # Display current room name
        room_name = ROOMS[current_room_index].split('/')[-1]  # Extract filename
        room_text = font.render(f"Room: {room_name}", True, BLACK)
        screen.blit(room_text, (SCREEN_WIDTH // 2 - 100, 10))

        # Flip the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    # Save updated level data to the current room's JSON file
    save_level(ROOMS[current_room_index], platforms, goal)

    pygame.quit()

if __name__ == '__main__':
    main()