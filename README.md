# Mutually Assured Draw

A small Python experiment where two AI players play Tic-Tac-Toe against each other.

The project records games as logs for later evaluation. Its initial goal is to explore whether repeated play converges on consistent draws.

## Status

Early experiment.

## Setup

```bash
python -m venv .venv
```

Activate the environment using your shell or editor, then install dependencies as they are added.

License
TBD

# ToDo: Mutually Assured Draw

## Phase 1: Core Search & Baseline
- [x] Add `Board.available_cells()` helper for move generation.
- [x] Implement `RandomPlayer` for baseline automated play and tests.
- [x] Define evaluation score types / heuristics (e.g. depth-weighted outcomes).
- [x] Implement vanilla recursive `MinimaxPlayer`.
- [x] Implement `AlphaBetaPlayer` (no transposition caching because it adds complexity without too much benefit).
- [x] Suite of validation tests:
  - Solver blocks immediate opponent wins.
  - Solver takes immediate winning lines.
  - Minimax vs. Minimax always resolves to `Outcome.DRAW` across both turn orders.

## Phase 2: Statistical & Learning Approaches
- [ ] Implement **Monte Carlo Tree Search (MCTS)**:
  - Selection (UCT - Upper Confidence bounds for Trees).
  - Expansion.
  - Simulation (rollouts via `RandomPlayer`).
  - Backpropagation.
- [ ] Implement **Tabular Q-Learning (Reinforcement Learning)**:
  - Q-table keyed by board state strings (`Board.serialize()`).
  - Epsilon-greedy exploration policy during self-play training.
  - Reward mapping (+1 for win, 0 for draw, -1 for loss).
- [ ] Arena / Tournament runner:
  - Pit every agent against one another (Random vs MCTS vs Q-Learning vs Minimax).
  - Generate win/loss/draw outcome matrices.