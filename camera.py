import pygame

SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 600
ROOM_WIDTH = 2600  # Width of the room
ROOM_HEIGHT = 1200  # Height of the room

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        """Adjust the position of an entity relative to the camera."""
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        """Update the camera's position to follow the target, but stay within room boundaries."""
        # Calculate the camera's position to center on the target
        x = -target.rect.x + int(SCREEN_WIDTH / 2)
        y = -target.rect.y + int(SCREEN_HEIGHT / 2)

        # Clamp the camera's position to stay within the room boundaries
        x = min(0, x)  # Don't scroll past the left edge
        x = max(-(ROOM_WIDTH - SCREEN_WIDTH), x)  # Don't scroll past the right edge
        y = min(0, y)  # Don't scroll past the top edge
        y = max(-(ROOM_HEIGHT - SCREEN_HEIGHT), y)  # Don't scroll past the bottom edge

        # Update the camera's position
        self.camera = pygame.Rect(x, y, self.width, self.height)