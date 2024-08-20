import pygame

class Player(pygame.sprite.Sprite):
    """Defines class for player-controlled avatar (probably a bird).
    
    Attributes:
        frames (List[pygame.Surface]): List of images representing the player sprite's animation frames.
        current_frame (int): Index of the current animation frame.
        image (pygame.Surface): The current image to be displayed for the sprite.
        x (int): The x-coordinate of the player.
        y (int): The y-coordinate of the player.
        y_speed (float): The current speed of the player in the y direction.
        animation_counter (int): Counter to control the animation speed.
        rect (pygame.Rect): The rectangle representing the player's position and size
    
    """
    def __init__(self, sprites: list[pygame.Surface], screen_height: int, gravity: float, jump_speed: float):
        """Initializes the player sprite.

        Args:
            sprites (list[pygame.Surface]): list of images representing the player sprite's animation frames
            screen_height (int): height of the game screen
            game_config (GameConfig): configuration object containing game settings
        """
        super().__init__()

        self.frames = sprites
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.animation_counter = 0

        # Set position
        self.x = 50
        self.y = screen_height // 2

        self.y_speed = 0
        self.gravity = gravity
        self.jump_speed = jump_speed
        
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self, screen: pygame.Surface) -> None:
        """Draws the sprite to the screen.

        Args:
            screen (pygame.Surface): surface to draw to
        
        Returns: None
        """
        # rotate sprite based on vertical speed
        rotated_image = pygame.transform.rotate(self.image, -self.y_speed * 3)
        new_rect = rotated_image.get_rect(center=self.rect.center)
        screen.blit(rotated_image, new_rect.topleft)

    def update(self) -> None:
        """Updates player position and sprite.

        Args: None

        Returns: None
        """
        self.y_speed += self.gravity
        self.y += self.y_speed
        self.rect.y = self.y

        # Handle animation
        self.animation_counter += 1
        if self.animation_counter % 5 == 0:  # Change frame every 5 ticks
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]

    def jump(self) -> None:
        """Updates player speed based on jump velocity.
        
        Args: None

        Returns: None
        """
        self.y_speed = self.jump_speed