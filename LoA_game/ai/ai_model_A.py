from copy import deepcopy
from ai.base_ai import BaseAI

class AiModelA(BaseAI):
    def __init__(self, game, color):
        super().__init__(game, color)
        self.settings = game.settings
        self.board = game.board.board_dict
        self.win_checker = game.win_checker
        self.moves = game.movement

    def evaluate(self, board, player):
        opponent = "W" if player == "B" else "B"
        
        player_positions = [pos for pos, piece in board.items() if piece == player]
        opponent_positions = [pos for pos, piece in board.items() if piece == opponent]
        
        if self.win_checker.check_win(player, board):
            return 100000  # Player wins
        if self.win_checker.check_win(opponent, board):
            return -100000  # Opponent wins

        def cluster_distance(positions):
            return max(abs(r1 - r2) + abs(c1 - c2) for (r1, c1) in positions for (r2, c2) in positions)
        
        player_cluster = cluster_distance(player_positions)
        opponent_cluster = cluster_distance(opponent_positions)
        central_control = sum(abs(r - self.settings.rows // 2) + abs(c - self.settings.cols // 2) for (r, c) in player_positions)
        
        return (self.settings.rows / max(1, len(opponent_positions))) * -15 + (opponent_cluster - player_cluster) * 20 - central_control * 5

    def minimax(self, board, depth, maximizing_player, player, alpha=float('-inf'), beta=float('inf')):
        if depth == 0 or self.win_checker.check_win("W", board) or self.win_checker.check_win("B", board):
            return self.evaluate(board, player), None
        
        valid_moves = self.get_all_valid_moves(board, player)
        best_move = None
        opponent = "W" if player == "B" else "B"
        
        if maximizing_player:
            max_eval = float('-inf')
            for piece, moves in valid_moves.items():
                for move in moves:
                    new_board = deepcopy(board)
                    self._move_piece_on_board(new_board, piece, move)
                    eval, _ = self.minimax(new_board, depth - 1, False, player, alpha, beta)
                    if eval > max_eval:
                        max_eval = eval
                        best_move = (piece, move)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for piece, moves in valid_moves.items():
                for move in moves:
                    new_board = deepcopy(board)
                    self._move_piece_on_board(new_board, piece, move)
                    eval, _ = self.minimax(new_board, depth - 1, True, player, alpha, beta)
                    if eval < min_eval:
                        min_eval = eval
                        best_move = (piece, move)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            return min_eval, best_move

    def get_all_valid_moves(self, board, player):
        valid_moves = {}
        for pos in board:
            if board[pos] == player:
                valid_moves[pos] = self.moves.get_valid_moves(pos[0], pos[1])
        return valid_moves
    
    def _move_piece_on_board(self, board, from_pos, to_pos):
        board[to_pos] = board[from_pos]
        del board[from_pos]
    
    def get_move(self, board_state) -> tuple[tuple[int, int], tuple[int, int]]:
        _, best_move = self.minimax(board_state, depth=3, maximizing_player=True, player=self.color)
        return best_move