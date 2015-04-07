import copy
import random

class cell():
""" Initilalizes cell object. A cell is a single box of a sudoku puzzle. 81 cells make up the body of a
sudoku puzzle. Initializes puzzle with all possible answers available, solved to false, and position of cell within the
sudoku puzzle"""
    def __init__(self, position):
        self.possibleAnswers = [1,2,3,4,5,6,7,8,9]
        self.answer = None
        self.position = position
        self.solved = False
        
"""Removes num from list of possible answers in cell object."""
    def remove(self, num):
        if num in self.possibleAnswers and self.solved == False:
            self.possibleAnswers.remove(num)
            if len(self.possibleAnswers) == 1:
                self.answer = self.possibleAnswers[0]
                self.solved = True
        if num in self.possibleAnswers and self.solved == True:
            self.answer = 0

""" Returns whether or not a cell has been solved"""
    def solvedMethod(self):
        return self.solved

""" Returns the position of a cell within a sudoku puzzle. x = row; y = col; z = box number"""
    def checkPosition(self):
        return self.position

""" Returns a list of possible answers that a cell can still use"""
    def returnPossible(self):
        return self.possibleAnswers

""" Returns an integer of the length of the possible answers list"""
    def lenOfPossible(self):
        return len(self.possibleAnswers)

""" Returns whether or not a cell has been solved"""
    def returnSolved(self):
        if self.solved == True:
            return self.possibleAnswers[0]
        else:
            return False
        
""" Sets an answer of a puzzle and sets a cell's solved method to true. This
method also eliminates all other possible numbers"""
    def setAnswer(self, num):
        if num in [1,2,3,4,5,6,7,8,9]:
            self.solved = True
            self.answer = num
            self.possibleAnswers = [num]
        else:
            raise(ValueError)
""" Resets all attributes of a cell to the original conditions"""        
    def reset(self):
        self.possibleAnswers = [1,2,3,4,5,6,7,8,9]
        self.answer = None
        self.solved = False

'''Creates an empty sudoku in row major form. Sets up all of the x, y, and z
coordinates for the sudoku cells'''
def emptySudoku():
    ans = []
    for x in range(1,10):
        if x in [7,8,9]:
            intz = 7
            z = 7
        if x in [4,5,6]:
            intz = 4
            z = 4
        if x in [1,2,3]:
            intz = 1
            z = 1
        for y in range(1,10):
            z = intz
            if y in [7,8,9]:
                z += 2
            if y in [4,5,6]:
                z += 1
            if y in [1,2,3]:
                z += 0
            c = cell((x,y,z))
            ans.append(c)
    return ans

'''Prints out a sudoku in a format that is easy for a human to read'''
def printSudoku(sudoku):
    row1 = []
    row2 = []
    row3 = []
    row4 = []
    row5 = []
    row6 = []
    row7 = []
    row8 = []
    row9 = []
    for i in range(81):
        if i in range(0,9):
            row1.append(sudoku[i].returnSolved())
        if i in range(9,18):
            row2.append(sudoku[i].returnSolved())
        if i in range(18,27):
            row3.append(sudoku[i].returnSolved())
        if i in range(27,36):
            row4.append(sudoku[i].returnSolved())
        if i in range(36,45):
            row5.append(sudoku[i].returnSolved())
        if i in range(45,54):
            row6.append(sudoku[i].returnSolved())
        if i in range(54,63):
            row7.append(sudoku[i].returnSolved())
        if i in range(63,72):
            row8.append(sudoku[i].returnSolved())
        if i in range(72,81):
            row9.append(sudoku[i].returnSolved())
    print(row1[0:3],row1[3:6],row1[6:10])
    print(row2[0:3],row2[3:6],row2[6:10])
    print(row3[0:3],row3[3:6],row3[6:10])
    print('')
    print(row4[0:3],row4[3:6],row4[6:10])
    print(row5[0:3],row5[3:6],row5[6:10])
    print(row6[0:3],row6[3:6],row6[6:10])
    print('')
    print(row7[0:3],row7[3:6],row7[6:10])
    print(row8[0:3],row8[3:6],row8[6:10])
    print(row9[0:3],row9[3:6],row9[6:10])

