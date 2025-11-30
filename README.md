# Console Connect 4

A console-based implementation of the classic Connect Four game built in Python. Features a clean terminal interface using ASCII box-drawing characters and colorful display using Colorama.

## Features

- **Two Game Modes**
  - Player vs Player: Two human players take turns
  - Player vs Computer: Play against an AI opponent using the Minimax algorithm

- **Clean Terminal UI**
  - ASCII box-drawing characters for the game board
  - Color-coded pieces (Red and Yellow)
  - Welcome screen with game rules
  - Clear screen between moves for clean gameplay

- **Smart AI Opponent**
  - Minimax algorithm with alpha-beta pruning
  - Depth-limited search (6 levels)
  - Strategic position evaluation

## Requirements

- Python 3.6+
- Colorama

## Installation

1. Clone the repository:
```bash
git clone https://github.com/paarthsiloiya/console-connect-4.git
cd console-connect-4
```

2. Install dependencies:
```bash
pip install colorama
```

## Usage

Run the game from the `src` directory:

```bash
cd src
python main.py
```

### Controls

- Enter a column number (1-7) to drop your piece
- Press `Q` to quit during gameplay
- Press `Y` or `N` when prompted to play again

## Project Structure

```
console-connect-4/
├── README.md
├── LICENSE
├── docs/
│   └── MINIMAX.md          # Documentation for the AI algorithm
└── src/
    ├── main.py             # Entry point and main game loop
    ├── game.py             # Game state management
    ├── board.py            # Board representation and logic
    ├── display.py          # Terminal UI rendering
    └── ai.py               # Minimax AI implementation
```

## How to Play

1. Launch the game and select a mode from the menu
2. Players take turns dropping colored discs into a 7-column, 6-row grid
3. Pieces fall to the lowest available position in the selected column
4. The first player to connect four discs in a row (horizontally, vertically, or diagonally) wins
5. If the board fills up with no winner, the game is a draw

## Game Display

```
   1   2   3   4   5   6   7 
  ┌───┬───┬───┬───┬───┬───┬───┐
  │   │   │   │   │   │   │   │
  ├───┼───┼───┼───┼───┼───┼───┤
  │   │   │   │   │   │   │   │
  ├───┼───┼───┼───┼───┼───┼───┤
  │   │   │   │ ● │   │   │   │
  ├───┼───┼───┼───┼───┼───┼───┤
  │   │   │ ● │ ● │   │   │   │
  ├───┼───┼───┼───┼───┼───┼───┤
  │   │ ● │ ● │ ● │   │   │   │
  ├───┼───┼───┼───┼───┼───┼───┤
  │ ● │ ● │ ● │ ● │   │   │   │
  └───┴───┴───┴───┴───┴───┴───┘
```

## AI Documentation

For detailed information about the Minimax algorithm and evaluation function used by the AI, see [MINIMAX.md](docs/MINIMAX.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.