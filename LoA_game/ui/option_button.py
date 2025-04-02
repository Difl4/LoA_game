import pygame
from ui.button import Button

class OptionButton(Button):
    """Class to handle option button with selectable choices."""

    def __init__(self, game, label, x_percent, y_percent):
        # Call the parent class (Button) constructor with y=0 because we handle y positioning manually
        super().__init__(game, label, 0)  # Pass 0 for y_pos as it's handled here
        
        # Calculate the absolute screen coordinates for x and y using percentage of screen size
        center_x = self.screen_rect.width * x_percent
        center_y = self.screen_rect.height * y_percent

        # Update the button's position
        self.rect.center = (center_x, center_y)

        # Initialize options from the settings
        self.options = game.settings.player_options
        self.selected_index = 0  # Default to the first option

        # Set the first option as the button message
        self._prep_msg(self.options[self.selected_index])

    def handle_event(self, event):
        """Handle the event when the user clicks on the option button."""
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            # Cycle through the options
            self.selected_index = (self.selected_index + 1) % len(self.options)
            self._prep_msg(self.options[self.selected_index])  # Update the button message