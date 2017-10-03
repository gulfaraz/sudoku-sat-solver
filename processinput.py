import os
import sat_solver

dataPath = "./data/"

currentDirectory = os.path.dirname(__file__)

rankFile = 0

def pre_process_input():
    f = open("input.log", "r")
    for (index, line) in enumerate(f):
        sudoku = line.rstrip("\n")
        if(len(sudoku) == 81 and sudoku.isdigit()):
            intermediateInputFilePath = os.path.relpath(dataPath + "intermediate_input_" + str(index+1) + ".log", currentDirectory)
            intermediateInputFile = open(intermediateInputFilePath, "w")
            rankFilePath = os.path.relpath(dataPath + "rank_" + str(index+1) + ".log", currentDirectory)
            global rankFile
            rankFile = open(rankFilePath, "w")
            rankFile.write("ClueCategory,ClueIndex,Clue,Rank\n")
            intermediateInputFile.write("\n".join(derive_sudoku(sudoku)) + "\n")
            intermediateInputFile.close()
            rankFile.close()
            print("python3 sat_solver.py " + str(index+1) + " " + dataPath + " > " + dataPath + "run_" + str(index+1) + ".log")
            os.system("python3 sat_solver.py " + str(index+1) + " " + dataPath + " > " + dataPath + "run_" + str(index+1) + ".log")
            #sat_solver.magic(index)
        else:
            print("ERROR: Invalid Sudoku - Ignoring Entry")
    print("python3 process_rank.py " + dataPath)
    os.system("python3 process_rank.py " + dataPath)
    f.close()

def derive_sudoku(original):
    derived_sudoku = [original]
    #numberOfClues = sum((c.isdigit() and int(c) > 0) for c in original)
    derived_sudoku += rollVariation(original)
    derived_sudoku += singleAbsentVariation(original)
    return derived_sudoku

def singleAbsentVariation(original):
    sudokuList = []
    count = 82 #depends on the number of entries in the derived sudoku
    for (charIndex, char) in enumerate(original):
        if int(char) > 0:
            sudokuList.append(replacer(original, "0", charIndex))
            rankFile.write("1," + str(count) + "," + char + "\n")
            count += 1
    return sudokuList

def rollVariation(original):
    sudokuList = []
    for index in range(len(original)):
        sudokuList.append(original[-index:]+original[:-index])
        rankFile.write("0," + str(index+1) + ",s" + str(index+1) + "\n")
    return sudokuList

def replacer(s, newstring, index, nofail=False):
    # raise an error if index is outside of the string
    if not nofail and index not in range(len(s)):
        raise ValueError("index outside given string")

    # if not erroring, but the index is still not in the correct range..
    if index < 0:  # add it to the beginning
        return newstring + s
    if index > len(s):  # add it to the end
        return s + newstring

    # insert the new string between "slices" of the original
    return s[:index] + newstring + s[index + 1:]

if __name__ == "__main__":
   pre_process_input()
