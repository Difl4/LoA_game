class ConnectivityFirstHeuristic:
    def __init__(self, settings):
        self.settings = settings
        self.center = (settings.rows // 2, settings.cols // 2)
        self.directions = settings.directions
    
    def evaluate(self, board, player):
        pieces = [pos for pos, p in board.items() if p == player]
        if not pieces:
            return 0.0
        
        # Primary: Connectivity score (0-1)
        connectivity = self._connectivity_score(board, player, pieces)
        
        # Secondary: Center proximity for disconnected pieces
        if connectivity < 1.0:
            cohesion = self._cohesion_score(pieces)
            return 0.8 * connectivity + 0.2 * cohesion
        return 1.0

    def _connectivity_score(self, board, player, pieces):
        visited = set()
        largest_cluster = 0
        
        for piece in pieces:
            if piece not in visited:
                cluster_size = self._find_cluster_size(board, player, piece, visited)
                largest_cluster = max(largest_cluster, cluster_size)
        
        return largest_cluster / len(pieces)

    def _find_cluster_size(self, board, player, start_pos, visited):
        stack = [start_pos]
        cluster_size = 0
        
        while stack:
            pos = stack.pop()
            if pos in visited:
                continue
                
            visited.add(pos)
            cluster_size += 1
            
            for dr, dc in self.directions:
                neighbor = (pos[0] + dr, pos[1] + dc)
                if neighbor in board and board[neighbor] == player:
                    stack.append(neighbor)
        
        return cluster_size

    def _cohesion_score(self, pieces):
        total_distance = sum(abs(r-self.center[0]) + abs(c-self.center[1]) 
                         for r, c in pieces)
        max_distance = self.settings.rows + self.settings.cols
        return 1 - (total_distance / (len(pieces) * max_distance))