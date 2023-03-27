"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None
from copy import deepcopy

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    empty_cnt = 0
    for row in board:
        for xy in row:
            if xy == EMPTY:
                empty_cnt += 1
    if empty_cnt%2:
        return X
    return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = []
    for x, row in enumerate(board):
        for y, xy in enumerate(row):
            if xy == EMPTY:
                actions.append((x,y))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    nuboard = deepcopy(board)
    nuboard[action[0]][action[1]] = player(board)
    return nuboard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # row or column
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != EMPTY:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != EMPTY:
            return board[0][i]
    # diagonal
    if board[1][1] != EMPTY and (board[0][0] == board[1][1] == board[2][2] or \
        board[0][2] == board[1][1] == board[2][0]):
        return board[1][1]
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True;
    for row in board:
        for val in row:
            if val == EMPTY:
                return False

    return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    the_winner = winner(board)
    if the_winner == X:
        return 1
    elif the_winner == O:
        return -1
    return 0

"""
function MAX-VALUE(state):
if TERMINAL(state):
return UTILITY(state)
v = -∞
for action in ACTIONS(state):
v = MAX(v, MIN-VALUE(RESULT(state, action)))
return v
"""
def max_value(board):
    if terminal(board):
        return utility(board)
    v = -100
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
        if v == 1:
            break
    return v

"""
function MIN-VALUE(state):
if TERMINAL(state):
return UTILITY(state)
v = ∞
for action in ACTIONS(state):
v = MIN(v, MAX-VALUE(RESULT(state, action)))
return v
"""
def min_value(board):
    if terminal(board):
        return utility(board)
    v = 100
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
        if v == -1:
            break
    return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    avail_actions = actions(board)
    final_action = (-99, -99)
    if player(board) == 'X':
        v = -100
        for a, action in enumerate(avail_actions):
            vv = min_value(result(board, action))
            if vv > v:
                final_action = action
                v = vv
    else:
        v = 100
        for a, action in enumerate(avail_actions):
            vv = max_value(result(board, action))
            if vv < v:
                final_action = action
                v = vv
    return final_action

