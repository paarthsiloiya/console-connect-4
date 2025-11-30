import os
from colorama import Fore, Style, init
from board import Board

init()


class Display:
    HORIZONTAL = '\u2500'
    VERTICAL = '\u2502'
    TOP_LEFT = '\u250C'
    TOP_RIGHT = '\u2510'
    BOTTOM_LEFT = '\u2514'
    BOTTOM_RIGHT = '\u2518'
    T_DOWN = '\u252C'
    T_UP = '\u2534'
    T_RIGHT = '\u251C'
    T_LEFT = '\u2524'
    CROSS = '\u253C'
    
    PLAYER1_PIECE = '\u25CF'
    PLAYER2_PIECE = '\u25CF'
    EMPTY_PIECE = ' '

    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def get_piece_display(cell: int) -> str:
        if cell == Board.PLAYER1:
            return f"{Fore.RED}{Display.PLAYER1_PIECE}{Style.RESET_ALL}"
        elif cell == Board.PLAYER2:
            return f"{Fore.YELLOW}{Display.PLAYER2_PIECE}{Style.RESET_ALL}"
        return Display.EMPTY_PIECE

    @staticmethod
    def render_board(board: Board, highlight_col: int = -1):
        Display.clear_screen()
        Display.print_header()
        
        print(f"\n{Fore.CYAN}  ", end="")
        for col in range(Board.COLS):
            if col == highlight_col:
                print(f" {Fore.GREEN}{col + 1}{Style.RESET_ALL}{Fore.CYAN} ", end="")
            else:
                print(f"  {col + 1} ", end="")
        print(Style.RESET_ALL)
        
        print(f"  {Display.TOP_LEFT}", end="")
        for col in range(Board.COLS):
            print(Display.HORIZONTAL * 3, end="")
            if col < Board.COLS - 1:
                print(Display.T_DOWN, end="")
        print(Display.TOP_RIGHT)
        
        for row in range(Board.ROWS):
            print(f"  {Display.VERTICAL}", end="")
            for col in range(Board.COLS):
                piece = Display.get_piece_display(board.grid[row][col])
                print(f" {piece} {Display.VERTICAL}", end="")
            print()
            
            if row < Board.ROWS - 1:
                print(f"  {Display.T_RIGHT}", end="")
                for col in range(Board.COLS):
                    print(Display.HORIZONTAL * 3, end="")
                    if col < Board.COLS - 1:
                        print(Display.CROSS, end="")
                print(Display.T_LEFT)
        
        print(f"  {Display.BOTTOM_LEFT}", end="")
        for col in range(Board.COLS):
            print(Display.HORIZONTAL * 3, end="")
            if col < Board.COLS - 1:
                print(Display.T_UP, end="")
        print(Display.BOTTOM_RIGHT)
        print()

    @staticmethod
    def print_header():
        title = """
   ____                            _     _  _   
  / ___|___  _ __  _ __   ___  ___| |_  | || |  
 | |   / _ \\| '_ \\| '_ \\ / _ \\/ __| __| | || |_ 
 | |__| (_) | | | | | | |  __/ (__| |_  |__   _|
  \\____\\___/|_| |_|_| |_|\\___|\\___|\\__|    |_|  
"""
        print(f"{Fore.CYAN}{title}{Style.RESET_ALL}")

    @staticmethod
    def print_welcome():
        Display.clear_screen()
        Display.print_header()
        
        print(f"\n{Fore.WHITE}{'=' * 50}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Welcome to Connect 4!{Style.RESET_ALL}".center(60))
        print(f"{Fore.WHITE}{'=' * 50}{Style.RESET_ALL}\n")
        
        print(f"  {Fore.RED}{Display.PLAYER1_PIECE}{Style.RESET_ALL} = Player 1 (Red)")
        print(f"  {Fore.YELLOW}{Display.PLAYER2_PIECE}{Style.RESET_ALL} = Player 2 (Yellow)\n")
        
        print(f"  {Fore.WHITE}Rules:{Style.RESET_ALL}")
        print("  - Players take turns dropping pieces")
        print("  - First to connect 4 in a row wins")
        print("  - Rows can be horizontal, vertical, or diagonal\n")
        
        print(f"{Fore.WHITE}{'=' * 50}{Style.RESET_ALL}\n")

    @staticmethod
    def print_menu() -> str:
        print(f"  {Fore.CYAN}Select Game Mode:{Style.RESET_ALL}\n")
        print(f"  {Fore.WHITE}[1]{Style.RESET_ALL} Two Players")
        print(f"  {Fore.WHITE}[2]{Style.RESET_ALL} Player vs Computer")
        print(f"  {Fore.WHITE}[Q]{Style.RESET_ALL} Quit\n")
        return input(f"  {Fore.GREEN}Enter choice: {Style.RESET_ALL}").strip().lower()

    @staticmethod
    def print_turn(player: int, is_computer: bool = False):
        if is_computer:
            print(f"  {Fore.MAGENTA}Computer is thinking...{Style.RESET_ALL}")
        else:
            color = Fore.RED if player == Board.PLAYER1 else Fore.YELLOW
            name = "Player 1" if player == Board.PLAYER1 else "Player 2"
            print(f"  {color}{name}'s turn{Style.RESET_ALL}")

    @staticmethod
    def print_winner(player: int, is_computer: bool = False):
        if is_computer and player == Board.PLAYER2:
            print(f"\n  {Fore.MAGENTA}{'*' * 30}{Style.RESET_ALL}")
            print(f"  {Fore.MAGENTA}  Computer wins!{Style.RESET_ALL}")
            print(f"  {Fore.MAGENTA}{'*' * 30}{Style.RESET_ALL}\n")
        else:
            color = Fore.RED if player == Board.PLAYER1 else Fore.YELLOW
            name = "Player 1" if player == Board.PLAYER1 else "Player 2"
            print(f"\n  {color}{'*' * 30}{Style.RESET_ALL}")
            print(f"  {color}  {name} wins!{Style.RESET_ALL}")
            print(f"  {color}{'*' * 30}{Style.RESET_ALL}\n")

    @staticmethod
    def print_draw():
        print(f"\n  {Fore.WHITE}{'*' * 30}{Style.RESET_ALL}")
        print(f"  {Fore.WHITE}  It's a draw!{Style.RESET_ALL}")
        print(f"  {Fore.WHITE}{'*' * 30}{Style.RESET_ALL}\n")

    @staticmethod
    def get_move_input() -> str:
        return input(f"  {Fore.GREEN}Enter column (1-7) or 'q' to quit: {Style.RESET_ALL}").strip().lower()

    @staticmethod
    def print_invalid_move():
        print(f"  {Fore.RED}Invalid move! Try again.{Style.RESET_ALL}")

    @staticmethod
    def print_computer_move(col: int):
        print(f"  {Fore.MAGENTA}Computer played column {col + 1}{Style.RESET_ALL}")

    @staticmethod
    def print_play_again() -> str:
        return input(f"  {Fore.GREEN}Play again? (y/n): {Style.RESET_ALL}").strip().lower()
