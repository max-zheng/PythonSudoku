# help from https://stackoverflow.com/questions/11571905/how-to-make-a-grid-in-wxpython

import  wx
from sudoku import Sudoku
from cell import Cell

# class Cell(wx.Panel): #cell
#     def __init__(self,parent,id,str_val):
#         wx.Panel.__init__(self,parent,id,style=wx.SIMPLE_BORDER)
#         self.size = wx.BoxSizer()
#         self.size.Add(wx.TextCtrl(self,-1,str_val),0,wx.EXPAND)
#         self.SetSizer(self.size)

class Block(wx.Panel): # grid
    """docstring for ."""
    def __init__(self, parent):
        wx.Panel.__init__(self,parent,style=wx.BORDER_RAISED)
        self.size = wx.GridSizer(3,3,0,0)
        for i in range(9):
            textbox = wx.TextCtrl(self,style=wx.TE_CENTER)
            textbox.SetMaxLength(1)
            self.size.Add(textbox,0,wx.GROW)

        self.SetSizer(self.size)

class SudokuGrid(wx.Panel):
    def __init__(self,parent):

        wx.Panel.__init__(self,parent)
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
        textValue = "Please fill in the givens"
        textbox = wx.TextCtrl(self,value=textValue,style=wx.TE_READONLY | wx.TE_MULTILINE | wx.TE_CENTRE)
        self.size = wx.BoxSizer(wx.VERTICAL)
        self.size.Add(button,0,wx.GROW)
        self.size.Add(grid,3,wx.GROW)
        self.size.Add(textbox,0,wx.GROW)
        self.SetSizer(self.size)
        self.Show()
        self.Centre()

        self.puzzle = None

    def onButton(self,event):
        self.puzzle = Sudoku(self.createPuzzleFromGrid())
        self.puzzle.printPuzzle()

    def isIntegerExcludingZero(self,str):
        return len(str) == 1 and str.isdigit() and str != "0"

    def createPuzzleFromGrid(self):
        puzzle = list()
        # get a list of all blocks
        blocks = self.size.GetChildren()[1].GetWindow().sz.GetChildren()

        # from blocks 1-3, get first 3 rows and append to puzzle
        for squareCounter in range(0,9,3):
            firstThreeRows = []
            for block in range(0,3):
                for square in range(0 + squareCounter,3 + squareCounter):
                    number = blocks[block].GetWindow().size.GetChildren()[square].GetWindow().GetValue()
                    if self.isIntegerExcludingZero(number):
                        firstThreeRows.append(Cell(int(number)))
                    else:
                        firstThreeRows.append(Cell())
            puzzle.append(firstThreeRows)

        # from blocks 4-6, get second 3 rows
        for squareCounter in range(0,9,3):
            secondThreeRows = []
            for block in range(3,6):
                for square in range(0 + squareCounter,3 + squareCounter):
                    number = blocks[block].GetWindow().size.GetChildren()[square].GetWindow().GetValue()
                    if self.isIntegerExcludingZero(number):
                        secondThreeRows.append(Cell(int(number)))
                    else:
                        secondThreeRows.append(Cell())
            puzzle.append(secondThreeRows)

        # from blocks 7-9, get last 3 rows
        for squareCounter in range(0,9,3):
            lastThreeRows = []
            for block in range(6,9):
                for square in range(0 + squareCounter,3 + squareCounter):
                    number = blocks[block].GetWindow().size.GetChildren()[square].GetWindow().GetValue()
                    if self.isIntegerExcludingZero(number):
                        lastThreeRows.append(Cell(int(number)))
                    else:
                        lastThreeRows.append(Cell())
            puzzle.append(lastThreeRows)
        return puzzle


if  __name__    ==  "__main__":
    a   =   wx.App(redirect=False)
    # f1 = wx.Frame(None,-1)
    # f   =   MyCustomPanel(f1,-1)
    i = Interface()
    a.MainLoop()
