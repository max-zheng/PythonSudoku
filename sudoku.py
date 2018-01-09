from cell import Cell

class Sudoku:

    # initialize a sudoku puzzle based on a 2D array which is passed in
    def __init__(self):
        self.puzzle = self.constructPuzzle()

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

    # def solve(self):
    #

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
