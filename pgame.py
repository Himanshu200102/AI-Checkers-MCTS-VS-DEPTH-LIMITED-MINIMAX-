import copy
import time

RED = "RED"
BLACK = "BLACK"
EMPTY = "_"
DIRECTIONS = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

class Board:
    def __init__(self):
        self.board = self.initialize_board()
        self.turn = RED

    def initialize_board(self):
        board = [[EMPTY] * 8 for _ in range(8)]
        for row in range(8):
            if row < 3 and row % 2 == 0:
                for col in range(1, 8, 2):
                    board[row][col] = BLACK
            elif row < 3 and row % 2 != 0:
                for col in range(0, 8, 2):
                    board[row][col] = BLACK
            elif row > 4 and row % 2 == 0:
                for col in range(1, 8, 2):
                    board[row][col] = RED
            elif row > 4 and row % 2 != 0:
                for col in range(0, 8, 2):
                    board[row][col] = RED
        return board

    def is_on_board(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8

    def get_piece(self, row, col):
        if self.is_on_board(row, col):
            return self.board[row][col]
        return None

    def move_piece(self, move):
        start_row, start_col, end_row, end_col = move
        piece = self.board[start_row][start_col]
        self.board[end_row][end_col] = piece
        self.board[start_row][start_col] = EMPTY

        delta_row = end_row - start_row
        delta_col = end_col - start_col
        if abs(delta_row) == 2 and abs(delta_col) == 2:
            capture_row = start_row + delta_row // 2
            capture_col = start_col + delta_col // 2
            self.board[capture_row][capture_col] = EMPTY

        if end_row == 0 and piece == RED:
            self.board[end_row][end_col] = "RED_KING"
        elif end_row == 7 and piece == BLACK:
            self.board[end_row][end_col] = "BLACK_KING"

    def legal_moves(self, player):
        moves = []
        captures = []

        move_directions = [(-1, -1), (-1, 1)] if player == RED else [(1, -1), (1, 1)]
        king_directions = DIRECTIONS

        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece is None or (player not in piece and "KING" not in piece):
                    continue

                directions = king_directions if "KING" in piece else move_directions

                for d_row, d_col in directions:
                    new_row, new_col = row + d_row, col + d_col
                    capture_row, capture_col = row + 2 * d_row, col + 2 * d_col
                    mid_row, mid_col = row + d_row, col + d_col

                    if self.is_on_board(new_row, new_col) and self.get_piece(new_row, new_col) == EMPTY:
                        moves.append((row, col, new_row, new_col))

                    if (self.is_on_board(capture_row, capture_col) and
                            self.get_piece(mid_row, mid_col) not in [EMPTY, player] and
                            self.get_piece(capture_row, capture_col) == EMPTY):
                        captures.append((row, col, capture_row, capture_col))

        return captures if captures else moves

    def evaluate(self, player):
        score = 0
        regular_piece_score = 3
        king_piece_score = 5

        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece == f"{player}":
                    score += regular_piece_score
                elif piece == f"{player}_KING":
                    score += king_piece_score
                elif piece != EMPTY:
                    score -= regular_piece_score if "KING" not in piece else king_piece_score

        return score

    def has_pieces(self, player):
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if player in piece:
                    return True
        return False

    def is_terminal(self):
        if not self.has_pieces(RED) or not self.has_pieces(BLACK):
            return True
        if not self.legal_moves(self.turn):
            return True
        return False

    def copy(self):
        return copy.deepcopy(self)

    def switch_turn(self):
        self.turn = RED if self.turn == BLACK else BLACK

class CheckersGame:
    def __init__(self, player1, player2, max_moves=10):
        self.board = Board()
        self.player1 = player1
        self.player2 = player2
        self.max_moves = max_moves
        self.decision_times_minimax = []
        self.decision_times_mcts = []

    def play_game(self):
        move_counter = 0
        while not self.board.is_terminal() and move_counter < self.max_moves:
            current_player = self.board.turn

            start_time = time.time()
            if current_player == RED:
                move = self.player1.choose_move(self.board)
                end_time = time.time()
                self.decision_times_minimax.append(end_time - start_time)
            else:
                move = self.player2.choose_move(self.board)
                end_time = time.time()
                self.decision_times_mcts.append(end_time - start_time)

            print(f"Selected move: {move}, Type: {type(move)}")
            print(f"Decision time: {end_time - start_time:.4f} seconds")
            self.board.move_piece(move)
            self.board.switch_turn()
            move_counter += 1

        red_score = self.board.evaluate(RED)
        black_score = self.board.evaluate(BLACK)

        if red_score > black_score:
            winner = "MINIMAX"
        elif black_score > red_score:
            winner = "MONTE CARLO TREE SEARCH"
        else:
            winner = "Draw"

        return winner, move_counter, self.decision_times_minimax, self.decision_times_mcts
