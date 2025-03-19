
class LOAMovement:
    def __init__(self, game):

        self.board = game.board.board_dict
        self.settings = game.settings

        self.directions = [
            (1, 0), (-1, 0),  # Horizontal (Right, Left)
            (0, 1), (0, -1),  # Vertical (Down, Up)
            (1, 1), (-1, -1), # Diagonal (Bottom-right, Top-left)
            (1, -1), (-1, 1)  # Diagonal (Bottom-left, Top-right)
        ]
    
    def count_pieces(self, row, col, d_row, d_col):
        """Count all pieces in a row, column, or diagonal using dictionary."""
        count = 1

        # Check forward direction (d_row, d_col)
        r, c = row + d_row, col + d_col
        while 0 <= r < self.settings.rows and 0 <= c < self.settings.cols:
            try:
                if (r, c) in self.board:
                    count += 1
            except KeyError:
                pass
            r += d_row
            c += d_col

        # Check backward direction (-d_row, -d_col)
        r, c = row - d_row, col - d_col
        while 0 <= r < self.settings.rows and 0 <= c < self.settings.cols:
            try:
                if (r, c) in self.board:  # If there's a piece
                    count += 1
            except KeyError:
                pass
            r -= d_row
            c -= d_col

        return count

    
    def get_valid_moves(self, row, col):
        """Return a list of all valid moves for a piece at (row, col)."""
        valid_moves = []

        for d_row, d_col in self.directions:
            move_distance = self.count_pieces(row, col, d_row, d_col)
            r, c = row + d_row * move_distance, col + d_col * move_distance

            # Ensure the move is within bounds
            if 0 <= r < self.settings.rows and 0 <= c < self.settings.cols:
                # Ensure the path is clear
                if self.is_path_clear(row, col, r, c):
                    valid_moves.append((r, c))
        
        return valid_moves
    
    def is_path_clear(self, row1, col1, row2, col2):
        """Check if the path between (row1, col1) and (row2, col2) is clear."""
        d_row = (row2 - row1) // max(1, abs(row2 - row1))  # Normalize direction (-1, 0, or 1)
        d_col = (col2 - col1) // max(1, abs(col2 - col1))  # Normalize direction (-1, 0, or 1)

        r, c = row1, col1
        
        while (r, c) != (row2, col2):
            try:
                if (r, c) in self.board:  # Obstacle in the way
                    if self.board[(r, c)] != self.board[(row1, col1)]:  # Verifies if it's an opponent
                        return False
            except KeyError:
                pass
            r += d_row
            c += d_col
        try:
            if (r, c) not in self.board:
                return True  # Empty spot, path is clear
            elif self.board[(r, c)] == self.board[(row1, col1)]:
                return False  # Piece of the same player, path blocked
            else:
                return True  # Opponent's piece, path is valid
        except KeyError:
            return True  # Empty destination, path is clear


