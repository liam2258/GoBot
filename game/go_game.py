class GoGame:
    def __init__(self, board_size=6):
        self.board_size = board_size
        self.board = [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.current_player = 'B'
        self.opposing_player = 'W'
        self.moves = []
        self.potential_ko = None
        self.pass_counter = 0
        self.b_captures = 0
        self.w_captures = 0
        self.is_over = False

    def find_groups(self):
        """
        Identifies and returns all groups of stones on the board. 
        A group is defined as a set of stones of the same color that are connected vertically. 
        The method uses a flood fill algorithm to find the groups.

        Returns:
        list: A list of dictionaries where each dictionary represents a group of stones. 
        Each dictionary contains keys 'player', 'stones', and a binary 'captured' flag.
        """
        groups = []
        visited = [[False for _ in range(self.board_size)] for _ in range(self.board_size)]

        def is_valid(row, col, player):
            return 0 <= row < self.board_size and 0 <= col < self.board_size and self.board[row][col] == player

        def flood_fill(row, col, group):
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            visited[row][col] = True
            group.append((row, col))

            for dx, dy in directions:
                new_row, new_col = row + dx, col + dy
                if is_valid(new_row, new_col, self.board[row][col]) and not visited[new_row][new_col]:
                    flood_fill(new_row, new_col, group)

        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] != ' ' and not visited[i][j]:
                    player = self.board[i][j]
                    group = []
                    flood_fill(i, j, group)

                    # Check if the group has any liberties
                    captured = True
                    for stone in group:
                        row, col = stone
                        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                            new_row, new_col = row + dx, col + dy
                            if (0 <= new_row < self.board_size and
                                    0 <= new_col < self.board_size and
                                    self.board[new_row][new_col] == ' '):
                                captured = False
                                break

                    groups.append({'player': player, 'stones': group, 'captured': captured})

        return groups
    
    def find_territory(self):
        """
        Identifies and returns all captured groups of empty spaces on the board. 
        A group of empty spaces is considered captured if it is completely surrounded by a player's stones.

        Returns:
        list: A list of dictionaries where each dictionary represents a captured group of empty spaces. 
        Each dictionary contains keys 'stones' and 'capturing_player', 
        and values representing the coordinates of the stones in the group, 
        and the player who has surrounded the group.
        """
        captured_empty_groups = []
        visited_empty = [[False for _ in range(self.board_size)] for _ in range(self.board_size)]

        def is_valid(row, col):
            return 0 <= row < self.board_size and 0 <= col < self.board_size

        def flood_fill(row, col, group):
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            visited_empty[row][col] = True
            group.append((row, col))

            for dx, dy in directions:
                new_row, new_col = row + dx, col + dy
                if is_valid(new_row, new_col) and not visited_empty[new_row][new_col] and self.board[new_row][new_col] == ' ':
                    flood_fill(new_row, new_col, group)

        for i in range(self.board_size):
            for j in range(self.board_size):
                if not visited_empty[i][j] and self.board[i][j] == ' ':
                    group = []
                    flood_fill(i, j, group)
                    captured = False
                    capturing_player = None

                    black_neighbor = False
                    white_neighbor = False

                    for stone in group:
                        row, col = stone
                        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                            new_row, new_col = row + dx, col + dy
                            if is_valid(new_row, new_col):
                                if self.board[new_row][new_col] == 'B':
                                    black_neighbor = True
                                    if white_neighbor:
                                        captured = False
                                        break
                                elif self.board[new_row][new_col] == 'W':
                                    white_neighbor = True
                                    if black_neighbor:
                                        captured = False
                                        break
                    
                    if not captured:
                        if black_neighbor and not white_neighbor:
                            captured = True
                            capturing_player = 'B'
                        elif white_neighbor and not black_neighbor:
                            captured = True
                            capturing_player = 'W'

                    if captured:
                        captured_empty_groups.append({'stones': group, 'capturing_player': capturing_player})

        return captured_empty_groups

    def count_territory(self):
        """
        Counts the territory for each player. Territory is defined as any empty points 
        that are completely surrounded by a player's stones, not including diagonal spaces. 

        Returns:
        dict: A dictionary with keys 'B' and 'W', and values representing the territory count for each player.
        """
        territory_count = {'B': 0, 'W': 0}
        captured_empty_groups = self.find_territory()

        for group_info in captured_empty_groups:
            capturing_player = group_info['capturing_player']
            if capturing_player is not None:
                territory_count[capturing_player] += len(group_info['stones'])

        return territory_count
    
    def calculate_score(self):
        """
        Counts the territory for each player. Territory is defined as any empty points 
        that are completely surrounded by a player's stones. 

        Returns:
        dict: A dictionary with keys 'B' and 'W', and values representing the territory count for each player.
        """
        score = self.count_territory()
        score['B'] += self.b_captures
        score['W'] += self.w_captures
        if score['W'] > score['B']:
            return {'winner': 'W', 'W Score': score['W'], 'B Score' : score['B']}
        elif score['W'] < score['B']:
            return {'winner': 'B', 'W Score': score['W'], 'B Score' : score['B']}
        else:
            return {'winner': 'Tie', 'W Score': score['W'], 'B Score' : score['B']}

    def print_board(self):
        print("   ", end="")
        for i in range(self.board_size):
            print(f"{i:2}", end=" ")
        print()

        for i in range(self.board_size):
            print(f"{i:2}", end=" ")
            for j in range(self.board_size):
                piece = self.board[i][j]
                if piece == 'B':
                    print("\u25CB ", end="")  # Unicode for black circle
                elif piece == 'W':
                    print("\u25CF ", end="")  # Unicode for white circle
                else:
                    print("\u00B7 ", end="")  # Unicode for middle dot
            print()

    def is_adjacent(self, row1, col1, row2, col2):
        """
        Checks if two moves are adjacent to each other on the board.
        Two moves are considered adjacent if they are next to each other horizontally or vertically.

        Parameters:
        row1, col1 (int): The row and column of the first move.
        row2, col2 (int): The row and column of the second move.

        Returns:
        bool: True if the moves are adjacent, False otherwise.
        """
        return abs(row1 - row2) + abs(col1 - col2) == 1
    
    def save_state(self):
        """
        Saves the current state of the board and other instance variables.
        """
        state = {
            'board': [row[:] for row in self.board],
            'board_size': self.board_size,
            'current_player': self.current_player,
            'opposing_player': self.opposing_player,
            'moves': self.moves[:],
            'potential_ko': self.potential_ko,
            'b_captures': self.b_captures,
            'w_captures': self.w_captures,
            'pass_counter': self.pass_counter
        }
        return state

    def restore_state(self, saved_state):
        """
        Restores the board and other instance variables to a previously saved state.
        """
        self.board = [row[:] for row in saved_state['board']]
        self.board_size = saved_state['board_size']
        self.current_player = saved_state['current_player']
        self.opposing_player = saved_state['opposing_player']
        self.moves = saved_state['moves'][:]
        self.potential_ko = saved_state['potential_ko']
        self.b_captures = saved_state['b_captures']
        self.w_captures = saved_state['w_captures']
        self.pass_counter = saved_state['pass_counter']

    def make_move(self, row, col=0, live=False):
        """
        Makes a move in the game. This includes checking the validity of the move, 
        checking for any captured stones, and updating the current score. 
        If the game is over, no more moves can be played. 
        If a player passes, the potential Ko is reset, the pass counter is incremented, 
        and the players are switched. If there have been 4 passes in a row, the game is over.

        Parameters:
        row (int or "pass"): The row to place the stone, or "pass" to pass the turn.
        col (int, optional): The column to place the stone. Defaults to 0.
        live (bool, optional): Whether to print live game updates. Defaults to False.

        Returns:
        bool: True if the move was made successfully, False otherwise.
        """
        if self.is_over:
            if live:
                print("Game is over, no more moves can be played")
            return False

        if row == "pass":  # Handling the pass move
            self.potential_ko = None
            self.pass_counter += 1
            self.current_player = 'W' if self.current_player == 'B' else 'B'
            self.opposing_player = 'B' if self.opposing_player == 'W' else 'W'
            if self.pass_counter >= 4:
                self.is_over = True
                if live:
                    print('Game Over:')
                    print(self.calculate_score())
            return True


        saved_state = self.save_state()

        if row < 0 or row >= self.board_size or col < 0 or col >= self.board_size:
            if live:
                print("Invalid move. Out of bounds.")
            return False

        if self.board[row][col] != ' ':
            if live:
                print("Invalid move. Cell is already occupied.")
            return False

        self.board[row][col] = self.current_player
        self.moves.append((row, col, self.current_player))
        groups = self.find_groups()

        captured_enemies = []

        # Check for captures of enemy pieces
        for group in groups:
            if group["captured"] and group["player"] is not self.current_player:
                for stone in group["stones"]:
                    row, col = stone
                    captured_enemies.append(stone)
                    self.board[row][col] = ' '
                    if self.current_player == 'B':
                        self.b_captures += 1
                    else:
                        self.w_captures += 1
                
        groups = self.find_groups()

         # Check for self-capture
        self_captured = False
        for group in groups:
            if group["captured"] and group["player"] == self.current_player:
                self_captured = True
                break

        # Undo captures and moves if self-capture occurs
        if self_captured:
            self.board[row][col] = ' '  # Undo the move
            if live:
                print("Invalid move. Self-capture is not allowed, try again.")
            self.restore_state(saved_state)
            return False
        
        if self.potential_ko and len(captured_enemies) == 1:
            if self.is_adjacent(row, col, self.potential_ko[0], self.potential_ko[1]):
                if live:
                    print("Invalid move. Violates ko, try again.")
                self.restore_state(saved_state)
                return False
            
        if len(captured_enemies) == 1:
            self.potential_ko = [row, col]
        else:
            self.potential_ko = None

        self.current_player = 'W' if self.current_player == 'B' else 'B'
        self.opposing_player = 'B' if self.opposing_player == 'W' else 'W'
        self.pass_counter = 0
        return True

    def get_valid_moves(self):
        """
        Get a list of valid moves for the current state of the board.
        A move is considered valid if it is a pass or if placing a stone on the board 
        at the move's coordinates does not violate the rules of the game.

        Returns:
        list: A list of tuples where each tuple represents a valid move. 
        Each tuple contains two elements: the row and the column of the move. 
        A pass is represented as ("pass", 0).
        """
        valid_moves = []
        saved_state = self.save_state()
        if self.pass_counter < 4:
            valid_moves.append(("pass", 0))

        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row][col] == ' ':
                    # Try making the move and check if it's valid
                    if self.make_move(row, col, False):
                        valid_moves.append((row, col))
                    # Restore the state for next iteration
                    self.restore_state(saved_state)

        return valid_moves
    
    def clone(self):
        """
        Clones the current instance of the GoGame class.

        Returns:
        GoGame: A new instance of the GoGame class with the same state as the current instance.
        """
        cloned_game = GoGame(self.board_size)

        cloned_game.board = [row[:] for row in self.board]
        cloned_game.current_player = self.current_player
        cloned_game.opposing_player = self.opposing_player
        cloned_game.moves = self.moves[:]
        cloned_game.potential_ko = self.potential_ko
        cloned_game.pass_counter = self.pass_counter
        cloned_game.b_captures = self.b_captures
        cloned_game.w_captures = self.w_captures
        cloned_game.is_over = self.is_over

        return cloned_game


