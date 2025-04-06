"""
Central module containing all AI implementations for the game.
Organized by algorithm type with clearly named variants.
"""

from ai.minimax_alpha_beta import AiModelA_AlphaBeta
from ai.negamax_alpha_beta import NegamaxAlphaBeta
from ai.MCTS import MonteCarloAI
from ai.connectivity_heuristic import ConnectivityFirstHeuristic
from ai.enhanced_heuristic import EnhancedHeuristic
from ai.proximity_to_center import ProximityToCenterHeuristic
from ai.minimax import MinimaxAI

# ======================
# Minimax Variants
# ======================

class MinimaxSimple(AiModelA_AlphaBeta):
    """Minimax with basic evaluation function."""
    def get_move(self, board_state):
        # Bind the evaluate method to this instance
        return super().get_move(board_state, lambda b, p: MinimaxAI.evaluate(self, b, p))

class MinimaxBetter(AiModelA_AlphaBeta):
    """Minimax with advanced evaluation function."""
    def get_move(self, board_state):
        # Bind the better_evaluate method to this instance
        return super().get_move(board_state, lambda b, p: MinimaxAI.better_evaluate(self, b, p))

class Random(AiModelA_AlphaBeta):
    """Minimax with random evaluation (for testing)."""
    def get_move(self, board_state):
        # Bind the random_evaluate method to this instance
        return super().get_move(board_state, lambda b, p: MinimaxAI.random_evaluate(self, b, p))

# ======================
# Negamax Variants
# ======================

class NegamaxSimple(NegamaxAlphaBeta):
    """Negamax with basic evaluation."""
    def get_move(self, board_state):
        return super().get_move(board_state, lambda b, p: MinimaxAI.evaluate(self, b, p))

class NegamaxBetter(NegamaxAlphaBeta):
    """Negamax with advanced evaluation."""
    def get_move(self, board_state):
        return super().get_move(board_state, lambda b, p: MinimaxAI.better_evaluate(self, b, p))

# ======================
# MCTS Variants
# ======================

class MCTSCenterMass(MonteCarloAI):
    """MCTS using center of mass heuristic."""
    def __init__(self, game, color, rollouts=1000):
        super().__init__(game, color, rollouts)
        self.heuristic = ProximityToCenterHeuristic(game.settings)
        self.search_depth = "N/A"  # MCTS doesn't use depth in the same way
        self.nodes_explored = self.rollouts  # Each rollout counts as a node

class MCTSEnhanced(MonteCarloAI):
    """MCTS using enhanced cluster heuristic."""
    def __init__(self, game, color, rollouts=1000):
        super().__init__(game, color, rollouts)
        self.heuristic = EnhancedHeuristic(game.settings)
        self.search_depth = "N/A"
        self.nodes_explored = self.rollouts

class MCTSConnectivity(MonteCarloAI):
    """MCTS focusing on piece connectivity."""
    def __init__(self, game, color, rollouts=1000):
        super().__init__(game, color, rollouts)
        self.heuristic = ConnectivityFirstHeuristic(game.settings)
        self.search_depth = "N/A"
        self.nodes_explored = self.rollouts

# Export all available AIs
__all__ = [
    'MinimaxSimple',
    'MinimaxBetter',
    'Random',
    'NegamaxSimple',
    'NegamaxBetter',
    'MCTSCenterMass',
    'MCTSEnhanced',
    'MCTSConnectivity'
]