import sys
from cell import Cell

class Sudoku:

    # initialize a sudoku puzzle based on a 2D array which is passed in
    def __init__(self):
        self.puzzle = self.constructPuzzle()
        self.knownSquares = 0

    # takes user input and changes it to a list of cells
    def changeInputToList(self,input):
        cellList = list()
        for i in range(9):
            if input[i] == '0':
                cellList.append(Cell())
            else:
                cellList.append(Cell(int(input[i])))
        return cellList

    # construct the puzzle by prompting user for each row
    def constructPuzzle(self):
        puzzle = list()
        for i in range(9):
            row = str(raw_input("Enter row %d of the puzzle. Enter a 0 for each blank space.\n-> " % (i + 1)))
            while len(row) != 9:
                row = str(raw_input("Invalid. Please enter 9 digits. Enter row %d of the puzzle. Enter a 0 for each blank space.\n-> " % (i + 1)))
            puzzle.append(self.changeInputToList(row))
        return puzzle

    # checks if current instance of board is valid. E.G. no 2 of same number in one row, col, 3x3 grid.
    def isBoardValid(self):
        isValid = True
        # iterate through row and col 1-9
        for num in range(9):
            if not self.isRowValid(num) or not self.isColumnValid(num):
                isValid = False

        # iterate through each grid
        for row in range(0,9,3):
            for col in range(0,9,3):
                if not self.isGridValid(row,col):
                    isValid = False
        return isValid

    # check for condition where one cell cannot be occupied by any number due to invalid board setup
    def isThereNoPossibleCandidates(self):
        noPossibleCandidates = False

        for row in range(9):
            for col in range(9):
                if not self.puzzle[row][col].isKnown:
                    if self.puzzle[row][col].values == [False,False,False,False,False,False,False,False,False]:
                        noPossibleCandidates = True
        return noPossibleCandidates

    # before solving, go through given known values and update adjacent. Also checks for the condition of insufficient givens
    def firstPass(self):
        for row in range(9):
            for col in range(9):
                currentCell = self.puzzle[row][col]
                if currentCell.isKnown:
                    self.visitCell(row,col,currentCell)

        if self.knownSquares < 17:
            print "Cannot solve puzzle. Insufficient givens. Puzzle must start with at least 17 known values for it to have one unique solution."
            self.printPuzzle()
            sys.exit(0)
        if not self.isBoardValid():
            print "Cannot solve puzzle. Duplicate given. Either a row, column, or grid has 2 of the same value."
            self.printPuzzle()
            sys.exit(0)
        if self.isThereNoPossibleCandidates():
            print "Cannot solve puzzle. At least one cell has no possible candidates."
            self.printPuzzle()
            sys.exit(0)

    # visit the cell and update adjacent row, col, and 3x3 block cells
    def visitCell(self,row,col,cell):
        self.knownSquares += 1
        self.updateSameRow(row,cell.num)
        self.updateSameColumn(col,cell.num)
        self.updateSameBlock(row,col,cell.num)

    # given a known value, remove that value from the list of possibilities for all cells in that row
    def updateSameRow(self,row,value):
        for col in range(9):
            isCellKnown = self.puzzle[row][col].isKnown
            isValueAPossibility = self.puzzle[row][col].values[value - 1]
            if not isCellKnown and isValueAPossibility:
                # if yes then remove it from the list of possibilities
                self.puzzle[row][col].values[value - 1] = False

    # given a known value, remove that value from the list of possibilities for all cells in that column
    def updateSameColumn(self,col,value):
        for row in range(9):
            isCellKnown = self.puzzle[row][col].isKnown
            isValueAPossibility = self.puzzle[row][col].values[value - 1]
            if not isCellKnown and isValueAPossibility:
                # if yes then remove it from the list of possibilities
                self.puzzle[row][col].values[value - 1] = False

    # given a known value, remove that value from the list of possibilities for all cells in that 3x3 block
    def updateSameBlock(self,row,col,value):
        # first determine which 3x3 block the cell belongs to
        # we do this by finding the upper left cell of the belonging block
        # math involved: row,col = row - row % 3, col - col % 3
        firstRowOfBlock = row - row % 3
        firstColOfBlock = col - col % 3

        # iterate through the 3x3 block, removing the possibility of value from each cell
        for row in range(3):
            for col in range(3):
                isCellKnown = self.puzzle[firstRowOfBlock + row][firstColOfBlock + col].isKnown
                isValueAPossibility = self.puzzle[firstRowOfBlock + row][firstColOfBlock + col].values[value - 1]
                if not isCellKnown and  isValueAPossibility:
                    # if yes then remove it from the list of possibilities
                    self.puzzle[firstRowOfBlock + row][firstColOfBlock + col].values[value - 1] = False

    def solve(self):

        while(self.knownSquares < 81):
            puzzleUpdated = False
            # iterate through 9x9 grid
            for row in range(9):
                for col in range(9):
                    currentCell = self.puzzle[row][col]
                    if not currentCell.isKnown:
                        validValue = currentCell.checkIfOneValidValue()
                        # if there exists one valid value in the cell
                        if validValue != 0:
                            currentCell.setCellToKnown(validValue)
                            self.visitCell(row,col,currentCell)
                            puzzleUpdated = True
            if puzzleUpdated == False:
                print "Need to use recursive backtracking. Puzzle so far:"
                self.printPuzzle()
                self.recursiveBacktrack()
                return
            else:
                print "Solving in progress"
                self.printPuzzle()

    def recursiveBacktrack(self):
        if self.isBoardValid():
            emptyIndex = self.findFirstUnknownIndex()
            indexRow = emptyIndex[0]
            indexCol = emptyIndex[1]
            if indexRow == -1 and indexCol == -1:
                return True

            for value in range(1,10):
                if self.puzzle[indexRow][indexCol].values[value - 1] == True:
                    self.puzzle[indexRow][indexCol].setCellToKnown(value)
                else:
                    continue
                if self.recursiveBacktrack():
                    return True
                self.puzzle[indexRow][indexCol].setCellToUnknown()
        return False

    # checks if a specific row is valid
    def isRowValid(self,row):
        numberCount = [0,0,0,0,0,0,0,0,0]

        # iterate through each row and count occurances of each number 1-9
        for col in range(9):
            if self.puzzle[row][col].isKnown:
                numberCount[self.puzzle[row][col].num - 1] += 1

        # if there is more than one occurance of a number 1-9, the board is invalid
        for count in numberCount:
            if count > 1:
                return False
        # otherwise the board is valid
        return True

    # checks if a specific column is valid
    def isColumnValid(self,col):
        numberCount = [0,0,0,0,0,0,0,0,0]

        # iterate through each row and count occurances of each number 1-9
        for row in range(9):
            if self.puzzle[row][col].isKnown:
                numberCount[self.puzzle[row][col].num - 1] += 1

        # if there is more than one occurance of a number 1-9, the board is invalid
        for count in numberCount:
            if count > 1:
                return False
        # otherwise the board is valid
        return True

    # checks if a specific 3x3 grid is valid. row, col passed in are the index of the top left cell of the grid
    def isGridValid(self,startRow,startCol):
        numberCount = [0,0,0,0,0,0,0,0,0]

        # iterate through each row and count occurances of each number 1-9
        for row in range(3):
            for col in range(3):
                if self.puzzle[startRow + row][startCol + col].isKnown:
                    numberCount[self.puzzle[startRow + row][startCol + col].num - 1] += 1

        # if there is more than one occurance of a number 1-9, the board is invalid
        for count in numberCount:
            if count > 1:
                return False
        # otherwise the board is valid
        return True

    # iterate through the board to find index of first unknown cell
    def findFirstUnknownIndex(self):
        index = [-1,-1]
        for row in range(9):
            for col in range(9):
                if not self.puzzle[row][col].isKnown:
                    index[0] = row
                    index[1] = col
        return index

    # prints the current state of the puzzle
    def printPuzzle(self):
        # for formatting
        rowCounter = 0
        colCounter = 0
        # upper border
        print "+-------+-------+-------+"
        for row in range(9):
            # left border
            print '|',
            for col in range(9):
                if self.puzzle[row][col].isKnown:
                    print self.puzzle[row][col].num,
                else:
                    print '.',
                # each 3rd column, add a vertical border
                colCounter += 1
                if colCounter == 3:
                    print "|",
                    colCounter = 0
            # no need for right border cause colCounter
            # newline
            print ""
            # each third row add a horizontal border
            rowCounter += 1
            if rowCounter == 3:
                print "+-------+-------+-------+"
                rowCounter = 0
        # no lower border needed because of rowCounter border

    # for debugging purposes
    def printPossibilities(self):
        for row in range(9):
            for col in range(9):
                if self.puzzle[row][col].isKnown:
                    print "(" + str(row) + "," + str(col) + ") Known: " + str(self.puzzle[row][col].num)
                else:
                    print "(" + str(row) + "," + str(col) + ") " + str(self.puzzle[row][col].values)
