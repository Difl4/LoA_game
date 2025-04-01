class BaseAI():
    """Interface all AIs must follow."""
    def __init__(self, game, color):
        self.game = game
        self.color = color
        self.search_depth = 3
        self.nodes_explored = 0