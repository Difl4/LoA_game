import pygame
from ui.button import Button

class OptionButton(Button):
    """Class to handle option button with selectable choices."""
    
    def __init__(self, game, label, x_percent, y_percent):
        # Initialize with default color (will be updated when options are set)
        super().__init__(game, label, x_percent, y_percent, "#e8d1a5", "white")
        
        # Initialize options from the settings
        self.options = game.settings.player_options
        self.selected_index = 0  # Default to the first option
        
        # Set the first option as the button message
        self.update_text()

    def update_text(self):
        """Update the button's text to show current selection."""
        self.text_input = f"{self.options[self.selected_index]}"
        self.text = self.font.render(self.text_input, True, self.base_color)
        self.text_rect = self.text.get_rect(center=self.rect.center)

    def handle_event(self, event):
        """Handle the event when the user clicks on the option button."""
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            # Cycle through the options
            self.selected_index = (self.selected_index + 1) % len(self.options)
            self.update_text()