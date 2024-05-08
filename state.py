import copy
import random

def random_point(minX: float, maxX: float, minY: float, maxY: float):
    x = random.uniform(minX, maxX)
    y = random.uniform(minY, maxY)
    return x, y

class Cell:
    def __init__(self, numberSeed, numberLarge = 0):
        self.numberSeed: int = numberSeed
        self.numberLarge: int = numberLarge
    
    def __str__(self):
        return self.value()
    
    def emptyCell(self):
        return self.numberSeed == 0 and self.numberLarge == 0
    
    def numberOfSeed(self):
        return self.numberSeed + self.numberLarge
    
    def value(self) -> int:
        return self.numberSeed + self.numberLarge*10
    
    def setSeedZero(self):
        self.numberSeed = 0
        self.numberLarge = 0
        
    def getValue(self):
        value = copy.deepcopy(self.value())
        self.setSeedZero()
        return value
    
    def addOneSeed(self):
        self.numberSeed += 1

class Move():
    def __init__(self, index: int, direction: str):
        #direction = "right" | "left"
        self.index = index
        self.direction = direction

class Board:
    def __init__(self):
        #declare 2 player's seed
        self.playerSeed = 0      #its me
        self.opponentSeed = 0    #its opponent
        
        #state of board
        self.playerCells: list[Cell] = [Cell(5), Cell(5), Cell(5), Cell(5), Cell(5)]
        self.opponentCells: list[Cell] = [Cell(5), Cell(5), Cell(5), Cell(5), Cell(5)]
        
        self.borrowPlayer = 0
        self.borrowOpponent = 0
        
        self.leftLargeCell = Cell(0, 1)    # index: 5 for player, -1 for opponent
        self.rightLargeCell = Cell(0, 1)   # index: -1 for player, 5 for opponent
        
        self.leftNormalPosition = []
        self.rightNormalPosition = []
        
        self.playerNormalPosition = [[], [], [], [], []]
        self.opponentNormalPosition = [[], [], [], [], []]
        
        self.initPosition(-1, -1, -1, -1)
        
    def initPosition(self, baseX: float, baseY: float, cell_width: float, cell_height: float):
        for _ in range(5):
            for __ in range(5):
                x, y = random_point(baseX + 50, baseX + cell_width - 50, baseY + 50, baseY + cell_height - 50)
                self.opponentNormalPosition[_] += [(x, y)]
                self.playerNormalPosition[_] += [(x, y + cell_height)]
            baseX += cell_width
            
    def addPosition(self, side: str, x: float, y: float, indexCell: int = -1):
        if side == 'left':
            self.leftNormalPosition += [(x, y)]
        elif side == 'right':
            self.rightNormalPosition += [(x, y)]
        elif side == 'player':
            self.playerNormalPosition[indexCell] += [(x, y)]
        else:
            self.opponentNormalPosition[indexCell] += [(x, y)]
    
    def removePosition(self, side: str, indexCell: int = -1):
        if side == 'left':
            self.leftNormalPosition.pop()
        elif side == 'right':
            self.rightNormalPosition.pop()
        elif side == 'player':
            self.playerNormalPosition[indexCell].pop()
        else:
            self.opponentNormalPosition[indexCell].pop()
            
    def print(self):
        print("---------------------------------------------")
        print("|      |     |     |     |     |     |      |")
        print(f"|      |  {self.opponentCells[4].value()}  |  {self.opponentCells[3].value()}  |  {self.opponentCells[2].value()}  |  {self.opponentCells[1].value()}  |  {self.opponentCells[0].value()}  |      |")
        print("|      |     |     |     |     |     |      |")
        print(f"|  {self.leftLargeCell.value() if self.leftLargeCell.value() else ' ' + str(self.leftLargeCell.value())}  |-----------------------------|  {self.rightLargeCell.value()}  |")
        print("|      |     |     |     |     |     |      |")
        print(f"|      |  {self.playerCells[0].value()}  |  {self.playerCells[1].value()}  |  {self.playerCells[2].value()}  |  {self.playerCells[3].value()}  |  {self.playerCells[4].value()}  |      |")
        print("|      |     |     |     |     |     |      |")
        print("---------------------------------------------")
        
        print("Player:", self.playerSeed)
        print("Opponent:", self.opponentSeed) 
        
    def terminalState(self):
        if self.leftLargeCell.value() == 0 and self.rightLargeCell.value() == 0:
            for i in range(5):
                self.playerSeed += self.playerCells[i].value()
                self.opponentSeed += self.opponentCells[i].value()
                
            return self.playerSeed - self.borrowPlayer + self.borrowOpponent, self.opponentSeed - self.borrowOpponent + self.borrowPlayer
        return False
    
    def winState(self):
        playerSeed, opponentSeed = self.terminalState()            
        return playerSeed > opponentSeed
    
    def isTerminalState(self):
        return self.leftLargeCell.value() == 0 and self.rightLargeCell.value() == 0
    
    def calcPlayerSeed(self):
        return self.playerSeed - self.borrowPlayer + self.borrowOpponent
    
    def calcOpponentSeed(self):
        return self.opponentSeed - self.borrowOpponent + self.borrowPlayer
    
    def noSeedAllCells(self, side):
        if side == 'player':
            for i in range(5):
                if self.playerCells[i].value() != 0:
                    return
            
            if self.playerSeed < 5:
                self.borrowPlayer = self.borrowPlayer + 5 - self.playerSeed
                self.playerSeed = 0
                self.opponentSeed = self.opponentSeed - (5 - self.playerSeed)
            
            for i in range(len(self.playerCells)):
                self.playerSeed -= 1
                self.playerCells[i].addOneSeed()
                self.addPosition('player', -1, -1, i)
        
        else:
            for i in range(5):
                if self.opponentCells[i].value() != 0:
                    return
                
            if self.opponentSeed < 5:
                self.borrowOpponent = self.borrowOpponent + 5 - self.opponentSeed
                self.opponentSeed = 0
                self.playerSeed = self.playerSeed - (5 - self.opponentSeed)
            
            for i in range(len(self.opponentCells)):
                self.opponentSeed -= 1
                self.opponentCells[i].addOneSeed()
                self.addPosition('opponent', -1, -1, i)
                
    def leftToRight(self, side: str, index: int) -> tuple[str, int, bool]: # return side, next index
        if side == 'rightMiddle' and index == 5:
            return 'opponent', 0, False
        
        if side == 'rightMiddle' and index == -1:
            return 'player', 4, False
        
        if side == 'leftMiddle' and index == 5:
            return 'opponent', 4, True
        
        if side == 'leftMiddle' and index == -1:
            return 'player', 0, True
        
        if side == 'player' and index + 1 == 5:
            return 'rightMiddle', -1, False
        
        if side == 'opponent' and index - 1 == -1:
            return 'rightMiddle', 5, False
        
        if side == 'player':
            return side, index + 1, True
        
        if side == 'opponent':
            return side, index - 1, True
        
    def rightToLeft(self, side: str, index: int) -> tuple[str, int, bool]: # return next index
        if side == 'rightMiddle' and index == -1:
            return 'opponent', 0, False
        
        if side == 'rightMiddle' and index == 5:
            return 'player', 4, False
        
        if side == 'leftMiddle' and index == 5:
            return 'player', 0, True
        
        if side == 'leftMiddle' and index == -1:
            return 'opponent', 4, True
        
        if side == 'opponent' and index + 1 == 5:
            return 'leftMiddle', -1, True
        
        if side == 'player' and index - 1 == -1:
            return 'leftMiddle', 5, True
        
        if side == 'player':
            return side, index - 1, False
        
        if side == 'opponent':
            return side, index + 1, False

    def handleEmptyCell(self, side: str, index: int, left_to_right: bool) -> int:
        # bang bang
        zero = self.playerCells[index].value() if side == 'player' else self.opponentCells[index].value()
        winSeed = 0
        
        while zero == 0:
            side, nextIndex, left_to_right = self.leftToRight(side, index) if left_to_right else self.rightToLeft(side, index)
            
            nextWin = 0
            if side == 'leftMiddle':
                nextWin = self.leftLargeCell.getValue()
                self.removePosition('left', nextIndex)
            elif side == 'rightMiddle':
                nextWin = self.rightLargeCell.getValue()
                self.removePosition('right', nextIndex)
            elif side == 'player':
                nextWin = self.playerCells[nextIndex].getValue()
                self.removePosition('player', nextIndex)
            elif side == 'opponent':
                nextWin = self.opponentCells[nextIndex].getValue()
                self.removePosition('opponent', nextIndex)
            
            if nextWin == 0:
                return winSeed
            
            winSeed += nextWin    
            side, index, left_to_right = self.leftToRight(side, nextIndex) if left_to_right else self.rightToLeft(side, nextIndex)
            if side == 'leftMiddle' or side == 'rightMiddle':
                break
            zero = self.playerCells[index].value() if side == 'player' else self.opponentCells[index].value()
            
        return winSeed

    def playerMove(self, index: int, direction: str):
        self.noSeedAllCells('player')
        
        if self.playerCells[index].value() == 0:
            raise Exception("Ô không có quân, chọn ô khác")
        
        current = self.playerCells[index].value()
        self.playerCells[index].setSeedZero()
        self.removePosition('player', index)
        
        side = 'player'
        left_to_right = True
        if direction == 'left':
            left_to_right = False

        while True:        
            while current != 0:
                if left_to_right:
                    side, index, left_to_right = self.leftToRight(side, index)
                else:
                    side, index, left_to_right = self.rightToLeft(side, index)
                
                current -= 1
                if side == 'leftMiddle':
                    self.leftLargeCell.addOneSeed()
                    self.addPosition('left', -1, -1)
                    
                elif side == 'rightMiddle':
                    self.rightLargeCell.addOneSeed()
                    self.addPosition('right', -1, -1)
                    
                elif side == 'player':
                    self.playerCells[index].addOneSeed()
                    self.addPosition('player', -1, -1, index)
                    
                elif side == 'opponent':
                    self.opponentCells[index].addOneSeed()
                    self.addPosition('opponent', -1, -1, index)
            
            if left_to_right:
                side, index, left_to_right = self.leftToRight(side, index)
            else:
                side, index, left_to_right = self.rightToLeft(side, index)
                    
            if side == 'leftMiddle' or side == 'rightMiddle':
                break

            value = -1
            if side == 'player':
                value = self.playerCells[index].getValue()
                self.removePosition('player', index)
            elif side == 'opponent':
                value = self.opponentCells[index].getValue()
                self.removePosition('opponent', index)
                
            if value == 0:
                self.playerSeed += self.handleEmptyCell(side, index, left_to_right)
                break
            current = value

    def opponentMove(self, index: int, direction: str):
        self.noSeedAllCells('opponent')
        
        if self.opponentCells[index].value() == 0:
            raise Exception("Ô không có quân, chọn ô khác")
        
        current = self.opponentCells[index].value()
        self.opponentCells[index].setSeedZero()
        self.removePosition('opponent', index)
        
        side = 'opponent'
        left_to_right = False
        if direction == 'left':
            left_to_right = True

        while True:        
            while current != 0:
                if left_to_right:
                    side, index, left_to_right = self.leftToRight(side, index)
                else:
                    side, index, left_to_right = self.rightToLeft(side, index)
                
                current -= 1
                if side == 'leftMiddle':
                    self.leftLargeCell.addOneSeed()
                    self.addPosition('left', -1, -1)

                elif side == 'rightMiddle':
                    self.rightLargeCell.addOneSeed()
                    self.addPosition('right', -1, -1)
                    
                elif side == 'player':
                    self.playerCells[index].addOneSeed()
                    self.addPosition('player', -1, -1, index)

                elif side == 'opponent':
                    self.opponentCells[index].addOneSeed()
                    self.addPosition('opponent', -1, -1, index)
            
            if left_to_right:
                side, index, left_to_right = self.leftToRight(side, index)
            else:
                side, index, left_to_right = self.rightToLeft(side, index)
                    
            if side == 'leftMiddle' or side == 'rightMiddle':
                break

            value = -1
            if side == 'player':
                value = self.playerCells[index].getValue()
                self.removePosition('player', index)
            elif side == 'opponent':
                value = self.opponentCells[index].getValue()
                self.removePosition('opponent', index)
                
            if value == 0:
                self.opponentSeed += self.handleEmptyCell(side, index, left_to_right)
                break
            current = value
                
