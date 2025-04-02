# ai/base_ai.py

class BaseAI():
    """Interface all AIs must follow."""
    def __init__(self, game, color):
        self.game = game
        self.color = color
        self.search_depth = 3
        self.nodes_explored = 0
        self.last_eval = None

    def get_move(self, board_state) -> tuple[tuple[int, int], tuple[int, int]]:
        """Return the best move based on plain minimax."""
        _, best_move = self.minimax(board_state, depth=self.search_depth, maximizing_player=True, player=self.color)
        return best_move