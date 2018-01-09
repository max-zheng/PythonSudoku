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

    # before solving, go through given known values and update adjacent
    def firstPass(self):
        for row in range(9):
            for col in range(9):
                currentCell = self.puzzle[row][col]
                if currentCell.isKnown:
                    self.visitCell(row,col,currentCell)

    # visit the cell and update adjacent row, col, and 3x3 block cells
    def visitCell(self,row,col,cell):
        self.knownSquares += 1
        self.updateSameRow(row,cell.num)
        self.updateSameColumn(row,cell.num)
        self.updateSameBlock(row,col,cell.num)

    # given a known value, remove that value from the list of possibilities for all cells in that row
    def updateSameRow(self,row,value):
        valueUpdated = False
        for col in range(9):
            isCellKnown = self.puzzle[row][col].isKnown
            isValueAPossibility = self.puzzle[row][col].values[value - 1]
            if not isCellKnown and isValueAPossibility:
                # if yes then remove it from the list of possibilities
                isCellKnown = False
                valueUpdated = True
        return valueUpdated

    # given a known value, remove that value from the list of possibilities for all cells in that column
    def updateSameColumn(self,col,value):
        valueUpdated = False
        for row in range(9):
            isCellKnown = self.puzzle[row][col].isKnown
            isValueAPossibility = self.puzzle[row][col].values[value - 1]
            if not isCellKnown and isValueAPossibility:
                # if yes then remove it from the list of possibilities
                isCellKnown = False
                valueUpdated = True
        return valueUpdated

    # given a known value, remove that value from the list of possibilities for all cells in that 3x3 block
    def updateSameBlock(self,row,col,value):
        valueUpdated = False
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
                    isCellKnown = False
                    valueUpdated = True

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
                            currentCell.setCellToKnown(oneValidValue)
                            self.visitCell(row,col,currentCell)
            self.printPuzzle()
                            # puzzleUpdated = True
            # if puzzleUpdated == False:
                # self.printPuzzle()
                # print "Puzzle is invalid!"
                # sys.exit(0)

        print "Puzzle is solved"


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
                    print '-',
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
