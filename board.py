import pygame
from pieces import Piece

class Board:
    """A class to manage the game board."""

    def __init__(self, game):
        """
        Initialize the board.
        
        Args:
            game: The instance of the main game class (LinesOfAction).
        """
        self.screen = game.screen
        self.settings = game.settings

        # Initialize an 8x8 matrix representation (None means empty)
        self.board_matrix = [[None for _ in range(self.settings.cols)] for _ in range(self.settings.rows)]

        # Initialize a sprite group for pieces.
        self.pieces = pygame.sprite.Group()

        # Create the initial set of pieces.
        self._create_pieces()
        
        # Store the valid moves for the selected piece.
        self.valid_moves = []

    def _create_pieces(self):
        """Create the initial set of pieces."""
        # Create white pieces.
        for col in (0, self.settings.cols - 1):
            for row in range(1, self.settings.rows - 1):
                pos = (col * self.settings.square_size, row * self.settings.square_size)
                piece = Piece(self.settings, 'white', pos)
                self.pieces.add(piece)
                self.board_matrix[row][col] = 'W'  # 'W' represents a white piece in the matrix

        # Create black pieces.
        for row in (0, self.settings.rows - 1):
            for col in range(1, self.settings.cols - 1):
                pos = (col * self.settings.square_size, row * self.settings.square_size)
                piece = Piece(self.settings, 'black', pos)
                self.pieces.add(piece)
                self.board_matrix[row][col] = 'B'  # 'B' represents a black piece in the matrix
        print(self.board_matrix)

    def draw_board(self):
        """Draw the game board with alternating colors."""
        for row in range(self.settings.rows):
            for col in range(self.settings.cols):
                color = (
                    self.settings.light_color 
                    if (row + col) % 2 == 0 
                    else self.settings.dark_color
                )
                pygame.draw.rect(
                    self.screen, color,
                    (col * self.settings.square_size, row * self.settings.square_size, 
                     self.settings.square_size, self.settings.square_size)
                )

    def draw_pieces(self):
        """Draw all the pieces on the board."""
        self.pieces.draw(self.screen)


    def check_win(self):
        mcopy = self.board_matrix.copy()
        for i in range(len(mcopy)):
            mcopy.append(None)
            mcopy.insert(0, None)
        mcopy.insert(0, [None]*len(self.board_matrix)+1)
        mcopy.append([None]*len(self.board_matrix)+1)
        w_count = 0
        b_count = 0
        w_connected = True
        b_connected = True
        for row in range(1, len(self.board_matrix)-1):
            for col in range(1, len(self.board_matrix[row])-1):
                if(self.board_matrix[row][col] == "W"):
                    w_count += 1
                    if(self.board_matrix[row-1][col-1] == "W" or self.board_matrix[row-1][col] == "W" or self.board_matrix[row-1][col+1] == "W" or self.board_matrix[row][col-1] == "W" or self.board_matrix[row][col+1] == "W" or self.board_matrix[row+1][col-1] == "W" or self.board_matrix[row+1][col] == "W" or self.board_matrix[row][col+1] == "W"):
                        pass
                    else:
                        w_connected = False
                if(self.board_matrix[row][col] == "B"):
                    b_count += 1
                    if(self.board_matrix[row-1][col-1] == "B" or self.board_matrix[row-1][col] == "B" or self.board_matrix[row-1][col+1] == "B" or self.board_matrix[row][col-1] == "B" or self.board_matrix[row][col+1] == "B" or self.board_matrix[row+1][col-1] == "B" or self.board_matrix[row+1][col] == "B" or self.board_matrix[row][col+1] == "B"):
                        pass
                    else:
                        w_connected = False
        if(w_connected or b_count == 1): return 1
        elif(b_connected or w_count == 1): return 2
        else: return 0
    
