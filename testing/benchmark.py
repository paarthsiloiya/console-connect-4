import sys
import time
import csv
import os
from datetime import datetime
from tqdm import tqdm
from board import Board
from new_ai import NewAI
from old_ai import OldAI


class Benchmark:
    def __init__(self, output_dir: str = "results"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.games_csv = os.path.join(output_dir, f"games_{timestamp}.csv")
        self.moves_csv = os.path.join(output_dir, f"moves_{timestamp}.csv")
        
        self.games_data = []
        self.moves_data = []

    def play_game(self, new_ai_first: bool, game_id: int, phase: int) -> dict:
        board = Board()
        game_start = time.time()
        
        if new_ai_first:
            player1_ai = NewAI(Board.PLAYER1)
            player2_ai = OldAI(Board.PLAYER2)
            player1_name = "NewAI"
            player2_name = "OldAI"
        else:
            player1_ai = OldAI(Board.PLAYER1)
            player2_ai = NewAI(Board.PLAYER2)
            player1_name = "OldAI"
            player2_name = "NewAI"
        
        current_player = Board.PLAYER1
        move_num = 0
        
        new_ai_move_times = []
        old_ai_move_times = []
        
        while True:
            move_start = time.time()
            
            if current_player == Board.PLAYER1:
                col = player1_ai.get_move(board)
                ai_name = player1_name
            else:
                col = player2_ai.get_move(board)
                ai_name = player2_name
            
            move_time = time.time() - move_start
            move_num += 1
            
            if ai_name == "NewAI":
                new_ai_move_times.append(move_time)
            else:
                old_ai_move_times.append(move_time)
            
            self.moves_data.append({
                "game_id": game_id,
                "phase": phase,
                "move_num": move_num,
                "player": current_player,
                "ai_name": ai_name,
                "column": col,
                "move_time": move_time
            })
            
            board.drop_piece(col, current_player)
            
            winner = board.check_winner()
            if winner != Board.EMPTY:
                game_time = time.time() - game_start
                
                if winner == Board.PLAYER1:
                    winner_name = player1_name
                else:
                    winner_name = player2_name
                
                game_data = {
                    "game_id": game_id,
                    "phase": phase,
                    "new_ai_first": new_ai_first,
                    "winner": winner_name,
                    "total_moves": move_num,
                    "game_time": game_time,
                    "new_ai_avg_move_time": sum(new_ai_move_times) / len(new_ai_move_times) if new_ai_move_times else 0,
                    "old_ai_avg_move_time": sum(old_ai_move_times) / len(old_ai_move_times) if old_ai_move_times else 0,
                    "new_ai_total_moves": len(new_ai_move_times),
                    "old_ai_total_moves": len(old_ai_move_times)
                }
                self.games_data.append(game_data)
                return game_data
            
            if board.is_full():
                game_time = time.time() - game_start
                game_data = {
                    "game_id": game_id,
                    "phase": phase,
                    "new_ai_first": new_ai_first,
                    "winner": "Draw",
                    "total_moves": move_num,
                    "game_time": game_time,
                    "new_ai_avg_move_time": sum(new_ai_move_times) / len(new_ai_move_times) if new_ai_move_times else 0,
                    "old_ai_avg_move_time": sum(old_ai_move_times) / len(old_ai_move_times) if old_ai_move_times else 0,
                    "new_ai_total_moves": len(new_ai_move_times),
                    "old_ai_total_moves": len(old_ai_move_times)
                }
                self.games_data.append(game_data)
                return game_data
            
            current_player = Board.PLAYER2 if current_player == Board.PLAYER1 else Board.PLAYER1

    def save_csv(self):
        with open(self.games_csv, 'w', newline='') as f:
            if self.games_data:
                writer = csv.DictWriter(f, fieldnames=self.games_data[0].keys())
                writer.writeheader()
                writer.writerows(self.games_data)
        
        with open(self.moves_csv, 'w', newline='') as f:
            if self.moves_data:
                writer = csv.DictWriter(f, fieldnames=self.moves_data[0].keys())
                writer.writeheader()
                writer.writerows(self.moves_data)

    def run_benchmark(self, num_games: int = 100):
        print(f"\n{'=' * 60}")
        print(f"  AI BENCHMARK: New AI vs Old AI ({num_games} games)")
        print(f"{'=' * 60}\n")
        
        games_per_side = num_games // 2
        game_id = 0
        
        print(f"  Phase 1: New AI plays first ({games_per_side} games)")
        phase1_bar = tqdm(total=games_per_side, desc="  Phase 1", unit="game", 
                         bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]')
        
        for i in range(games_per_side):
            game_id += 1
            self.play_game(new_ai_first=True, game_id=game_id, phase=1)
            phase1_bar.update(1)
        
        phase1_bar.close()
        
        print(f"\n  Phase 2: Old AI plays first ({games_per_side} games)")
        phase2_bar = tqdm(total=games_per_side, desc="  Phase 2", unit="game",
                         bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]')
        
        for i in range(games_per_side):
            game_id += 1
            self.play_game(new_ai_first=False, game_id=game_id, phase=2)
            phase2_bar.update(1)
        
        phase2_bar.close()
        
        self.save_csv()
        
        print(f"\n  Results saved to:")
        print(f"    - {self.games_csv}")
        print(f"    - {self.moves_csv}")
        
        self.print_summary()

    def print_summary(self):
        total = len(self.games_data)
        new_wins = sum(1 for g in self.games_data if g["winner"] == "NewAI")
        old_wins = sum(1 for g in self.games_data if g["winner"] == "OldAI")
        draws = sum(1 for g in self.games_data if g["winner"] == "Draw")
        
        phase1_games = [g for g in self.games_data if g["phase"] == 1]
        phase2_games = [g for g in self.games_data if g["phase"] == 2]
        
        phase1_new_wins = sum(1 for g in phase1_games if g["winner"] == "NewAI")
        phase1_old_wins = sum(1 for g in phase1_games if g["winner"] == "OldAI")
        phase1_draws = sum(1 for g in phase1_games if g["winner"] == "Draw")
        
        phase2_new_wins = sum(1 for g in phase2_games if g["winner"] == "NewAI")
        phase2_old_wins = sum(1 for g in phase2_games if g["winner"] == "OldAI")
        phase2_draws = sum(1 for g in phase2_games if g["winner"] == "Draw")
        
        avg_game_time = sum(g["game_time"] for g in self.games_data) / total
        avg_new_move_time = sum(g["new_ai_avg_move_time"] for g in self.games_data) / total
        avg_old_move_time = sum(g["old_ai_avg_move_time"] for g in self.games_data) / total
        
        print(f"\n{'=' * 60}")
        print(f"  SUMMARY")
        print(f"{'=' * 60}")
        print(f"\n  Overall Results ({total} games):")
        print(f"    New AI Wins: {new_wins} ({new_wins/total*100:.1f}%)")
        print(f"    Old AI Wins: {old_wins} ({old_wins/total*100:.1f}%)")
        print(f"    Draws: {draws} ({draws/total*100:.1f}%)")
        print(f"\n  Phase 1 (New AI First):")
        print(f"    New AI Wins: {phase1_new_wins}")
        print(f"    Old AI Wins: {phase1_old_wins}")
        print(f"    Draws: {phase1_draws}")
        print(f"\n  Phase 2 (Old AI First):")
        print(f"    New AI Wins: {phase2_new_wins}")
        print(f"    Old AI Wins: {phase2_old_wins}")
        print(f"    Draws: {phase2_draws}")
        print(f"\n  Timing:")
        print(f"    Avg Game Time: {avg_game_time:.2f}s")
        print(f"    Avg New AI Move Time: {avg_new_move_time*1000:.2f}ms")
        print(f"    Avg Old AI Move Time: {avg_old_move_time*1000:.2f}ms")
        print(f"{'=' * 60}\n")


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
