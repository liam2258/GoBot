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
        ['B', 'B', ' ', ' ', ' ', ' '],
        ['B', 'B', ' ', ' ', ' ', ' '],
        [' ', ' ', 'W', 'W', ' ', ' '],
        [' ', ' ', 'W', 'W', ' ', ' '],
        [' ', ' ', ' ', ' ', 'B', ' '],
        [' ', ' ', ' ', ' ', ' ', 'B']
    ]
    game.b_captures = 1
    game.w_captures = 1
    score = game.calculate_score()
    assert score['winner'] == 'Tie'
    assert score['B Score'] == 1
    assert score['W Score'] == 1 