# main.py
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
from game_objects.projectile import Projectile
from game_objects.target import Target

# Initialize Pygame
pygame.init()

# Screen dimensions (scaled up)
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
    for y in range(SCREEN_HEIGHT):
        color = [
            start_color[i] + (end_color[i] - start_color[i]) * y // SCREEN_HEIGHT
            for i in range(3)
        ]
        pygame.draw.line(screen, color, (0, y), (SCREEN_WIDTH, y))

def load_level(filename):
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
            'decorations': [],
            'targets': []
        }

def increment_room(room_name):
    match = re.match(r'room(\d+)([A-Za-z])', room_name)
    if match:
        room_number = int(match.group(1))
        room_letter = match.group(2)
        return f'room{room_number + 1}{room_letter}'
    return room_name

def swap_room_letter(room_name):
    match = re.match(r'room(\d+)([A-Za-z])', room_name)
    if match:
        return f'room{match.group(1)}B' if match.group(2) == 'A' else f'room{match.group(1)}A'
    return room_name

def reset_player_and_camera(player, camera, spawn_point, position=None):
    """Reset the player and camera to the starting position."""
    if position:
        player.rect.x, player.rect.y = position
    else:
        player.rect.x = spawn_point.rect.x
        player.rect.y = spawn_point.rect.y
    camera.camera.x = 0
    camera.camera.y = 0

def switch_game_state(player, camera, all_sprites, platforms):
    global CURRENT_ROOM
    CURRENT_ROOM = swap_room_letter(CURRENT_ROOM)
    level_data = load_level(f'levels/{CURRENT_ROOM}.json')
    # store player position
    player_position = (player.rect.x, player.rect.y)
    all_sprites.empty()
    platforms.empty()
    all_sprites, platforms, new_goal, spawn_point, targets = load_room(level_data)
    reset_player_and_camera(player, camera, spawn_point, player_position)
    player.set_platforms(platforms)
    player.z_index = 0
    # switching player state
    player.switch_player_state()
    all_sprites.add(player)
    return new_goal, all_sprites, platforms, spawn_point, targets

def next_level(player, camera, all_sprites, platforms):
    global CURRENT_ROOM
    CURRENT_ROOM = increment_room(CURRENT_ROOM)
    level_data = load_level(f'levels/{CURRENT_ROOM}.json')
    all_sprites.empty()
    platforms.empty()
    all_sprites, platforms, new_goal, spawn_point, targets = load_room(level_data)
    reset_player_and_camera(player, camera, spawn_point)
    player.z_index = 0
    all_sprites.add(player)
    return new_goal, all_sprites, platforms, spawn_point

def load_room(level_data):
    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    targets = pygame.sprite.Group()

    for platform_data in level_data['platforms']:
        platform = Platform(platform_data['x'], platform_data['y'], platform_data['width'], platform_data['height'], platform_data.get('breakable', False))
        platform.z_index = 0
        platforms.add(platform)
        all_sprites.add(platform)
    for decoration_data in level_data.get('decorations', []):
        decoration = Decoration(
            DECORATION_TYPES[decoration_data['type']],
            decoration_data['x'],
            decoration_data['y'],
            decoration_data.get('z_index', 0)
        )
        all_sprites.add(decoration)
    for target_data in level_data.get('targets', []):
        target = Target(target_data['x'], target_data['y'])
        target.z_index = 0
        targets.add(target)
        all_sprites.add(target)

    goal = Goal(**level_data['goal'])
    goal.z_index = 0
    all_sprites.add(goal)
    spawn_point = SpawnPoint(**level_data['spawn_point'])
    spawn_point.z_index = 0
    all_sprites.add(spawn_point)
    return all_sprites, platforms, goal, spawn_point, targets

def main():
    global CURRENT_ROOM
    background = pygame.image.load('backgrounds/middle_ground.png').convert_alpha()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, background.get_height()))
    background_rect = background.get_rect()
    background_rect.bottom = SCREEN_HEIGHT
    level_data = load_level(f'levels/{CURRENT_ROOM}.json')
    all_sprites, platforms, goal, spawn_point, targets = load_room(level_data)
    projectiles = pygame.sprite.Group()
    player = Player()
    reset_player_and_camera(player, Camera(SCREEN_WIDTH, SCREEN_HEIGHT), spawn_point)
    player.set_platforms(platforms)
    all_sprites.add(player)
    camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
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
                elif event.key == pygame.K_RETURN:
                    goal, all_sprites, platforms, spawn_point, targets = switch_game_state(player, camera, all_sprites, platforms)
                    player.set_platforms(platforms)
                    print(f"Moving to {CURRENT_ROOM}")
                elif event.key == pygame.K_r:
                    reset_player_and_camera(player, camera, spawn_point)
                    print(f"Resting {CURRENT_ROOM}")
                elif event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_p:
                    player.attack()
                    # check if player is colliding with breakable platform if so break it
                    attack_rect = player.rect.inflate(20,10)  # Expand collision area by 20 pixels width, 10 pixels height
                    if player.player_state:
                        if player.last_direction_faced == 'right':
                            # create a projectile from the player towards the right
                            projectile = Projectile(pygame.image.load('sprites/projectiles/arrow.png').convert_alpha(), player.rect.x, player.rect.y, 1, 10)
                            projectile.set_platforms(platforms)
                            projectile.set_targets(targets)
                            projectiles.add(projectile)
                        elif player.last_direction_faced == 'left':
                            # create a projectile from the player towards the left
                            projectile = Projectile(pygame.image.load('sprites/projectiles/arrow.png').convert_alpha(), player.rect.x, player.rect.y, -1, 10)
                            projectile.set_platforms(platforms)
                            projectile.set_targets(targets)
                            projectiles.add(projectile)
                    else:
                        for platform in platforms:
                            if attack_rect.colliderect(platform.rect):
                                if platform.broken():
                                    platforms.remove(platform)
                                    all_sprites.remove(platform)
                                    player.set_platforms(platforms)
                                    # set all platforms of projectiles
                                    for sprite in all_sprites:
                                        if isinstance(sprite, Projectile):
                                            sprite.set_platforms(platforms)

            elif event.type == pygame.USEREVENT + 1:  # Custom attack animation timer
                player.attacking = False
                player.set_player_image('sprites/player/player.png')  # Reset to idle sprite

            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_a, pygame.K_d]:
                    player.stop()



        # Check for collisions between projectiles and targets
        for projectile in projectiles:
            if isinstance(projectile, Projectile):
                new_platform = projectile.update()
                if new_platform:
                    platforms.add(new_platform)
                    all_sprites.add(new_platform)

        # Update all sprites
        all_sprites.update()

        if pygame.sprite.collide_rect(player, goal):
            goal, all_sprites, platforms, spawn_point = next_level(player, camera, all_sprites, platforms)
            player.set_platforms(platforms)
            print(f"Moving to {CURRENT_ROOM}")

        camera.update(player)
        draw_gradient(screen, START_COLOR, END_COLOR)
        screen.blit(background, background_rect.topleft)
        sorted_sprites = sorted(all_sprites.sprites() + projectiles.sprites(), key=lambda sprite: getattr(sprite, 'z_index', 0))

        for sprite in sorted_sprites:
            screen.blit(sprite.image, camera.apply(sprite))
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()