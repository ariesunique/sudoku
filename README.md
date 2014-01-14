sudoku
======

This repo contains python code to solve a sudoku puzzle. There are two different versions of the code. 
   sudoku_solver.py -- this is my code. 
   simple_sudoku_solver.py -- I found this code on this website - http://freepythontips.wordpress.com/2013/09/01/sudoku-solver-in-python/
   
I implemented my solution first and then looked to see how the other developer did it. The algorithms used are very different. I find that the simple_sudoku_solver provides a very elegant solution with very few lines of code. However, this solution relies heavily on recursion and thus is a bit time-intensive. My solution is not as simple/straightforward, but it gets the job done and runs faster than the recursive solution. However, it uses a few maps and lists and thus probably takes up more memory.

Both program require a filename input to the command line. The file should contain the rows of the sudoku puzzle with 0s in place of the blanks (ie, the file should contain 9 lines with 9 digits on each line, no spaces). I've included several sample files, of varying degrees of difficulty. These were obtained from this site - http://www.sudoku.ws/
