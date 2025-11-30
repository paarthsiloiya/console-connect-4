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

- **Alpha**: Best score the maximizing player can guarantee (starts at -∞)
- **Beta**: Best score the minimizing player can guarantee (starts at +∞)

### Pruning Condition

When `beta <= alpha`, we can stop evaluating further branches because:
- The minimizing player already has a better option elsewhere
- The maximizing player won't choose this path

### Benefits

Alpha-beta pruning can reduce the number of nodes evaluated from O(b^d) to O(b^(d/2)) in the best case, where:
- b = branching factor (average number of valid moves)
- d = search depth

## Search Depth

The AI uses a maximum depth of **6 moves** ahead. This provides:
- Good strategic play
- Reasonable computation time
- Balance between performance and intelligence

## Evaluation Function

When the search reaches maximum depth without finding a terminal state, the board is evaluated using a heuristic function.

### Scoring Components

#### 1. Terminal States

```
Win for AI:      +10000 + depth
Loss for AI:     -10000 - depth
Draw:            0
```

The depth bonus ensures the AI prefers winning sooner and losing later.

#### 2. Center Column Control

```
Center pieces: +3 points each
```

Center column control is valuable in Connect 4 because:
- More potential winning combinations pass through the center
- Provides flexibility for future moves

#### 3. Window Evaluation

The board is scanned using a sliding window of 4 cells in all directions:
- Horizontal
- Vertical
- Diagonal (both directions)

Each window is scored based on piece counts:

| AI Pieces | Empty | Opponent | Score |
|-----------|-------|----------|-------|
| 4         | 0     | 0        | +100  |
| 3         | 1     | 0        | +5    |
| 2         | 2     | 0        | +2    |
| 0         | 1     | 3        | -4    |

### Window Patterns Explained

#### Four in a Row (+100)
```
[ ● ● ● ● ]  → Winning position
```

#### Three with Opening (+5)
```
[ ● ● ● _ ]  → One move from winning
```

#### Two with Openings (+2)
```
[ ● ● _ _ ]  → Potential threat
```

#### Blocking Opponent (-4)
```
[ ○ ○ ○ _ ]  → Must block this threat
```

## Move Selection

The AI evaluates all valid moves and selects the one with the highest score:

```
1. Generate all valid column moves
2. For each move:
   a. Create a copy of the board
   b. Make the move
   c. Run minimax to get score
3. Collect all moves with the best score
4. Randomly select one (adds variety when moves are equal)
```

## Example Game Tree

```
                Current Board
                   Score: ?
                 /    |    \
                /     |     \
            Col 1    Col 4    Col 7
             /          |      \
         Opponent   Opponent   Opponent
        responds    responds   responds
         /    \     /    \     /    \
       ...   ...  ...   ...  ...   ...
        ↓           ↓           ↓
    Evaluate    Evaluate    Evaluate
```

## Complexity Analysis

### Time Complexity

- Without pruning: O(b^d) where b ≈ 7, d = 6
- With alpha-beta: O(b^(d/2)) in best case

### Space Complexity

- O(d) for the recursion stack
- O(d × board_size) for board copies

## Strengths and Limitations

### Strengths

- Guaranteed optimal play against another optimal player
- Alpha-beta pruning significantly reduces search space
- Evaluation function captures key Connect 4 strategies

### Limitations

- Depth limit may miss long-term strategies
- Evaluation is heuristic, not perfect
- Cannot learn or adapt during gameplay

## Further Improvements

Possible enhancements to the AI:

1. **Transposition Tables**: Cache evaluated positions to avoid redundant calculations
2. **Iterative Deepening**: Start with shallow search and progressively deepen
3. **Move Ordering**: Evaluate center columns first for better pruning
4. **Opening Book**: Pre-computed best moves for opening positions
5. **Dynamic Depth**: Increase depth for critical positions
