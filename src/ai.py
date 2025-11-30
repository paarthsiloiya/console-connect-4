import random
from typing import Tuple
from board import Board


class AI:
    MAX_DEPTH = 6
    
    def __init__(self, player: int):
        self.player = player
        self.opponent = Board.PLAYER1 if player == Board.PLAYER2 else Board.PLAYER2

    def get_move(self, board: Board) -> int:
        valid_moves = board.get_valid_moves()
        if len(valid_moves) == 1:
            return valid_moves[0]
        
        best_score = float('-inf')
        best_moves = []
        
        for col in valid_moves:
            new_board = board.copy()
            new_board.drop_piece(col, self.player)
            score = self._minimax(new_board, self.MAX_DEPTH - 1, float('-inf'), float('inf'), False)
            
            if score > best_score:
                best_score = score
                best_moves = [col]
            elif score == best_score:
                best_moves.append(col)
        
        return random.choice(best_moves)

    def _minimax(self, board: Board, depth: int, alpha: float, beta: float, is_maximizing: bool) -> float:
        winner = board.check_winner()
        if winner == self.player:
            return 10000 + depth
        if winner == self.opponent:
            return -10000 - depth
        if board.is_full() or depth == 0:
            return self._evaluate_board(board)
        
        valid_moves = board.get_valid_moves()
        
        if is_maximizing:
            max_eval = float('-inf')
            for col in valid_moves:
                new_board = board.copy()
                new_board.drop_piece(col, self.player)
                eval_score = self._minimax(new_board, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for col in valid_moves:
                new_board = board.copy()
                new_board.drop_piece(col, self.opponent)
                eval_score = self._minimax(new_board, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval

    def _evaluate_board(self, board: Board) -> float:
        score = 0.0
        
        center_col = Board.COLS // 2
        center_count = sum(1 for row in range(Board.ROWS) if board.grid[row][center_col] == self.player)
        score += center_count * 3
        
        score += self._evaluate_lines(board)
        
        return score

    def _evaluate_lines(self, board: Board) -> float:
        score = 0.0
        
        for row in range(Board.ROWS):
            for col in range(Board.COLS - 3):
                window = [board.grid[row][col + i] for i in range(4)]
                score += self._evaluate_window(window)
        
        for row in range(Board.ROWS - 3):
            for col in range(Board.COLS):
                window = [board.grid[row + i][col] for i in range(4)]
                score += self._evaluate_window(window)
        
        for row in range(Board.ROWS - 3):
            for col in range(Board.COLS - 3):
                window = [board.grid[row + i][col + i] for i in range(4)]
                score += self._evaluate_window(window)
        
        for row in range(3, Board.ROWS):
            for col in range(Board.COLS - 3):
                window = [board.grid[row - i][col + i] for i in range(4)]
                score += self._evaluate_window(window)
        
        return score

    def _evaluate_window(self, window: list) -> float:
        score = 0.0
        player_count = window.count(self.player)
        opponent_count = window.count(self.opponent)
        empty_count = window.count(Board.EMPTY)
        
        if player_count == 4:
            score += 100
        elif player_count == 3 and empty_count == 1:
            score += 5
        elif player_count == 2 and empty_count == 2:
            score += 2
        
        if opponent_count == 3 and empty_count == 1:
            score -= 4
        
        return score
