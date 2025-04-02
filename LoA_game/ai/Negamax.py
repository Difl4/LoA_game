def negamax(self, board, depth, player):
    opponent = "W" if player == "B" else "B"
    board1 = self.dict_to_matrix(board)

    #Base case: return evaluation
    if depth == 0 or self.win_checker.check_win("W", board) != 0 or self.win_checker.check_win("B", board) != 0:
        return self.evaluate(board1, player), None

    valid_moves = self.get_all_valid_moves(board1, player)
    best_value = -1000000
    best_move = None

    for move in valid_moves:
        nega_val, _ = self.negamax(move, depth - 1, opponent)
        nega_val = -nega_val  #Value negation

        if nega_val > best_value:
            best_value = nega_val
            best_move = move

    return best_value, best_move