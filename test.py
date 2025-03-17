import pytest
from movement import LOAMovement

class TestLOAMovement:
    @pytest.fixture
    def custom_board(self):
        """Creates a custom board for testing."""
        board = [
            [None, None, 'W', 'B', 'W', 'W', None, None],
            [None, None, None, 'W', None, None, None, None],
            ['W', None, None, None, None, 'W', None, 'W'],
            [None, 'W', None, None, None, None, 'W', None],
            ['W', None, None, 'B', None, None, None, 'W'],
            [None, None, 'W', None, 'W', None, None, None],
            [None, None, None, 'W', None, 'W', None, None],
            [None, None, 'W', None, None, None, None, 'B'],
        ]
        return LOAMovement(board)

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
