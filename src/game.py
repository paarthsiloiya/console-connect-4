from board import Board
from display import Display
from ai import AI


class Game:
    def __init__(self, vs_computer: bool = False):
        self.board = Board()
        self.current_player = Board.PLAYER1
        self.vs_computer = vs_computer
        self.ai = AI(Board.PLAYER2) if vs_computer else None
        self.game_over = False
        self.winner = Board.EMPTY
        self.last_computer_move = -1

    def switch_player(self):
        self.current_player = Board.PLAYER2 if self.current_player == Board.PLAYER1 else Board.PLAYER1

    def make_move(self, col: int) -> bool:
        if self.board.drop_piece(col, self.current_player):
            winner = self.board.check_winner()
            if winner != Board.EMPTY:
                self.game_over = True
                self.winner = winner
            elif self.board.is_full():
                self.game_over = True
            else:
                self.switch_player()
            return True
        return False

    def computer_move(self) -> int:
        if self.ai and self.current_player == Board.PLAYER2:
            col = self.ai.get_move(self.board)
            self.make_move(col)
            return col
        return -1

    def play(self) -> bool:
        while not self.game_over:
            Display.render_board(self.board)
            
            is_computer_turn = self.vs_computer and self.current_player == Board.PLAYER2
            Display.print_turn(self.current_player, is_computer_turn, self.vs_computer)
            
            if is_computer_turn:
                self.last_computer_move = self.computer_move()
            else:
                if self.last_computer_move >= 0:
                    Display.print_computer_move(self.last_computer_move)
                    self.last_computer_move = -1
                move_input = Display.get_move_input()
                
                if move_input == 'q':
                    return False
                
                try:
                    col = int(move_input) - 1
                    if not self.make_move(col):
                        Display.print_invalid_move()
                        input("  Press Enter to continue...")
                except ValueError:
                    Display.print_invalid_move()
                    input("  Press Enter to continue...")
        
        Display.render_board(self.board)
        
        if self.winner != Board.EMPTY:
            is_computer = self.vs_computer and self.winner == Board.PLAYER2
            Display.print_winner(self.winner, is_computer)
        else:
            Display.print_draw()
        
        return True
