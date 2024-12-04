#!/usr/bin/env python3
from collections import Counter

# Fix path so we can do a relative import: https://stackoverflow.com/a/27876800
if __name__ == "__main__":
    if not __package__:
        import sys
        from os import path

        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

        # Relative imports here
        from util import *

INPUT_FILE = "4-input.txt"
# INPUT_FILE='4a-example.txt'
# INPUT_FILE='4a2-example.txt'


def xmas_checker(matrix: list[str], cur_row: int, cur_col: int):
    """
    Check if "XMAS" appears in all orientations from the specified position

    The orientations can be horizontal, vertical, and diagonal

    May also appear backwards
    """
    def helper(
        matrix: list[str], cur_row: int, cur_col: int, row_incr: int, col_incr: int
    ):
        CHECK_WORD = "XMAS"
        for i in range(len(CHECK_WORD)):
            if matrix[cur_row + i * row_incr][cur_col + i * col_incr] != CHECK_WORD[i]:
                return False
        return True
    return [
        helper(matrix, cur_row, cur_col, row_incr=0, col_incr=1),
        helper(matrix, cur_row, cur_col, row_incr=0, col_incr=-1),
        helper(matrix, cur_row, cur_col, row_incr=1, col_incr=0),
        helper(matrix, cur_row, cur_col, row_incr=-1, col_incr=0),
        helper(matrix, cur_row, cur_col, row_incr=1, col_incr=1),
        helper(matrix, cur_row, cur_col, row_incr=-1, col_incr=-1),
        helper(matrix, cur_row, cur_col, row_incr=1, col_incr=-1),
        helper(matrix, cur_row, cur_col, row_incr=-1, col_incr=1),
    ]


def x_mas_checker(matrix: list[str], cur_row: int, cur_col: int):
    """
    Checks that mas forms an x shape

    e.g.
    ```
    M S
     A
    M S
    ```
    """

    if matrix[cur_row][cur_col] != "A":
        return False

    side1_count = Counter(
        [matrix[cur_row - 1][cur_col - 1], matrix[cur_row + 1][cur_col + 1]]
    )
    side2_count = Counter(
        [matrix[cur_row + 1][cur_col - 1], matrix[cur_row - 1][cur_col + 1]]
    )
    return (
        side1_count["M"]
        == side1_count["S"]
        == side2_count["M"]
        == side2_count["S"]
        == 1
    )


# Add padding and upper case input
input = ["." * 5 + line.upper() + "." * 5 for line in get_file_contents(INPUT_FILE)[0]]
input = ["." * len(input[0])] * 5 + input + ["." * len(input[0])] * 5


def answer_a(input: list[str]):
    res = []
    for row_i, row in enumerate(input):
        for col_i, col in enumerate(row):
            if "X" == col:
                res.extend(xmas_checker(input, row_i, col_i))
    return res


def answer_b(input: list[str]):
    return [
        x_mas_checker(input, row_i, col_i)
        for row_i, row in enumerate(input)
        for col_i, col in enumerate(row)
    ]


print("a:", sum(answer_a(input)))
print("b:", sum(answer_b(input)))
