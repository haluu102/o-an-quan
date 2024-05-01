import copy

class Cell:
    def __init__(self, numberSeed, numberLarge = 0):
        self.numberSeed = numberSeed
        self.numberLarge = numberLarge
    
    def __str__(self):
        return self.value()
    
    def emptyCell(self):
        return self.numberSeed == 0 and self.numberLarge == 0
    
    def value(self):
        return self.numberSeed + self.numberLarge*10
    
    def setSeedZero(self):
        self.numberSeed = 0
    
    def addOneSeed(self):
        self.numberSeed += 1
    
class Board:
    def __init__(self):
        #declare 2 player's seed
        self.playerSeed = 0      #its me
        self.opponentSeed = 0    #its opponent
        
        #state of board
        self.playerCells: list[Cell] = [Cell(5), Cell(5), Cell(5), Cell(5), Cell(5)]
        self.opponentCells: list[Cell] = [Cell(5), Cell(5), Cell(5), Cell(5), Cell(5)]
        self.leftLargeCell = Cell(0, 1)
        self.rightLargeCell = Cell(0, 1)
    
    def print(self):
        print("---------------------------------------------")
        print("|      |     |     |     |     |     |      |")
        print(f"|      |  {self.opponentCells[4].value()}  |  {self.opponentCells[3].value()}  |  {self.opponentCells[2].value()}  |  {self.opponentCells[1].value()}  |  {self.opponentCells[0].value()}  |      |")
        print("|      |     |     |     |     |     |      |")
        print(f"|  {self.leftLargeCell.value()}  |-----------------------------|  {self.rightLargeCell.value()}  |")
        print("|      |     |     |     |     |     |      |")
        print(f"|      |  {self.playerCells[0].value()}  |  {self.playerCells[1].value()}  |  {self.playerCells[2].value()}  |  {self.playerCells[4].value()}  |  {self.playerCells[4].value()}  |      |")
        print("|      |     |     |     |     |     |      |")
        print("---------------------------------------------")
        
    def terminalState(self):
        if self.leftLargeCell.value() == 0 and self.rightLargeCell.value() == 0:
            for i in range(5):
                self.playerSeed += self.playerCells[i].value()
                self.opponentSeed += self.opponentCells[i].value()
                
            return self.playerSeed, self.opponentSeed
        return False, False
    
    def winState(self):
        playerSeed, opponentSeed = self.terminalState()            
        return playerSeed > opponentSeed
    
    def leftToRight(self, side: str, index: int, take: bool): # return next index, seed
        if side == 'player':
            if index == 5:
                if take:
                    value = copy.deepcopy(self.rightLargeCell.value())
                    self.rightLargeCell.setSeedZero()    
                    return -10, value
                self.rightLargeCell.addOneSeed()
                return -10, -1  # start at index 0 of opponent's side
            
            if take:
                value = copy.deepcopy(self.playerCells[index].value())
                self.playerCells[index].setSeedZero()
                return index + 1, value
            else:
                self.playerCells[index].addOneSeed()
                return index + 1, -1
        else:
            if index == -1:
                if take:
                    value = copy.deepcopy(self.rightLargeCell.value())
                    self.rightLargeCell.setSeedZero()    
                    return -10, value
                self.rightLargeCell.addOneSeed()
                return -4, -1 # start at index 4 of player's side
            
            if take:
                value = copy.deepcopy(self.opponentCells[index].value())
                self.opponentCells[index].setSeedZero()
                return index - 1, value
            else:
                self.opponentCells[index].addOneSeed()
                return index - 1, -1
            
    def rightToLeft(self, side: str, index: int, take: bool):
        if side == 'player':
            if index == -1:
                if take:
                    value = copy.deepcopy(self.leftLargeCell.value())
                    self.leftLargeCell.setSeedZero()    
                    return -10, value
                self.leftLargeCell.addOneSeed()
                return -4, -1 # start at index 4 of opponent's side
            
            if take:
                value = copy.deepcopy(self.playerCells[index].value())
                self.playerCells[index].setSeedZero()
                return index - 1, value
            else:
                self.playerCells[index].addOneSeed()
                return index - 1, -1
        else:
            if index == 5:
                if take:
                    value = copy.deepcopy(self.leftLargeCell.value())
                    self.leftLargeCell.setSeedZero()    
                    return -10, value
                self.leftLargeCell.addOneSeed()
                return -10, -1 # start at index 4 of player's side
            
            if take:
                value = copy.deepcopy(self.opponentCells[index].value())
                self.opponentCells[index].setSeedZero()
                return index + 1, value
            else:
                self.opponentCells[index].addOneSeed()
                return index + 1, -1
    
    def handleEmptyCell(self, index: int, direction: str, side: str, sideCells: list[Cell], sideSeed: int):
        if direction == 'LEFT_TO_RIGHT':
            winSeeds = 0
            while sideCells[index].value() == 0:
                index, value = self.leftToRight(side, index, True)
                self.leftToRight(side, index, True)
                winSeeds += value
            sideSeed += winSeeds
        else:
            winSeeds = 0
            while sideCells[index].value() == 0:
                index, value = self.rightToLeft(side, index, True)
                self.rightToLeft(side, index, True)
                winSeeds += value
            sideSeed += winSeeds
            
    def playerMove(self, index: int, direction: str):
        current = self.playerCells[index].value()
        self.playerCells[index].setSeedZero()
        
        left_to_right: bool
        if direction == 'left':
            index -= 1
            left_to_right = False
            updateCurrent = False

            while current >= 0:
                if left_to_right:
                    if current == 0:
                        index, value = self.leftToRight('opponent', index, True)
                        current = value
                        updateCurrent = True
                    else:    
                        index, value = self.leftToRight('opponent', index, False)
                    if index < 0: 
                        left_to_right = False
                    index = index = 0 if index == -10 else -index if index == -4 else index
                    
                    if current == 0:
                        self.handleEmptyCell(index, 'LEFT_TO_RIGHT' if left_to_right == True else 'RIGHT_TO_LEFT', 'opponent', self.opponentCells, self.playerSeed)
                        break
                else:
                    if current == 0:
                        index, value = self.rightToLeft('player', index, True)
                        current = value
                        updateCurrent = True
                    else:    
                        index, value = self.rightToLeft('player', index, False)
                    
                    if index < 0: 
                        left_to_right = True
                    index = index = 0 if index == -10 else -index if index == -4 else index
                    
                    if current == 0:
                        self.handleEmptyCell(index, 'LEFT_TO_RIGHT' if left_to_right == True else 'RIGHT_TO_LEFT', 'player', self.playerCells, self.opponentSeed)
                        break
                if updateCurrent:
                    updateCurrent = False
                else:
                    current -= 1
        else:
            left_to_right = True
            index += 1
            updateCurrent = False

            while current > 0:
                if left_to_right:
                    if current == 0:
                        index, value = self.leftToRight('player', index, True)
                        current = value
                        updateCurrent = True
                    else:    
                        index, value = self.leftToRight('player', index, False)
                    if index < 0: 
                        left_to_right = False
                    index = index = 0 if index == -10 else -index if index == -4 else index
                    
                    if current == 0:
                        self.handleEmptyCell(index, 'LEFT_TO_RIGHT' if left_to_right == True else 'RIGHT_TO_LEFT', 'player', self.playerCells, self.opponentSeed)
                        break
                else:
                    if current == 0:
                        index, value = self.rightToLeft('opponent', index, True)
                        current = value
                        updateCurrent = True
                    else:    
                        index, value = self.rightToLeft('opponent', index, False)
                    if index < 0: 
                        left_to_right = True
                    index = index = 0 if index == -10 else -index if index == -4 else index
                    
                    if current == 0:
                        self.handleEmptyCell(index, 'LEFT_TO_RIGHT' if left_to_right == True else 'RIGHT_TO_LEFT', 'opponent', self.opponentCells, self.playerSeed)
                        break
                if updateCurrent:
                    updateCurrent = False
                else:
                    current -= 1

    def opponentMove(self, index: int, direction: str):
        current = self.opponentCells[index].value()
        self.opponentCells[index].setSeedZero()
        
        left_to_right: bool
        if direction == 'right':
            left_to_right = False
            index -= 1
            updateCurrent = False

            while current > 0:
                if left_to_right:
                    if current == 0:
                        index, value = self.leftToRight('opponent', index, True)
                        current = value
                        updateCurrent = True
                    else:    
                        index, value = self.leftToRight('opponent', index, False)
                    if index < 0: 
                        left_to_right = False
                    index = index = 0 if index == -10 else -index if index == -4 else index
                    
                    if current == 0:
                        self.handleEmptyCell(index, 'LEFT_TO_RIGHT' if left_to_right == True else 'RIGHT_TO_LEFT', 'opponent', self.opponentCells, self.playerSeed)
                        break
                else:
                    if current == 0:
                        index, value = self.rightToLeft('player', index, True)
                        current = value
                        updateCurrent = True
                    else:    
                        index, value = self.rightToLeft('player', index, False)
                    if index < 0: 
                        left_to_right = True
                    index = index = 0 if index == -10 else -index if index == -4 else index
                    
                    if current == 0:
                        self.handleEmptyCell(index, 'LEFT_TO_RIGHT' if left_to_right == True else 'RIGHT_TO_LEFT', 'player', self.playerCells, self.opponentSeed)
                        break
                if updateCurrent:
                    updateCurrent = False
                else:
                    current -= 1
        else:
            left_to_right = True
            index += 1
            updateCurrent = False

            while current > 0:
                if left_to_right:
                    if current == 0:
                        index, value = self.leftToRight('player', index, True)
                        current = value
                        updateCurrent = True
                    else:    
                        index, value = self.leftToRight('player', index, False)
                    
                    if index < 0: 
                        left_to_right = False
                    index = index = 0 if index == -10 else -index if index == -4 else index
                    
                    if current == 0:
                        self.handleEmptyCell(index, 'LEFT_TO_RIGHT' if left_to_right == True else 'RIGHT_TO_LEFT', 'player', self.playerCells, self.opponentSeed)
                        break
                else:
                    if current == 0:
                        index, value = self.rightToLeft('opponent', index, True)
                        current = value
                        updateCurrent = True
                    else:    
                        index, value = self.rightToLeft('opponent', index, False)
                    if index < 0: 
                        left_to_right = True
                    index = index = 0 if index == -10 else -index if index == -4 else index
                    
                    if current == 0:
                        self.handleEmptyCell(index, 'LEFT_TO_RIGHT' if left_to_right == True else 'RIGHT_TO_LEFT', 'opponent', self.opponentCells, self.playerSeed)
                        break
                if updateCurrent:
                    updateCurrent = False
                else:
                    current -= 1

                
board = Board()
board.playerMove(0, 'left')
board.print()