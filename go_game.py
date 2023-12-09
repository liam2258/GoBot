class GoGame:
    def __init__(self, board_size=6):
        self.board_size = board_size
        self.board = [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.current_player = 'B'  # 'B' for Black, 'W' for White
        self.opposing_player = 'W'
        self.moves = []
        self.potential_ko = None
        self.pass_counter = 0
        self.b_captures = 0
        self.w_captures = 0
        self.is_over = False

    def find_groups(self):
        '''
        Used to identify all of the groups of stones, which
        player they belong to, and if they're currently captured.
        '''
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
        '''
        Used to identify and return all captured groups of empty spaces on the board.
        '''
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
        territory_count = {'B': 0, 'W': 0}
        captured_empty_groups = self.find_territory()

        for group_info in captured_empty_groups:
            capturing_player = group_info['capturing_player']
            if capturing_player is not None:
                territory_count[capturing_player] += len(group_info['stones'])

        return territory_count
    
    def calculate_score(self):
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
            print(i, end=" ")
        print()

        for i in range(self.board_size):
            print(f"{i:2}", end=" ")
            for j in range(self.board_size):
                print(f"{self.board[i][j]}", end=" ")
            print()

    def is_adjacent(self, row1, col1, row2, col2):
        """
        Checks if two moves are adjacent to each other on the board.
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
            'w_captures': self.w_captures
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

    def make_move(self, row, col=0, live=True):
        '''
        Contains all the logic for making a move in the game

        This includes checking the validity of the move, checking
        for any captured stones, and updating the current score
        '''
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

        # Undo captrues and moves if self-capture occurs
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

    # TODO Change this to just getting empty squares
    def get_valid_moves(self):
        """
        Get a list of valid moves for the current state of the board.
        """
        valid_moves = []
        saved_state = self.save_state()
        # pass is always a valid move
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
