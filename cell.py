class cell():
    
    """A cell is a single unit of a sudoku puzzle. A sudoku puzzle is composed of 81 cells.
    Initialize a cell with a list of possible answers that can be put in
    an answer (if one exists), position in the sudoku puzzle, and whether or not
    the answer has been selected for the box"""
    def __init__(self, position):
        self.possibleAnswers = [1,2,3,4,5,6,7,8,9]
        self.answer = None
        self.position = position
        self.solved = False
    """Removes a value from the list of possible answers for a cell"""
    def remove(self, num):
        if num in self.possibleAnswers and self.solved == False:
            self.possibleAnswers.remove(num)
            if len(self.possibleAnswers) == 1:
                self.answer = self.possibleAnswers[0]
                self.solved = True
        else:
            raise(ValueError)
        
    """Returns whether or not a cell has been solved"""
    def solvedMethod(self):
        return self.solved
    
    """Returns the position of the cell in the sudoku puzzle"""
    def checkPosition(self):
        return self.position
    
    """Returns a list of possible answers that can be filled into the cell"""
    def returnPossible(self):
        return self.possibleAnswers
    
    """Returns the length of the possible answers list as an integer"""
    def lenOfPossible(self):
        return len(self.possibleAnswers)
    
    """Returns the value if the cell has been solved, otherwise it returns false"""
    def returnSolved(self):
        if self.solved == True:
            return self.possibleAnswers[0]
        else:
            return False
        
    """Sets the state of the cell to solved, sets the answer to a num, and eliminates all other
    possible answers from the possible answer list except for the given number"""
    def setAnswer(self, num):
        if num in [1,2,3,4,5,6,7,8,9]:
            self.solved = True
            self.answer = num
            self.possibleAnswers = [num]
        else:
            raise(ValueError)

def emptySudoku():
    ans = []
    for x in range(1,10):
        if x in [7,8,9]:
            z = 3
        if x in [4,5,6]:
            z = 2
        if x in [1,2,3]:
            z = 1
        for y in range(1,10):
            if y in [7,8,9]:
                z += 2
            if y in [4,5,6]:
                z += 1
            if y in [1,2,3]:
                z += 0
            c = cell((x,y,z))
            ans.append(c)
    return ans
