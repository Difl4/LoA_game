Hello! Welcome to our project, Lines of Action.

What is Lines of Action?

Lines of Action is a board game played on an 8x8 board, where 24 pieces: 12 black and 12 white, are placed on the outtermost square of the board, excluding the corners.
Pieces of the same colour are placed in oppsite directions of the board, so as to make a cornerless 6x6 square with parallel edges of the same colour.
The objective of the game is to have all the pieces of the same colour connect on the board. Two pieces being connected means that they are placed in adjacent squares, 
either vertically, horizontally or even diagonally. 

How do I play?

The first player to make a move is awlays the one who has the black pieces.
Whilst on either player's turn, any piece can be selected, with its next possible positions being defined by how many pieces, independent of their colour, are in the 
same row, column and diagonal, including the selected piece to move.
The number of pieces in the same row as the selected piece determine the number of squares it will have to jump, if played horizontally, either forward or backwards.
The same logic applies to vertical and diagonal moves.
However, there are some restrictions to movement. Upon the selection of a piece to move:
  - if there is another of the same colour already in the desired position, that move becomes illegal, having the piece to be moved elsewhere;
  - if there are any opposing pieces in the path to the desired position, that piece is now blocked to move in that direction, making that an illegal move as well.
Any piece will remain blocked in one or more directions as long as there are opposing pieces in the path from the current position to the desired one.

Upon making a move, if a piece is to land in a space occupied by an opposing piece, having respected the previously enumerated rules, it will "eat" the opposing piece,
removing it permanently from the game. But don´t be fooled! Less pieces means less connections to make!

If further clarification about the game is needed, you may check https://pt.wikipedia.org/wiki/Lines_of_Action.

Our coding project

In this folder you will find six other directories and two files.
The folder "ai" contains all the different playable artificial intelligences we developed, as well as the utility functions designed to guide their search. They are 
all structured as Python classes that follow a same interface described in "base_ai.py", which defines the attributes game, colour of current player, search depth 
and number of nodes explored whenever an AI player is initialized.
In this same directory there also are:
  - two files that operate the Monte Carlo Tree Search (MCTS), "MCTS.py" and "MCTS_node.py";
  - the file "minimax.py", that contains the "MinimaxAI" class, which operates according to "base_ai.py" and becomes a search algorithm model for all subsequent AI's, homing the utility functions that will guide the different searches. It is also in this module where the random player is implemented ; 
  - "minimax_no_pruning.py", "minimax_alpha_beta.py", "negamax_no_pruning.py" and "negamax_alpha_beta.py" which contain the playable AI's following these algorithms;
  - "enhanced_heuristic.py" and "proximity_to_center.py", two classes that operate the utility functions to be used by the MCTS.
  - the file "all_ai.py", a central module containing all AI implementations for the game, organized by algorithm type with clearly named variants.
    
The folder "config" contains the modules "settings.py", defining all the game's configurations, allowing for board size, colour and screen size total costumization, and
"translations.py", where data can be easily passed from matrix form to pixel form and vice-versa.

The directory "game" where the board and pieces objects are defined, as long with the movement, the pre-game initial screen and the termination state check conditions. It is also 
in "game" where the module "lines_of_action.py", that calls all other modules and operates the entirety of the game, is.

The folder "tests" homes a pytest module where case-specific game scenarios can be tested in multiple inquiries at the same time.

The directory "ui" contains the files "button.py" and "option_button.py", which configurate the intial screen´s selectable buttons for game customization.

The files "log.txt" where all played games are registered in text form, and "main.py", where the module that runs the game, "lines_of_action.py", is called and the pygame loop 
starts. In order to play the game, "main.py" is the only file that needs to be executed.

This project was developed by,
David Pereira
Miguel Ribeiro
Tiago Sousa
