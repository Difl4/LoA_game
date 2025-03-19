import sys
import pygame
from settings import Settings
from board import Board
from movement import LOAMovement
from translations import get_matrix_position
from copy import deepcopy


class LinesOfAction:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()
        self.clock = pygame.time.Clock()

        # Set up the screen.
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Lines Of Action")

        # Initialize the board and movement logic.
        self.board = Board(self)
        self.movement = LOAMovement(self.board.board_matrix)

        # Selected piece state
        self.selected_piece = None
        self.valid_moves = []

    def run_game(self):
        """Start the main loop for the game."""
        i = 0
        print(self.check_win(self.board.board_matrix))
        while (self.check_win(self.board.board_matrix) == 0):
        #while(True):
            #self._check_events()

            self._update_screen()

            #move = self.find_best_move(self.board.board_matrix, 3, i % 2 + 1)
            if(i % 2 == 0):
                _, move = self.minimax(self.board.board_matrix, 3, True, "B")
            else:
                _, move = self.minimax(self.board.board_matrix, 3, False, "W")

            self._move_piece(move[0], move[1])
            i += 1


            # self._update_screen()
            self.clock.tick(self.settings.fps)

    def _check_events(self):
        """Handle key and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_click(event.pos)

    def _handle_mouse_click(self, pos):
        """Handle selecting and moving pieces."""
        row, col = get_matrix_position(pos[0], pos[1], self.settings.square_size)
        piece = self.board.board_matrix[row][col]  # Get piece at clicked location

        if piece in ('W', 'B'):
            # Select a piece and show valid moves
            self.selected_piece = (row, col)
            self.valid_moves = self.movement.get_valid_moves(row, col)
        elif (row, col) in self.valid_moves:
            # Move the selected piece
            self._move_piece(self.selected_piece, (row, col))

    def _move_piece(self, from_pos, to_pos):
        """Move a piece from one position to another."""
        print(f"Moving piece {self.board.board_matrix[from_pos[0]][from_pos[1]]} from {from_pos} to {to_pos}")
        row_from, col_from = from_pos
        row_to, col_to = to_pos

        # Update board state
        self.board.board_matrix[row_to][col_to] = self.board.board_matrix[row_from][col_from]
        self.board.board_matrix[row_from][col_from] = None

        # Update the visual piece sprite
        for piece in self.board.pieces:
            if piece.rect.topleft == (col_from * self.settings.square_size, row_from * self.settings.square_size):
                piece.rect.topleft = (col_to * self.settings.square_size, row_to * self.settings.square_size)
                break

        # Deselect piece after move
        self.selected_piece = None
        self.valid_moves = []

    def _update_screen(self):
        """Update and redraw the game screen."""
        self.board.draw_board()
        self.board.draw_pieces()
        self.board.draw_valid_moves(self.valid_moves)
        pygame.display.flip()



    def evaluate(self, board, player):
        # Heuristic function for Lines of Action
        opponent = "W" if player == "B" else "B"
        
        # Example heuristic:
        # 1. Cluster cohesion: Minimize the maximum distance between pieces
        # 2. Control: More central positioning is better
        # 3. Piece count: More pieces are advantageous
        
        player_positions = [(r, c) for r in range(len(board)) for c in range(len(board[r])) if board[r][c] == player]
        opponent_positions = [(r, c) for r in range(len(board)) for c in range(len(board[r])) if board[r][c] == opponent]
        
        if not player_positions: return -1000  # Losing condition
        if not opponent_positions: return 1000  # Winning condition
        
        def cluster_distance(positions):
            return max(abs(r1 - r2) + abs(c1 - c2) for (r1, c1) in positions for (r2, c2) in positions)
        
        player_cluster = cluster_distance(player_positions)
        opponent_cluster = cluster_distance(opponent_positions)
        
        central_control = sum(abs(r - len(board) // 2) + abs(c - len(board[0]) // 2) for (r, c) in player_positions)
        
        return (len(player_positions) - len(opponent_positions)) * 10 + (opponent_cluster - player_cluster) * 5 - central_control


    def minimax(self, board, depth, maximizing_player, player):
        if depth == 0 or self.check_win(board) != 0:
            return self.evaluate(board, player), None

        valid_moves = self.movement.get_all_valid_moves(board, player)
        best_move = None

        if maximizing_player:
            max_eval = float('-inf')
            for piece in valid_moves:
                for move in piece[1:]:
                    new_board = deepcopy(board)
                    self._move_piece_on_board(new_board, piece[0], move)
                    eval, _ = self.minimax(new_board, depth - 1, False, player)
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
                    new_board = deepcopy(board)
                    self._move_piece_on_board(new_board, piece[0], move)
                    eval, _ = self.minimax(new_board, depth - 1, True, player)
                    if eval < min_eval:
                        min_eval = eval
                        best_move = (piece[0], move)
            # print(f"Min Eval: {min_eval} Best Move: {best_move}")
            # time.sleep(1000000)
            return min_eval, best_move

    def _move_piece_on_board(self, board, from_pos, to_pos):
        """Move a piece on the board without updating the visual representation."""
        row_from, col_from = from_pos
        row_to, col_to = to_pos
        board[row_to][col_to] = board[row_from][col_from]
        board[row_from][col_from] = None




    def check_win(self, board):
        def is_connected(board, piece):
            visited = set()
            directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
            
            def dfs(r, c):
                stack = [(r, c)]
                while stack:
                    row, col = stack.pop()
                    if (row, col) not in visited:
                        visited.add((row, col))
                        for dr, dc in directions:
                            nr, nc = row + dr, col + dc
                            if 0 <= nr < len(board) and 0 <= nc < len(board[0]) and board[nr][nc] == piece:
                                stack.append((nr, nc))
            
            # Find the first piece of the given type
            for r in range(len(board)):
                for c in range(len(board[r])):
                    if board[r][c] == piece:
                        dfs(r, c)
                        break
                if visited:
                    break
            
            # Check if all pieces of the given type are connected
            for r in range(len(board)):
                for c in range(len(board[r])):
                    if board[r][c] == piece and (r, c) not in visited:
                        return False
            return True

        w_count = sum(row.count("W") for row in board)
        b_count = sum(row.count("B") for row in board)

        w_connected = is_connected(board, "W")
        b_connected = is_connected(board, "B")

        #print(f"W: {w_count} B: {b_count} W Connected: {w_connected} B Connected: {b_connected}")

        if w_connected or b_count == 1:
            return 1  # White wins
        elif b_connected or w_count == 1:
            return 2  # Black wins
        else:
            return 0  # No winner yet