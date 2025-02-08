import pygame
import sys
import json
import os
import re
from player import Player
from camera import Camera
from game_objects.platform import Platform
from game_objects.goal import Goal
from game_objects.decoration import Decoration
from game_objects.spawn_point import SpawnPoint

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
CURRENT_ROOM = 'room1A'

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Platformer")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Load all decoration types
DECORATION_TYPES = {
    name.split('.')[0]: pygame.image.load(os.path.join('sprites/decorations', name)).convert_alpha()
    for name in os.listdir('sprites/decorations')
    if name.endswith('.png')
}

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
            if 'decorations' not in level_data:
                level_data['decorations'] = []
        return level_data
    except FileNotFoundError:
        return {
            'platforms': [],
            'goal': {'x': 100, 'y': 100, 'width': 50, 'height': 50},
            'spawn_point': {'x': 0, 'y': 0, 'width': 50, 'height': 50},
            'decorations': []
        }

def increment_room(room_name):
    """Increment the room number (e.g., room1A → room2A)."""
    match = re.match(r'room(\d+)([A-Za-z])', room_name)
    if match:
        room_number = int(match.group(1))
        room_letter = match.group(2)
        return f'room{room_number + 1}{room_letter}'
    return room_name

def reset_player_and_camera(player, camera, spawn_point):
    """Reset the player and camera to the starting position."""
    player.rect.x = spawn_point.rect.x
    player.rect.y = spawn_point.rect.y
    camera.camera.x = 0
    camera.camera.y = 0

def next_level(player, camera, all_sprites, platforms):
    """Move to the next level."""
    global CURRENT_ROOM
    CURRENT_ROOM = increment_room(CURRENT_ROOM)

    # Load new level data
    level_data = load_level(f'levels/{CURRENT_ROOM}.json')

    # Clear existing sprites
    all_sprites.empty()
    platforms.empty()

    # Load new platforms (z_index = 0)
    for platform_data in level_data['platforms']:
        platform = Platform(
            platform_data['x'],
            platform_data['y'],
            platform_data['width'],
            platform_data['height']
        )
        platform.z_index = 0
        platforms.add(platform)
        all_sprites.add(platform)

    # Load new decorations with their z_index
    for decoration_data in level_data.get('decorations', []):
        decoration = Decoration(
            DECORATION_TYPES[decoration_data['type']],
            decoration_data['x'],
            decoration_data['y'],
            decoration_data.get('z_index', 0)  # Default to 0 if not specified
        )
        decoration.decoration_type = decoration_data['type']
        decoration.z_index = decoration_data.get('z_index', 0)
        all_sprites.add(decoration)

    # Load new goal (z_index = 0)
    goal_data = level_data['goal']
    new_goal = Goal(
        goal_data['x'],
        goal_data['y'],
        goal_data['width'],
        goal_data['height']
    )
    new_goal.z_index = 0
    all_sprites.add(new_goal)

    # Load new spawn point (z_index = 0)
    spawn_point_data = level_data['spawn_point']
    spawn_point = SpawnPoint(
        spawn_point_data['x'],
        spawn_point_data['y'],
        spawn_point_data['width'],
        spawn_point_data['height']
    )
    spawn_point.z_index = 0
    all_sprites.add(spawn_point)

    # Reset player position and add back to sprites
    reset_player_and_camera(player, camera, spawn_point)
    player.z_index = 0
    all_sprites.add(player)

    return new_goal

def main():
    global CURRENT_ROOM

    # Create sprite groups
    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()

    # Load and scale background image
    background = pygame.image.load('backgrounds/middle_ground.png').convert_alpha()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, background.get_height()))
    background_rect = background.get_rect()
    background_rect.bottom = SCREEN_HEIGHT

    # Load initial level data
    level_data = load_level(f'levels/{CURRENT_ROOM}.json')

    # Load platforms (z_index = 0)
    for platform_data in level_data['platforms']:
        platform = Platform(platform_data['x'], platform_data['y'], platform_data['width'], platform_data['height'])
        platform.z_index = 0
        platforms.add(platform)
        all_sprites.add(platform)

    # Load decorations with their z_index
    for decoration_data in level_data.get('decorations', []):
        decoration = Decoration(
            DECORATION_TYPES[decoration_data['type']],
            decoration_data['x'],
            decoration_data['y'],
            decoration_data.get('z_index', 0)  # Default to 0 if not specified
        )
        decoration.decoration_type = decoration_data['type']
        all_sprites.add(decoration)

    # Load goal (z_index = 0)
    goal_data = level_data['goal']
    goal = Goal(goal_data['x'], goal_data['y'], goal_data['width'], goal_data['height'])
    goal.z_index = 0
    all_sprites.add(goal)

    # Load spawn_point (z_index = 0)
    spawn_point_data = level_data['spawn_point']
    spawn_point = SpawnPoint(spawn_point_data['x'], spawn_point_data['y'], spawn_point_data['width'], spawn_point_data['height'])
    spawn_point.z_index = 0
    all_sprites.add(spawn_point)

    # Create player (z_index = 0)
    player = Player()
    player.rect.x = spawn_point.rect.x
    player.rect.y = spawn_point.rect.y
    player.z_index = 0
    player.set_platforms(platforms)
    all_sprites.add(player)

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

        # Check for goal collision
        if pygame.sprite.collide_rect(player, goal):
            goal = next_level(player, camera, all_sprites, platforms)
            print(f"Moving to {CURRENT_ROOM}")

        # Update camera
        camera.update(player)

        # Draw everything
        draw_gradient(screen, START_COLOR, END_COLOR)
        screen.blit(background, background_rect.topleft)

        # Sort sprites by z_index for proper layering
        sorted_sprites = sorted(all_sprites, key=lambda sprite: sprite.z_index)

        # Draw all sprites in order of z_index
        for sprite in sorted_sprites:
            screen.blit(sprite.image, camera.apply(sprite))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()