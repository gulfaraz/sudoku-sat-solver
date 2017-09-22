intermediateInputFile = open("intermediate_input.log", "w")
rankFile = open("rank.log", "w")
rankFile.write("Clue,Rank\n")

def pre_process_input():
    f = open("input.log", "r")
    for line in f:
        sudoku = line.rstrip("\n")
        if(len(sudoku) == 81 and sudoku.isdigit()):
            intermediateInputFile.write("\n".join(derive_sudoku(sudoku)) + "\n")
        else:
            print("ERROR: Invalid Sudoku - Ignoring Entry")
    intermediateInputFile.close()
    f.close()

def derive_sudoku(original):
    derived_sudoku = [original]
    #numberOfClues = sum((c.isdigit() and int(c) > 0) for c in original)
    derived_sudoku += singleAbsentVariation(original)
    return derived_sudoku

def singleAbsentVariation(original):
    sudokuList = []
    for (charIndex, char) in enumerate(original):
        if int(char) > 0:
            sudokuList.append(replacer(original, "0", charIndex))
            rankFile.write(char + "\n")
    rankFile.close()
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
