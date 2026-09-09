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

ToDo:
- Board.is_full() tests.
- A game-state model that tracks the current player and validates turn flow.
- A terminal/log-friendly board formatter.
- A Game loop that accepts moves from a player interface.