class minimaxNode:
    def __init__(self, level: int = 0, playerTurn: int = 0, index: int = 0, position: int = 0, board: Board = None):
        self.level = level
        self.playerTurn = playerTurn
        self.index = index
        self.position = position

        if playerTurn == 0:
            self.board = Board()
        else:
            self.board = self.build(board)
            
        self.value = self.board.calcPlayerSeed() - self.board.calcOpponentSeed()
        self.threshold = self.value

        self.children = []

    def build(self, board) -> Board:
        if self.playerTurn == 1:
            board.playerMove(self.index, self.position)
        else:
            board.opponentMove(self.index, self.position)
        return board
    
    def isLeaf(self):
        return self.board.isTerminalState()
class minimaxTree:
    def __init__(self, playerTurn):
        self.root = minimaxNode(0, playerTurn)
        self.maxLevel = 10**10
        self.build(self.root)

    def build(self, curNode: minimaxNode):
        if curNode.isLeaf() or curNode.level > self.maxLevel:
            return

        #build children state
        for index in range(5):
            if curNode.playerTurn and curNode.board.playerCells[index] == 0:
                continue
            
            if curNode.playerTurn == 0 and curNode.board.opponentCells[index] == 0:
                continue
            
            for position in ('left', 'right'):
                board = copy.deepcopy(curNode.board)
                
                if curNode.playerTurn == 0:
                    newNode = minimaxNode(1, 1, index, position, board)
                else:
                    newNode = minimaxNode(curNode.level + 1, -curNode.playerTurn, index, position, board)
                curNode.children.append(newNode)
                self.build(newNode)

tree = minimaxTree(0)