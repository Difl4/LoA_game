from ai.minimax import MinimaxAI

class NegamaxAlphaBeta(MinimaxAI):
    def negamax(self, board, depth, player, evalfunction, alpha=float('-inf'), beta=float('inf')):
        self.nodes_explored += 1
        """Negamax with Alpha-Beta Pruning."""
        opponent = "W" if player == "B" else "B"

        if depth == 0 or self.win_checker.check_win(player, board) or self.win_checker.check_win(opponent, board):
            return evalfunction(board, player), None

        valid_moves = self.get_all_valid_moves(board, player)
        best_value = float('-inf')
        best_move = None

        for piece, moves in valid_moves.items():
            for move in moves:
                new_board = board.copy()
                self._move_piece_on_board(new_board, piece, move)

                nega_val, _ = self.negamax(new_board, depth - 1, opponent, evalfunction, -beta, -alpha)
                nega_val = -nega_val

                if nega_val > best_value:
                    best_value = nega_val
                    best_move = (piece, move)

                alpha = max(alpha, best_value)
                if alpha >= beta:
                    break

        return best_value, best_move
    
    def get_move(self, board_state, evalfunction) -> tuple[tuple[int, int], tuple[int, int]]:
        """Return the best move based on negamax with alpha-beta pruning."""
        _, best_move = self.negamax(board_state, depth=self.search_depth, player=self.color, evalfunction=evalfunction)
        return best_move
