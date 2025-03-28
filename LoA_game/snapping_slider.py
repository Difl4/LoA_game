import pygame

class Selector:
    def __init__(self, game, label, x, y):
        self.screen = game.screen
        self.settings = game.settings
        self.label = label
        self.options = self.settings.player_options
        self.selected_index = 0
        self.font = pygame.font.SysFont(None, 36)
        self.rect = pygame.Rect(x, y, 200, 50)  # Adjust size as needed

    def draw(self):
        # Draw label
        label_surf = self.font.render(self.label, True, (0, 0, 0))
        self.screen.blit(label_surf, (self.rect.x, self.rect.y - 30))

        # Draw selector box
        pygame.draw.rect(self.screen, (200, 200, 200), self.rect)
        pygame.draw.rect(self.screen, (0, 0, 0), self.rect, 2)

        # Draw selected option
        option_surf = self.font.render(self.options[self.selected_index], True, (0, 0, 0))
        option_rect = option_surf.get_rect(center=self.rect.center)
        self.screen.blit(option_surf, option_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            # Cycle through options
            self.selected_index = (self.selected_index + 1) % len(self.options)