from go_game import GoGame
from mct import MonteCarloTree

def play_game():
    board_size = 6
    game = GoGame(board_size)

    print("Do you want to move first or second? (first/second)")
    user_turn = input().strip().lower()

    
    if user_turn == "first":
        while not game.is_over:
            user_input = input("Enter 'pass' to pass or enter X and Y coordinates (e.g., '2 3'): ").strip().lower()
            if user_input == "pass":
                game.make_move("pass")
            else:
                x, y = map(int, user_input.split())
                game.make_move(x, y, live=True)

            tree = MonteCarloTree(game)
            best_move = tree.best_move(iterations=100)
            game.make_move(best_move[0], best_move[1])
            game.print_board()

        print(game.calculate_score())
    elif user_turn == "second":
        while not game.is_over:
            tree = MonteCarloTree(game)
            best_move = tree.best_move(100)
            game.make_move(best_move[0], best_move[1])
            game.print_board()

            user_input = input("Enter 'pass' to pass or enter X and Y coordinates (e.g., '2 3'): ").strip().lower()
            if user_input == "pass":
                game.make_move("pass")
            else:
                x, y = map(int, user_input.split())
                game.make_move(x, y, live=True)

        print(game.calculate_score())
    else:
        print("Invalid input. Please enter 'first' or 'second'.")
        user_turn = input().strip().lower()


play_game()


if __name__ == "__main__":
    play_game()
    # game = GoGame(board_size=6)  # Initialize game
    # tree = MonteCarloTree(game)
    # best_move = tree.best_move(iterations=len(game.get_valid_moves()))  # Run MCTS algorithm
    # print("Best Move:", best_move)

    # Testing Ko
    # game.make_move(0, 2)
    # game.make_move(1, 4)
    # game.make_move('pass', 0)
    # game.make_move('pass', 0)
    # game.make_move('pass', 0)
    # game.make_move('pass', 0)
    # game.make_move(1, 1)
    # game.make_move(1, 2)
    # game.make_move(2, 2)
    # game.make_move(0, 3)
    # game.make_move(5, 5)
    # game.make_move(2, 3)
    # game.make_move(1, 3)
    # game.make_move(1, 2)