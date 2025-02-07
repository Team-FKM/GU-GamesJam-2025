import pygame
import sys
import json
import re  # For parsing room numbers
from player import Player
from camera import Camera
from game_objects.platform import Platform
from game_objects.goal import Goal

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
START_COLOR = (0, 128, 255)
END_COLOR = (255, 255, 255)

# Initialize current room
CURRENT_ROOM = 'room1A'  # Start with room1A

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

def load_level(filename):
    """Load level data from a JSON file."""
    try:
        with open(filename, 'r') as file:
            level_data = json.load(file)
        return level_data
    except FileNotFoundError:
        return {'platforms': [], 'goal': {'x': 100, 'y': 100, 'width': 50, 'height': 50}}  # Default level data

def increment_room(room_name):
    """Increment the room number (e.g., room1A → room2A)."""
    match = re.match(r'room(\d+)([A-Za-z])', room_name)
    if match:
        room_number = int(match.group(1))
        room_letter = match.group(2)
        return f'room{room_number + 1}{room_letter}'
    return room_name  # Fallback if the room name doesn't match the pattern

def reset_player_and_camera(player, camera):
    """Reset the player and camera to the starting position."""
    player.rect.x = SCREEN_WIDTH // 2
    player.rect.y = SCREEN_HEIGHT // 2
    camera.camera.x = 0
    camera.camera.y = 0


def next_level(player, camera, all_sprites, platforms):
    """Move to the next level."""
    global CURRENT_ROOM
    CURRENT_ROOM = increment_room(CURRENT_ROOM)

    # Load new level data
    level_data = load_level(f'levels/{CURRENT_ROOM}.json')

    # Clear existing platforms and goal
    for sprite in all_sprites:
        if isinstance(sprite, (Platform, Goal)):
            sprite.kill()

    # Load new platforms
    for platform_data in level_data['platforms']:
        platform = Platform(
            platform_data['x'],
            platform_data['y'],
            platform_data['width'],
            platform_data['height']
        )
        platforms.add(platform)
        all_sprites.add(platform)

    # Load new goal
    goal_data = level_data['goal']
    new_goal = Goal(
        goal_data['x'],
        goal_data['y'],
        goal_data['width'],
        goal_data['height']
    )
    all_sprites.add(new_goal)

    # Reset player position
    reset_player_and_camera(player, camera)

    return new_goal  # Return the new goal object


def main():
    global CURRENT_ROOM  # Use the global CURRENT_ROOM variable

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

    # Load level data from JSON file
    level_data = load_level(f'levels/{CURRENT_ROOM}.json')

    # Load platforms
    for platform_data in level_data['platforms']:
        platform = Platform(platform_data['x'], platform_data['y'], platform_data['width'], platform_data['height'])
        platforms.add(platform)
        all_sprites.add(platform)

    # Load goal
    goal_data = level_data['goal']
    goal = Goal(goal_data['x'], goal_data['y'], goal_data['width'], goal_data['height'])
    all_sprites.add(goal)

    # Initialize camera
    camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

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

        if pygame.sprite.collide_rect(player, goal):
            # Load the new level and update the goal reference
            goal = next_level(player, camera, all_sprites, platforms)
            print(f"Moving to {CURRENT_ROOM}")


        # Update camera
        camera.update(player)

        # Draw everything
        draw_gradient(screen, START_COLOR, END_COLOR)
        screen.blit(background, background_rect.topleft)
        for sprite in all_sprites:
            screen.blit(sprite.image, camera.apply(sprite))

        # Flip the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()