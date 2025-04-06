import random
from ai.base_ai import BaseAI

class MinimaxAI(BaseAI):
    def __init__(self, game, color):
        super().__init__(game, color)
        self.settings = game.settings
        self.board = game.board.board_dict
        self.win_checker = game.win_checker
        self.moves = game.movement

    def get_all_valid_moves(self, board, player):
        valid_moves = {}
        for pos in board:
            if board[pos] == player:
                valid_moves[pos] = self.moves.get_valid_moves(pos[0], pos[1])
        return valid_moves

    def random_evaluate(self, board, player):
        return random.randint(-100000, 100000)

    def evaluate(self, board, player):
        opponent = "W" if player == "B" else "B"
        
        player_positions = [pos for pos, piece in board.items() if piece == player]
        opponent_positions = [pos for pos, piece in board.items() if piece == opponent]
        
        if self.win_checker.check_win(player, board):
            return 100000  # Player wins
        if self.win_checker.check_win(opponent, board):
            return -100000  # Opponent wins

        def cluster_distance(positions):
            if len(positions) < 2:
                return 0  # No distance to measure
            return max(abs(r1 - r2) + abs(c1 - c2) for (r1, c1) in positions for (r2, c2) in positions)
        
        player_cluster = cluster_distance(player_positions)  # Distance between the furthest pieces
        opponent_cluster = cluster_distance(opponent_positions)
        central_control = sum(abs(r - self.settings.rows // 2) + abs(c - self.settings.cols // 2) for (r, c) in player_positions)    

        return (self.settings.rows / max(1, len(opponent_positions))) * -15 + (opponent_cluster - player_cluster) * 20 - central_control * 5

    def better_evaluate(self, board, player):
        opponent = "W" if player == "B" else "B"

        # Use dictionaries for fast lookups
        player_positions = {pos: True for pos, piece in board.items() if piece == player}
        opponent_positions = {pos: True for pos, piece in board.items() if piece == opponent}

        def analyze_clusters(board, player_positions):
            visited = set()
            clusters = []

            #cluster_id = 0  # Unique ID for each cluster

            for position in player_positions:
                if position not in visited:
                    stack = [position]
                    cluster_size = 0

                    while stack:
                        row, col = stack.pop()
                        if (row, col) in visited:
                            continue

                        visited.add((row, col))
                        cluster_size += 1

                        # Check all 8 directions for connected pieces
                        for dr, dc in self.settings.directions:
                            nr, nc = row + dr, col + dc
                            if (nr, nc) in player_positions and (nr, nc) not in visited:
                                stack.append((nr, nc))

                    clusters.append(cluster_size)
                    #cluster_id += 1

            return len(clusters), clusters

        np_clusters, p_clusters = analyze_clusters(board, player_positions)
        no_clusters, o_clusters = analyze_clusters(board, opponent_positions)

        if np_clusters == 1:
            return 100000  # Player wins
        if no_clusters == 1:
            return -100000  # Opponent wins

        cluster_score = 0
        cluster_score += sum([cluster ** 2 for cluster in p_clusters]) 
        cluster_score *= no_clusters / (np_clusters**2)

        # Central control metric
        central_control = sum(abs(r - self.settings.rows // 2) + abs(c - self.settings.cols // 2) for (r, c) in player_positions)

        player_moves = self.get_all_valid_moves(board, player)
        nplayer_moves = sum((len(moves)-1) for moves in player_moves.values())

        #return cluster_score * 2 + (len(opponent_positions) * 3) - central_control * 25
        return cluster_score * 3 + (len(opponent_positions) * 5) - central_control * 15 + nplayer_moves * 10 

    def _move_piece_on_board(self, board, from_pos, to_pos):
        """Move a piece on the board without updating the visual representation."""
        board[to_pos] = board[from_pos]
        del board[from_pos]
