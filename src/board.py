from typing import Optional, List


class Board:
    ROWS = 6
    COLS = 7
    EMPTY = 0
    PLAYER1 = 1
    PLAYER2 = 2

    def __init__(self):
        self.grid: List[List[int]] = [[self.EMPTY for _ in range(self.COLS)] for _ in range(self.ROWS)]
        self.last_move: Optional[int] = None

    def copy(self) -> 'Board':
        new_board = Board()
        new_board.grid = [row[:] for row in self.grid]
        new_board.last_move = self.last_move
        return new_board

    def drop_piece(self, col: int, player: int) -> bool:
        if col < 0 or col >= self.COLS:
            return False
        if self.grid[0][col] != self.EMPTY:
            return False
        for row in range(self.ROWS - 1, -1, -1):
            if self.grid[row][col] == self.EMPTY:
                self.grid[row][col] = player
                self.last_move = col
                return True
        return False

    def is_valid_move(self, col: int) -> bool:
        return 0 <= col < self.COLS and self.grid[0][col] == self.EMPTY

    def get_valid_moves(self) -> List[int]:
        return [col for col in range(self.COLS) if self.is_valid_move(col)]

    def is_full(self) -> bool:
        return all(self.grid[0][col] != self.EMPTY for col in range(self.COLS))

    def check_winner(self) -> int:
        for row in range(self.ROWS):
            for col in range(self.COLS - 3):
                if self.grid[row][col] != self.EMPTY:
                    if (self.grid[row][col] == self.grid[row][col + 1] ==
                        self.grid[row][col + 2] == self.grid[row][col + 3]):
                        return self.grid[row][col]

        for row in range(self.ROWS - 3):
            for col in range(self.COLS):
                if self.grid[row][col] != self.EMPTY:
                    if (self.grid[row][col] == self.grid[row + 1][col] ==
                        self.grid[row + 2][col] == self.grid[row + 3][col]):
                        return self.grid[row][col]

        for row in range(self.ROWS - 3):
            for col in range(self.COLS - 3):
                if self.grid[row][col] != self.EMPTY:
                    if (self.grid[row][col] == self.grid[row + 1][col + 1] ==
                        self.grid[row + 2][col + 2] == self.grid[row + 3][col + 3]):
                        return self.grid[row][col]

        for row in range(3, self.ROWS):
            for col in range(self.COLS - 3):
                if self.grid[row][col] != self.EMPTY:
                    if (self.grid[row][col] == self.grid[row - 1][col + 1] ==
                        self.grid[row - 2][col + 2] == self.grid[row - 3][col + 3]):
                        return self.grid[row][col]

        return self.EMPTY

    def get_row_for_column(self, col: int) -> int:
        for row in range(self.ROWS - 1, -1, -1):
            if self.grid[row][col] == self.EMPTY:
                return row
        return -1
