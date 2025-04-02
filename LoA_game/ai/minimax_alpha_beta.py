from copy import deepcopy
from ai.minimax import MinimaxAI

class AiModelA_AlphaBeta(MinimaxAI):
    #def __init__(self, game, color):
    #    super().__init__(game, color)

    def minimax(self, board, depth, maximizing_player, player, alpha=float('-inf'), beta=float('inf')):
        if depth == 0 or self.win_checker.check_win("W", board) or self.win_checker.check_win("B", board):
            return self.better_evaluate(board, player), None

        valid_moves = self.get_all_valid_moves(board, player)
        best_move = None

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
                        break  # Alpha-beta cutoff
            return max_eval, best_move
        else:
            min_eval = float('inf')
            opponent = "W" if player == "B" else "B"
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
                        break  # Alpha-beta cutoff
            return min_eval, best_move
