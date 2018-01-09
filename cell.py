class Cell:

    # initialize the cell
    def __init__(self, num = None):
        # if no num parameter provided then cell is not known
        if num is None:
            self.isKnown = False
            #values = list of possible values the cell can have.
            #Index of list represents corresponding number offset by 1, because 0 indexed.
            #When it's found that cell cannot be a certain number, change corresponding index to false.
            self.values = [True,True,True,True,True,True,True,True,True]
            self.num = None
        else: # otherwise cell is known
            self.isKnown = True
            self.num = num
            self.values = [False,False,False,False,False,False,False,False,False]
            self.values[num - 1] = True

    # check if cell has only one valid value, in which case it becomes a known cell
    # if one valid value found, return the valid number, otherwise returns 0
    def checkIfOneValidValue(self):
        numberOfValidValues = 0
        indexOfLastValidValue = -1
        for x in range(0,9):
            if self.values[x] == True:
                numberOfValidValues += 1
                indexOfLastValidValue = x
        if numberOfValidValues == 1:
            return indexOfLastValidValue + 1
        else:
            return 0

    # once value of cell is determined, sets cell to be a known cell having the value passed in
    def setCellToKnown(self,num):
        self.isKnown = True
        self.num = num

    # override = operator to check equality based on cell's known value
    # if the value of either cell is not known, then False is returned
    def __eq__(self, other):
        if type(self) == type(other) and self.isKnown == True and other.isKnown == True:
            return self.num == other.num
        return False
