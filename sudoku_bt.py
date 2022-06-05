
import math
import numpy as np


def generate(n):
    """genrates a sudoku table with given dimension of n

    Args:
        n (int): dimension

    Raises:
        Exception: when n is less than 2

    Returns:
        []: list that holds sudoku table ([[]*n]*n)
    """
    if n < 2:
        raise Exception("dimension must be bigger than one!")
    table = np.zeros((n**2, n**2), dtype=np.uint32)
    solve(table)
    return table


def show(table):
    """shows a [[]*n]*n list as a sudoku table

    Args:
        table (list): list that holds sudoku table
    """
    n = table.shape[0]
    nsq = int(math.sqrt(n))
    for x in range(n):
        if x % nsq == 0:
            print()
        for y in range(n):
            if y % nsq == 0:
                print(end="  ")
            print("{ye:3d}".format(ye=table[x, y]), end=" ")
        print()


def puzzle(table, difficulty=50):
    """set 0 value to random elements to make puzzle of a completesudoku table

    Args:
        table (list): list that holds sudoku table
        difficulty (int, optional): Difficulty of puzzle in percent. Defaults to 50.

    Raises:
        Exception: when difficulty is not in [20-80]%

    Returns:
        list: sudoku puzzle table
    """
    n = int(math.sqrt(len(table)))
    puzzle_table = table.copy()
    if(difficulty > 80 and difficulty < 20):
        raise Exception("difficulty is NOT in range [10%,80%]!")
    else:
        remove_num = math.floor((difficulty) / 100 * n**4)
        removed_list = random.sample(range(1, n**4 + 1), remove_num)
        for num in removed_list:
            row = num // n**2 - 1
            col = num % n**2 - 1
            puzzle_table[row][col] = 0
    return puzzle_table


def check(table):
    """check if table is a complete correct sudoku table

    Args:
        table (list): list that holds incomplete sudoku table

    Returns:
        Boolean: True if table is an acceptable answer
    """
    n = int(math.sqrt(len(table)))
    acc_ans = set([k for k in range(1, n**2+1)])
    for row in table:
        if(set(row) == acc_ans):
            pass
        else:
            print("1")
            return False
    for col_num in range(n**2):
        if(set([rows[col_num] for rows in table]) == acc_ans):
            pass
        else:
            print("2")
            return False
    for squ_row in range(n):
        for squ_col in range(n):
            squ_vals = []
            for rows in table[squ_row*n:squ_row*n+n]:
                for elem in rows[squ_col*n:squ_col*n+n]:
                    squ_vals.append(elem)
            if(set(squ_vals) == acc_ans):
                pass
            else:
                print("3")
                return False
    return True


def solve(table, row=0, col=0):
    """solves sudoku puzzle for element[row][col]

    Args:
        table (list): list that holds incomplete sudoku table
        row (int, optional): Defaults to 0.
        col (int, optional): Defaults to 0.

    """
    n = table.shape[0]
    if col >= n:
        row += 1
        col = 0
    if row >= n:
        return True
    value = table[row, col]
    if table[row, col] == 0:
        possible_ans = possible_answers(table, row, col)
    else:
        possible_ans = np.unique([table[row, col]])
    np.random.shuffle(possible_ans)
    for ans in possible_ans:
        table[row, col] = ans
        if solve(table, row, col+1):
            return True
        else:
            table[row, col] = value


def possible_answers(table, row, col):
    """find possible answers for element[row][col]

    Args:
        table (list): list that holds incomplete sudoku table
        row (_type_): row
        col (_type_): colomn

    Returns:
        set: set of possible answers
    """
    n = table.shape[0]
    n = int(math.sqrt(n))
    row_vals = np.unique(table[row])
    col_vals = np.unique(table[:, col])
    squ_row = row // n
    squ_col = col // n
    squ_vals = np.unique(table[squ_row*n:squ_row*n+n,
                               squ_col*n:squ_col*n+n].flatten())

    possible_ans = np.unique(np.arange(1, n**2 + 1))
    possible_ans = np.setdiff1d(possible_ans, squ_vals, assume_unique=True)
    possible_ans = np.setdiff1d(possible_ans, col_vals, assume_unique=True)
    possible_ans = np.setdiff1d(possible_ans, row_vals, assume_unique=True)
    return possible_ans
