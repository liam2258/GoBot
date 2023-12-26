import pytest
from .go_game import GoGame

def test_initialization():
    game = GoGame(6)
    assert game.board_size == 6
    assert game.current_player == 'B'
    assert game.opposing_player == 'W'
    assert game.is_over == False

# Testing the find_groups() function

def test_find_groups():
    game = GoGame(6)
    game.board = [
        ['B', ' ', ' ', ' ', ' ', ' '],
        [' ', 'B', ' ', ' ', ' ', ' '],
        [' ', ' ', 'B', ' ', ' ', ' '],
        [' ', ' ', ' ', 'B', ' ', ' '],
        [' ', ' ', ' ', ' ', 'B', ' '],
        [' ', ' ', ' ', ' ', ' ', 'B']
    ]
    groups = game.find_groups()
    assert len(groups) == 6
    for group in groups:
        assert len(group['stones']) == 1

def test_find_groups_multiple_stones():
    game = GoGame(6)
    game.board = [
        ['B', 'B', ' ', ' ', ' ', ' '],
        ['B', 'B', ' ', ' ', ' ', ' '],
        [' ', ' ', 'B', 'B', ' ', ' '],
        [' ', ' ', 'B', 'B', ' ', ' '],
        [' ', ' ', ' ', ' ', 'B', ' '],
        [' ', ' ', ' ', ' ', ' ', 'B']
    ]
    groups = game.find_groups()
    assert len(groups) == 4
    for group in groups:
        if len(group['stones']) == 4:
            assert all(stone in group['stones'] for stone in [(0, 0), (0, 1), (1, 0), (1, 1)]) or all(stone in group['stones'] for stone in [(2, 2), (2, 3), (3, 2), (3, 3)])
        else:
            assert len(group['stones']) == 1

# Testing count_territory() function

def test_count_territory():
    game = GoGame(6)
    game.board = [
        ['B', 'B', ' ', ' ', ' ', ' '],
        ['B', 'B', ' ', ' ', ' ', ' '],
        [' ', ' ', 'W', 'W', ' ', ' '],
        [' ', 'W', 'W', 'W', ' ', 'B'],
        [' ', 'W', ' ', 'W', 'B', ' '],
        [' ', 'W', ' ', 'W', ' ', 'B']
    ]
    territory = game.count_territory()
    assert territory['B'] == 1
    assert territory['W'] == 2

def test_count_territory_no_territory():
    game = GoGame(6)
    game.board = [
        ['B', ' ', ' ', ' ', ' ', ' '],
        [' ', 'B', ' ', ' ', ' ', ' '],
        [' ', ' ', 'W', ' ', ' ', ' '],
        [' ', ' ', ' ', 'W', ' ', ' '],
        [' ', ' ', ' ', ' ', 'B', ' '],
        [' ', ' ', ' ', ' ', ' ', 'B']
    ]
    territory = game.count_territory()
    assert territory['B'] == 0
    assert territory['W'] == 0

# Testing the calculate_score() function

def test_calculate_score():
    game = GoGame(6)
    game.board = [
        [' ', 'B', ' ', ' ', ' ', ' '],
        ['B', 'B', ' ', ' ', ' ', ' '],
        [' ', ' ', 'W', 'W', ' ', ' '],
        [' ', 'W', 'W', 'W', ' ', ' '],
        [' ', 'W', ' ', 'W', 'B', ' '],
        [' ', 'W', ' ', 'W', ' ', 'B']
    ]
    game.b_captures = 2
    game.w_captures = 0
    score = game.calculate_score()
    assert score['winner'] == 'B'
    assert score['B Score'] == 3
    assert score['W Score'] == 2

def test_calculate_score_tie():
    game = GoGame(6)
    game.board = [
        ['B', 'B', 'W', ' ', 'W', ' '],
        ['B', 'B', 'W', ' ', 'W', ' '],
        [' ', 'B', 'W', 'W', ' ', ' '],
        [' ', 'B', 'W', 'W', ' ', ' '],
        ['B', 'B', ' ', ' ', 'B', ' '],
        [' ', ' ', ' ', ' ', ' ', 'B']
    ]
    game.b_captures = 1
    game.w_captures = 1
    score = game.calculate_score()
    assert score['winner'] == 'Tie'
    assert score['B Score'] == 3
    assert score['W Score'] == 3

# Testing the make_move() function 

def test_make_move_valid():
    game = GoGame(6)
    assert game.make_move(0, 0)  # Valid move
    assert game.board[0][0] == 'B'  # Assuming 'B' is the current player

def test_make_move_out_of_bounds():
    game = GoGame(6)
    assert not game.make_move(-1, 0)  # Invalid move, out of bounds
    assert not game.make_move(0, 6)  # Invalid move, out of bounds

def test_make_move_pass():
    game = GoGame(6)
    assert game.make_move("pass")  # Valid pass
    assert game.pass_counter == 1
    assert game.current_player == 'W'  # Assuming 'B' was the current player

def test_make_move_game_over():
    game = GoGame(6)
    game.is_over = True
    assert not game.make_move(0, 0)  # Game is over, move should not be allowed


# Testing the get_valid_moves() function


def test_get_valid_moves_empty_board():
    game = GoGame(6)
    valid_moves = game.get_valid_moves()
    assert len(valid_moves) == 37  # 36 board positions + pass
    assert ("pass", 0) in valid_moves
    for row in range(6):
        for col in range(6):
            assert (row, col) in valid_moves

def test_get_valid_moves_filled_board():
    game = GoGame(6)
    game.board = [['B' for _ in range(6)] for _ in range(6)]  # Fill the board with 'B'
    valid_moves = game.get_valid_moves()
    assert len(valid_moves) == 1  # Only pass is valid
    assert valid_moves[0] == ("pass", 0)

def test_get_valid_moves_some_positions_filled():
    game = GoGame(6)
    game.board[0][0] = 'B'
    game.board[5][5] = 'W'
    valid_moves = game.get_valid_moves()
    assert len(valid_moves) == 35  # 34 board positions + pass
    assert ("pass", 0) in valid_moves
    assert (0, 0) not in valid_moves
    assert (5, 5) not in valid_moves