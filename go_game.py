class GoGame:
    def __init__(self, board_size=6):
        self.board_size = board_size
        self.board = [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.current_player = 'B'  # 'B' for Black, 'W' for White
        self.moves = []

    def find_groups(self):
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
        # Print the Go board
        print("   ", end="")
        for i in range(self.board_size):
            print(chr(i + 65), end=" ")
        print()

        for i in range(self.board_size):
            print(f"{i:2}", end=" ")
            for j in range(self.board_size):
                print(f"{self.board[i][j]}", end=" ")
            print()

    def make_move(self, row, col):
        if row < 0 or row >= self.board_size or col < 0 or col >= self.board_size:
            print("Invalid move. Out of bounds.")
            return False

        if self.board[row][col] != ' ':
            print("Invalid move. Cell is already occupied.")
            return False

        self.board[row][col] = self.current_player
        self.moves.append((row, col, self.current_player))
        groups = self.find_groups()

        for group in groups:
            if group["captured"]:
                for stone in group["stones"]:
                    row, col = stone
                    self.board[row][col] = ' '


        # TODO: Add logic to handle capturing stones, check for surrounded groups, etc.

        self.current_player = 'W' if self.current_player == 'B' else 'B'  # Change player turn
        return True
