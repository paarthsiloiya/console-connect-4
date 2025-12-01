# Testing & Benchmarking Documentation

This project includes a comprehensive benchmarking suite to evaluate the performance improvements of the AI. The testing infrastructure is located in the `testing/` directory.

## Overview

The goal of the testing suite is to compare the "Old AI" (basic Minimax) against the "New AI" (Enhanced Minimax with optimizations) to quantify improvements in:
- Win rates
- Decision speed (move time)
- Game duration
- Strategic depth

## Directory Structure

The `testing/` folder contains the following components:

- **`benchmark.py`**: The main script to run automated games between the two AIs.
- **`analysis.ipynb`**: A Jupyter Notebook for visualizing results with graphs and statistics.
- **`old_ai.py`**: The baseline AI implementation (Depth 6, basic evaluation).
- **`new_ai.py`**: The enhanced AI implementation (Dynamic depth, Transposition Tables, Move Ordering, Threat Detection).
- **`board.py`**: A standalone copy of the game logic to ensure tests run independently of the main game source.

## Running Benchmarks

To run a new benchmark comparison:

1. Navigate to the testing directory:
   ```bash
   cd testing
   ```

2. Run the benchmark script:
   ```bash
   python benchmark.py
   ```

### What happens during a benchmark?
- The script runs **50 games** (configurable in `benchmark.py`).
- **Phase 1**: New AI plays as Player 1 (First), Old AI as Player 2.
- **Phase 2**: Old AI plays as Player 1 (First), New AI as Player 2.
- A progress bar shows the status of each phase.
- Results are saved to CSV files in the `results/` directory (or parent `results/` directory).

### Output Files
Two CSV files are generated with a timestamp (e.g., `games_20231025_120000.csv`):
- **`games_*.csv`**: Summary of each game (Winner, Total Moves, Duration, Average Move Times).
- **`moves_*.csv`**: Detailed log of every move (Move Number, Player, Time Taken).

## Analyzing Results

To visualize the data:

1. Open `testing/analysis.ipynb` in VS Code or Jupyter Lab.
2. Run all cells.

The notebook will automatically load the most recent CSV files and generate:
- **Win Rate Charts**: Pie and bar charts showing overall and phase-specific win rates.
- **Time Analysis**: Histograms and boxplots of game durations.
- **Performance Metrics**: Comparison of average move times.
- **Progression Graphs**: How move times change as the game progresses (opening vs endgame).
- **Summary Table**: A detailed statistical breakdown.

## AI Versions Compared

### Old AI (`old_ai.py`)
- **Algorithm**: Minimax with Alpha-Beta Pruning.
- **Depth**: Fixed at 6.
- **Evaluation**: Basic positional scoring (center control, connected pieces).

### New AI (`new_ai.py`)
- **Algorithm**: Minimax with Alpha-Beta Pruning.
- **Optimizations**:
  - **Transposition Tables**: Caches board states to avoid re-calculating identical positions.
  - **Move Ordering**: Explores promising moves (center columns) first to maximize pruning.
  - **Dynamic Depth**: Adjusts search depth (6-12) based on the number of pieces on the board.
  - **Threat Detection**: Identifies immediate threats and "odd/even" parity traps (Zugzwang).
  - **Killer Moves**: Prioritizes winning moves immediately.

## Metrics

The benchmark tracks:
- **Win Rate**: Percentage of games won by each AI.
- **Draw Rate**: Percentage of games ending in a tie.
- **Move Time**: Time taken (in milliseconds) for the AI to decide a move.
- **Game Time**: Total duration of a match.
