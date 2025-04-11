import math

class MCTSNode:
    def __init__(self, state, parent=None, move=None):
        self.state = state.copy()  # Ensure we always have a state
        self.parent = parent
        self.move = move
        self.children = []
        self.visits = 0
        self.wins = 0.0
        self.untried_moves = []
    
    def uct_score(self, total_simulations, exploration=1.4):
        if self.visits == 0:
            return float('inf')
        return (self.wins / self.visits) + exploration * math.sqrt(math.log(total_simulations + 1) / (self.visits + 1))

    def best_child(self, exploration=1.4):
        if not self.children:
            return None
        total_visits = sum(child.visits for child in self.children)
        return max(self.children, key=lambda c: c.uct_score(total_visits, exploration))

    def is_fully_expanded(self):
        return len(self.untried_moves) == 0