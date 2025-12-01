import sys
from board import Board
from ai import AI as NewAI
from old_ai import AI as OldAI


class Benchmark:
    def __init__(self):
        self.results = {
            "new_ai_wins": 0,
            "old_ai_wins": 0,
            "draws": 0,
            "new_ai_as_p1_wins": 0,
            "new_ai_as_p2_wins": 0,
            "old_ai_as_p1_wins": 0,
            "old_ai_as_p2_wins": 0,
            "total_moves": 0,
            "games_played": 0
        }

    def play_game(self, new_ai_first: bool) -> int:
        board = Board()
        
        if new_ai_first:
            player1_ai = NewAI(Board.PLAYER1)
            player2_ai = OldAI(Board.PLAYER2)
        else:
            player1_ai = OldAI(Board.PLAYER1)
            player2_ai = NewAI(Board.PLAYER2)
        
        current_player = Board.PLAYER1
        moves = 0
        
        while True:
            if current_player == Board.PLAYER1:
                col = player1_ai.get_move(board)
            else:
                col = player2_ai.get_move(board)
            
            board.drop_piece(col, current_player)
            moves += 1
            
            winner = board.check_winner()
            if winner != Board.EMPTY:
                self.results["total_moves"] += moves
                return winner
            
            if board.is_full():
                self.results["total_moves"] += moves
                return 0
            
            current_player = Board.PLAYER2 if current_player == Board.PLAYER1 else Board.PLAYER1

    def run_benchmark(self, num_games: int = 100):
        print(f"\n{'=' * 60}")
        print(f"  AI BENCHMARK: New AI vs Old AI ({num_games} games)")
        print(f"{'=' * 60}\n")
        
        games_per_side = num_games // 2
        
        print(f"  Phase 1: New AI plays first ({games_per_side} games)")
        print(f"  ", end="")
        for i in range(games_per_side):
            winner = self.play_game(new_ai_first=True)
            self.results["games_played"] += 1
            
            if winner == Board.PLAYER1:
                self.results["new_ai_wins"] += 1
                self.results["new_ai_as_p1_wins"] += 1
                print("N", end="")
            elif winner == Board.PLAYER2:
                self.results["old_ai_wins"] += 1
                self.results["old_ai_as_p2_wins"] += 1
                print("O", end="")
            else:
                self.results["draws"] += 1
                print("D", end="")
            
            if (i + 1) % 50 == 0:
                print(f" [{i + 1}]")
                if i + 1 < games_per_side:
                    print("  ", end="")
            sys.stdout.flush()
        
        print(f"\n\n  Phase 2: Old AI plays first ({games_per_side} games)")
        print(f"  ", end="")
        for i in range(games_per_side):
            winner = self.play_game(new_ai_first=False)
            self.results["games_played"] += 1
            
            if winner == Board.PLAYER1:
                self.results["old_ai_wins"] += 1
                self.results["old_ai_as_p1_wins"] += 1
                print("O", end="")
            elif winner == Board.PLAYER2:
                self.results["new_ai_wins"] += 1
                self.results["new_ai_as_p2_wins"] += 1
                print("N", end="")
            else:
                self.results["draws"] += 1
                print("D", end="")
            
            if (i + 1) % 50 == 0:
                print(f" [{i + 1}]")
                if i + 1 < games_per_side:
                    print("  ", end="")
            sys.stdout.flush()
        
        print("\n")
        self.print_results()

    def print_results(self):
        total = self.results["games_played"]
        new_wins = self.results["new_ai_wins"]
        old_wins = self.results["old_ai_wins"]
        draws = self.results["draws"]
        
        new_win_rate = (new_wins / total) * 100 if total > 0 else 0
        old_win_rate = (old_wins / total) * 100 if total > 0 else 0
        draw_rate = (draws / total) * 100 if total > 0 else 0
        avg_moves = self.results["total_moves"] / total if total > 0 else 0
        
        print(f"{'=' * 60}")
        print(f"  RESULTS")
        print(f"{'=' * 60}")
        print()
        print(f"  Total Games: {total}")
        print(f"  Average Moves per Game: {avg_moves:.1f}")
        print()
        print(f"  {'-' * 40}")
        print(f"  Overall Results:")
        print(f"  {'-' * 40}")
        print(f"  New AI Wins:  {new_wins:3d}  ({new_win_rate:5.1f}%)")
        print(f"  Old AI Wins:  {old_wins:3d}  ({old_win_rate:5.1f}%)")
        print(f"  Draws:        {draws:3d}  ({draw_rate:5.1f}%)")
        print()
        print(f"  {'-' * 40}")
        print(f"  Breakdown by Starting Position:")
        print(f"  {'-' * 40}")
        print(f"  New AI as Player 1 (first): {self.results['new_ai_as_p1_wins']} wins")
        print(f"  New AI as Player 2 (second): {self.results['new_ai_as_p2_wins']} wins")
        print(f"  Old AI as Player 1 (first): {self.results['old_ai_as_p1_wins']} wins")
        print(f"  Old AI as Player 2 (second): {self.results['old_ai_as_p2_wins']} wins")
        print()
        
        if new_wins > old_wins:
            improvement = ((new_wins - old_wins) / max(old_wins, 1)) * 100
            print(f"  {'=' * 40}")
            print(f"  NEW AI is STRONGER!")
            print(f"  Win rate improvement: +{improvement:.1f}%")
            print(f"  {'=' * 40}")
        elif old_wins > new_wins:
            print(f"  {'=' * 40}")
            print(f"  OLD AI performed better in this test")
            print(f"  {'=' * 40}")
        else:
            print(f"  {'=' * 40}")
            print(f"  Both AIs performed equally!")
            print(f"  {'=' * 40}")
        print()


def main():
    num_games = 100
    if len(sys.argv) > 1:
        try:
            num_games = int(sys.argv[1])
        except ValueError:
            pass
    
    benchmark = Benchmark()
    benchmark.run_benchmark(num_games)


if __name__ == "__main__":
    main()
