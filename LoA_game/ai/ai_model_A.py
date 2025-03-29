from copy import deepcopy
import random

class AiModelA:
    def __init__(self, game, color):
        self.settings = game.settings
        self.board = game.board.board_dict
        self.win_checker = game.win_checker
        self.moves = game.movement
        self.color = color


    def dict_to_matrix(self, board_dict):
        # print("poi")
        # print(board_dict)
        board = [[None for _ in range(self.settings.cols)] for _ in range(self.settings.rows)]
        for i,u in board_dict: board[i][u] = board_dict[(i,u)]
        return board
    

    def matrix_to_dict(self, board):
        board_dict = {}
        for i in range(self.settings.rows):
            for u in range(self.settings.cols):
                if board[i][u] is not None:
                    board_dict[(i,u)] = board[i][u]
        return board_dict
    

    def random_evaluate(self, board, player):
        return random.randint(-1000, 1000)
    

    def evaluate(self, board, player):

        opponent = "W" if player == "B" else "B"
         
        player_positions = [(r, c) for r in range(len(board)) for c in range(len(board[r])) if board[r][c] == player]
        opponent_positions = [(r, c) for r in range(len(board)) for c in range(len(board[r])) if board[r][c] == opponent]

        dict_board = self.matrix_to_dict(board)
        if(self.win_checker.check_win(player, dict_board)): return 100000               # Player ganha
        if(self.win_checker.check_win(opponent, dict_board)): return -100000            # Opponent ganha

        def cluster_distance(positions):
            return max(abs(r1 - r2) + abs(c1 - c2) for (r1, c1) in positions for (r2, c2) in positions)
        
        player_cluster = cluster_distance(player_positions)       #Quando maior, maior a diferença de posição das duas peças mais afastadas
        opponent_cluster = cluster_distance(opponent_positions)

        central_control = sum(abs(r - len(board) // 2) + abs(c - len(board[0]) // 2) for (r, c) in player_positions)    #Quando maior, mais afastado do centro

        return (self.settings.rows / len(opponent_positions)) * -15 + (opponent_cluster - player_cluster) * 20 - central_control * 5

 
    def minimax(self, board, depth, maximizing_player, player):

        board1 = self.dict_to_matrix(board)


        if depth == 0 or self.win_checker.check_win("W", board) != 0 or self.win_checker.check_win("B", board) != 0:
            return self.evaluate(board1, player), None
 
        valid_moves = self.get_all_valid_moves(board1, player)
        best_move = None
 
        if maximizing_player:
            max_eval = float('-inf')
            for piece in valid_moves:
                for move in piece[1:]:
                    new_board = deepcopy(board1)
                    self._move_piece_on_board(new_board, piece[0], move)
                    eval, _ = self.minimax(self.matrix_to_dict(new_board), depth - 1, False, player)
                    if eval > max_eval:
                        max_eval = eval
                        best_move = (piece[0], move)
            # print(f"Max Eval: {max_eval} Best Move: {best_move}")
            # time.sleep(1000000)
            return max_eval, best_move
        else:
            min_eval = float('inf')
            opponent = "W" if player == "B" else "B"
            for piece in valid_moves:
                for move in piece[1:]:
                    new_board = deepcopy(board1)
                    self._move_piece_on_board(new_board, piece[0], move)
                    eval, _ = self.minimax(self.matrix_to_dict(new_board), depth - 1, True, player)
                    if eval < min_eval:
                        min_eval = eval
                        best_move = (piece[0], move)
            # print(f"Min Eval: {min_eval} Best Move: {best_move}")
            # time.sleep(1000000)
            return min_eval, best_move
        
    def get_all_valid_moves(self, board, player):
        cur_pos = [(r, c) for r in range(len(board)) for c in range(len(board[r])) if board[r][c] == player]
        all_valid_moves = []
        
        for pos in cur_pos:
            all_valid_moves += [[pos] + self.moves.get_valid_moves(pos[0], pos[1])]
 
        #print(all_valid_moves)
        return all_valid_moves
    
    def _move_piece_on_board(self, board, from_pos, to_pos):
        """Move a piece on the board without updating the visual representation."""
        row_from, col_from = from_pos
        row_to, col_to = to_pos
        board[row_to][col_to] = board[row_from][col_from]
        board[row_from][col_from] = None