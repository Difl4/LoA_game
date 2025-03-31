# ai/base_ai.py
from abc import ABC, abstractmethod

class BaseAI(ABC):
    """Interface all AIs must follow."""
    def __init__(self, game, color):
        self.game = game
        self.color = color

    @abstractmethod
    def get_move(self, board_state) -> tuple[tuple[int, int], tuple[int, int]]:
        """Return (from_pos, to_pos) for the best move."""
        pass