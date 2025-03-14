import sys
import pygame
from settings import Settings
from board import Board

class LinesOfAction:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()
        self.clock = pygame.time.Clock()

        # Set up the screen.
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Lines Of Action")

        # Initialize the board.
        self.board = Board(self)

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            # Watch for events.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # Redraw the screen.
            self.board.draw_board()
            self.board.draw_pieces()

            # Update the display.
            pygame.display.flip()
            self.clock.tick(self.settings.fps)