import  wx
from sudoku import Sudoku
from cell import Cell

# 3x3 grid each consisting of 9 cells
class Block(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self,parent,style=wx.BORDER_RAISED)
        self.size = wx.GridSizer(3,3,0,0)
        for i in range(9):
            cell = wx.TextCtrl(self,style=wx.TE_CENTER)
            # only want to have one digit per cell
            cell.SetMaxLength(1)
            self.size.Add(cell,0,wx.GROW)

        self.SetSizer(self.size)

# the entire 9x9 sudoku puzzle
class SudokuGrid(wx.Panel):

    def __init__(self,parent):
        wx.Panel.__init__(self,parent)
        # 3x3 sizer of 3x3 grids
        self.sz = wx.GridSizer(3,3,0,0)
        for i in range(9):
            self.sz.Add(Block(self),0,wx.GROW)
        self.SetSizer(self.sz)

class Interface(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self,None, title="Sudoku Solver")
        button = wx.Button(self,label="Solve")
        button.Bind(wx.EVT_BUTTON, self.onButton)
        grid = SudokuGrid(self)
        textValue = "\n\nPlease fill in the givens with values 1-9"
        textbox = wx.TextCtrl(self,value=textValue,style=wx.TE_READONLY | wx.TE_MULTILINE | wx.ALIGN_CENTER)

        self.size = wx.BoxSizer(wx.VERTICAL)
        self.size.Add(button,1,wx.GROW)
        self.size.Add(grid,10,wx.GROW)
        self.size.Add(textbox,3,wx.GROW)
        self.SetSizer(self.size)
        self.Show()
        self.Centre()

        self.sudoku = None

    # when solve is pressed, populate backend grid using user given values
    def onButton(self,event):
        if self.size.GetChildren()[0].GetWindow().GetLabel() == "Solve":
            self.sudoku = Sudoku(self.createPuzzleFromGrid())
            self.sudoku.printPuzzle()
            # no error message
            self.sudoku.beforeSolveVisitKnownCells()
            errorMessage = self.sudoku.checkForInvalidBoard()
            if errorMessage == "":
                self.sudoku.solve()
                self.populateGridUsingPuzzle()
                # change button label to "Solve another puzzle"
                self.size.GetChildren()[0].GetWindow().SetLabel("Solve another puzzle?")
                self.size.GetChildren()[2].GetWindow().SetValue("\n\nSolved!")
            else:
                self.size.GetChildren()[2].GetWindow().SetValue("\n\n" + errorMessage)
        # else if it says "Solve another puzzle?"
        else:
            self.resetGrid()
            self.size.GetChildren()[0].GetWindow().SetLabel("Solve")
            self.size.GetChildren()[2].GetWindow().SetValue("\n\nPlease fill in the givens with values 1-9")

    # checks if cell string is a digit from 1-9
    def isIntegerExcludingZero(self,str):
        return str.isdigit() and str != "0"

    # similar to constructPuzzle() but instead of prompting the user, it scrapes from the user edited grid interface
    def createPuzzleFromGrid(self):
        puzzle = list()
        # get a list of all blocks
        blocks = self.size.GetChildren()[1].GetWindow().sz.GetChildren()

        # from blocks 1-3, get first 3 rows and append to puzzle
        for squareCounter in range(0,9,3):
            firstThreeRows = []
            for block in range(0,3):
                for square in range(0 + squareCounter,3 + squareCounter):
                    number = blocks[block].GetWindow().size.GetChildren()[square].GetWindow()
                    if self.isIntegerExcludingZero(number.GetValue()):
                        # change color to blue because it is a given
                        number.SetForegroundColour(wx.BLUE)
                        firstThreeRows.append(Cell(int(number.GetValue())))
                    else:
                        firstThreeRows.append(Cell())
            puzzle.append(firstThreeRows)

        # from blocks 4-6, get second 3 rows
        for squareCounter in range(0,9,3):
            secondThreeRows = []
            for block in range(3,6):
                for square in range(0 + squareCounter,3 + squareCounter):
                    number = blocks[block].GetWindow().size.GetChildren()[square].GetWindow()
                    if self.isIntegerExcludingZero(number.GetValue()):
                        number.SetForegroundColour(wx.BLUE)
                        secondThreeRows.append(Cell(int(number.GetValue())))
                    else:
                        secondThreeRows.append(Cell())
            puzzle.append(secondThreeRows)

        # from blocks 7-9, get last 3 rows
        for squareCounter in range(0,9,3):
            lastThreeRows = []
            for block in range(6,9):
                for square in range(0 + squareCounter,3 + squareCounter):
                    number = blocks[block].GetWindow().size.GetChildren()[square].GetWindow()
                    if self.isIntegerExcludingZero(number.GetValue()):
                        number.SetForegroundColour(wx.BLUE)
                        lastThreeRows.append(Cell(int(number.GetValue())))
                    else:
                        lastThreeRows.append(Cell())
            puzzle.append(lastThreeRows)
        return puzzle

    # using the backend sudoku puzzle, populate the GUI grid
    def populateGridUsingPuzzle(self):

        blocks = self.size.GetChildren()[1].GetWindow().sz.GetChildren()

        sudokuRow = 0
        sudokuCol = 0
        for squareCounter in range(0,9,3):
            for block in range(0,3):
                for square in range(0 + squareCounter,3 + squareCounter):
                    number = blocks[block].GetWindow().size.GetChildren()[square].GetWindow()
                    number.SetValue(str(self.sudoku.puzzle[sudokuRow][sudokuCol].num))
                    number.SetEditable(False)
                    sudokuCol += 1
            # reached end of col, need to reset col and increment row
            sudokuCol = 0
            sudokuRow += 1

        for squareCounter in range(0,9,3):
            for block in range(3,6):
                for square in range(0 + squareCounter,3 + squareCounter):
                    number = blocks[block].GetWindow().size.GetChildren()[square].GetWindow()
                    number.SetValue(str(self.sudoku.puzzle[sudokuRow][sudokuCol].num))
                    number.SetEditable(False)
                    sudokuCol += 1
            # reached end of col, need to reset col and increment row
            sudokuCol = 0
            sudokuRow += 1

        for squareCounter in range(0,9,3):
            for block in range(6,9):
                for square in range(0 + squareCounter,3 + squareCounter):
                    number = blocks[block].GetWindow().size.GetChildren()[square].GetWindow()
                    number.SetValue(str(self.sudoku.puzzle[sudokuRow][sudokuCol].num))
                    number.SetEditable(False)
                    sudokuCol += 1

            # reached end of col, need to reset col and increment row
            sudokuCol = 0
            sudokuRow += 1

    # reset the grid back all empty cells
    def resetGrid(self):

        blocks = self.size.GetChildren()[1].GetWindow().sz.GetChildren()
        for block in blocks:
            for square in block.GetWindow().size.GetChildren():
                square.GetWindow().SetValue("")
                square.GetWindow().SetEditable(True)

# runs the program
if  __name__    ==  "__main__":
    app = wx.App(redirect=False)
    gui = Interface()
    app.MainLoop()
