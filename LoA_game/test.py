import pytest
from movement import LOAMovement

class MockSettings:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.directions = self.directions = [
            (1, 0), (-1, 0),  # Horizontal (Right, Left)
            (0, 1), (0, -1),  # Vertical (Down, Up)
            (1, 1), (-1, -1), # Diagonal (Bottom-right, Top-left)
            (1, -1), (-1, 1)  # Diagonal (Bottom-left, Top-right)
        ]

class MockBoard:
    def __init__(self, board_dict):
        self.board_dict = board_dict

class MockGame:
    def __init__(self, board_dict, rows, cols):
        self.board = MockBoard(board_dict)
        self.settings = MockSettings(rows, cols)

class TestLOAMovement:
    @pytest.fixture
    def custom_board(self):
        """Creates a custom board for testing."""
        board_dict = {
            (0, 2): 'W', (0, 3): 'B', (0, 4): 'W', (0, 5): 'W',
            (1, 3): 'W',
            (2, 0): 'W', (2, 5): 'W', (2, 7): 'W',
            (3, 1): 'W', (3, 6): 'W',
            (4, 0): 'W', (4, 3): 'B', (4, 7): 'W',
            (5, 2): 'W', (5, 4): 'W',
            (6, 3): 'W', (6, 5): 'W',
            (7, 2): 'W', (7, 7): 'B',
        }
        rows = 8
        cols = 8
        game = MockGame(board_dict, rows, cols)
        return LOAMovement(game)

    def test_count_pieces(self, custom_board):
        sample = custom_board
        assert sample.count_pieces(2, 0, 1, 0) == 2  # Check vertical count
        assert sample.count_pieces(4, 3, 0, 1) == 3  # Check horizontal count
        assert sample.count_pieces(3, 1, -1, 1) == 4  # Check diagonal count

    def test_path_clear(self, custom_board):
        sample = custom_board
        assert sample.is_path_clear(2, 0, 4, 0) is False  # Path should be blocked
        assert sample.is_path_clear(3, 1, 5, 1) is True  # Path should be clear

    def test_valid_moves(self, custom_board):
        sample = custom_board
        # Piece in the middle of the board
        assert set(sample.get_valid_moves(4, 3)) == {(4, 0), (4, 6), (1, 0)}

        # Piece in the corner
        assert set(sample.get_valid_moves(7, 7)) == {(4, 7), (7, 5), (6, 6)}

        # Piece surrounded by others
        assert set(sample.get_valid_moves(0, 3)) == {(1, 2)}

if __name__ == "__main__":
    pytest.main()
