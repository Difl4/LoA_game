class LOAUnionFind:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.parent = {}
        self.rank = {}

    def find(self, pos):
        # Path compression
        if self.parent[pos] != pos:
            self.parent[pos] = self.find(self.parent[pos])
        return self.parent[pos]

    def union(self, pos1, pos2):
        root1 = self.find(pos1)
        root2 = self.find(pos2)
        if root1 == root2:
            return
        if self.rank[root1] < self.rank[root2]:
            self.parent[root1] = root2
        else:
            self.parent[root2] = root1
            if self.rank[root1] == self.rank[root2]:
                self.rank[root1] += 1

    def initialize_from_board(self, board, player, directions):
        """
        board: dict of positions -> pieces
        player: 'W' or 'B'
        directions: list of (dr, dc)
        """
        self.parent.clear()
        self.rank.clear()
        
        player_positions = [pos for pos, piece in board.items() if piece == player]

        for pos in player_positions:
            self.parent[pos] = pos
            self.rank[pos] = 0

        for row, col in player_positions:
            for dr, dc in directions:
                nr, nc = row + dr, col + dc
                neighbor = (nr, nc)
                if neighbor in board and board[neighbor] == player:
                    self.union((row, col), neighbor)

    def is_fully_connected(self):
        """Check if all pieces share the same root."""
        roots = set(self.find(pos) for pos in self.parent)
        return len(roots) == 1