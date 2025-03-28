import pygame
from pieces import Piece

class Board:
    """A class to manage the game board."""

    def __init__(self, game):
        """
        Initialize the board.
        
        Args:
            game: The instance of the main game class (LinesOfAction).
        """
        self.screen = game.screen
        self.settings = game.settings

        # Initialize a dictionary to store the piece locations
        self.board_dict = {}

        # Initialize a sprite group for pieces.
        self.pieces = pygame.sprite.Group()

        # Create the initial set of pieces.
        self._create_pieces()
        
        # Store the valid moves for the selected piece.
        self.valid_moves = []

    def _create_pieces(self):
        """Create the initial set of pieces."""
        # Create white pieces.
        for col in (0, self.settings.cols - 1):
            for row in range(1, self.settings.rows - 1):
                pos = (col * self.settings.square_size, row * self.settings.square_size)
                piece = Piece(self.settings, 'white', pos)
                self.pieces.add(piece)
                self.board_dict[(row, col)] = 'W'  # 'W' represents a white piece in the matrix

        # Create black pieces.
        for row in (0, self.settings.rows - 1):
            for col in range(1, self.settings.cols - 1):
                pos = (col * self.settings.square_size, row * self.settings.square_size)
                piece = Piece(self.settings, 'black', pos)
                self.pieces.add(piece)
                self.board_dict[(row, col)] = 'B'  # 'B' represents a black piece in the matrix
        print(self.board_dict)

    def draw_board(self):
        """Draw the game board with alternating colors."""
        for row in range(self.settings.rows):
            for col in range(self.settings.cols):
                color = (
                    self.settings.light_color 
                    if (row + col) % 2 == 0 
                    else self.settings.dark_color
                )
                pygame.draw.rect(
                    self.screen, color,
                    (col * self.settings.square_size, row * self.settings.square_size, 
                     self.settings.square_size, self.settings.square_size)
                )
    
    def reset_board(self):
        """Reset the board to the initial state."""
        # Clear the existing pieces and board dictionary
        self.pieces.empty()  # Remove all pieces from the sprite group
        self.board_dict.clear()  # Clear the dictionary holding piece locations
        self._create_pieces()

    def draw_pieces(self):
        """Draw all the pieces on the board."""
        self.pieces.draw(self.screen)

    def draw_valid_moves(self, valid_moves):
        """Draw circles on the board to show valid move locations."""
        for row, col in valid_moves:
            center_x = col * self.settings.square_size + self.settings.square_size // 2
            center_y = row * self.settings.square_size + self.settings.square_size // 2
            pygame.draw.circle(self.screen, (255, 0, 0), (center_x, center_y), 10)
