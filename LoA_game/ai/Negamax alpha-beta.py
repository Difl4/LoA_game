def negamax(self, board, depth, player, alpha, beta):
    opponent = "W" if player == "B" else "B"
    board1 = self.dict_to_matrix(board)

    if depth == 0 or self.win_checker.check_win("W", board) != 0 or self.win_checker.check_win("B", board) != 0:
        return self.evaluate(board1, player), None

    valid_moves = self.get_all_valid_moves(board1, player)
    best_value = -float("inf")
    best_move = None

    for move in valid_moves:
        new_board = self.make_move(board1, move, player)
        nega_val, _ = self.negamax(new_board, depth - 1, opponent, -beta, -alpha)
        nega_val = -nega_val

        if nega_val > best_value:
            best_value = nega_val
            best_move = move

        alpha = max(alpha, best_value)  # Update alpha

        if alpha >= beta:  # Cutting condition
            break  # Skip other moves

    return best_value, best_move