'''Generates a completed sudoku. Sudoku is completly random'''
def sudokuGen():
    cells = [i for i in range(81)] ## our cells is the positions of cells not currently set
    sudoku = emptySudoku()
    while len(cells) != 0:
        lowestNum = []
        Lowest = []
        for i in cells:
            lowestNum.append(sudoku[i].lenOfPossible())  ## finds all the lengths of of possible answers for each remaining cell
        m = min(lowestNum)  ## finds the minimum of those
        '''Puts all of the cells with the lowest number of possible answers in a list titled Lowest'''
        for i in cells:
            if sudoku[i].lenOfPossible() == m:
                Lowest.append(sudoku[i])
        '''Now we randomly choose a possible answer and set it to the cell'''
        choiceElement = random.choice(Lowest)
        choiceIndex = sudoku.index(choiceElement) 
        cells.remove(choiceIndex)                 
        position1 = choiceElement.checkPosition()
        if choiceElement.solvedMethod() == False:  ##the actual setting of the cell
            possibleValues = choiceElement.returnPossible()
            finalValue = random.choice(possibleValues)
            choiceElement.setAnswer(finalValue)
            for i in cells:  ##now we iterate through the remaining unset cells and remove the input if it's in the same row, col, or box
                position2 = sudoku[i].checkPosition()
                if position1[0] == position2[0]:
                    sudoku[i].remove(finalValue)
                if position1[1] == position2[1]:
                    sudoku[i].remove(finalValue)
                if position1[2] == position2[2]:
                    sudoku[i].remove(finalValue)

        else:
            finalValue = choiceElement.returnSolved()
            for i in cells:  ##now we iterate through the remaining unset cells and remove the input if it's in the same row, col, or box
                position2 = sudoku[i].checkPosition()
                if position1[0] == position2[0]:
                    sudoku[i].remove(finalValue)
                if position1[1] == position2[1]:
                    sudoku[i].remove(finalValue)
                if position1[2] == position2[2]:
                    sudoku[i].remove(finalValue)
    return sudoku

""" Checks to see if an input a completed sudoku puzzle is of the correct format and abides by all
of the rules of a sudoku puzzle. Returns True if the puzzle is correct. False if otherwise"""
def sudokuChecker(sudoku):
    for i in range(len(sudoku)):
        for n in range(len(sudoku)):
            if i != n:
                position1 = sudoku[i].checkPosition()
                position2 = sudoku[n].checkPosition()
                if position1[0] == position2[0] or position1[1] == position2[1] or position1[2] == position2[2]:
                    num1 = sudoku[i].returnSolved()
                    num2 = sudoku[n].returnSolved()
                    if num1 == num2:
                        return False
    return True

'''Generates a completed sudoku. Sudoku is in the correct format and is completly random'''
def perfectSudoku():
    result = False
    while result == False:
        s = sudokuGen()
        result = sudokuChecker(s)
##        print(result)
    return s

""" Input an incomplete Sudoku puzzle and solver method will return the solution to the puzzle. First checks to see if any obvious answers can be set
then checks the rows columns and boxes for obvious solutions. Lastly the solver 'guesses' a random possible answer from a random cell and checks to see if that is a
possible answer. If the 'guessed' answer is incorrect, then it removes the guess and tries a different answer in a different cell and checks for a solution. It does this until
all of the cells have been solved. Returns a printed solution to the puzzle and the number of guesses that it took to complete the puzzle. The number of guesses is
a measure of the difficulty of the puzzle. The more guesses that it takes to solve a given puzzle the more challenging it is to solve the puzzle"""
def solver(sudoku, f = 0):
    if f > 900:
        return False
    guesses = 0
    copy_s = copy.deepcopy(sudoku)
    cells = [i for i in range(81)] ## our cells is the positions of cells not currently set
    solvedCells = []
    for i in cells:
        if copy_s[i].lenOfPossible() == 1:
            solvedCells.append(i)
    while solvedCells != []:
        for n in solvedCells:
            cell = copy_s[n]
            position1 = cell.checkPosition()
            finalValue = copy_s[n].returnSolved()
            for i in cells:  ##now we itterate through the remaing unset cells and remove the input if it's in the same row, col, or box
                position2 = copy_s[i].checkPosition()
                if position1[0] == position2[0]:
                    copy_s[i].remove(finalValue)
                if position1[1] == position2[1]:
                    copy_s[i].remove(finalValue)
                if position1[2] == position2[2]:
                    copy_s[i].remove(finalValue)
                if copy_s[i].lenOfPossible() == 1 and i not in solvedCells and i in cells:
                    solvedCells.append(i)
                ##print(n)
            solvedCells.remove(n)
            cells.remove(n)
        if cells != [] and solvedCells == []:
            lowestNum=[]
            lowest = []
            for i in cells:
                lowestNum.append(copy_s[i].lenOfPossible())
            m = min(lowestNum)
            for i in cells:
                if copy_s[i].lenOfPossible() == m:
                    lowest.append(copy_s[i])
            randomChoice = random.choice(lowest)
            randCell = copy_s.index(randomChoice)
            randGuess = random.choice(copy_s[randCell].returnPossible())
            copy_s[randCell].setAnswer(randGuess)
            solvedCells.append(randCell)
            guesses += 1
    if sudokuChecker(copy_s):
        if guesses <=5:
            level = 'easy'
        if guesses > 5:
            level = 'hard'
        return copy_s, guesses
    else:
        return solver(sudoku, f+1)
    
