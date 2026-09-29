# Mutually Assured Draw

This is a small side project I built to explore machine learning.

It is inspired by the film *WarGames* (1983), in which a young boy hacks into a computer to play games. Unfortunately, the computer is connected to NORAD, and he chooses "Thermonuclear War". The computer then begins trying to start World War III.

Fortunately, they convince it that mutually assured destruction is futile by having it play Tic-Tac-Toe: a game that ends in a draw when both players play optimally.

I began by implementing the game simply, then worked my way from random play through Minimax and Alpha-Beta to Q-learning, which reaches the famous conclusion.

## Features

- Immutable board and game-state model
- Typed domain concepts using enums, `NewType`, and dataclasses
- Random, Minimax, Alpha-Beta, and tabular Q-learning players
- Alpha-Beta pruning with caching of fully evaluated positions
- Q-learning with epsilon-greedy exploration
- Self-play and opponent-based training
- Compact, replayable match logs
- Head-to-head evaluation with swapped X/O assignments
- Tests for game rules, players, training, and tournament behavior

## Installation

Requires Python 3.11 or later and [uv](https://docs.astral.sh/uv/).

```bash
git clone <repository-url>
cd mutually-assured-draw
uv sync
```

## Run the tests:

```bash
uv run pytest
```

## Usage
Run the WOPR-inspired training experiment:

```bash
uv run python scripts/wopr.py
```

The script trains a Q-learning player against Alpha-Beta, periodically evaluates it with exploration disabled, and stops once it reaches its configured no-loss target.

A successful run ends with:

```bash
A strange game. The only winning move is not to play.
```

## Design Notes
### Game model
Board and GameState are immutable. Applying a move returns a new GameState, which makes search and training transitions predictable.

Moves use the Cell enum:

```bash
0 | 1 | 2
--+---+--
3 | 4 | 5
--+---+--
6 | 7 | 8
```

Match logs store the starting player, ordered cells, and final outcome. Intermediate states can be reconstructed by replaying the moves.

### Learning and evaluation
The Q-learning player stores action values in a table keyed by board state and action. During training it uses epsilon-greedy exploration; during evaluation, exploration is disabled.

Training and evaluation are deliberately separate. Training updates the Q-table, while tournament functions only play and report matches.

### Alpha-Beta caching
Multiple move orders can reach the same Tic-Tac-Toe position. Alpha-Beta caches terminal and fully evaluated positions.

Scores from pruned branches are not cached as exact values, because pruning establishes a bound rather than necessarily the position's exact minimax score.

## Lessons Learned
- Tabular Q-learning is machine learning: it learns action values from experience rather than receiving hard-coded move rules.
- Against optimal Tic-Tac-Toe, avoiding losses is a more meaningful training objective than seeking wins.
- Evaluation samples can be noisy; multiple successful evaluations give stronger evidence than one small no-loss result.
- Alpha-Beta pruning improves search, and caching repeated positions provides a substantial additional speedup.
- Separating game mechanics, agents, training, and evaluation keeps the project easier to test and extend.

## Roadmap

### Phase 1: Core Search & Baseline
- [x] Add `Board.available_cells()` helper for move generation.
- [x] Implement `RandomPlayer` for baseline automated play and tests.
- [x] Define evaluation score types / heuristics (e.g. depth-weighted outcomes).
- [x] Implement vanilla recursive `MinimaxPlayer`.
- [x] Implement `AlphaBetaPlayer` (no transposition caching because it adds complexity without too much benefit).
- [x] Suite of validation tests:
  - Solver blocks immediate opponent wins.
  - Solver takes immediate winning lines.
  - Minimax vs. Minimax always resolves to `Outcome.DRAW` across both turn orders.

### Phase 2: Statistical & Learning Approaches
- [canceled] Implement **Monte Carlo Tree Search (MCTS)**:
  - Selection (UCT - Upper Confidence bounds for Trees).
  - Expansion.
  - Simulation (rollouts via `RandomPlayer`).
  - Backpropagation.
- [x] Implement **Tabular Q-Learning (Reinforcement Learning)**:
  - Q-table keyed by board state strings (`Board.serialize()`).
  - Epsilon-greedy exploration policy during self-play training.
  - Reward mapping (+1 for win, 0 for draw, -1 for loss).
- [x] Arena / Tournament runner:
  - Pit every agent against one another (Random vs MCTS vs Q-Learning vs Minimax).
  - Generate win/loss/draw outcome matrices.

- [x] Implement Tabular Q-Learning (Reinforcement Learning):
  - Q-table and epsilon-greedy training
  - Win/draw/loss reward mapping
  - Training against Alpha-Beta
- [x] Implement head-to-head tournament evaluation:
  - Swapped X/O assignments for fairness
  - Aggregated win/loss/draw results
- [ ] Extend tournament evaluation:
  - Round-robin scheduling across all agents
  - Win/loss/draw matrix output