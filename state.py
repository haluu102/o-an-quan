import copy
import sys

sys.setrecursionlimit(10**9 + 10**9)

class Cell:
    def __init__(self, numberSeed, numberLarge = 0):
        self.numberSeed: int = numberSeed
        self.numberLarge: int = numberLarge
    
    def __str__(self):
        return self.value()
    
    def emptyCell(self):
        return self.numberSeed == 0 and self.numberLarge == 0
    
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
    
    def print(self):
        print("---------------------------------------------")
        print("|      |     |     |     |     |     |      |")
        print(f"|      |  {self.opponentCells[4].value()}  |  {self.opponentCells[3].value()}  |  {self.opponentCells[2].value()}  |  {self.opponentCells[1].value()}  |  {self.opponentCells[0].value()}  |      |")
        print("|      |     |     |     |     |     |      |")
        print(f"|  {self.leftLargeCell.value() if self.leftLargeCell.value() else ' ' + str(self.leftLargeCell.value())}  |-----------------------------|  {self.rightLargeCell.value()}  |")
        print("|      |     |     |     |     |     |      |")
        print(f"|      |  {self.playerCells[0].value()}  |  {self.playerCells[1].value()}  |  {self.playerCells[2].value()}  |  {self.playerCells[4].value()}  |  {self.playerCells[4].value()}  |      |")
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
        return False, False
    
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
            if self.playerSeed < 5:
                self.borrowPlayer = self.borrowPlayer + 5 - self.playerSeed
                self.playerSeed = 0
                self.opponentSeed = self.opponentSeed - (5 - self.playerSeed)
            
            for cell in self.playerCells:
                cell.addOneSeed()
        
        else:
            if self.opponentSeed < 5:
                self.borrowOpponent = self.borrowOpponent + 5 - self.opponentSeed
                self.opponentSeed = 0
                self.playerSeed = self.playerSeed - (5 - self.opponentSeed)
            
            for cell in self.opponentCells:
                cell.addOneSeed()
    
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
            
            if side == 'leftMiddle':
                winSeed += self.leftLargeCell.getValue()
            elif side == 'rightMiddle':
                winSeed += self.rightLargeCell.getValue()
            elif side == 'player':
                winSeed += self.playerCells[nextIndex].getValue()
            elif side == 'opponent':
                winSeed += self.opponentCells[nextIndex].getValue()
                
            side, index, left_to_right = self.leftToRight(side, nextIndex) if left_to_right else self.rightToLeft(side, nextIndex)
            if side == 'leftMiddle' or side == 'rightMiddle':
                break
            zero = self.playerCells[index].value() if side == 'player' else self.opponentCells[index].value()
            
        return winSeed

    def playerMove(self, index: int, direction: str):
        self.noSeedAllCells('player')
        
        current = self.playerCells[index].value()
        self.playerCells[index].setSeedZero()
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
                    value = self.leftLargeCell.addOneSeed()
                elif side == 'rightMiddle':
                    value = self.rightLargeCell.addOneSeed()
                elif side == 'player':
                    value = self.playerCells[index].addOneSeed()
                elif side == 'opponent':
                    value = self.opponentCells[index].addOneSeed()
            
            if left_to_right:
                side, index, left_to_right = self.leftToRight(side, index)
            else:
                side, index, left_to_right = self.rightToLeft(side, index)
                    
            if side == 'leftMiddle' or side == 'rightMiddle':
                break

            value = -1
            if side == 'player':
                value = self.playerCells[index].getValue()
            elif side == 'opponent':
                value = self.opponentCells[index].getValue()
                
            if value == 0:
                self.playerSeed += self.handleEmptyCell(side, index, left_to_right)
                break
            current = value

    def opponentMove(self, index: int, direction: str):
        self.noSeedAllCells('opponent')
        
        current = self.opponentCells[index].value()
        self.opponentCells[index].setSeedZero()
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
                    value = self.leftLargeCell.addOneSeed()
                elif side == 'rightMiddle':
                    value = self.rightLargeCell.addOneSeed()
                elif side == 'player':
                    value = self.playerCells[index].addOneSeed()
                elif side == 'opponent':
                    value = self.opponentCells[index].addOneSeed()
            
            if left_to_right:
                side, index, left_to_right = self.leftToRight(side, index)
            else:
                side, index, left_to_right = self.rightToLeft(side, index)
                    
            if side == 'leftMiddle' or side == 'rightMiddle':
                break

            value = -1
            if side == 'player':
                value = self.playerCells[index].getValue()
            elif side == 'opponent':
                value = self.opponentCells[index].getValue()
                
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

    def build(self, board):
        if self.playerTurn == 1:
            board.playerMove(self.index, self.position)
        else:
            board.opponentMove(self.index, self.position)
        return board
    
    def isLeaf(self):
        return self.board.isTerminalState()
    
class minimaxTree:
    def __init__(self):
        self.root = minimaxNode(0)
        self.maxLevel = 10**10
        self.build(self.root)

    def build(self, curNode: minimaxNode):
        if curNode.isLeaf() or curNode.level > self.maxLevel:
            return

        #build children state
        for index in range(5):
            for position in ('left', 'right'):
                board = copy.deepcopy(curNode.board)
                
                if curNode.playerTurn == 0:
                    newNode = minimaxNode(1, 1, index, position, board)
                else:
                    newNode = minimaxNode(curNode.level + 1, -curNode.playerTurn, index, position, board)
                curNode.children.append(newNode)
                self.build(newNode)

tree = minimaxTree()
