"""
http://freepythontips.wordpress.com/2013/09/01/sudoku-solver-in-python/
"""

class MyException(Exception):
    pass

import sys

def same_row(i,j): return (i/9 == j/9)
def same_col(i,j): return (i-j) % 9 == 0
def same_block(i,j): return (i/27 == j/27 and i%9/3 == j%9/3)

def r(a):
  i = a.find('0')
  if i == -1:
    #sys.exit(a)
    raise MyException(a)

  excluded_numbers = set()
  for j in range(81):
    if same_row(i,j) or same_col(i,j) or same_block(i,j):
      excluded_numbers.add(a[j])

  for m in '123456789':
    if m not in excluded_numbers:
      r(a[:i]+m+a[i+1:])


def display(res):
    rowcount = 1
    colcount = 1

    for n in res:
        print n,
        if colcount % 3 == 0:
            print "|",
        if colcount % 9 == 0:
            print ""
            if rowcount % 3 == 0:
                print "-----------------------"
            rowcount += 1
        colcount += 1



if __name__ == '__main__':
  if len(sys.argv) == 2: # and len(sys.argv[1]) == 81:
    filename = sys.argv[1]
    f = open(filename)
    sudoku = "".join([line.strip("\n").strip() for line in f.readlines()])
    f.close()

    if len(sudoku) != 81:
        sys.exit("file incorrectly formatted - must contain 81 digits")

    #print "Input\n"
    #display(sudoku)
    #print "\n"
    try:
        r(sudoku)
    except MyException as e:
        print "Answer\n"
        display(str(e))
  else:
    print 'Usage: python sudoku.py puzzle'
    print 'where puzzle is an 81 char string representing the puzzle read left-to-right, top-to-bottom, and 0 is a blank'
