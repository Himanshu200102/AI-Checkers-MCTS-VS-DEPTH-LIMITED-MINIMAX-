import math
import random

class Node:
    def __init__(self, state, parent=None, move=None):
        self.state = state
        self.parent = parent
        self.move = move
        self.children = []
        self.visits = 0
        self.wins = 0

    def uct(self, exploration=1.41):
        if self.visits == 0:
            return float('inf')
        return self.wins / self.visits + exploration * math.sqrt(math.log(self.parent.visits) / self.visits)

class MCTSPlayer:
    def __init__(self, iterations):
        self.iterations = iterations

    def select_node(self, node):
        best_child = max(node.children, key=lambda child: child.uct())
        return best_child

    def expand_node(self, node):
        if node.state.is_terminal():
            return

        legal_moves = node.state.legal_moves(node.state.turn)

        for move in legal_moves:
            new_state = node.state.copy()
            new_state.move_piece(move)
            new_node = Node(state=new_state, parent=node, move=move)
            node.children.append(new_node)

    def simulate(self, board):
        current_board = board.copy()
        while not current_board.is_terminal():
            moves = current_board.legal_moves(current_board.turn)
            if moves:
                move = random.choice(moves)
                current_board.move_piece(move)
            else:
                break

        result = current_board.evaluate(current_board.turn)
        win = 1 if result > 0 else 0
        return win

    def backpropagate(self, node, win):
        while node is not None:
            node.visits += 1
            node.wins += win
            node = node.parent

    def mcts(self, root):
        for iteration in range(self.iterations):
            node = root

            while node.children:
                node = self.select_node(node)

            if not node.state.is_terminal():
                self.expand_node(node)
                if node.children:
                    node = random.choice(node.children)
                else:
                    break

            result = self.simulate(node.state)
            win = 1 if result > 0 else 0
            self.backpropagate(node, win)

        best_child = max(root.children, key=lambda child: child.visits)
        return best_child.move

    def choose_move(self, board):
        root = Node(board)
        best_move = self.mcts(root)
        print(f"MCTS chosen move: {best_move}, Type: {type(best_move)}")
        return best_move
