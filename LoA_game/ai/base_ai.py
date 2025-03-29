# ai/base_ai.py
# esta clase não fui eu que criei foi totalmente o chat gpt.
# A ideia é estruturar as futuras IAs com base nesta porque todas vão ter algo em comum.
# Utilizamos "inheritance" desta classe e depois também é útil para verificar se se trata de uma IA porque basta usar o método isinstance() com esta classe
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