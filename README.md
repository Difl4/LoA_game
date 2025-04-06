Hello! Welcome to our project, Lines of Action.

What is Lines of Action?

Lines of Action is a board game played on an 8x8 board, where 24 pieces: 12 black and 12 white, are placed on the outtermost square of the board, excluding the corners.
Pieces of the same colour are placed in oppsite directions of the board, therefore, making a cornerless 6x6 square with parallel edges of the same colour.
The objective of the game is to have all the pieces of the same colour connect on the board. Two pieces being connected means that they are placed in adjacent squares, 
either vertically, horizontally or even diagonally. 

How do I play?

The first player to make a move is awlays the one who has the black pieces.
Whilst on either player's turn, any piece can be selected, with its next possible positions being defined by how many pieces, independent of their colour, are int the 
same row, collumn and diagonal, including the selected piece to move.
The number of pieces in the same row as the selected piece determine the number os squares it will have to jump, if played horizontally, either forward or backwards.
The same logic applies to vertical and diagonal moves.
However, there are some restrictions to movement. Upon the selection of a piece to move:
  - if there is another of the same colour already in the desired position, that move becomes illegal, having the piece to be moved elsewhere;
  - if there are any opposing pieces in the path to the desired position, that piece is now blocked to move in that direction, making that an illegal move as well.
Any piece will remain blocked in one or more directions as long as there are opposing pieces in the path from the current position to the desired one.
Upon making a move, if a piece is to land in a space occupied by an opposing piece, having respected the previously enumerated rules, it will "eat" the opposing piece,
removing it permanently from the game. But don´t be fooled! Less pieces means less connections to make!

Our coding project

In this folder you will find six other directories and four files.
The folder "ai" contains all the different playable artificial intelligences we developed, as well as the utility function designed to guide their search. They are 
all structured as Python classes, that follow a same interface described in "base_ai", which defines the attributes game, colour of current player, search depth 
and number of nodes explored whenever an AI player is initialized.
In this same directory there also are:
  - two files that operate the Monte Carlo Tree Search (MCTS), "MCTS" and "MCTS_node";
  - the file "minimax", that contains the "MinimaxAI" class, which operates according to "base_ai" and becomes a search algorithm model for all subsequent AI's, also
  - homing the utility functions that will guide the different searches; 
  - "minimax_no_pruning", "minimax_alpha_beta", "negamax_no_pruning" and "negamax_alpha_beta" which contain the playable AI's following these algorithms;
  - "enhanced_heuristic", "proximity_to_center" and "union_find", three classes that operate the utility functions to be used by the MCTS.
    
The folder "config" contains the modules "settings", defining all the game's configurations, allowing for board size, colour and screen size total costumization, and
"translations", where data can be easily passed from matrix form to pixel form and vice-versa.

The directory "game" where 