""" Uses the solver method to solve a puzzle. This method was built in order to avoid recursion depth errors. Returns True if the puzzle is solvable and
false if otherwise"""
def solve(sudoku, n = 0):
    if n < 30:
        s = solver(sudoku)
        if s != False:
            return s
        else:
            solve(sudoku, n+1)
    else:
        return False
""" Generates a puzzle with a unique solution. """
def puzzleGen(sudoku):
    cells = [i for i in range(81)]
    while cells != []:
        copy_s = copy.deepcopy(sudoku)
        randIndex = random.choice(cells)
        cells.remove(randIndex)
        copy_s[randIndex].reset()
        s = solve(copy_s)
        if s[0] == False:
            f = solve(sudoku)
            print("Guesses: " + str(f[1]))
            return printSudoku(sudoku)
        elif equalChecker(s[0],solve(copy_s)[0]):
            if equalChecker(s[0],solve(copy_s)[0]):
                sudoku[randIndex].reset()
        else:
            f = solve(sudoku)
            print("Guesses: " + str(f[1]))
            return printSudoku(sudoku)

""" Checks to see if two puzzles are the same"""
def equalChecker(s1,s2):
    for i in range(len(s1)):
        if s1[i].returnSolved() != s2[i].returnSolved():
            return False
    return True

###Puzzles

##Easy Puzzle
s = emptySudoku()
s[0].setAnswer(3)
s[1].setAnswer(9)
s[5].setAnswer(2)
s[8].setAnswer(6)
s[10].setAnswer(5)
s[13].setAnswer(8)
s[14].setAnswer(6)
s[18].setAnswer(2)
s[26].setAnswer(3)
s[28].setAnswer(3)
s[30].setAnswer(7)
s[38].setAnswer(1)
s[40].setAnswer(6)
s[42].setAnswer(8)
s[50].setAnswer(1)
s[52].setAnswer(9)
s[54].setAnswer(4)
s[62].setAnswer(7)
s[66].setAnswer(4)
s[67].setAnswer(3)
s[70].setAnswer(5)
s[72].setAnswer(8)
s[75].setAnswer(6)
s[79].setAnswer(3)
s[80].setAnswer(2)


##hard puzzle
g = emptySudoku()
g[0].setAnswer(8)
g[1].setAnswer(6)
g[4].setAnswer(2)
g[12].setAnswer(7)
g[16].setAnswer(5)
g[17].setAnswer(9)
g[31].setAnswer(6)
g[33].setAnswer(8)
g[37].setAnswer(4)
g[47].setAnswer(5)
g[48].setAnswer(3)
g[53].setAnswer(7)
g[64].setAnswer(2)
g[69].setAnswer(6)
g[74].setAnswer(7)
g[75].setAnswer(5)
g[77].setAnswer(9)

