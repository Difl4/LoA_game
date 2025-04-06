# button.py
import pygame

class Button(pygame.sprite.Sprite):
    def __init__(self, game, text, x_percent, y_percent, base_color, hovering_color, size_factor=1):
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        
        # Convert percentage coordinates to pixel coordinates
        self.x_pos = int(x_percent * self.settings.screen_width)
        self.y_pos = int(y_percent * self.settings.screen_height)
        
        self.font = pygame.font.SysFont(None, 48)
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.text_input = text
        self.size_factor = size_factor
        
        # Create button surface
        self.image = pygame.Surface(
            (self.settings.button_width, self.settings.button_height), 
            pygame.SRCALPHA
        )
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        
        # Render text
        self.text = self.font.render(self.text_input, True, self.base_color)
        self.text_rect = self.text.get_rect(center=self.rect.center)

    def update(self):
        """Update the button's appearance and draw it."""
        mouse_pos = pygame.mouse.get_pos()
        self.change_color(mouse_pos)
        self.screen.blit(self.image, self.rect)
        self.screen.blit(self.text, self.text_rect)

    def check_for_input(self, position):
        """Check if the position is within the button's rect."""
        return self.rect.collidepoint(position)

    def change_color(self, position):
        """Change color if mouse is hovering over the button."""
        if self.check_for_input(position):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
        self.text_rect = self.text.get_rect(center=self.rect.center)