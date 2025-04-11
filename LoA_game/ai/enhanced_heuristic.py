class EnhancedHeuristic:
    def __init__(self, settings):
        self.settings = settings
        self.center = (settings.rows // 2, settings.cols // 2)
        self.directions = settings.directions
    
    def evaluate(self, board, player):
        opponent = 'W' if player == 'B' else 'B'
        player_pieces = [pos for pos, p in board.items() if p == player]
        opponent_pieces = [pos for pos, p in board.items() if p == opponent]
        
        if not player_pieces:
            return 0.0

        # 1. Connectivity score (50% weight)
        connectivity = self._connectivity_score(board, player, player_pieces)
        
        # 2. Opponent connectivity (20% weight, inverted)
        opponent_connectivity = self._connectivity_score(board, opponent, opponent_pieces)
        
        # 3. Center control (20% weight)
        center_control = self._center_control_score(player_pieces)
        
        # 4. Mobility (10% weight)
        mobility = self._mobility_score(board, player)
        
        # Combined evaluation
        return (0.5 * connectivity + 
                0.2 * (1 - opponent_connectivity) + 
                0.2 * center_control + 
                0.1 * mobility)

    def _connectivity_score(self, board, player, pieces):
        """Calculate connectivity score (0-1)"""
        if len(pieces) == 1:
            return 1  # Single piece case
            
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

    def _center_control_score(self, pieces):
        """Calculate center control score (0-1)"""
        if not pieces:
            return 0.0
            
        total_distance = 0
        max_possible = self.settings.rows + self.settings.cols
        
        for (r, c) in pieces:
            # Manhattan distance to center
            distance = abs(r - self.center[0]) + abs(c - self.center[1])
            normalized = 1 - (distance / max_possible)
            total_distance += normalized
            
        return total_distance / len(pieces)

    def _mobility_score(self, board, player):
        """Calculate mobility score (0-1)"""
        total_moves = 0
        max_possible = 0
        
        for pos in board:
            if board[pos] == player:
                max_possible += 8
                total_moves += len(list(self._get_valid_moves_single(pos, board)))
        
        if max_possible == 0:
            return 0.0
            
        return total_moves / max_possible

    def _get_valid_moves_single(self, pos, board):
        """Helper to get moves for single piece"""
        row, col = pos
        for dr, dc in self.directions:
            new_r, new_c = row + dr, col + dc
            if 0 <= new_r < self.settings.rows and 0 <= new_c < self.settings.cols:
                yield (new_r, new_c)