##hard puzzle
h = emptySudoku()
h[0].setAnswer(2)
h[1].setAnswer(5)
h[5].setAnswer(4)
h[7].setAnswer(8)
h[12].setAnswer(8)
h[15].setAnswer(1)
h[17].setAnswer(7)
h[19].setAnswer(8)
h[21].setAnswer(6)
h[25].setAnswer(5)
h[26].setAnswer(3)
h[29].setAnswer(2)
h[31].setAnswer(3)
h[35].setAnswer(1)
h[45].setAnswer(3)
h[49].setAnswer(9)
h[51].setAnswer(7)
h[54].setAnswer(5)
h[55].setAnswer(7)
h[59].setAnswer(3)
h[61].setAnswer(1)
h[63].setAnswer(8)
h[65].setAnswer(6)
h[68].setAnswer(2)
h[73].setAnswer(2)
h[75].setAnswer(7)
h[79].setAnswer(4)
h[80].setAnswer(9)

## Easy Puzzles ##
easy1 = emptySudoku()
easy1[0].setAnswer(6)
easy1[3].setAnswer(2)
easy1[4].setAnswer(7)
easy1[6].setAnswer(8)
easy1[8].setAnswer(5)
easy1[11].setAnswer(2)
easy1[12].setAnswer(4)
easy1[15].setAnswer(6)
easy1[17].setAnswer(3)
easy1[18].setAnswer(3)
easy1[26].setAnswer(7)
easy1[27].setAnswer(9)
easy1[29].setAnswer(3)
easy1[31].setAnswer(1)
easy1[32].setAnswer(7)
easy1[33].setAnswer(2)
easy1[36].setAnswer(5)
easy1[38].setAnswer(8)
easy1[39].setAnswer(3)
easy1[40].setAnswer(9)
easy1[44].setAnswer(4)
easy1[47].setAnswer(6)
easy1[52].setAnswer(3)
easy1[62].setAnswer(8)
easy1[67].setAnswer(5)
easy1[68].setAnswer(4)
easy1[69].setAnswer(9)
easy1[70].setAnswer(7)
easy1[72].setAnswer(4)
easy1[74].setAnswer(5)

easy2 = emptySudoku()
easy2[0].setAnswer(4)
easy2[3].setAnswer(3)
easy2[5].setAnswer(5)
easy2[9].setAnswer(1)
easy2[11].setAnswer(8)
easy2[12].setAnswer(9)
easy2[14].setAnswer(4)
easy2[15].setAnswer(7)
easy2[19].setAnswer(3)
easy2[20].setAnswer(9)
easy2[21].setAnswer(6)
easy2[22].setAnswer(7)
easy2[27].setAnswer(7)
easy2[28].setAnswer(2)
easy2[29].setAnswer(3)
easy2[33].setAnswer(4)
easy2[35].setAnswer(5)
easy2[37].setAnswer(8)
easy2[43].setAnswer(2)
easy2[45].setAnswer(9)
easy2[47].setAnswer(4)
easy2[51].setAnswer(1)
easy2[52].setAnswer(3)
easy2[53].setAnswer(7)
easy2[58].setAnswer(4)
easy2[59].setAnswer(6)
easy2[60].setAnswer(8)
easy2[61].setAnswer(5)
easy2[65].setAnswer(5)
easy2[66].setAnswer(2)
easy2[68].setAnswer(1)
easy2[69].setAnswer(3)
easy2[71].setAnswer(6)
easy2[75].setAnswer(8)
easy2[77].setAnswer(3)
easy2[80].setAnswer(2)

easy3 = emptySudoku()
easy3[1].setAnswer(3)
easy3[2].setAnswer(7)
easy3[3].setAnswer(5)
easy3[5].setAnswer(6)
easy3[7].setAnswer(4)
easy3[11].setAnswer(4)
easy3[12].setAnswer(9)
easy3[13].setAnswer(3)
easy3[18].setAnswer(9)
easy3[19].setAnswer(5)
easy3[22].setAnswer(7)
easy3[23].setAnswer(1)
easy3[26].setAnswer(6)
easy3[33].setAnswer(9)
easy3[34].setAnswer(1)
easy3[35].setAnswer(4)
easy3[38].setAnswer(1)
easy3[42].setAnswer(7)
easy3[45].setAnswer(7)
easy3[46].setAnswer(6)
easy3[47].setAnswer(8)
easy3[54].setAnswer(2)
easy3[57].setAnswer(6)
easy3[58].setAnswer(1)
easy3[61].setAnswer(3)
easy3[62].setAnswer(5)
easy3[67].setAnswer(2)
easy3[68].setAnswer(5)
easy3[69].setAnswer(6)
easy3[73].setAnswer(1)
easy3[75].setAnswer(3)
easy3[77].setAnswer(9)
easy3[78].setAnswer(8)
easy3[79].setAnswer(7)

