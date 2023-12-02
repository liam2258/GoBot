class GoGame:
    def __init__(self, board_size=6):
        self.board_size = board_size
        self.board = [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.current_player = 'B'  # 'B' for Black, 'W' for White
        self.opposing_player = 'W'
        self.moves = []
        self.potential_ko = None

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

    def print_board(self):
        print("   ", end="")
        for i in range(self.board_size):
            print(chr(i + 65), end=" ")
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
        Saves the current state of the board.
        """
        return [row[:] for row in self.board]

    def restore_state(self, saved_state):
        """
        Restores the board to a previously saved state.
        """
        self.board = [row[:] for row in saved_state]

    def make_move(self, row, col):
        '''
        Contains all the logic for making a move in the game

        This includes checking the validity of the move, checking
        for any captured stones, and updating the current score
        '''

        saved_state = self.save_state()

        if row < 0 or row >= self.board_size or col < 0 or col >= self.board_size:
            print("Invalid move. Out of bounds.")
            return False

        if self.board[row][col] != ' ':
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
            print("Invalid move. Self-capture is not allowed, try again.")
            self.restore_state(saved_state)
            return False
        
        if self.potential_ko and len(captured_enemies) == 1:
            if self.is_adjacent(row, col, self.potential_ko[0], self.potential_ko[1]):
                print("Invalid move. Violates ko, try again.")
                self.restore_state(saved_state)
                return False
            
        if len(captured_enemies) == 1:
            self.potential_ko = [row, col]
        else:
            self.potential_ko = None

        for group in groups:
            if group["captured"]:
                for stone in group["stones"]:
                    row, col = stone
                    self.board[row][col] = ' '

        self.current_player = 'W' if self.current_player == 'B' else 'B'
        self.opposing_player = 'B' if self.opposing_player == 'W' else 'W'
        return True
