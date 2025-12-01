import random
from typing import Tuple, Dict, Optional, List, Set
from board import Board


class NewAI:
    MIN_DEPTH = 6
    MAX_DEPTH = 12
    EXACT = 0
    LOWER_BOUND = 1
    UPPER_BOUND = 2
    
    def __init__(self, player: int):
        self.player = player
        self.opponent = Board.PLAYER1 if player == Board.PLAYER2 else Board.PLAYER2
        self.transposition_table: Dict[int, Tuple[float, int, int]] = {}
        self.move_order = [3, 2, 4, 1, 5, 0, 6]
        self.player_is_first = (player == Board.PLAYER1)

    def _board_hash(self, board: Board) -> int:
        h = 0
        for row in range(Board.ROWS):
            for col in range(Board.COLS):
                h = h * 3 + board.grid[row][col]
        return h

    def _count_pieces(self, board: Board) -> int:
        count = 0
        for row in range(Board.ROWS):
            for col in range(Board.COLS):
                if board.grid[row][col] != Board.EMPTY:
                    count += 1
        return count

    def _get_dynamic_depth(self, board: Board) -> int:
        pieces = self._count_pieces(board)
        if pieces <= 8:
            return self.MIN_DEPTH
        elif pieces <= 20:
            return self.MIN_DEPTH + 2
        elif pieces <= 30:
            return self.MAX_DEPTH - 2
        else:
            return self.MAX_DEPTH

    def _get_playable_row(self, board: Board, col: int) -> int:
        for row in range(Board.ROWS - 1, -1, -1):
            if board.grid[row][col] == Board.EMPTY:
                return row
        return -1

    def _find_threats(self, board: Board, player: int) -> List[Tuple[int, int, bool]]:
        threats = []
        
        for row in range(Board.ROWS):
            for col in range(Board.COLS - 3):
                window = [(row, col + i) for i in range(4)]
                cells = [board.grid[r][c] for r, c in window]
                if cells.count(player) == 3 and cells.count(Board.EMPTY) == 1:
                    empty_idx = cells.index(Board.EMPTY)
                    threat_row, threat_col = window[empty_idx]
                    is_odd = (Board.ROWS - 1 - threat_row) % 2 == 1
                    threats.append((threat_row, threat_col, is_odd))
        
        for row in range(Board.ROWS - 3):
            for col in range(Board.COLS):
                window = [(row + i, col) for i in range(4)]
                cells = [board.grid[r][c] for r, c in window]
                if cells.count(player) == 3 and cells.count(Board.EMPTY) == 1:
                    empty_idx = cells.index(Board.EMPTY)
                    threat_row, threat_col = window[empty_idx]
                    is_odd = (Board.ROWS - 1 - threat_row) % 2 == 1
                    threats.append((threat_row, threat_col, is_odd))
        
        for row in range(Board.ROWS - 3):
            for col in range(Board.COLS - 3):
                window = [(row + i, col + i) for i in range(4)]
                cells = [board.grid[r][c] for r, c in window]
                if cells.count(player) == 3 and cells.count(Board.EMPTY) == 1:
                    empty_idx = cells.index(Board.EMPTY)
                    threat_row, threat_col = window[empty_idx]
                    is_odd = (Board.ROWS - 1 - threat_row) % 2 == 1
                    threats.append((threat_row, threat_col, is_odd))
        
        for row in range(3, Board.ROWS):
            for col in range(Board.COLS - 3):
                window = [(row - i, col + i) for i in range(4)]
                cells = [board.grid[r][c] for r, c in window]
                if cells.count(player) == 3 and cells.count(Board.EMPTY) == 1:
                    empty_idx = cells.index(Board.EMPTY)
                    threat_row, threat_col = window[empty_idx]
                    is_odd = (Board.ROWS - 1 - threat_row) % 2 == 1
                    threats.append((threat_row, threat_col, is_odd))
        
        return threats

    def _is_threat_playable(self, board: Board, threat_row: int, threat_col: int) -> bool:
        playable_row = self._get_playable_row(board, threat_col)
        return playable_row == threat_row

    def _evaluate_threats(self, board: Board) -> float:
        score = 0.0
        
        my_threats = self._find_threats(board, self.player)
        opp_threats = self._find_threats(board, self.opponent)
        
        for threat_row, threat_col, is_odd in my_threats:
            if self._is_threat_playable(board, threat_row, threat_col):
                score += 200
            else:
                playable_row = self._get_playable_row(board, threat_col)
                if playable_row >= 0 and playable_row > threat_row:
                    distance = playable_row - threat_row
                    is_favorable = (self.player == Board.PLAYER1 and is_odd) or \
                                   (self.player == Board.PLAYER2 and not is_odd)
                    if is_favorable:
                        score += max(60 - distance * 8, 10)
                    else:
                        score += max(30 - distance * 5, 5)
        
        for threat_row, threat_col, is_odd in opp_threats:
            if self._is_threat_playable(board, threat_row, threat_col):
                score -= 180
            else:
                playable_row = self._get_playable_row(board, threat_col)
                if playable_row >= 0 and playable_row > threat_row:
                    distance = playable_row - threat_row
                    is_favorable = (self.opponent == Board.PLAYER1 and is_odd) or \
                                   (self.opponent == Board.PLAYER2 and not is_odd)
                    if is_favorable:
                        score -= max(55 - distance * 8, 8)
                    else:
                        score -= max(25 - distance * 5, 3)
        
        double_threats = {}
        for threat_row, threat_col, is_odd in my_threats:
            key = threat_col
            if key not in double_threats:
                double_threats[key] = []
            double_threats[key].append(threat_row)
        
        for col, rows in double_threats.items():
            if len(rows) >= 2:
                rows_sorted = sorted(rows)
                for i in range(len(rows_sorted) - 1):
                    if rows_sorted[i + 1] - rows_sorted[i] == 1:
                        score += 150
        
        return score

    def _detect_zugzwang(self, board: Board) -> float:
        score = 0.0
        
        my_threats = self._find_threats(board, self.player)
        opp_threats = self._find_threats(board, self.opponent)
        
        opp_threat_positions = set((r, c) for r, c, _ in opp_threats)
        
        for col in range(Board.COLS):
            playable_row = self._get_playable_row(board, col)
            if playable_row < 0 or playable_row == 0:
                continue
            
            above_row = playable_row - 1
            
            for threat_row, threat_col, is_odd in opp_threats:
                if threat_col == col and threat_row == above_row:
                    score -= 100
                    break
            
            for threat_row, threat_col, is_odd in my_threats:
                if threat_col == col and threat_row == above_row:
                    score += 90
                    break
        
        for row, col, is_odd in my_threats:
            playable = self._get_playable_row(board, col)
            if playable >= 0 and playable < row:
                cells_between = row - playable
                if cells_between % 2 == 0:
                    has_opp_threat_between = False
                    for check_row in range(playable, row):
                        if (check_row, col) in opp_threat_positions:
                            has_opp_threat_between = True
                            break
                    if not has_opp_threat_between:
                        is_favorable = (self.player == Board.PLAYER1 and is_odd) or \
                                       (self.player == Board.PLAYER2 and not is_odd)
                        if is_favorable:
                            score += 120
        
        return score

    def _order_moves(self, board: Board, valid_moves: list, is_maximizing: bool) -> list:
        move_scores = []
        player = self.player if is_maximizing else self.opponent
        
        for col in valid_moves:
            score = 0
            
            if col == 3:
                score += 10
            elif col in [2, 4]:
                score += 5
            elif col in [1, 5]:
                score += 2
            
            new_board = board.copy()
            new_board.drop_piece(col, player)
            if new_board.check_winner() == player:
                score += 1000
            
            opponent = self.opponent if is_maximizing else self.player
            test_board = board.copy()
            test_board.drop_piece(col, opponent)
            if test_board.check_winner() == opponent:
                score += 500
            
            move_scores.append((col, score))
        
        move_scores.sort(key=lambda x: x[1], reverse=True)
        return [col for col, _ in move_scores]

    def get_move(self, board: Board) -> int:
        valid_moves = board.get_valid_moves()
        if len(valid_moves) == 1:
            return valid_moves[0]
        
        for col in valid_moves:
            new_board = board.copy()
            new_board.drop_piece(col, self.player)
            if new_board.check_winner() == self.player:
                return col
        
        for col in valid_moves:
            new_board = board.copy()
            new_board.drop_piece(col, self.opponent)
            if new_board.check_winner() == self.opponent:
                return col
        
        depth = self._get_dynamic_depth(board)
        best_score = float('-inf')
        best_moves = []
        
        ordered_moves = self._order_moves(board, valid_moves, True)
        
        for col in ordered_moves:
            new_board = board.copy()
            new_board.drop_piece(col, self.player)
            score = self._minimax(new_board, depth - 1, float('-inf'), float('inf'), False)
            
            if score > best_score:
                best_score = score
                best_moves = [col]
            elif score == best_score:
                best_moves.append(col)
        
        center_moves = [m for m in best_moves if m == 3]
        if center_moves:
            return center_moves[0]
        return best_moves[0] if best_moves else valid_moves[0]

    def _minimax(self, board: Board, depth: int, alpha: float, beta: float, is_maximizing: bool) -> float:
        board_hash = self._board_hash(board)
        
        if board_hash in self.transposition_table:
            stored_score, stored_depth, flag = self.transposition_table[board_hash]
            if stored_depth >= depth:
                if flag == self.EXACT:
                    return stored_score
                elif flag == self.LOWER_BOUND:
                    alpha = max(alpha, stored_score)
                elif flag == self.UPPER_BOUND:
                    beta = min(beta, stored_score)
                if alpha >= beta:
                    return stored_score
        
        winner = board.check_winner()
        if winner == self.player:
            return 100000 + depth
        if winner == self.opponent:
            return -100000 - depth
        if board.is_full() or depth == 0:
            return self._evaluate_board(board)
        
        valid_moves = board.get_valid_moves()
        ordered_moves = self._order_moves(board, valid_moves, is_maximizing)
        
        original_alpha = alpha
        
        if is_maximizing:
            max_eval = float('-inf')
            for col in ordered_moves:
                new_board = board.copy()
                new_board.drop_piece(col, self.player)
                eval_score = self._minimax(new_board, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            
            if max_eval <= original_alpha:
                flag = self.UPPER_BOUND
            elif max_eval >= beta:
                flag = self.LOWER_BOUND
            else:
                flag = self.EXACT
            self.transposition_table[board_hash] = (max_eval, depth, flag)
            
            return max_eval
        else:
            min_eval = float('inf')
            for col in ordered_moves:
                new_board = board.copy()
                new_board.drop_piece(col, self.opponent)
                eval_score = self._minimax(new_board, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            
            if min_eval >= beta:
                flag = self.LOWER_BOUND
            elif min_eval <= original_alpha:
                flag = self.UPPER_BOUND
            else:
                flag = self.EXACT
            self.transposition_table[board_hash] = (min_eval, depth, flag)
            
            return min_eval

    def _evaluate_board(self, board: Board) -> float:
        score = 0.0
        
        center_col = Board.COLS // 2
        center_count = sum(1 for row in range(Board.ROWS) if board.grid[row][center_col] == self.player)
        score += center_count * 6
        
        for col in [2, 4]:
            adj_count = sum(1 for row in range(Board.ROWS) if board.grid[row][col] == self.player)
            score += adj_count * 3
        
        score += self._evaluate_lines(board)
        
        score += self._evaluate_threats(board)
        
        score += self._detect_zugzwang(board)
        
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
            score += 1000
        elif player_count == 3 and empty_count == 1:
            score += 50
        elif player_count == 2 and empty_count == 2:
            score += 10
        
        if opponent_count == 4:
            score -= 1000
        elif opponent_count == 3 and empty_count == 1:
            score -= 80
        elif opponent_count == 2 and empty_count == 2:
            score -= 8
        
        return score
