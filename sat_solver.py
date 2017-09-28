# Author: Gulfaraz Rahman, 2017
# Original Author: Nicholas Pilkington, 2015
# License: MIT

import os
import pycosat
import processlog
import sys

currentDirectory = os.path.dirname(__file__)

N = 9
M = 3

def exactly_one(variables):
    cnf = [ variables ]
    n = len(variables)

    for i in range(n):
        for j in range(i+1, n):
            v1 = variables[i]
            v2 = variables[j]
            cnf.append([-v1, -v2])

    return cnf

def transform(i, j, k):
    return i*N*N + j*N + k + 1

def inverse_transform(v):
    v, k = divmod(v-1, N)
    v, j = divmod(v, N)
    v, i = divmod(v, N)
    return i, j, k

def solve_input_file(f):
    for line in f:
        sudoku = line.rstrip("\n")
        if(len(sudoku) == 81 and sudoku.isdigit()):
            constraints = convert_to_array(sudoku)
            solve_sudoku(constraints)
        else:
            print("ERROR: Invalid Sudoku - Ignoring Entry")
    f.close()

def convert_to_array(sudokuString):
    sudokuArray = []
    for (index, value) in enumerate(sudokuString):
        value = int(value)
        row = int(index / 9)
        col = index % 9
        if(value > 0):
            sudokuArray.append((row, col, value))
    return sudokuArray

def solve_sudoku(constraints):
    cnf = []

    # Cell, row and column constraints
    for i in range(N):
        for s in range(N):
            cnf = cnf + exactly_one([ transform(i, j, s) for j in range(N) ])
            cnf = cnf + exactly_one([ transform(j, i, s) for j in range(N) ])

        for j in range(N):
            cnf = cnf + exactly_one([ transform(i, j, k) for k in range(N) ])

    # Sub-matrix constraints
    for k in range(N):
        for x in range(M):
            for y in range(M):
                v = [ transform(y*M + i, x*M + j, k) for i in range(M) for j in range(M)]
                cnf = cnf + exactly_one(v)


    # A 16-constraint Sudoku
    '''
    constraints = [
        (0, 3, 7),
        (1, 0, 1),
        (2, 3, 4),
        (2, 4, 3),
        (2, 6, 2),
        (3, 8, 6),
        (4, 3, 5),
        (4, 5, 9),
        (5, 6, 4),
        (5, 7, 1),
        (5, 8, 8),
        (6, 4, 8),
        (6, 5, 1),
        (7, 2, 2),
        (7, 7, 5),
        (8, 1, 4),
        (8, 6, 3)
    ]
    '''
    #print(constraints)

    cnf = cnf + [[transform(z[0], z[1], z[2])-1] for z in constraints]

    textSuDoKu = ""
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n")
    for solution in pycosat.itersolve(cnf, verbose=1):
        #print(len(solution))
        X = [ inverse_transform(v) for v in solution if v > 0]
        for i, cell in enumerate(sorted(X, key=lambda h: h[0] * N*N + h[1] * N)):
            textSuDoKu += str(cell[2]+1)
            if (i+1) % N == 0:
                textSuDoKu += ""#"\n"
            else:
                textSuDoKu += ""#"|"
        textSuDoKu += "\n"#"-----------------\n"
            #print cell[2]+1, " ",
            #if (i+1) % N == 0: print ""
    print(textSuDoKu)

def magic(index, dataPath):
    intermediateInputFilePath = os.path.relpath(dataPath + "intermediate_input_" + str(int(index)) + ".log", currentDirectory)
    intermediateInputFile = open(intermediateInputFilePath, "r")
    try:
        f = intermediateInputFile
    except FileNotFoundError:
        print("ERROR: Try again. A sudoku is a line with a string 000900000000000004400100000000000002020005340831000050900060000040380007057010200. You can have multiple sudokus in a file separated by a newline.")
    else:
        #print("LOG: Reading from " + inputFileName)
        solve_input_file(f)
        processlog.post_process_log(index, dataPath)

if __name__ == "__main__":
    magic(str(sys.argv[1]), str(sys.argv[2]))