# Tem outra alternativa que já confirmei que funciona no módulo dos testes para esta função. Vejam qual preferem. Aínda não testei esta.
    def possible_moves(self, row, col):                         # Returns a list of tuples of possible coordinates for a given coordinates' piece
        current_piece = self.board_matrix[row][col]
        total_moves = []
        count = 0

        if(current_piece == "W"):
            opposite_piece = "B"
        else:
            opposite_piece = "W"
        #Calculate Horizontally

        stop = False
        horizontal_moves = []
        for i in range(len(self.board_matrix[row])):
            if(self.board_matrix[row][i] == current_piece):
                if(stop == False):
                    horizontal_moves.append(0)
                count += 1
            elif(self.board_matrix[row][i] == opposite_piece):
                count += 1
                if(i < col):
                    horizontal_moves = [0]*i
                    horizontal_moves.append(1)
                else:
                    if(stop == False):
                        horizontal_moves.append(1)
                        horizontal_moves += [0]*(len(self.board_matrix[row])-i)
                        stop = True
            else:
                if(stop == False):
                    horizontal_moves.append(1)
        for i in range(len(horizontal_moves)):
            if(abs(i - col) == count and horizontal_moves[i] == 1):
                total_moves.append((row, i))

        #Calculate Vertically
        count = 0
        stop = False
        veritcal_moves = []
        for i in range(len(self.board_matrix)):
            if(self.board_matrix[i][col] == current_piece):
                if(stop == False):
                    veritcal_moves.append(0)
                count += 1
            elif(self.board_matrix[i][col] == opposite_piece):
                count += 1
                if(i < row):
                    veritcal_moves = [0]*i
                    veritcal_moves.append(1)
                else:
                    if(stop == False):
                        veritcal_moves.append(1)
                        veritcal_moves += [0]*(len(self.board_matrix[row])-i)
                        stop = True
            else:
                if(stop == False):
                    veritcal_moves.append(1)
        for i in range(len(veritcal_moves)):
            if(abs(i - row) == count and veritcal_moves[i] == 1):
                total_moves.append((i, col))

        #Calculate Diagonally (Down to the right)

        count = 0
        diag1_moves = []
        stop = False
        minn = min(row, col)
        sub = abs(row - col)
        if(minn == row):
            for i in range(sub, len(self.board_matrix[row])):
                if(self.board_matrix[i - sub][ i] == current_piece):
                    count += 1
                elif(self.board_matrix[i - sub][ i] == opposite_piece):
                    count += 1
                    if(i - sub < col):
                        if(stop == False):
                            diag1_moves = []
                            diag1_moves.append((i - sub, i))
                    else:
                        if(stop == False):
                            diag1_moves.append((i - sub, i))
                        stop = True
                else:
                    if(stop == False):
                        diag1_moves.append((i - sub, i))
        else:
            for i in range(sub, len(self.board_matrix[row])):
                if(self.board_matrix[i][ i - sub] == current_piece):
                    count += 1
                elif(self.board_matrix[i][ i - sub] == opposite_piece):
                    count += 1
                    if(i - sub < row):
                        if(stop == False):
                            diag1_moves = []
                            diag1_moves.append((i, i - sub))
                    else:
                        if(stop == False):
                            diag1_moves.append((i, i - sub))
                        stop = True
                else:
                    if(stop == False):
                        diag1_moves.append((i, i - sub))
        for (i, u) in diag1_moves:
            if(abs(i - row) == count):
                total_moves.append((i, u))


        #Calculate diagonally (Up to the right)

        count = 0
        diag2_moves = []
        stop = False
        sum = row + col
        tmp = len(self.board_matrix[row]) - 1
        if(len(self.board_matrix[row]) > sum):
            for i in range(sum+1):
                if(self.board_matrix[sum - i][i] == current_piece):
                    count += 1
                elif(self.board_matrix[sum-i][i] == opposite_piece):
                    count += 1
                    if(i < col):
                        diag2_moves = []
                        diag2_moves.append((sum-i, i))
                    else:
                        if(stop == False):
                            diag2_moves.append((sum-i, i))
                        stop = True
                else:
                    if(stop == False):
                        diag2_moves.append((sum-i, i))
            for (i, u) in diag2_moves:
                if(abs(i-row) == count):
                    total_moves.append((i, u))
        else:
            for i in range(7 - (sum % 8)):
                if(self.board_matrix[tmp - i][sum - tmp + i] == current_piece):
                    count += 1
                elif(self.board_matrix[tmp - i][sum - tmp + i] == opposite_piece):
                    count += 1
                    if(tmp - i > row):
                        diag2_moves = []
                        diag2_moves.append((tmp - i, sum - tmp + i))
                    else:
                        if(stop == False):
                            diag2_moves.append((tmp - i, sum - tmp + i))
                        stop = True
                else:
                    if(stop == False):
                        diag2_moves.append((tmp - i, sum - tmp + i))
            for (i, u) in diag2_moves:
                if(abs(i-row) == count):
                    total_moves.append((i, u))
        
        return total_moves
        
        def draw_valid_moves(self, valid_moves):
        """Draw circles on the board to show valid move locations."""
        for row, col in valid_moves:
            center_x = col * self.settings.square_size + self.settings.square_size // 2
            center_y = row * self.settings.square_size + self.settings.square_size // 2
            pygame.draw.circle(self.screen, (255, 0, 0), (center_x, center_y), 10)
