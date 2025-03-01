import pygame
import sys
from audio_manager import AudioManager

# Screen dimensions
SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize Pygame
pygame.init()

# Fonts
font = pygame.font.Font(None, 74)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Platformer Menu")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Load menu background
menu_background = pygame.image.load('backgrounds/menu_bg.png').convert_alpha()
menu_background = pygame.transform.scale(menu_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Initialize AudioManager
audio_manager = AudioManager()
audio_manager.load_music('audio/music/Monty-Python.mp3')
audio_manager.play_music()

# Load mute button images
mute_button_image = pygame.image.load('sprites/menu/mute_button.png').convert_alpha()
mute_button_selected_image = pygame.image.load('sprites/menu/mute_selected_button.png').convert_alpha()
mute_button_image = pygame.transform.scale(mute_button_image, (50, 50))
mute_button_selected_image = pygame.transform.scale(mute_button_selected_image, (50, 50))

# Mute state
is_muted = False

def draw_text(text, font, color, surface, x, y):
    """Helper function to draw text on the screen."""
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def credits_screen():
    """Credits screen loop."""
    while True:
        screen.blit(menu_background, (0, 0))
        draw_text("Credits", font, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
        draw_text("Game developed by Fraser Levack, Kai, Rem & Tough", font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        draw_text("Score by @Rosenrot on Newgrounds", font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
        draw_text("Press ESC to return to the main menu", font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return  # Return to the main menu

        pygame.display.flip()
        clock.tick(60)

def main_menu():
    """Main menu loop."""
    global is_muted

    start_button_image = pygame.image.load('sprites/menu/start_button.png').convert_alpha()
    start_button_selected_image = pygame.image.load('sprites/menu/start_selected_button.png').convert_alpha()
    quit_button_image = pygame.image.load('sprites/menu/quit_button.png').convert_alpha()
    quit_button_selected_image = pygame.image.load('sprites/menu/quit_selected_button.png').convert_alpha()
    credits_button_image = pygame.image.load('sprites/menu/credits_button.png').convert_alpha()
    credits_button_selected_image = pygame.image.load('sprites/menu/credits_selected_button.png').convert_alpha()

    start_button_image = pygame.transform.scale(start_button_image, (200, 100))
    start_button_selected_image = pygame.transform.scale(start_button_selected_image, (200, 100))
    quit_button_image = pygame.transform.scale(quit_button_image, (200, 100))
    quit_button_selected_image = pygame.transform.scale(quit_button_selected_image, (200, 100))
    credits_button_image = pygame.transform.scale(credits_button_image, (200, 100))
    credits_button_selected_image = pygame.transform.scale(credits_button_selected_image, (200, 100))

    while True:
        screen.blit(menu_background, (0, 0))

        # Draw title
        draw_text("Glasgow Knight", font, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 8)

        # Draw buttons
        mouse_pos = pygame.mouse.get_pos()
        start_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 150, 200, 100)
        credits_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 100)
        quit_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 150, 200, 100)
        mute_button = pygame.Rect(SCREEN_WIDTH - 60, SCREEN_HEIGHT - 60, 50, 50)

        # Change button images on hover
        if start_button.collidepoint(mouse_pos):
            screen.blit(start_button_selected_image, start_button.topleft)
        else:
            screen.blit(start_button_image, start_button.topleft)

        if credits_button.collidepoint(mouse_pos):
            screen.blit(credits_button_selected_image, credits_button.topleft)
        else:
            screen.blit(credits_button_image, credits_button.topleft)

        if quit_button.collidepoint(mouse_pos):
            screen.blit(quit_button_selected_image, quit_button.topleft)
        else:
            screen.blit(quit_button_image, quit_button.topleft)

        if mute_button.collidepoint(mouse_pos):
            screen.blit(mute_button_selected_image, mute_button.topleft)
        else:
            screen.blit(mute_button_image, mute_button.topleft)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(mouse_pos):
                    return  # Exit the menu and start the game
                if credits_button.collidepoint(mouse_pos):
                    credits_screen()  # Go to the credits screen
                if quit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()
                if mute_button.collidepoint(mouse_pos):
                    is_muted = not is_muted
                    audio_manager.set_music_volume(0 if is_muted else 1)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main_menu()