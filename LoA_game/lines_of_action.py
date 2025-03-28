import sys
import pygame
from settings import Settings
from board import Board
from movement import LOAMovement
from win_check import WinChecker
from button import Button
from option_button import OptionButton
from game_flow import GameFlow

class LinesOfAction:
    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()
        self.clock = pygame.time.Clock()

        # Set up the screen.
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Lines Of Action")

        # Initialize the board and movement logic.
        self.board = Board(self)
        self.movement = LOAMovement(self)
        self.win_checker = WinChecker(self)  # Initialize WinChecker

        # Initialize the game flow class
        self.game_flow = GameFlow(self)

        # Make the play button and option buttons
        self.play_button = Button(self, "Play", self.settings.screen_height // 2)
        self.white_selector = OptionButton(self, "White Player", 0.25, 0.75)
        self.black_selector = OptionButton(self, "Black Player", 0.75, 0.75)

        # Add the player text
        self.white_player_text = "White Pieces"
        self.black_player_text = "Black Pieces"

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self._update_screen()
            if self.game_flow.game_active:
                self.game_flow.handle_turn()  # <-- Handle AI turn if necessary
            self.clock.tick(self.settings.fps)

    def _check_events(self):
        """Handle key and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if not self.game_flow.game_active:
                    self._check_play_button(mouse_pos)
                    self.white_selector.handle_event(event)  # Handle the white player option button event
                    self.black_selector.handle_event(event)  # Handle the black player option button event
                else:
                    self.game_flow.select_piece(mouse_pos)  # <-- Select piece through GameFlow

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        if self.play_button.rect.collidepoint(mouse_pos):
            self.game_flow.game_active = True

            white_choice = self.white_selector.options[self.white_selector.selected_index]
            black_choice = self.black_selector.options[self.black_selector.selected_index]

            # Pass the choices to the game flow to initialize the players (including AI)
            self.game_flow.start_game(white_choice, black_choice)  # <-- Initialize game flow with player choices

    def _update_screen(self):
        """Update and redraw the game screen."""
        self.board.draw_board()

        if self.game_flow.game_active:
            self.board.draw_pieces()
            self.board.draw_valid_moves(self.game_flow.valid_moves)  # <-- Draw valid moves from GameFlow
            self._draw_player_text(self.settings.screen_width // 2, 20, f"{self.game_flow.current_turn} Player's Turn")
        else:
            self.play_button.draw_button()
            self.white_selector.draw_button()  # Draw the white player option button
            self.black_selector.draw_button()  # Draw the black player option button
            self._draw_player_text(self.white_selector.rect.centerx, self.white_selector.rect.centery - 30, self.white_player_text)
            self._draw_player_text(self.black_selector.rect.centerx, self.black_selector.rect.centery - 30, self.black_player_text)
        pygame.display.flip()

    def _draw_player_text(self, x, y, text):
        """Draw the text (selected player) above the button."""
        font = pygame.font.SysFont(None, 36)
        player_text = font.render(text, True, (204, 85, 0))  # White color for text
        text_rect = player_text.get_rect(center=(x, y))
        self.screen.blit(player_text, text_rect)
