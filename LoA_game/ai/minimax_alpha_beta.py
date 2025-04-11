from ai.minimax import MinimaxAI

class AiModelA_AlphaBeta(MinimaxAI):
    def minimax(self, board, depth, maximizing_player, player, evalfunction, alpha=float('-inf'), beta=float('inf')):
        self.nodes_explored += 1
        if depth == 0 or self.win_checker.check_win("W", board) or self.win_checker.check_win("B", board):
            return evalfunction(board, player), None

        valid_moves = self.get_all_valid_moves(board, player)
        best_move = None

        if maximizing_player:
            max_eval = float('-inf')
            for piece, moves in valid_moves.items():
                for move in moves:
                    new_board = board.copy()
                    self._move_piece_on_board(new_board, piece, move)
                    eval, _ = self.minimax(new_board, depth - 1, False, player, evalfunction, alpha, beta)
                    if eval > max_eval:
                        max_eval = eval
                        best_move = (piece, move)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break  # Alpha-beta cutoff
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for piece, moves in valid_moves.items():
                for move in moves:
                    new_board = board.copy()
                    self._move_piece_on_board(new_board, piece, move)
                    eval, _ = self.minimax(new_board, depth - 1, True, player, evalfunction, alpha, beta)
                    if eval < min_eval:
                        min_eval = eval
                        best_move = (piece, move)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break  # Alpha-beta cutoff
            return min_eval, best_move
        
    def get_move(self, board_state, evalfunction) -> tuple[tuple[int, int], tuple[int, int]]:
        """Return the best move based on plain minimax."""
        _, best_move = self.minimax(board_state, depth=self.search_depth, maximizing_player=True, player=self.color, evalfunction=evalfunction)
        return best_move