easy4 = emptySudoku()
easy4[0].setAnswer(3)
easy4[1].setAnswer(9)
easy4[7].setAnswer(4)
easy4[8].setAnswer(6)
easy4[12].setAnswer(9)
easy4[13].setAnswer(3)
easy4[14].setAnswer(7)
easy4[15].setAnswer(2)
easy4[17].setAnswer(8)
easy4[19].setAnswer(7)
easy4[22].setAnswer(6)
easy4[26].setAnswer(5)
easy4[28].setAnswer(1)
easy4[29].setAnswer(3)
easy4[31].setAnswer(2)
easy4[33].setAnswer(8)
easy4[34].setAnswer(6)
easy4[36].setAnswer(2)
easy4[40].setAnswer(9)
easy4[41].setAnswer(3)
easy4[42].setAnswer(1)
easy4[44].setAnswer(7)
easy4[49].setAnswer(1)
easy4[50].setAnswer(8)
easy4[51].setAnswer(4)
easy4[53].setAnswer(2)
easy4[54].setAnswer(8)
easy4[61].setAnswer(2)
easy4[62].setAnswer(1)
easy4[64].setAnswer(3)
easy4[67].setAnswer(5)
easy4[70].setAnswer(7)
easy4[71].setAnswer(4)
easy4[72].setAnswer(5)
easy4[74].setAnswer(4)
easy4[75].setAnswer(1)
easy4[76].setAnswer(7)
easy4[78].setAnswer(9)
easy4[79].setAnswer(8)
easy4[80].setAnswer(3)

easy5 = emptySudoku()
easy5[1].setAnswer(9)
easy5[2].setAnswer(8)
easy5[3].setAnswer(7)
easy5[5].setAnswer(2)
easy5[7].setAnswer(3)
easy5[8].setAnswer(6)
easy5[11].setAnswer(5)
easy5[12].setAnswer(6)
easy5[13].setAnswer(9)
easy5[14].setAnswer(8)
easy5[18].setAnswer(2)
easy5[20].setAnswer(4)
easy5[21].setAnswer(1)
easy5[25].setAnswer(7)
easy5[27].setAnswer(8)
easy5[28].setAnswer(4)
easy5[30].setAnswer(5)
easy5[33].setAnswer(6)
easy5[35].setAnswer(3)
easy5[36].setAnswer(9)
easy5[39].setAnswer(4)
easy5[44].setAnswer(8)
easy5[46].setAnswer(7)
easy5[47].setAnswer(6)
easy5[52].setAnswer(1)
easy5[53].setAnswer(4)
easy5[58].setAnswer(1)
easy5[59].setAnswer(3)
easy5[61].setAnswer(6)
easy5[62].setAnswer(5)
easy5[63].setAnswer(3)
easy5[64].setAnswer(1)
easy5[65].setAnswer(2)
easy5[68].setAnswer(6)
easy5[69].setAnswer(4)
easy5[73].setAnswer(5)
easy5[75].setAnswer(8)
easy5[76].setAnswer(7)
easy5[78].setAnswer(3)
easy5[79].setAnswer(2)


## Medium Puzzles ##
medium1 = emptySudoku()
medium1[1].setAnswer(2)
medium1[8].setAnswer(5)
medium1[9].setAnswer(3)
medium1[11].setAnswer(8)
medium1[18].setAnswer(1)
medium1[23].setAnswer(6)
medium1[25].setAnswer(7)
medium1[28].setAnswer(5)
medium1[32].setAnswer(9)
medium1[34].setAnswer(8)
medium1[38].setAnswer(7)
medium1[43].setAnswer(3)
medium1[45].setAnswer(4)
medium1[47].setAnswer(3)
medium1[49].setAnswer(7)
medium1[50].setAnswer(2)
medium1[51].setAnswer(6)
medium1[54].setAnswer(5)
medium1[58].setAnswer(6)
medium1[59].setAnswer(8)
medium1[62].setAnswer(9)
medium1[65].setAnswer(2)
medium1[70].setAnswer(4)
medium1[75].setAnswer(9)
medium1[76].setAnswer(5)

