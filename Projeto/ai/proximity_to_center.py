class ProximityToCenterHeuristic:
    def __init__(self, settings):
        self.settings = settings
        self.center = (self.settings.rows // 2, self.settings.cols // 2)  # Middle of the board

    def evaluate(self, board, player):
        player_positions = [(row, col) for (row, col), piece in board.items() if piece == player]

        if not player_positions:  # In case there are no pieces for the player
            return 0

        # Calculate the center of mass for the player
        total_row = sum(r for r, c in player_positions)
        total_col = sum(c for r, c in player_positions)
        center_of_mass = (total_row / len(player_positions), total_col / len(player_positions))

        # Calculate the sum of distances of each piece to the center of mass
        total_distance = 0
        for r, c in player_positions:
            # Make sure the position is valid
            if (r, c) not in board:
                continue  # Skip invalid positions

            distance = abs(r - center_of_mass[0]) + abs(c - center_of_mass[1])
            total_distance += distance

        # Normalize the distance
        max_possible_distance = self.settings.rows + self.settings.cols - 2
        normalized_distance = total_distance / len(player_positions)

        # Higher proximity = better, so we want to return a higher value for closer proximity
        # The heuristic should favor lower distances, so we can subtract from a max possible score
        # Higher is better (minimizing distance is the goal).
        return 1 - (normalized_distance / max_possible_distance)
