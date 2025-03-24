class WinChecker:
    def __init__(self, game):

        self.directions = game.settings.directions
        self.board = game.board.board_dict

    def check_win(self, piece, board1 = None):
        """
        Checks if all pieces of the given type are connected.
        :param piece: 'W' or 'B'
        :return: True if all pieces of the given type are connected, False otherwise.
        """
        # Get all positions of the all the teams pieces
        # print("dsa")
        # print(board1)
        board1 = board1 or self.board # By doing this it sets the board1 to the first value it encounters

        positions = [pos for pos, p in board1.items() if p == piece]
        if not positions:
            return False  # No pieces to check

        visited = set()

        def dfs(pos):
            """Performs DFS to mark all reachable positions of the same color."""
            stack = [pos]
            while stack:
                row, col = stack.pop()
                if (row, col) in visited:
                    continue
                visited.add((row, col))

                # Check all 8 possible movement directions
                for dr, dc in self.directions:
                    nr, nc = row + dr, col + dc
                    if (nr, nc) in self.board and self.board[(nr, nc)] == piece:
                        stack.append((nr, nc))

        # Start DFS from the first found piece
        dfs(positions[0])

        # If all pieces of this type were visited, they are connected
        return len(visited) == len(positions)
