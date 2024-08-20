import pygame

class Button:
    """UI clickable button.

    Represents a button in a Pygame application, with customizable text, colors,
    and hover effects. The button can detect clicks and change appearance based
    on mouse interaction.

    Attributes:
        rect (pygame.Rect): The rectangle defining the button's position and size.
        text (str): The text displayed on the button.
        font (pygame.font.Font): The font used to render the button's text.
        color (tuple): The RGB color of the button in its normal state.
        hover_color (tuple): The RGB color of the button when hovered over.
    """

    def __init__(self, x, y, width, height, text, font, color, hover_color):
        """
        Initializes a Button instance with the given attributes.

        Args:
            x (int): The x-coordinate of the top-left corner of the button.
            y (int): The y-coordinate of the top-left corner of the button.
            width (int): The width of the button.
            height (int): The height of the button.
            text (str): The text displayed on the button.
            font (pygame.font.Font): The font used to render the button's text.
            color (tuple): The RGB color of the button in its normal state.
            hover_color (tuple): The RGB color of the button when hovered over.
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
    
    def draw(self, screen):
        """
        Draws the button on the screen, changing color when hovered over.

        Args:
            screen (pygame.Surface): The surface on which to draw the button.
        """
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)

        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self):
        """
        Checks if the button has been clicked.

        Returns:
            bool: True if the button is clicked, False otherwise.
        """
        return self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]

