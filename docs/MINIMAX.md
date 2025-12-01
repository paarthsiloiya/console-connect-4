# Minimax Algorithm in Connect 4

This document explains the Minimax algorithm implementation used by the AI opponent in this Connect 4 game.

## Overview

The Minimax algorithm is a decision-making algorithm used in two-player games. It assumes both players play optimally and works by simulating all possible future game states to find the best move.

## How Minimax Works

### Basic Concept

The algorithm creates a game tree where:
- Each node represents a game state
- Each edge represents a possible move
- Leaf nodes are terminal states (win, loss, or draw) or states at maximum search depth

### The Two Players

- **Maximizing Player (AI)**: Tries to maximize the score
- **Minimizing Player (Opponent)**: Tries to minimize the score

### Algorithm Flow

```
function minimax(board, depth, isMaximizing):
    if game_over or depth == 0:
        return evaluate(board)
    
    if isMaximizing:
        maxScore = -infinity
        for each valid move:
            make move for AI
            score = minimax(board, depth-1, false)
            maxScore = max(maxScore, score)
        return maxScore
    else:
        minScore = +infinity
        for each valid move:
            make move for opponent
            score = minimax(board, depth-1, true)
            minScore = min(minScore, score)
        return minScore
```

## Alpha-Beta Pruning

Our implementation uses alpha-beta pruning to optimize the search. This technique eliminates branches that cannot possibly influence the final decision.

### Parameters

- **Alpha**: Best score the maximizing player can guarantee (starts at -infinity)
- **Beta**: Best score the minimizing player can guarantee (starts at +infinity)

### Pruning Condition

When `beta <= alpha`, we can stop evaluating further branches because:
- The minimizing player already has a better option elsewhere
- The maximizing player won't choose this path

### Benefits

Alpha-beta pruning can reduce the number of nodes evaluated from O(b^d) to O(b^(d/2)) in the best case, where:
- b = branching factor (average number of valid moves)
- d = search depth

## Transposition Table

The AI uses a transposition table (hash table) to cache previously evaluated board positions.

### How It Works

1. Each board position is converted to a unique hash value
2. When a position is evaluated, the result is stored with:
   - The score
   - The depth at which it was evaluated
   - A flag indicating the type of bound (exact, lower, or upper)
3. Before evaluating a position, the table is checked for a cached result

### Bound Types

| Flag | Meaning | Usage |
|------|---------|-------|
| EXACT | The stored score is exact | Return immediately |
| LOWER_BOUND | Score >= stored value | Update alpha |
| UPPER_BOUND | Score <= stored value | Update beta |

### Benefits

- Avoids re-evaluating identical positions reached via different move orders
- Significantly speeds up the search in the mid-to-late game
- Enables deeper searches within the same time

## Move Ordering

Moves are evaluated in a strategic order to maximize alpha-beta pruning efficiency.

### Ordering Heuristics

1. **Immediate wins**: Moves that win the game are checked first (+1000)
2. **Blocking moves**: Moves that block opponent wins (+500)
3. **Center preference**: Center column gets priority (+10)
4. **Adjacent columns**: Columns 2 and 4 get secondary priority (+5)
5. **Edge columns**: Columns 1 and 5 get lower priority (+2)

### Why Order Matters

Good move ordering ensures that the best moves are evaluated first, causing more cutoffs:

```
Without ordering: Evaluate all 7^6 = 117,649 positions
With ordering:    Evaluate ~7^3 = 343 positions (best case)
```

## Dynamic Depth

The search depth adjusts based on the game phase for optimal performance.

### Depth Scaling

| Pieces on Board | Search Depth |
|-----------------|--------------|
| 0-8 (early)     | 6 levels     |
| 9-20 (mid)      | 8 levels     |
| 21-30 (late)    | 10 levels    |
| 31+ (endgame)   | 12 levels    |

### Rationale

- **Early game**: Fewer critical decisions, shallower search is sufficient
- **Mid game**: Tactical play increases, moderate depth needed
- **Late game**: Fewer moves available, deeper search is fast and finds wins

## Evaluation Function

When the search reaches maximum depth without finding a terminal state, the board is evaluated using a heuristic function.

### Scoring Components

#### 1. Terminal States

```
Win for AI:      +100000 + depth
Loss for AI:     -100000 - depth
Draw:            0
```

The depth bonus ensures the AI prefers winning sooner and losing later.

#### 2. Positional Control

```
Center column (3):     +6 points per piece
Adjacent columns (2,4): +3 points per piece
```

Center control is crucial in Connect 4 for flexibility and threat creation.

#### 3. Window Evaluation

The board is scanned using a sliding window of 4 cells in all directions:
- Horizontal
- Vertical
- Diagonal (both directions)

Each window is scored based on piece counts:

| AI Pieces | Empty | Opponent | Score |
|-----------|-------|----------|-------|
| 4         | 0     | 0        | +1000 |
| 3         | 1     | 0        | +50   |
| 2         | 2     | 0        | +10   |
| 0         | 1     | 3        | -80   |
| 0         | 2     | 2        | -8    |

