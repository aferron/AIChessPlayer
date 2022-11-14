# Binary Board Representations
> The following integers represent binary states for the chess board. These variables are used in order to check membership in sections of the board for heuristic purposes.

> To see if a pawn is in any position in the board a bitwise and can be used with any of the state representations. For example BB_BACKRANKS is a binary representations where both back rows are full of pawns. Using a bitwise and with another board will return 0 if none of the ones overlap, and nonzero otherwise.

1. Victory - This will check if a pawn has reached the end of the board.
    - chess.BB_BACK_RANKS
2. Any specific square can be selected using its identifier BB_Xy where the letter (X) is a column position and the number(y) is a row position. Example:
    - chess.BB_A1
    - chess.BB_b8
    - Tools:
        * Convert a letter to the next: chr(ord('A') + 1)
3. Each column full of pawns. This can be used to see if the oponent has an oposing pawn in the row ahead.
    - COLUMN A    72340172838076673
    - COLUMN B    144680345676153346
    - COLUMN C    289360691352306692
    - COLUMN D    578721382704613384
    - COLUMN E    1157442765409226768
    - COLUMN F    2314885530818453536
    - COLUMN G    4629771061636907072
    - COLUMN H    9259542123273814144
