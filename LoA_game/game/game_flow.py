from ai.base_ai import BaseAI
from ai.all_ai import (
    MinimaxSimple,
    MinimaxBetter,
    Random,
    NegamaxSimple,
    NegamaxBetter,
    MCTSCenterMass,
    MCTSEnhanced,
    MCTSConnectivity
)
from config.translations import get_matrix_position
import threading
import time
import pygame

class GameFlow:
    """Handles the flow of the game, including turns and win checking."""

    def __init__(self, game):
        self.game = game
        self.board = game.board
        self.movement = game.movement
        self.win_checker = game.win_checker
        self.settings = game.settings
        self.screen = game.screen
        self._update_screen = game._update_screen
        self.game_active = False
        self.selected_piece = None
        self.valid_moves = []
        self.current_turn = 'B'
        self.white_player = None
        self.black_player = None
        self.last_move_to = None

        self.PLAYER_MAP = {
            'Human': None,
            'Minimax | Easy': MinimaxSimple,
            'Minimax | Hard': MinimaxBetter,
            'Random': Random,
            'Negamax | Very Easy': NegamaxSimple,
            'Negamax | Easy': NegamaxBetter,
            'MCTS | Very Hard': MCTSCenterMass,
            'MCTS | Hard': MCTSEnhanced,
            'MCTS | Medium': MCTSConnectivity
        }

        # Ai flags
        self.ai_thinking = False
        self.ai_move = None
        self.ai_player = None

    def start_game(self, white_choice, black_choice):
        """Initialize players and start the game using a dictionary mapping."""
        self.game_active = True
        self.white_player = self._initialize_player(white_choice, 'W')
        self.black_player = self._initialize_player(black_choice, 'B')
        self.current_turn = 'B'

        # Log game start with separator
        with open("log.txt", "a") as logfile:
            logfile.write("\n\n" + "=" * 80 + "\n")
            logfile.write(f"NEW GAME STARTED\n")
            logfile.write(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            logfile.write(f"White Player: {white_choice}\n")
            logfile.write(f"Black Player: {black_choice}\n")
            logfile.write("=" * 80 + "\n\n")

    def _initialize_player(self, choice, color):
        """Initialize a player based on the selected choice."""
        player_class = self.PLAYER_MAP.get(choice)
        return player_class(self, color) if player_class else 'Human'

    def switch_turn(self):
        """Switch turns between players."""
        self.current_turn = 'W' if self.current_turn == 'B' else 'B'

    def handle_turn(self):
        """Handle the turn for the current player."""
        if self.ai_thinking:
            return  # Don't process anything while AI is thinking
        
        current_player = self.black_player if self.current_turn == 'B' else self.white_player
        if isinstance(current_player, BaseAI):
            self._start_ai_turn(current_player)

    def _start_ai_turn(self, ai_player):
        """Launch AI calculation in a separate thread"""
        self.ai_thinking = True
        self.ai_move = None
        self.ai_player = ai_player
    
        def ai_thread():
            start = time.time()
            self.ai_move = self.ai_player.get_move(self.board.board_dict)
            time_taken = time.time() - start
            
            with open("log.txt", "a") as logfile:
                logfile.write(f"""
                AI Type: {type(ai_player).__name__}
                Move: {self.ai_move}
                Time: {time_taken:.2f}s
                Depth: {self.ai_player.search_depth}
                Nodes: {self.ai_player.nodes_explored}\n
                """)
            print(f"AI took {time_taken:.2f} seconds to make a move.")

        threading.Thread(target=ai_thread, daemon=True).start()

    def update(self):
        """Should be called every frame from main game loop"""
        if self.ai_thinking and self.ai_move is not None:
            self._finish_ai_turn()

    def _finish_ai_turn(self):
        """Execute the AI's move and clean up"""
        try:
            if self.ai_move:
                self._move_piece(*self.ai_move)
                self.check_for_winner()
        finally:
            self.ai_thinking = False
            self.ai_move = None
            self.ai_player = None

    def _move_piece(self, from_pos, to_pos):
        """Move a piece on the board."""
        row_from, col_from = from_pos
        row_to, col_to = to_pos

        # Capture opponent's piece if present
        if (row_to, col_to) in self.board.board_dict and self.board.board_dict[(row_to, col_to)] != self.current_turn:
            self._capture_piece(row_to, col_to)

        # Update board state
        self.board.board_dict[(row_to, col_to)] = self.board.board_dict.pop((row_from, col_from))

        # Update the visual piece sprite
        for piece in self.board.pieces:
            if piece.rect.topleft == (col_from * self.settings.square_size, row_from * self.settings.square_size):
                piece.rect.topleft = (col_to * self.settings.square_size, row_to * self.settings.square_size)
                break
        self.last_move_to =(row_to, col_to)
        print(f"Moving {self.current_turn} from {from_pos} to {to_pos}")

        self.selected_piece = None
        self.valid_moves = []

    def _capture_piece(self, row, col):
        """Remove a captured piece from the board."""
        del self.board.board_dict[(row, col)]
        for piece in self.board.pieces:
            if piece.rect.topleft == (col * self.settings.square_size, row * self.settings.square_size):
                self.board.pieces.remove(piece)
                break

    def check_for_winner(self):
        """Check if there is a winner and handle game end."""
        if self.win_checker.check_win('W'):
            self._handle_game_end('W')
        elif self.win_checker.check_win('B'):
            self._handle_game_end('B')
        else:
            self.switch_turn()

    def _handle_game_end(self, winner):
        """Display winner and return to menu."""
        # Log the game result
        with open("log.txt", "a") as logfile:
            logfile.write(f"\nGAME RESULT: {winner} Player Wins!\n")
            logfile.write("=" * 80 + "\n\n")  # Add separator after game ends
        
        # Display winner message
        self._update_screen()  # Ensure board is drawn first
        
        font = pygame.font.SysFont(None, 72)
        winner_text = font.render(f"{winner} Player Wins!", True, (255, 255, 255))
        text_rect = winner_text.get_rect(center=(self.settings.screen_width//2, self.settings.screen_height//2))
        
        # Create semi-transparent overlay
        overlay = pygame.Surface((self.settings.screen_width, self.settings.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Semi-transparent black
        
        # Draw everything
        self.screen.blit(overlay, (0, 0))
        self.screen.blit(winner_text, text_rect)
        pygame.display.flip()
        
        # Wait before returning to menu
        pygame.time.wait(3000)  # 3 second delay
        self.reset_game()

    def reset_game(self):
        """Reset the game state and transition back to the main menu."""
        self.white_player = None
        self.black_player = None
        self.current_turn = 'B'
        self.game_active = False
        self.selected_piece = None
        self.last_move_to = None
        self.valid_moves = []
        self.board.reset_board()
        self.game.in_menu = True  # Signal to return to menu

    def select_piece(self, pos):
        """Handle piece selection and valid move generation."""
        if not self.game_active or isinstance((self.black_player if self.current_turn == 'B' else self.white_player), BaseAI):
            return  # Ignore clicks when it's the AI's turn
        
        row, col = get_matrix_position(pos[0], pos[1], self.settings.square_size)
        clicked_piece = self.board.board_dict.get((row, col))

        if self.selected_piece and self.current_turn != self.board.board_dict[self.selected_piece]:
            self.selected_piece = None
            self.valid_moves = []

        if self.selected_piece:
            if (row, col) in self.valid_moves:
                self._move_piece(self.selected_piece, (row, col))
                self.check_for_winner()
            else:
                self.selected_piece = None
                self.valid_moves = []
        elif clicked_piece == self.current_turn:
            self.selected_piece = (row, col)
            self.valid_moves = self.movement.get_valid_moves(row, col)