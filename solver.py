from copy import deepcopy
from pprint import pprint
from typing import Literal


def print_board(board: list[list[int]]) -> None:
    pprint(board, width=len(board) * 5)


def find_empty(board: list[list[int]]) -> tuple[int, int]:
    length = len(board)
    for i in range(length):
        for j in range(length):
            if board[i][j] == 0:
                return (i, j)

    return ()


def is_valid(board: list[list[int]], num: Literal[1, 2], pos: tuple[int, int]) -> bool:

    def no_three_in_line(board_: list[list[int]]) -> bool:
        for i in board_:
            if len(str(i).replace(" ", "").replace(",", "").replace("111", "").replace("222", "")) != len(board) + 2:
                return False
        return True

    board = deepcopy(board)

    board[pos[0]][pos[1]] = num

    eq_filt = lambda x: x == num

    col_count = len(list(filter(eq_filt, (i for i in board[pos[0]]))))
    row_count = len(list(filter(eq_filt, (i[pos[1]] for i in board))))

    length = len(board)
    half = length // 2
    board_transpose = list(zip(*board))

    # the row count
    for i in board:
        if 0 in i:
            continue
        if not board.count(i) == 1:
            return False

    # the col count
    for i in board_transpose:
        if 0 in i:
            continue

        else:
            if not board_transpose.count(i) == 1:
                return False

    if col_count > half or row_count > half:
        return False

    # check nothing is three in a row
    if not no_three_in_line(board):
        return False

    # check nothing is three in a col
    if not no_three_in_line(board_transpose):
        return False
    return True


def solve(board: list[list[int]]) -> bool:

    find = find_empty(board)

    if not find:
        return True

    else:
        row, col = find
        for i in [1, 2]:
            if is_valid(board, i, find):
                board[row][col] = i

                if solve(board):
                    return True

                board[row][col] = 0

        return False
