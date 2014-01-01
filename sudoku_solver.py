#-------------------
# Sudoku
#
# input: filename
#   Specify a filename on the command line. The filename contains data for
#   the sudoku board game as a sparse matrix
#
#   -verbose flag displays the game in its various stages as it is being solved
#
# output: the final board as a solution and the time taken to solve the puzzle
#
# display() method displays the board in its current state
#
# Algorithm:
#   Maintain a dict of lists - the keys are the box names (81),
#       each key points to a list of possible values for that square
#       all are initialized to 1 - 9
#   Maintain a dict of rows - the key is the row num (1 - 9), the value is
#       a list of the box names in that row
#   Maintain a dict of cols - see rows
#   Maintain a dict of boxes - see rows
#
#-------------------

import random
import sys
import time
import argparse
import copy


def print_timing(func):
    def wrapper(*arg):
        t1 = time.clock()
        func(*arg)
        t2 = time.clock()
        print "Code completed in %.3f ms" % (t2-t2)*1000.0
    return wrapper


def generate_rows():
    rows = []
    for i in xrange(1,10):
        names = []
        for j in "ABCDEFGHI":
            boxname = j + str(i)
            names.append(boxname)
        rows.append(names)
    return rows


def generate_cols():
    cols = []
    for j in "ABCDEFGHI":
        names = []
        for i in xrange(1,10):
            boxname = j + str(i)
            names.append(boxname)
        cols.append(names)
    return cols


def generate_possibles():
    global board
    possibles = {}
    for i in xrange(1,10):
        for j in "ABCDEFGHI":
            boxname = j + str(i)
            if boxname in board:
                possibles[boxname] = [board[boxname]]
            else:
                possibles[boxname] = [n for n in xrange(1, 10)]
    return possibles


def generate_test_board():
    board = {}
    board["A1"] = 3
    board["B1"] = 9
    board["E1"] = 6
    board["G1"] = 8
    board["I1"] = 7
    board["B2"] = 2
    board["E2"] = 3
    board["H2"] = 5
    board["F3"] = 5
    board["H3"] = 9
    board["I3"] = 6
    board["A4"] = 9
    board["D4"] = 5
    board["F4"] = 2
    board["G4"] = 4
    board["C6"] = 3
    board["D6"] = 9
    board["F6"] = 7
    board["I6"] = 2
    board["A7"] = 8
    board["B7"] = 1
    board["D7"] = 6
    board["B8"] = 3
    board["E8"] = 5
    board["H8"] = 8
    board["A9"] = 5
    board["C9"] = 2
    board["E9"] = 9
    board["H9"] = 4
    board["I9"] = 3

    return board


def generate_board(infile):
    lines = infile.readlines()
    infile.close()

    board = {}
    for i, line in zip(xrange(1,10), lines):
        line = line.rstrip("\n")
        line = line.strip()
        if len(line) != 9:
            raise Exception("input file incorrectly formatted, each line must contain 9 digits")
        for j, num in zip("ABCDEFGHI", line):
            boxname = j + str(i)
            n = int(num)
            if n == 0:
                continue
            board[boxname] = n
    return board


def display():
    global row, board
    rowcount = 1
    colcount = 1
    for boxes in rows:
        for name in boxes:
            print board.get(name, 0),
            if colcount % 3 == 0:
                print "|",
            colcount += 1
        print ""
        if rowcount % 3 == 0:
            print "-----------------------"
        rowcount += 1


def solve(collection):
    global board, possibles, args, pairs
    progress = False

    """
    Maintain a list of possible values for each cell (1-9). Iterate over each
    cell in the collection (row, col, box) and use the process of elimination
    to remove numbers from the list of possible values for that cell.
    """
    for cell in board.keys()[:]:
        value = board[cell]
        for boxes in collection:
            if cell not in boxes:
                continue
            for box in boxes:
                if box == cell:
                    continue
                if value in possibles[box]:
                    possibles[box].remove(value)
                    if len(possibles[box]) == 1:
                        board[box] = possibles[box][0]
                        progress = True
                        if args.verbose:
                            print "A: Assign %d to %s" % (possibles[box][0], box)
                        del(possibles[box][0])
    """
    Iterate over the empty cells in the collection and determine if there is only
    one cell position for a particular digit.
    """
    for boxes in collection:
        found = [board.get(box) for box in boxes]
        for n in xrange(1, 10):
            temp = []
            for box in boxes:
                if box not in board and n in possibles[box] and n not in found:
                    temp.append(box)
            if len(temp) == 1:
                progress = True
                board[temp[0]] = n
                if args.verbose:
                    print "B: Assign %d to %s" % (n,temp[0])

    """
    Check to see if there are 2 cells in a collection that have only 2 possible
    values
    """
    for boxes in collection:
        tmp = []
        names = []
        box1, box2 = None, None
        found = False
        for box in boxes:
            if box in pairs:
                continue
            if len(possibles[box]) == 2:
                for l, name in zip(tmp, names):
                    if set(l) == set(possibles[box]):
                        box1 = name
                        box2 = box
                        if args.verbose:
                            print "Found two equal sets - %s and %s" % (box1, box2)
                        found = True
                        break
                else:
                    tmp.append(possibles[box])
                    names.append(box)

        if found:
            progress = True
            pairs.append(box1)
            pairs.append(box2)
            for box in boxes:
                if box != box1 and box != box2:
                    values = possibles[box1]
                    for v in values:
                        if v in possibles[box]:
                            possibles[box].remove(v)

    """
    Are there any cells with only one value? If so, assign
    """
    for boxes in collection:
        to_remove = []
        for box in boxes:
            if len(possibles[box]) == 1:
                value = possibles[box][0]
                board[box] = possibles[box][0]
                progress = True
                if args.verbose:
                    print "C: Assign %d to %s" % (value, box)
                to_remove.append(value)
        for box in boxes:
            for i in to_remove:
                if i in possibles[box]:
                    possibles[box].remove(i)



    return progress


