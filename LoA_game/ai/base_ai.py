# ai/base_ai.py

class BaseAI():
    """Interface all AIs must follow."""
    def __init__(self, game, color):
        self.game = game
        self.color = color

    def get_move(self, board_state) -> tuple[tuple[int, int], tuple[int, int]]:  # ✅ Implemented correctly
        """Return the best move based on plain minimax."""
        _, best_move = self.minimax(board_state, depth=3, maximizing_player=True, player=self.color)
        return best_move