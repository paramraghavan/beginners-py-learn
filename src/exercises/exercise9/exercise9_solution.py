'''
ll Test Cases:
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
'''

def reversi(board):
    result = None

    spc_char = ' '

    # stores the indexes of all the spaces
    list_ctr = []
    counter = 0;
    for item in board:
        if item == spc_char:
            list_ctr.append(counter)
        counter += 1

    print(list_ctr)

    pos = 0
    count_of_O = 0
    board_len = len(board)
    # looping over space positions
    for item in list_ctr:
        print(item)
        local_pos = item
        local_count_of_O = 0
        # left
        if local_pos is not 0:
            for i in range(local_pos - 1, -1, -1):
                print(i)
                if 'O' == board[i]:
                    local_count_of_O += 1
                elif 'X' == board[i]:
                    # terminate match
                    if local_count_of_O > 0:
                        # check if valid
                        if local_count_of_O > count_of_O:
                            count_of_O = local_count_of_O
                            pos = local_pos
                    break
                else:
                    break

        print(f'local_pos: {local_pos}')

        if local_pos == board_len:
            continue
        # right
        local_count_of_O = 0
        for i in range(local_pos + 1, board_len, 1):
            print(i)
            if 'O' == board[i]:
                local_count_of_O += 1
            elif 'X' == board[i]:
                # terminate match
                if local_count_of_O > 0:
                    # check if valid
                    if local_count_of_O > count_of_O:
                        count_of_O = local_count_of_O
                        pos = local_pos
                break
            else:
                break

        result = (pos, count_of_O)

    return result

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

result = reversi(board2)
if result is not None:
    print(result[0], result[1])