medium2 = emptySudoku()
medium2[0].setAnswer(5)
medium2[5].setAnswer(6)
medium2[8].setAnswer(1)
medium2[11].setAnswer(9)
medium2[12].setAnswer(1)
medium2[13].setAnswer(3)
medium2[17].setAnswer(5)
medium2[20].setAnswer(4)
medium2[23].setAnswer(2)
medium2[24].setAnswer(6)
medium2[25].setAnswer(3)
medium2[27].setAnswer(4)
medium2[29].setAnswer(8)
medium2[37].setAnswer(9)
medium2[38].setAnswer(5)
medium2[42].setAnswer(7)
medium2[43].setAnswer(1)
medium2[51].setAnswer(3)
medium2[53].setAnswer(4)
medium2[55].setAnswer(8)
medium2[56].setAnswer(7)
medium2[57].setAnswer(6)
medium2[60].setAnswer(5)
medium2[63].setAnswer(6)
medium2[67].setAnswer(5)
medium2[68].setAnswer(3)
medium2[69].setAnswer(9)
medium2[72].setAnswer(3)
medium2[75].setAnswer(8)
medium2[80].setAnswer(7)

medium3 = emptySudoku()
medium3[2].setAnswer(5)
medium3[5].setAnswer(8)
medium3[6].setAnswer(6)
medium3[8].setAnswer(1)
medium3[9].setAnswer(7)
medium3[13].setAnswer(2)
medium3[17].setAnswer(9)
medium3[18].setAnswer(8)
medium3[19].setAnswer(4)
medium3[25].setAnswer(3)
medium3[28].setAnswer(7)
medium3[29].setAnswer(3)
medium3[30].setAnswer(6)
medium3[31].setAnswer(8)
medium3[32].setAnswer(5)
medium3[33].setAnswer(1)
medium3[37].setAnswer(5)
medium3[39].setAnswer(2)
medium3[45].setAnswer(2)
medium3[46].setAnswer(9)
medium3[49].setAnswer(1)
medium3[53].setAnswer(3)
medium3[56].setAnswer(7)
medium3[59].setAnswer(2)
medium3[60].setAnswer(8)
medium3[61].setAnswer(5)
medium3[62].setAnswer(4)
medium3[63].setAnswer(6)
medium3[70].setAnswer(1)
medium3[71].setAnswer(7)
medium3[75].setAnswer(7)
medium3[76].setAnswer(9)
medium3[78].setAnswer(2)

medium4 = emptySudoku()
medium4[0].setAnswer(1)
medium4[8].setAnswer(3)
medium4[12].setAnswer(7)
medium4[15].setAnswer(1)
medium4[20].setAnswer(7)
medium4[21].setAnswer(8)
medium4[26].setAnswer(2)
medium4[31].setAnswer(6)
medium4[32].setAnswer(3)
medium4[33].setAnswer(4)
medium4[34].setAnswer(5)
medium4[37].setAnswer(4)
medium4[39].setAnswer(5)
medium4[42].setAnswer(6)
medium4[43].setAnswer(3)
medium4[44].setAnswer(1)
medium4[45].setAnswer(5)
medium4[47].setAnswer(3)
medium4[49].setAnswer(7)
medium4[50].setAnswer(4)
medium4[53].setAnswer(9)
medium4[56].setAnswer(6)
medium4[60].setAnswer(7)
medium4[61].setAnswer(8)
medium4[62].setAnswer(5)
medium4[65].setAnswer(5)
medium4[66].setAnswer(6)
medium4[67].setAnswer(8)
medium4[69].setAnswer(2)
medium4[72].setAnswer(4)
medium4[76].setAnswer(5)
medium4[77].setAnswer(9)
medium4[80].setAnswer(6)

