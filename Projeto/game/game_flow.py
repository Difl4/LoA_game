from ai.base_ai import BaseAI
from ai.minimax_alpha_beta import AiModelA_AlphaBeta
from ai.minimax_no_pruning import AiModelA_NoPruning
from ai.negamax_no_pruning import Negamax
from ai.negamax_alpha_beta import NegamaxAlphaBeta
from config.translations import get_matrix_position
import threading
import time

class GameFlow:
    """Handles the flow of the game, including turns and win checking."""

    def __init__(self, game):

        self.board = game.board
        self.movement = game.movement
        self.win_checker = game.win_checker
        self.settings = game.settings
        self._update_screen = game._update_screen
        self.game_active = False
        self.selected_piece = None
        self.valid_moves = []
        self.current_turn = 'B'
        self.white_player = None
        self.black_player = None

        self.PLAYER_MAP = {
            'Human': None,
            'Minimax(cuts)': AiModelA_AlphaBeta,
            'Minimax(no cuts)': AiModelA_NoPruning,
            'Negamax(cuts)': NegamaxAlphaBeta,
            'Negamax(no cuts)': Negamax
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
        print(f"Moving piece from {from_pos} to {to_pos}")
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
        """Check if there is a winner."""
        if self.win_checker.check_win(self.current_turn):
            print(f"{self.current_turn} wins!")
            self.game_active = False
            self.reset_game()
        else:
            self.switch_turn()

    def reset_game(self):
        """Reset the game state and transition back to the main menu."""
        self.white_player = None
        self.black_player = None
        self.current_turn = 'B'
        self.game_active = False
        self.board.reset_board()
        self._update_screen()

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