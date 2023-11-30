from go_game import GoGame

if __name__ == "__main__":
    game = GoGame()

    game.make_move(0, 0)
    game.make_move(0, 1)
    game.make_move(5, 5)
    game.make_move(1, 0)
    game.make_move(4, 5)

    game.print_board()
    stone_groups = game.find_groups()
    print("Stone Groups:", stone_groups)