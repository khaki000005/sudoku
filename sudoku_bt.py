import random
import math


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
    table = [[0 for x in range(n**2)]
             for y in range(n**2)]
    solve(table)
    return table


def show(table):
    """shows a [[]*n]*n list as a sudoku table

    Args:
        table (list): list that holds sudoku table
    """    
    n = int(math.sqrt(len(table)))
    for x, xe in enumerate(table):
        if x % n == 0:
            print()
        for y, ye in enumerate(xe):
            if y % n == 0:
                print(end="  ")
            print("{ye:3d}".format(ye=ye), end=" ")
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
    n = int(math.sqrt(len(table)))
    if col >= n**2:
        row += 1
        col = 0
    if row >= n**2:
        return True
    value = table[row][col]
    if table[row][col] == 0:
        possible_ans = possible_answers(table, row, col)
    else:
        possible_ans = set([table[row][col]])
    possible_ans = list(possible_ans)
    random.shuffle(possible_ans)
    for ans in possible_ans:
        table[row][col] = ans
        if solve(table, row, col+1):
            return True
        else:
            table[row][col] = value


def possible_answers(table, row, col):
    """find possible answers for element[row][col]

    Args:
        table (list): list that holds incomplete sudoku table
        row (_type_): row
        col (_type_): colomn

    Returns:
        set: set of possible answers
    """    
    n = int(math.sqrt(len(table)))
    row_vals = set(table[row])
    col_vals = set([rows[col] for rows in table])
    squ_row = row // n
    squ_col = col // n
    squ_vals = set()
    for rows in table[squ_row*n:squ_row*n+n]:
        for elem in rows[squ_col*n:squ_col*n+n]:
            squ_vals.add(elem)
    possible_ans = set([ans for ans in range(1, n**2+1)])
    possible_ans = possible_ans - squ_vals - col_vals - row_vals
    return possible_ans