### Window Patterns Explained

#### Four in a Row (+1000)
```
[ AI AI AI AI ]  -> Winning position
```

#### Three with Opening (+50)
```
[ AI AI AI __ ]  -> One move from winning
```

#### Two with Openings (+10)
```
[ AI AI __ __ ]  -> Developing threat
```

#### Blocking Opponent Three (-80)
```
[ OP OP OP __ ]  -> Critical block needed
```

## Advanced Threat-Based Evaluation

The AI implements sophisticated threat detection that goes beyond simple pattern matching.

### Threat Detection

A **threat** is a position where a player has 3 pieces in a line with one empty cell that would complete a win. The AI scans all four directions (horizontal, vertical, both diagonals) to find these threats.

### Odd/Even Threat Theory

In Connect 4, the row parity of a threat is crucial:

- **Odd threats**: Empty winning cell is on an odd row (counting from bottom, 1-indexed)
- **Even threats**: Empty winning cell is on an even row

Due to the alternating nature of play:
- **First player (Red)** benefits from odd threats
- **Second player (Yellow)** benefits from even threats

This is because the first player makes moves on odd turns (1st, 3rd, 5th...) and the second player on even turns.

### Threat Scoring

| Threat Type | Condition | Score |
|-------------|-----------|-------|
| Playable threat | Can win immediately | +500 |
| Favorable parity | Matches player's turn parity | +150 |
| Unfavorable parity | Opposite parity | +80 |
| Opponent playable | Must block now | -450 |
| Opponent favorable | Their parity advantage | -140 |

### Double Threats

When a player has two threats in the same column on adjacent rows, this creates an **unblockable** situation - blocking one threat enables the other:

```
Column 4:
Row 3: [ AI AI AI __ ]  <- Threat 1
Row 2: [ AI AI AI __ ]  <- Threat 2 (adjacent)

Bonus: +300 points
```

## Zugzwang Detection

**Zugzwang** is a situation where any move a player makes worsens their position. In Connect 4, this often occurs when playing a piece sets up the opponent's winning threat.

### How It Works

For each column, the AI simulates:
1. What happens if we play there
2. Does it create a winning cell for the opponent directly above?

```
Before:           After playing col 4:
|   |   |   |     |   |   |   |
|   |   |   |     | W |   |   |  <- Opponent's winning cell activated!
|   |   |   |     | X |   |   |  <- Our piece
| O | O | O |     | O | O | O |
```

### Zugzwang Scoring

| Situation | Score |
|-----------|-------|
| Our move creates opponent threat above | -200 |
| Opponent move creates our threat above | +180 |
| We control threat with favorable parity | +250 |

### Forced Play Detection

The AI also detects when:
- An even number of cells must be filled before reaching a threat
- No opponent threats exist between the playable cell and our threat
- The parity favors us

This indicates a **winning position** even if the win is many moves away.

## Immediate Threat Detection

Before running the full search, the AI checks for:

1. **Winning moves**: If any move wins, take it immediately
2. **Blocking moves**: If opponent can win next turn, block it

This optimization ensures critical moves are never missed and speeds up obvious decisions.

## Example Game Tree

```
              Current Board
                 Score: ?
               /    |    \
              /     |     \
          Col 3     Col 2    Col 4    (ordered by priority)
            /        |          \
        Opponent   Opponent   Opponent
        responds   responds   responds
         /    \     /    \     /    \
       ...   ...  ...   ...  ...   ...
        |           |           |
    [cached]    Evaluate    [pruned]
```

## Complexity Analysis

### Time Complexity

- Without optimizations: O(b^d) where b = 7, d = 6-12
- With alpha-beta: O(b^(d/2)) in best case
- With transposition table: Further reduced by cache hits
- With move ordering: Approaches best-case alpha-beta performance

### Space Complexity

- O(d) for the recursion stack
- O(d x board_size) for board copies
- O(n) for transposition table where n = unique positions evaluated

## Performance Comparison

| Optimization | Nodes Evaluated | Speed Improvement |
|--------------|-----------------|-------------------|
| None         | ~117,000        | 1x (baseline)     |
| Alpha-Beta   | ~10,000         | ~10x              |
| + Move Order | ~2,000          | ~50x              |
| + Trans Table| ~500            | ~200x             |
| + Dynamic D  | Varies          | Adaptive          |

## Strengths

- Near-optimal play in most situations
- Fast decision making with optimizations
- Handles tactical positions well
- Adapts search depth to game phase

## Limitations

- Evaluation is heuristic, not perfect
- Transposition table uses memory
- Cannot learn or adapt during gameplay
- Opening play is reasonable but not perfect

## Further Improvements

Possible enhancements:

1. **Iterative Deepening**: Start shallow and progressively deepen within time limit
2. **Opening Book**: Pre-computed optimal opening moves
3. **Killer Move Heuristic**: Remember moves that caused cutoffs
4. **History Heuristic**: Track historically good moves
5. **Null Move Pruning**: Skip moves to detect weak positions faster
