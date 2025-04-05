import pygame

class Button(pygame.sprite.Sprite):
    def __init__(self, image, pos, text_input, font, base_color, hovering_color, size_factor=1):
        super().__init__()
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.text_input = text_input
        self.size_factor = size_factor
        self.render_text(self.base_color)

        if self.image is None:
            # Create a transparent surface based on the size of the text
            self.image = pygame.Surface((self.text.get_width(), self.text.get_height()), pygame.SRCALPHA)  # Transparent surface
            self.image.fill((0, 0, 0, 0))  # Completely transparent background
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def render_text(self, color):
        # Render text on the button with the provided color
        self.text = self.font.render(self.text_input, True, color)
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkforinput(self, position):
        return self.rect.collidepoint(position)

    def change_color(self, position):
        if self.checkforinput(position):
            self.render_text(self.hovering_color)
        else:
            self.render_text(self.base_color)