from go_game import GoGame
from mct import MonteCarloTree

def play_game():
    board_size = 6
    game = GoGame(board_size)  # Initialize the game

    print("Do you want to move first or second? (first/second)")
    user_turn = input().strip().lower()

    
    if user_turn == "first":
        while not game.is_over:
            user_input = input("Enter 'pass' to pass or enter X and Y coordinates (e.g., '2 3'): ").strip().lower()
            if user_input == "pass":
                # Implement logic for the user passing
                game.make_move("pass")
            else:
                x, y = map(int, user_input.split())
                game.make_move(x, y, live=True)
            
            # Update the game state with the user's move
            # Implement game logic for the user's move

            tree = MonteCarloTree(game)
            best_move = tree.best_move(iterations=100)
            game.make_move(best_move[0], best_move[1])
            game.print_board()
            # Update the game state with AI's move
            # Implement game logic for the AI's move

            # Repeat the process until the game ends
        print(game.calculate_score())
    elif user_turn == "second":
        while not game.is_over:
            tree = MonteCarloTree(game)
            best_move = tree.best_move(100)
            game.make_move(best_move[0], best_move[1])
            game.print_board()
            # Update the game state with AI's move
            # Implement game logic for the AI's move

            user_input = input("Enter 'pass' to pass or enter X and Y coordinates (e.g., '2 3'): ").strip().lower()
            if user_input == "pass":
                # Implement logic for the user passing
                game.make_move("pass")
            else:
                x, y = map(int, user_input.split())
                game.make_move(x, y, live=True)
            
            # Update the game state with the user's move
            # Implement game logic for the user's move

            # Repeat the process until the game ends
        print(game.calculate_score())
    else:
        print("Invalid input. Please enter 'first' or 'second'.")
        user_turn = input().strip().lower()


play_game()


if __name__ == "__main__":
    play_game()
    # game = GoGame(board_size=6)  # Initialize your game
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