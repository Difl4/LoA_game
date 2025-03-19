import sys
import pygame
from settings import Settings
from board import Board
from movement import LOAMovement
from translations import get_matrix_position

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

        # Initialize the board and movement logic.
        self.board = Board(self)
        print(f"initializing movement")
        self.movement = LOAMovement(self)

        # Selected piece state
        self.selected_piece = None
        self.valid_moves = []

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self._update_screen()
            self.clock.tick(self.settings.fps)

    def _check_events(self):
        """Handle key and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_click(event.pos) # Gives (x, y) pixel coordinates

    def _handle_mouse_click(self, pos):
        """Handle selecting and moving pieces."""
        row, col = get_matrix_position(pos[0], pos[1], self.settings.square_size)

        if (row, col) in self.board.board_dict:
            piece = self.board.board_dict[(row, col)]  # Get piece at clicked location
        else:
            piece = None  # No piece at the clicked location
    
        if piece in ('W', 'B'):
            # Select a piece and show valid moves
            self.selected_piece = (row, col)
            self.valid_moves = self.movement.get_valid_moves(row, col)
        elif (row, col) in self.valid_moves:
            # Move the selected piece
            self._move_piece(self.selected_piece, (row, col))

    def _move_piece(self, from_pos, to_pos):
        """Move a piece from one position to another."""
        row_from, col_from = from_pos
        row_to, col_to = to_pos

        # Update board state
        self.board.board_dict[(row_to, col_to)] = self.board.board_dict[(row_from, col_from)]
        del self.board.board_dict[(row_from, col_from)]

        # Update the visual piece sprite
        for piece in self.board.pieces:
            if piece.rect.topleft == (col_from * self.settings.square_size, row_from * self.settings.square_size):
                piece.rect.topleft = (col_to * self.settings.square_size, row_to * self.settings.square_size)
                break

        # Deselect piece after move
        self.selected_piece = None
        self.valid_moves = []

    def _update_screen(self):
        """Update and redraw the game screen."""
        self.board.draw_board()
        self.board.draw_pieces()
        self.board.draw_valid_moves(self.valid_moves)
        pygame.display.flip()
