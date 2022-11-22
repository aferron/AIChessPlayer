# AIChessPlayer
**An exploration of methods to improve the classic Artificial Intelligence algorithm Minimax as used by an adversial chess-playing agent**
---
## Install Requirements:
```bash
# Used libraries include chess, gmpy2, and numpy.
# The node class within also requires python 3.7+.
pip install -r requirements.txt
```
---
## Chess
> The name of the game is pawn chess. Each player starts with a row of pawns with all of the normal legal moves. If one pawn gets to the other end of the board the game is over. If there is a stalemate they tie.

> This project uses the python [Chess Library](https://python-chess.readthedocs.io/en/latest/).

> The building block of the chess library is a 64 bit integer state representation. To track all pawns for a particular player for example each 1 or 0 in the binary of the integer corresponds to a position on the board. As such, each player has an integer to track their pawns, rooks, knights, bishops, king, and queen.

>Using binary representations decreases processing time.

```python
# Binary representations where each column is full of ones
# and each 1 represents a pawn. The binary itself is
# read from the top row right to left. This has been
# adjusted to match the game for viewing purposes.
# See STATEVARS.md for more state representations.

COLUMN H: int representation: 9259542123273814144
COLUMN H: chess.board('7p/7p/7p/7p/7p/7p/7p/7p')
# [[0 0 0 0 0 0 0 1]
#  [0 0 0 0 0 0 0 1]
#  [0 0 0 0 0 0 0 1]
#  [0 0 0 0 0 0 0 1]
#  [0 0 0 0 0 0 0 1]
#  [0 0 0 0 0 0 0 1]
#  [0 0 0 0 0 0 0 1]
#  [0 0 0 0 0 0 0 1]]
```
---
### Environment
> The created environment contains a customized board and game class to adjust for the nuances of pawn chess. The victory condition has been replaced in addition to the move mechanics - a custom class has been used to simplify the move making process.
---
### Movement
> Movement is controlled using normal mechanics example: A2 to A4. Using our own class called __make_a_move a player can move a piece from position 1 to position 2.
```python
__make_a_move(chess.A2, chess.A4)
```
---
### Victory
> Victory is defined by a pawn making it to the other side. This is checked using a flag in the chess library called BB_BACKRANKS. Doing a bitwise 'and' with this and the position of all pawns for a player will return 0 if no pawn has made it to the back and a different positive integer otherwise.
---
### Algorithms
1. Minimax
    - Alpha Beta Pruning
---
### Heuristics

---
### Tools
- Board to Array: Convert any 64 bit int into a 1 or 2d array for binary free heuristics processing.
