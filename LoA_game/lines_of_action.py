import sys
import pygame
from settings import Settings
from board import Board
from movement import LOAMovement
from translations import get_matrix_position
from win_check import WinChecker
from button import Button
from ai_model_A import AiModelA

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

        # Selected piece state
        self.selected_piece = None
        self.valid_moves = []

        self.game_active = False

        # Make the play button
        self.buttons = [
            Button(self, "Play Human", 150),
            Button(self, "Play AI", 250),
            Button(self, "Watch AI", 350)
        ]

        # Turn state
        self.current_turn = 'B'  # Black goes first

        # AI game mode flag
        self.ai_game = False

        # Human-AI game mode flag
        self.h_ai_game = False

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._update_screen()
            if self.game_active:
                if self.ai_game:
                    self._play_ai_turn()
                elif self.h_ai_game:
                    if self.current_turn == 'B':
                        pass
                    elif self.current_turn == 'W':
                        self._play_ai_turn()
            self._check_events()
            self.clock.tick(self.settings.fps)

    def _check_events(self):
        """Handle key and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if not self.game_active:
                    self._check_play_button(mouse_pos)

                if not self.ai_game:
                    self._handle_mouse_click(mouse_pos) # Gives (x, y) pixel coordinates
    
    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        if self.buttons[0].rect.collidepoint(mouse_pos):
            self.game_active = True
        
        elif self.buttons[1].rect.collidepoint(mouse_pos):
            self.game_active = True
            self.h_ai_game = True
            self.ai_model_w = AiModelA(self)
        
        elif self.buttons[2].rect.collidepoint(mouse_pos):
            self.game_active = True
            self.ai_game = True  # AI vs AI mode
            self.ai_model_b = AiModelA(self)  # Create AI instance for Black
            self.ai_model_w = AiModelA(self)  # Create AI instance for White

    def _post_move_actions(self):
        """Check for win conditions and switch turns after a move."""
        if self.win_checker.check_win(self.current_turn):
            print(f"{self.current_turn} wins!")
            self.game_active = False  # Stop the game
            return  # Exit function early

        self._switch_turn()  # Switch turn if no one has won

    def _handle_mouse_click(self, pos):
        """Handle selecting and moving pieces."""
        if not self.game_active:
            return  # Ignore clicks if the game is over

        row, col = get_matrix_position(pos[0], pos[1], self.settings.square_size)
        clicked_piece = self.board.board_dict.get((row, col))  # Get the clicked piece

        if self.selected_piece:
            # If a piece is selected, try to move it
            if (row, col) in self.valid_moves:
                self._move_piece(self.selected_piece, (row, col))
                self._post_move_actions()  # <--- This ensures turn switching and win checking!
            else:
                # Clicked an invalid move location, deselect the piece
                self.selected_piece = None
                self.valid_moves = []
        elif clicked_piece == self.current_turn:
            # Select a piece if it's the player's turn
            self.selected_piece = (row, col)
            self.valid_moves = self.movement.get_valid_moves(row, col)

    def _move_piece(self, from_pos, to_pos):
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
        if self.game_active:
            self.board.draw_board()
            self.board.draw_pieces()
            self.board.draw_valid_moves(self.valid_moves)

        else:
            self.board.draw_board()
            for button in self.buttons:
                button.draw_button()

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
    
    def _play_ai_turn(self):
        """Handle AI's turn to make a move."""
        if self.current_turn == 'B':
            # AI "B" turn
            _, best_move = self.ai_model_b.minimax(self.board.board_dict, 3, True, 'B')
        else:
            # AI "W" turn
            _, best_move = self.ai_model_w.minimax(self.board.board_dict, 3, True, 'W')
        
        # Perform the move
        if best_move:
            from_pos, to_pos = best_move
            self._move_piece(from_pos, to_pos)
        
        self._post_move_actions()  # Check win and switch turns