medium5 = emptySudoku()
medium5[1].setAnswer(9)
medium5[2].setAnswer(8)
medium5[8].setAnswer(7)
medium5[9].setAnswer(6)
medium5[15].setAnswer(9)
medium5[18].setAnswer(4)
medium5[23].setAnswer(3)
medium5[26].setAnswer(5)
medium5[27].setAnswer(1)
medium5[28].setAnswer(5)
medium5[31].setAnswer(2)
medium5[32].setAnswer(8)
medium5[33].setAnswer(7)
medium5[34].setAnswer(9)
medium5[37].setAnswer(4)
medium5[39].setAnswer(3)
medium5[40].setAnswer(7)
medium5[42].setAnswer(1)
medium5[43].setAnswer(5)
medium5[44].setAnswer(6)
medium5[46].setAnswer(3)
medium5[47].setAnswer(9)
medium5[50].setAnswer(5)
medium5[51].setAnswer(4)
medium5[64].setAnswer(6)
medium5[65].setAnswer(7)
medium5[67].setAnswer(8)
medium5[69].setAnswer(5)
medium5[71].setAnswer(4)
medium5[77].setAnswer(4)
medium5[78].setAnswer(2)
medium5[79].setAnswer(1)
medium5[80].setAnswer(9)

##hard puzzle
h3 = emptySudoku()
h3[0].setAnswer(1)
h3[5].setAnswer(4)
h3[7].setAnswer(3)
h3[12].setAnswer(3)
h3[15].setAnswer(9)
h3[16].setAnswer(8)
h3[17].setAnswer(4)
h3[18].setAnswer(9)
h3[21].setAnswer(6)
h3[25].setAnswer(7)
h3[32].setAnswer(9)
h3[33].setAnswer(7)
h3[34].setAnswer(5)
h3[38].setAnswer(6)
h3[42].setAnswer(8)
h3[46].setAnswer(1)
h3[47].setAnswer(7)
h3[48].setAnswer(2)
h3[55].setAnswer(5)
h3[59].setAnswer(6)
h3[62].setAnswer(2)
h3[63].setAnswer(6)
h3[64].setAnswer(7)
h3[65].setAnswer(9)
h3[68].setAnswer(3)
h3[73].setAnswer(4)
h3[75].setAnswer(5)
h3[80].setAnswer(7)


##hard puzzle
h4 = emptySudoku()
h4[0].setAnswer(6)
h4[4].setAnswer(3)
h4[7].setAnswer(2)
h4[10].setAnswer(4)
h4[14].setAnswer(8)
h4[18].setAnswer(8)
h4[19].setAnswer(5)
h4[21].setAnswer(2)
h4[22].setAnswer(7)
h4[24].setAnswer(1)
h4[27].setAnswer(3)
h4[33].setAnswer(6)
h4[34].setAnswer(7)
h4[40].setAnswer(2)
h4[46].setAnswer(6)
h4[47].setAnswer(1)
h4[53].setAnswer(5)
h4[56].setAnswer(4)
h4[58].setAnswer(1)
h4[59].setAnswer(9)
h4[61].setAnswer(8)
h4[62].setAnswer(3)
h4[66].setAnswer(4)
h4[70].setAnswer(1)
h4[73].setAnswer(8)
h4[76].setAnswer(5)
h4[80].setAnswer(6)

##hard puzzle
h5 = emptySudoku()
h5[0].setAnswer(4)
h5[4].setAnswer(2)
h5[5].setAnswer(7)
h5[18].setAnswer(8)
h5[19].setAnswer(6)
h5[21].setAnswer(9)
h5[23].setAnswer(4)
h5[24].setAnswer(1)
h5[29].setAnswer(9)
h5[30].setAnswer(7)
h5[31].setAnswer(8)
h5[36].setAnswer(6)
h5[37].setAnswer(2)
h5[43].setAnswer(8)
h5[44].setAnswer(7)
h5[49].setAnswer(1)
h5[50].setAnswer(2)
h5[51].setAnswer(3)
h5[56].setAnswer(5)
h5[57].setAnswer(3)
h5[59].setAnswer(8)
h5[61].setAnswer(1)
h5[62].setAnswer(2)
h5[75].setAnswer(5)
h5[76].setAnswer(6)
h5[80].setAnswer(3)
