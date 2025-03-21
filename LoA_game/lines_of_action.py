import sys
import pygame
from settings import Settings
from board import Board
from movement import LOAMovement
from translations import get_matrix_position
from win_check import WinChecker
from ai_model_A import AiModelA
import time

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
        self.movement = LOAMovement(self)
        self.win_checker = WinChecker(self)  # Initialize WinChecker

        self.ai_model = AiModelA(self)
        # Selected piece state
        self.selected_piece = None
        self.valid_moves = []

        # Turn state
        self.current_turn = 'B'  # Black goes first

    def run_game(self):
        """Start the main loop for the game."""
        i = 0
        while True:
            # self._check_events()
            self._update_screen()

            if(i % 2 == 0):
                _, move = self.ai_model.minimax(self.board.board_dict, 3, True, "B")
            else:
                _, move = self.ai_model.minimax(self.board.board_dict, 3, False, "W")


            self._move_piece(move[0], move[1])
            i += 1

            if(self.win_checker.check_win("W", self.board.board_dict) != 0):
                print("Vitória do branco")
                self._update_screen()
                time.sleep(100000)
                return
            elif(self.win_checker.check_win("B", self.board.board_dict) != 0):
                print("Vitória do preto")
                self._update_screen()
                time.sleep(100000)
                return

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

        if piece == self.current_turn:  # Only allow current player's piece to be selected
            # Select a piece and show valid moves
            self.selected_piece = (row, col)
            self.valid_moves = self.movement.get_valid_moves(row, col)
        elif (row, col) in self.valid_moves:
            # Move the selected piece
            self._move_piece(self.selected_piece, (row, col))

            # Check for win condition after the move


            if self.win_checker.check_win("W", self.board.board_dict):
                print(f"W wins!")
                sys.exit()
            elif self.win_checker.check_win("B", self.board.board_dict):
                print(f"B wins!")
                sys.exit()
            # Switch turn to the other player
            self._switch_turn()

    def _move_piece(self, from_pos, to_pos):
        #print("dsa")
        """Move a piece from one position to another."""
        print(f"Moving piece {self.board.board_dict[(from_pos[0], from_pos[1])]} from {from_pos} to {to_pos}")
        row_from, col_from = from_pos
        row_to, col_to = to_pos

        # Check if the destination has an opponent's piece
        if (row_to, col_to) in self.board.board_dict:
            if self.board.board_dict[(row_to, col_to)] != self.current_turn:
                # Capture the opponent's piece
                self._capture_piece(row_to, col_to)

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

    def _switch_turn(self):
        """Switch turns between players."""
        if self.current_turn == 'B':
            self.current_turn = 'W'  # Switch to white
        else:
            self.current_turn = 'B'  # Switch to black

    def _update_screen(self):
        """Update and redraw the game screen."""
        self.board.draw_board()
        self.board.draw_pieces()
        self.board.draw_valid_moves(self.valid_moves)
        pygame.display.flip()
    
    def _capture_piece(self, row, col):
        """Remove a captured piece from the board."""
        # Remove the piece from the board dictionary
        del self.board.board_dict[(row, col)]

        # Remove the piece from the sprite group
        for piece in self.board.pieces:
            if piece.rect.topleft == (col * self.settings.square_size, row * self.settings.square_size):
                self.board.pieces.remove(piece)
                break