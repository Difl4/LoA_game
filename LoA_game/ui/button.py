import pygame

class Button:
    """"A class to build buttons for the game."""

    def __init__(self, game, msg, y_pos):
        """"Initialize the buttons attributes."""
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the buton.
        self.width = game.settings.button_width
        self.height = game.settings.button_height
        self.button_color = (255, 0, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        center_x = self.screen_rect.width // 2

        # Build the butons rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (center_x, y_pos)

        # The buton message needs to be prepped only once
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn message into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
        
    def draw_button(self):
        """Draw blank button and then draw message."""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)