class MinimaxPlayer:
    def __init__(self, depth):
        self.depth = depth

    def minimax(self, board, depth, maximizing, player):
        if depth == 0 or board.is_terminal():
            return board.evaluate(player), None

        moves = board.legal_moves(player)
        best_move = None

        if maximizing:
            max_eval = float('-inf')
            for move in moves:
                new_board = board.copy()
                new_board.move_piece(move)
                eval, _ = self.minimax(new_board, depth - 1, False, player)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in moves:
                new_board = board.copy()
                new_board.move_piece(move)
                eval, _ = self.minimax(new_board, depth - 1, True, player)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
            return min_eval, best_move

    def choose_move(self, board):
        _, best_move = self.minimax(board, self.depth, True, board.turn)
        print(f"Minimax chosen move: {best_move}, Type: {type(best_move)}")
        return best_move
