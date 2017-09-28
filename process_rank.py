import os
import pycosat
import sys
from scipy.stats import rankdata

currentDirectory = os.path.dirname(__file__)

def post_rank_log(dataPath):
    f = open("input.log", "r")
    consolidatedRanksFilePath = os.path.relpath(dataPath + "rank.log", currentDirectory)
    consolidatedRanksFile = open(consolidatedRanksFilePath, "w")
    consolidatedRanksFile.write("ClueCategory,ClueType,Clue,Min,Dense\n")
    for (index, line) in enumerate(f):
        sudoku = line.rstrip("\n")
        if(len(sudoku) == 81 and sudoku.isdigit()):
            rankFilePath = os.path.relpath(dataPath + "rank_" + str(index+1) + ".log", currentDirectory)
            rankFile = open(rankFilePath, "r")
            for line in rankFile:
                strippedLine = line.rstrip("\n")
                if strippedLine[0:4]!="Clue":
                    consolidatedRanksFile.write(strippedLine+"\n")
            rankFile.close()
        else:
            print("ERROR: Invalid Sudoku - Ignoring Entry")
    consolidatedRanksFile.close()
    f.close()

if __name__ == "__main__":
    post_rank_log(str(sys.argv[1]))
