import pygame

# Player settings
PLAYER_WIDTH = 55
PLAYER_HEIGHT = 100
PLAYER_COLOR = (0, 128, 255)
PLAYER_SPEED = 5
GRAVITY = 1
JUMP_STRENGTH = 15
ACCELERATION = 0.6
MAX_SPEED = 6
ANIMATION_SPEED = 150  # Time between frame changes in milliseconds


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('sprites/player/player.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.change_x = 0
        self.change_y = 0
        self.on_ground = False
        self.attacking = False
        self.acceleration = 0
        self.player_state = False
        self.last_direction_faced = 'right'

        # Animation variables
        self.walking_frame = 1  # Track which walking frame we're on
        self.last_frame_update = pygame.time.get_ticks()  # Track when we last changed frames

    def update(self):
        self.calc_grav()
        self.rect.x += self.change_x

        # Update animation if moving
        if self.acceleration != 0:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_frame_update > ANIMATION_SPEED:
                self.walking_frame = 3 - self.walking_frame  # Toggle between 1 and 2
                self.last_frame_update = current_time
                # Update the walking animation frame
                if self.acceleration < 0:  # Moving left
                    self.set_player_image(f'sprites/player/player_left{self.walking_frame}.png')
                else:  # Moving right
                    self.set_player_image(f'sprites/player/player_right{self.walking_frame}.png')

        # Check for collision with platforms
        platform_hit_list = pygame.sprite.spritecollide(self, self.platforms, False)
        for platform in platform_hit_list:
            if self.change_x > 0:
                self.rect.right = platform.rect.left
            elif self.change_x < 0:
                self.rect.left = platform.rect.right

        self.rect.y += self.change_y

        # Check for collision with platforms
        platform_hit_list = pygame.sprite.spritecollide(self, self.platforms, False)
        for platform in platform_hit_list:
            if self.change_y > 0:
                self.rect.bottom = platform.rect.top
                self.on_ground = True
                self.change_y = 0
            elif self.change_y < 0:
                self.rect.top = platform.rect.bottom
                self.change_y = 0

        if not self.on_ground:
            self.set_player_image('sprites/player/player_fall.png')
        elif self.change_x == 0 and self.acceleration == 0 and not self.attacking:
            self.set_player_image('sprites/player/player.png')

        # Apply acceleration
        if self.acceleration != 0:
            self.change_x += self.acceleration
            if self.change_x > MAX_SPEED:
                self.change_x = MAX_SPEED
            elif self.change_x < -MAX_SPEED:
                self.change_x = -MAX_SPEED
        else:
            # Apply deceleration
            if self.change_x > 0:
                self.change_x -= ACCELERATION
                if self.change_x < 0:
                    self.change_x = 0
            elif self.change_x < 0:
                self.change_x += ACCELERATION
                if self.change_x > 0:
                    self.change_x = 0

    def set_player_image(self, image):
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))

    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += GRAVITY

        if self.rect.y >= 1200 - PLAYER_HEIGHT and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = 1200 - PLAYER_HEIGHT
            self.on_ground = True

    def jump(self):
        if self.on_ground:
            self.change_y = -JUMP_STRENGTH
            self.on_ground = False

    def attack(self):
        self.attacking = True
        if self.player_state:
            self.set_player_image('sprites/player/player_attackB.png')
        else:
            self.set_player_image('sprites/player/player_attackA.png')
        pygame.time.set_timer(pygame.USEREVENT + 1, 100)  # Custom event for ending attack animation

    def go_left(self):
        self.acceleration = -ACCELERATION
        self.last_direction_faced = 'left'

    def go_right(self):
        self.acceleration = ACCELERATION
        self.last_direction_faced = 'right'

    def stop(self):
        self.acceleration = 0
        if self.change_x > 0:
            self.change_x -= ACCELERATION / 2  # Smoother deceleration
            if self.change_x < 0:
                self.change_x = 0
        elif self.change_x < 0:
            self.change_x += ACCELERATION / 2  # Smoother deceleration
            if self.change_x > 0:
                self.change_x = 0
        self.set_player_image('sprites/player/player.png')

    def switch_player_state(self):
        self.player_state = not self.player_state

    def set_platforms(self, platforms):
        self.platforms = platforms