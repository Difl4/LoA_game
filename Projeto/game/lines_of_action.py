import sys
import pygame
from config.settings import Settings
from game.board import Board
from game.movement import LOAMovement
from game.win_check import WinChecker
from game.main_menu import MainMenu
from game.game_flow import GameFlow
from ai.base_ai import BaseAI

class LinesOfAction:
    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()
        self.clock = pygame.time.Clock()

        # Set up the screen
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Lines Of Action")

        # Initialize game components
        self.board = Board(self)
        self.movement = LOAMovement(self)
        self.win_checker = WinChecker(self)
        self.game_flow = GameFlow(self)
        self.main_menu = MainMenu(self)

        # Game state flags
        self.running = True
        self.in_menu = True

    def run_game(self):
        """Start the main loop for the game."""
        while self.running:
            if self.in_menu:
                self._run_menu_loop()
            else:
                self._run_game_loop()

    def _run_menu_loop(self):
        """Run the menu loop."""
        self.main_menu.run_menu()
        # After exiting menu, check if we should start the game
        if self.game_flow.game_active:
            self.in_menu = False

    def _run_game_loop(self):
        """Run the main game loop."""
        self._check_events()
        self._update_screen()

        if self.game_flow.game_active:
            self.game_flow.handle_turn()
            self.game_flow.update()
        else:
            # Game ended, return to menu
            self.in_menu = True

        self.clock.tick(self.settings.fps)

    def _check_events(self):
        """Handle key and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not self.in_menu and self.game_flow.game_active:
                    current_player = (self.game_flow.black_player if self.game_flow.current_turn == 'B' 
                                    else self.game_flow.white_player)
                    if not isinstance(current_player, BaseAI):
                        mouse_pos = pygame.mouse.get_pos()
                        self.game_flow.select_piece(mouse_pos)

    def _update_screen(self):
        """Update and redraw the game screen."""
        if not self.in_menu:
            self.board.draw_board(self.game_flow.last_move_to)
            if self.game_flow.game_active:
                self.board.draw_pieces()
                self.board.draw_valid_moves(self.game_flow.valid_moves)
                self._draw_player_text(
                    self.settings.screen_width // 2, 20, 
                    f"{self.game_flow.current_turn} Player's Turn"
                )
            pygame.display.flip()

    def _draw_player_text(self, x, y, text):
        """Draw the current player's turn text."""
        font = pygame.font.SysFont(None, 36)
        player_text = font.render(text, True, (204, 85, 0))
        text_rect = player_text.get_rect(center=(x, y))
        self.screen.blit(player_text, text_rect)