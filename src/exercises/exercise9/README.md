<pre>
You are creating Flippy, an AI that plans to take over the world by solving games having to do with flipping things. 
First the AI must master a one-dimensional game called Reversi.

There are two players, denoted by 'X' (the AI player) and 'O'.The goal is to place a new 'X' in a blank space on the board to 
capture the 'O' tokens between two 'X' tokens (with no spaces in between). A move can capture to the left or the right, not both,
of the newly placed 'X'.

The valid moves in this example are 4, 5, and 13 (the blank spaces):
   0    1    2    3    4    5    6    7    8    9   10   11   12   13
[ 'X', 'O', 'O', 'O', ' ', ' ', 'O', 'O', 'X', 'O', 'X', 'X', 'O', ' ' ]
* Move at 13 (flips 12)                                       <--- 'X' 
* A move at 4 <------ 'X' (flips 1, 2 and 3)      
* Move at 5                 'X' --------->  (flips 6 and 7)

The optimal move captures as many 'O' as possible. In this case, that move is 4, which captures three tokens).

Write a function that, given a board, returns the optimal move for 'X', together with how many tokens are captured.

Test Input:
board1 = [ 'X', 'O', 'O', 'O', ' ', ' ', 'O', 'O', 'X', 'O', 'X', 'X', 'O', ' ' ] => 4,3 (in any order: the best move is at index 4 and captures 3 tokens)
board2 = [ 'X', 'X', 'O', ' ', 'O', 'O', 'O', 'O', ' ', 'X', 'O', 'O', ' ' ] => 12,2
board3 = [ ' ', 'O', 'X'] => 0,1
board4 = [ 'X', 'O' ] => None/null (no open space)
board5 = [ 'X', 'O', ' ' ] => 2,1
board6 = [ 'X', 'O', ' ', 'O', 'O', 'X', 'O', ' ', ' ' ] => 2,2 (if a move captures both left and right we only count the larger
  of the two captures)
board7 = [ 'X', 'O', 'O', ' ', 'O', 'O', 'O' ] => 3,2
board8 = [ 'O', 'O', ' ', 'X' ] => None/null
board9 = [ 'X', 'O', ' ', 'X', 'O', ' ', 'O', 'X' ] => 2,1 or 5,1
board10 = [ 'X', 'O', 'X', ' ' ] => None/null

All Test Cases:
reversi(board1) => 4,3 
reversi(board2) => 12,2
reversi(board3) => 0,1
reversi(board4) => None/null
reversi(board5) => 2,1
reversi(board6) => 2,2
reversi(board7) => 3,2
reversi(board8) => None/null
reversi(board9) => 2,1 or 5,1
reversi(board10) => None/null

Complexity Variables:
n = length of the board
"""

board1 = [ 'X', 'O', 'O', 'O', ' ', ' ', 'O', 'O', 'X', 'O', 'X', 'X', 'O', ' ' ] 
board2 = [ 'X', 'X', 'O', ' ', 'O', 'O', 'O', 'O', ' ', 'X', 'O', 'O', ' ' ] 
board3 = [ ' ', 'O', 'X']
board4 = [ 'X', 'O' ] 
board5 = [ 'X', 'O', ' ' ] 
board6 = [ 'X', 'O', ' ', 'O', 'O', 'X', 'O', ' ', ' ' ] 
board7 = [ 'X', 'O', 'O', ' ', 'O', 'O', 'O' ]
board8 = [ 'O', 'O', ' ', 'X' ]
board9 = [ 'X', 'O', ' ', 'X', 'O', ' ', 'O', 'X' ]
board10 = [ 'X', 'O', 'X', ' ' ]

</pre>
