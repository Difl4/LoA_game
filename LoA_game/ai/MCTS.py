from ai.base_ai import BaseAI
from ai.MCTS_node import MCTSNode

class MonteCarloAI(BaseAI):
    def __init__(self, game, color):
        super().__init__(game, color)
        self.win_checker = game.win_checker
        self.heuristic = None  # To be set by subclasses
        self.moves = game.movement
        self.nodes_explored = 0  # Initialize counter
        
    def get_move(self, board_state):
        self.nodes_explored = 0
        if not board_state:
            return None
            
        root = MCTSNode(board_state.copy())
        root.untried_moves = list(self._get_valid_moves(board_state))

        num_rollouts = len(root.untried_moves)
        
        if not root.untried_moves and not root.children:
            return None
        
        for _ in range(num_rollouts):
            self.nodes_explored += 1
            node = self._tree_policy(root)
            if node is None:
                continue
                
            result = self._simulate(node.state.copy())
            self._backpropagate(node, result)
        #for child in root.children:
        #    print(f"Move: {child.move}, Visits: {child.visits}, Wins: {child.wins}, Win rate: {child.wins / (child.visits + 1e-6)}")

        return self._best_move(root)

    def _tree_policy(self, node):
        while node is not None and not self._is_terminal(node):
            if not node.is_fully_expanded():
                return self._expand(node)
            else:
                node = node.best_child()
        return node

    def _expand(self, node):
        if not node.untried_moves:
            return node
        move = node.untried_moves.pop()
        new_state = node.state.copy()
        self._apply_move(new_state, move)
        child = MCTSNode(new_state, node, move)
        child.untried_moves = list(self._get_valid_moves(new_state))
        node.children.append(child)
        #print(f"Expanded move: {move}")
        return child

    def _simulate(self, state):
        if not state:
            return 0.0
            
        if self.win_checker.check_win(self.color, state):
            return 1.0
        if self.win_checker.check_win(self._opponent(self.color), state):
            return 0.0
        return self.heuristic.evaluate(state, self.color)

    def _backpropagate(self, node, result):
        while node is not None:
            node.visits += 1
            node.wins += result
            result = 1 - result  # Alternate perspective
            node = node.parent

    def _best_move(self, root):
        if not root or not root.children:
            return None
            
        # Robust selection considering both visits and win rate
        def score(child):
            visit_weight = child.visits
            win_rate = child.wins / (child.visits + 1e-6)
            return visit_weight + win_rate
            
        best_child = max(root.children, key=score)
        return best_child.move if best_child else None

    def _is_terminal(self, node):
        if node is None or not hasattr(node, 'state'):
            return True
        return (self.win_checker.check_win(self.color, node.state) or
                self.win_checker.check_win(self._opponent(self.color), node.state))

    def _get_valid_moves(self, board):
        if not board:
            return []
            
        for pos in board:
            if board[pos] == self.color:
                for move in self.moves.get_valid_moves(pos[0], pos[1]):
                    yield (pos, move)

    def _apply_move(self, board, move):
        if not board or not move:
            return
            
        from_pos, to_pos = move
        if from_pos in board:
            board[to_pos] = board[from_pos]
            del board[from_pos]

    def _opponent(self, color):
        return 'W' if color == 'B' else 'B'