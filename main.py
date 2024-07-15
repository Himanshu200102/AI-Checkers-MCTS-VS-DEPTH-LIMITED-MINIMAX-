from pgame import CheckersGame
from agents.minimax import MinimaxPlayer
from agents.mcts import MCTSPlayer
import matplotlib.pyplot as plt

def compare_algorithms(num_games, minimax_depth, mcts_iterations):
    decision_times_minimax = []
    decision_times_mcts = []

    for game_num in range(1, num_games + 1):
        print(f"\nStarting game {game_num}")
        player1 = MinimaxPlayer(minimax_depth)
        player2 = MCTSPlayer(mcts_iterations)
        game = CheckersGame(player1, player2)
        winner, moves, times_minimax, times_mcts = game.play_game()
        decision_times_minimax.extend(times_minimax)
        decision_times_mcts.extend(times_mcts)

    plot_decision_times(decision_times_minimax, decision_times_mcts)

def plot_decision_times(times_minimax, times_mcts):
    plt.figure(figsize=(10, 5))
    plt.plot(times_minimax, label='Minimax Decision Times', color='blue')
    plt.plot(times_mcts, label='MCTS Decision Times', color='red')
    plt.xlabel('Move Number')
    plt.ylabel('Decision Time (seconds)')
    plt.title('Decision Times for Minimax and MCTS Algorithms')
    plt.legend()
    plt.show()

def compare_algorithms_score(num_games, minimax_depth, mcts_iterations):
    minimax_wins = 0
    mcts_wins = 0
    draws = 0
    total_moves = 0

    for game_num in range(1, num_games + 1):
        print(f"\nStarting game {game_num}")
        game = CheckersGame(minimax_depth, mcts_iterations)
        winner, moves, times_minimax, times_mcts = game.play_game()
        total_moves += moves

        if winner == "MINIMAX":
            minimax_wins += 1
        elif winner == "MONTE CARLO TREE SEARCH":
            mcts_wins += 1
        else:
            draws += 1

    avg_moves_per_game = total_moves / num_games
    print("\n--- Results Summary ---")
    print(f"Total Games: {num_games}")
    print(f"Minimax Wins: {minimax_wins}")
    print(f"MCTS Wins: {mcts_wins}")
    print(f"Draws: {draws}")
    print(f"Average Moves per Game: {avg_moves_per_game}")


if __name__ == "__main__":
    num_games = 10
    minimax_depth = 3
    mcts_iterations = 500
    compare_algorithms(num_games, minimax_depth, mcts_iterations)
    # compare_algorithms_score(num_games, minimax_depth, mcts_iterations)