import pygame
import random
from classes.player import Player

class Obstacle(pygame.sprite.Sprite):
    """
    Represents an obstacle in the game with support for animation.

    Attributes:
        sprites (list[pygame.Surface]): List of images representing the obstacle's animation frames.
        current_frame (int): Index of the current animation frame.
        image_top (pygame.Surface): The current image to be displayed for the top of the obstacle.
        image_bottom (pygame.Surface): The current image to be displayed for the bottom of the obstacle.
        rect_top (pygame.Rect): The rectangle representing the position and size of the top of the obstacle.
        rect_bottom (pygame.Rect): The rectangle representing the position and size of the bottom of the obstacle.
        animation_counter (int): Counter to control the animation speed.
    """
    def __init__(self, x: int, sprites: list[pygame.Surface], screen_height: int, gap: int = 200, speed: int = 3):
        """Initializes the obstacles.

        Args:
            screen_height (int): height of screen
        """
        super().__init__()
        self.sprites = sprites
        self.current_frame = 0
        self.animation_counter = 0
        self.speed = speed

        # Set initial images and rectangles
        self.image_top = pygame.transform.flip(self.sprites[self.current_frame], False, True)
        self.image_bottom = self.sprites[self.current_frame]
        self.gap = gap

        self.x = x
        self.height = random.randint(50, screen_height - self.gap - 50)
        self.rect_top = self.image_top.get_rect(topleft=(self.x, self.height - self.image_top.get_height()))
        self.rect_bottom = self.image_bottom.get_rect(topleft=(self.x, self.height + self.gap))

    def draw(self, screen: pygame.Surface) -> None:
        """Draws the obstacle to the screen.

        Args:
            screen (pygame.Surface): The surface to draw the obstacle on.
        """
        screen.blit(self.image_top, self.rect_top.topleft)
        screen.blit(self.image_bottom, self.rect_bottom.topleft)

    def update(self) -> None:
        """Updates the obstacle's position and animation frame."""
        self.rect_top.x -= self.speed
        self.rect_bottom.x -= self.speed

        # Handle animation
        self.animation_counter += 1
        if self.animation_counter % 5 == 0:  # Change frame every 5 ticks
            self.current_frame = (self.current_frame + 1) % len(self.sprites)

            self.image_top = pygame.transform.flip(self.sprites[self.current_frame], False, True)
            self.image_bottom = self.sprites[self.current_frame]

            self.rect_top = self.image_top.get_rect(topleft=(self.rect_top.x, self.height - self.image_top.get_height()))
            self.rect_bottom = self.image_bottom.get_rect(topleft=(self.rect_bottom.x, self.height + self.gap))

    def off_screen(self) -> bool:
        """Checks if the obstacle is off the screen.

        Returns:
            bool: True if the obstacle is off the screen, False otherwise.
        """
        return self.rect_top.right < 0

    def collides_with(self, player: Player) -> bool:
        """Checks if the obstacle collides with the player.

        Args:
            player (Player): The player object to check for collision.
        
        Returns:
            bool: True if a collision occurs, False otherwise.
        """
        return self.rect_top.colliderect(player.rect) or self.rect_bottom.colliderect(player.rect)