def guess():
    global board, possibles, pairs, guesses, args

    name = pairs.pop(0)
    name2 = pairs.pop(0)
    while possibles[name] != 2 and len(pairs)>=2:
        name = pairs.pop(0)
        name2 = pairs.pop(0)

    #print name, possibles[name]

    guesses.append(copy.copy(board))
    guesses.append(str(name) + str(possibles[name][0]))
    guesses.append(str(name2) + str(possibles[name2][1]))
    guesses.append(copy.deepcopy(possibles))

    board[name] = possibles[name][0]
    board[name2] = possibles[name2][1]

    if args.verbose:
        print "\nGuessing %d at %s" % (possibles[name][0], name)
        print "\nGuessing %d at %s" % (possibles[name2][1], name2)


def guess_again():
    global board, possibles, guesses, args
    possibles = guesses.pop()
    guess1 = guesses.pop()
    guess2 = guesses.pop()
    board = guesses.pop()

    val1 = guess1[-1]
    val2 = guess2[-1]
    name1 = guess1[:-1]
    name2 = guess2[:-1]

    board[name2] = int(val1)
    board[name1] = int(val2)

    if args.verbose:
        print "Assigning %s to %s" % (val1, name2)
        print "Assigning %s to %s" % (val2, name1)
        display()



def done():
    global board, args
    for i in xrange(1,10):
        for j in "ABCDEFGHI":
            boxname = j + str(i)
            if boxname not in board:
                return False

    if not validate(rows) or not validate(cols) or not validate(boxes):
        if args.verbose:
            print "Unfortunately that solution is not correct."
        guess_again()
        return False
    else:
        print "Yay, your solution is correct!"
    return True


def validate(collection):
    for boxes in collection:
        nums = set([board.get(box) for box in boxes])
        if len(nums) < 9:
            return False
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Program that solves a sudoku puzzle.")
    parser.add_argument("infile", type=file, help="filename containing the sudoku puzzle to be solved")
    parser.add_argument("outfile", nargs="?", type=argparse.FileType("w"), default=sys.stdout,
        help="write output to this file if present, else stdout")
    parser.add_argument("-v", "--verbose", action="store_true",
        help="display progress as code solves puzzle.")
    parser.add_argument("-iter", "--maxiters", type=int, default=50,
        help="number of iterations code will make in attept to solve puzzle, default=50")
    try:
        args = parser.parse_args()
    except IOError:
        print("input file not found")
        exit(1)

    board = {}
    try:
        board = generate_board(args.infile)
    except ValueError:
        print "One of the lines contained a non-digit char. Please check your input."
        exit(1)
    except Exception as e:
        print "There was a problem reading the input file:", e
        exit(1)

    rows = generate_rows()
    cols = generate_cols()
    boxes = [
        ["A1", "B1", "C1", "A2", "B2", "C2", "A3", "B3", "C3"],
        ["D1", "E1", "F1", "D2", "E2", "F2", "D3", "E3", "F3"],
        ["G1", "H1", "I1", "G2", "H2", "I2", "G3", "H3", "I3"],
        ["A4", "B4", "C4", "A5", "B5", "C5", "A6", "B6", "C6"],
        ["D4", "E4", "F4", "D5", "E5", "F5", "D6", "E6", "F6"],
        ["G4", "H4", "I4", "G5", "H5", "I5", "G6", "H6", "I6"],
        ["A7", "B7", "C7", "A8", "B8", "C8", "A9", "B9", "C9"],
        ["D7", "E7", "F7", "D8", "E8", "F8", "D9", "E9", "F9"],
        ["G7", "H7", "I7", "G8", "H8", "I8", "G9", "H9", "I9"],
    ]

    #board = generate_test_board()
    display()

    possibles = generate_possibles()

    # stack to keep track of the guesses
    guesses = []
    pairs = []

    n = 1
    t1 = time.time()
    while not done():
        if n > args.maxiters:
            print "\nUnfortunately we were unable to solve the puzzle in %d iterations. \
                    Try increasing the maxiters value.\n" % args.maxiters
            display()
            break

        if args.verbose:
            print "\nIteration %d __________________________" % n

        if args.verbose:
            print "\nprocessing rows"

        row_progress = solve(rows)

        if args.verbose:
            print "\nprocessing cols"

        col_progress = solve(cols)

        if args.verbose:
            print "\nprocessing boxes"

        box_progress = solve(boxes)

        if not row_progress and not col_progress and not box_progress:
            if args.verbose:
                print "\nSolver stuck after %d iterations. Program will need to guess." % n
                display()
            guess()
        n += 1
    else:
        t2 = time.time()
        print "\nSolved the puzzle in %d iterations and %.2f ms.\n" % (n, (t2-t1)*1000.0)
        display()

