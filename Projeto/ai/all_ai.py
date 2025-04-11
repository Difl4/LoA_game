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
        def evaluate(board, player):
            return MinimaxAI.evaluate(self, board, player)
        
        return super().get_move(board_state, evaluate)

class MinimaxBetter(AiModelA_AlphaBeta):
    """Minimax with advanced evaluation function."""
    def get_move(self, board_state):
        def evaluate(board, player):
            return MinimaxAI.better_evaluate(self, board, player)
        
        return super().get_move(board_state, evaluate)

class Random(AiModelA_AlphaBeta):
    """Minimax with random evaluation (for testing)."""
    def get_move(self, board_state):
        def evaluate(board, player):
            return MinimaxAI.random_evaluate(self, board, player)
        
        return super().get_move(board_state, evaluate)

# ======================
# Negamax Variants
# ======================

class NegamaxSimple(NegamaxAlphaBeta):
    """Negamax with basic evaluation."""
    def get_move(self, board_state):
        def evaluate(board, player):
            return MinimaxAI.evaluate(self, board, player)
        
        return super().get_move(board_state, evaluate)

class NegamaxBetter(NegamaxAlphaBeta):
    """Negamax with advanced evaluation."""
    def get_move(self, board_state):
        def evaluate(board, player):
            return MinimaxAI.better_evaluate(self, board, player)
        
        return super().get_move(board_state, evaluate)

# ======================
# MCTS Variants
# ======================

class MCTSCenterMass(MonteCarloAI):
    """MCTS using center of mass heuristic."""
    def __init__(self, game, color):
        super().__init__(game, color)
        self.heuristic = ProximityToCenterHeuristic(game.settings)
        self.search_depth = "N/A"  # MCTS doesn't use depth in the same way

class MCTSEnhanced(MonteCarloAI):
    """MCTS using enhanced cluster heuristic."""
    def __init__(self, game, color):
        super().__init__(game, color)
        self.heuristic = EnhancedHeuristic(game.settings)
        self.search_depth = "N/A"

class MCTSConnectivity(MonteCarloAI):
    """MCTS focusing on piece connectivity."""
    def __init__(self, game, color):
        super().__init__(game, color)
        self.heuristic = ConnectivityFirstHeuristic(game.settings)
        self.search_depth = "N/A"

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
