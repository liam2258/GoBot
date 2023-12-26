from go_game import GoGame
from mct import MonteCarloTree

def play_game():
    board_size = 6
    game = GoGame(board_size)

    while True:
        print("Do you want to move first or second? (first/second)")
        user_turn = input().strip().lower()
        if user_turn in ["first", "second"]:
            break
        print("Invalid input. Please enter 'first' or 'second'.")

    if user_turn == "first":
        while not game.is_over:
            while True:
                user_input = input("Enter 'pass' to pass or enter X and Y coordinates (e.g., '2 3'): ").strip().lower()
                if user_input == "pass":
                    game.make_move("pass")
                    break
                else:
                    try:
                        x, y = map(int, user_input.split())
                        if 0 <= x < board_size and 0 <= y < board_size:
                            game.make_move(x, y, live=True)
                            break
                        else:
                            print("Invalid coordinates. Please enter coordinates within the board size.")
                    except ValueError:
                        print("Invalid input. Please enter 'pass' or two integers separated by a space.")

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

            while True:
                user_input = input("Enter 'pass' to pass or enter X and Y coordinates (e.g., '2 3'): ").strip().lower()
                if user_input == "pass":
                    game.make_move("pass")
                    break
                else:
                    try:
                        x, y = map(int, user_input.split())
                        if 0 <= x < board_size and 0 <= y < board_size:
                            game.make_move(x, y, live=True)
                            break
                        else:
                            print("Invalid coordinates. Please enter coordinates within the board size.")
                    except ValueError:
                        print("Invalid input. Please enter 'pass' or two integers separated by a space.")

if __name__ == "__main__":
    play_game()