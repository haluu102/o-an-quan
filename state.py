import copy
import sys
import random

sys.setrecursionlimit(10**9 + 10**9)

dct = {}

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

    def makeHashString(self):
        return str(self.numberSeed) + "-" + str(self.numberLarge)

    def hash(self):
        return hash((self.numberSeed, self.numberLarge))

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
        
        self.playerLargeSeed = 0      #its me
        self.opponentLargeSeed = 0    #its opponent
        
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

    def hash(self):
        return hash((self.playerCells, self.opponentCells, self.leftLargeCell, self.rightLargeCell))
        
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
        
        print("Player:", self.playerSeed, self.playerLargeSeed)
        print("Opponent:", self.opponentSeed, self.opponentLargeSeed) 
        
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
    
    def shouldPlayerBorrow(self):
        for i in range(5):
                if self.playerCells[i].value() != 0:
                    return False
        return True
            
    def shouldOpponentBorrow(self):
        for i in range(5):
                if self.opponentCells[i].value() != 0:
                    return False
        return True
    
    def noSeedAllCells(self, side):
        if side == 'player':
            for i in range(5):
                if self.playerCells[i].value() != 0:
                    return
            
            if (self.playerLargeSeed == 1 and 10 <= self.playerSeed < 15) or (self.playerLargeSeed == 2 and 20 <= self.playerSeed < 25):
                self.opponentLargeSeed += 1
                self.playerLargeSeed -= 1
            
            if self.playerSeed < 5 and self.opponentSeed >= 5 - self.playerSeed:
                self.borrowPlayer = self.borrowPlayer + 5 - self.playerSeed
                self.opponentSeed = self.opponentSeed - (5 - self.playerSeed)
                self.playerSeed = 5
                        
            for i in range(5):
                if self.playerSeed == 0:
                    break
                
                self.playerSeed -= 1
                self.playerCells[i].addOneSeed()
        
        else:
            for i in range(5):
                if self.opponentCells[i].value() != 0:
                    return
                
            if (self.opponentLargeSeed == 1 and 10 <= self.opponentSeed < 15) or (self.opponentLargeSeed == 2 and 20 <= self.opponentSeed < 25):
                self.playerLargeSeed += 1
                self.opponentLargeSeed -= 1
                
            if self.opponentSeed < 5 and self.playerSeed >= 5 - self.opponentSeed:
                self.borrowOpponent = self.borrowOpponent + 5 - self.opponentSeed
                self.playerSeed = self.playerSeed - (5 - self.opponentSeed)
                self.opponentSeed = 5
            
            for ii in range(5):
                if self.opponentSeed == 0:
                    break
                
                self.opponentSeed -= 1
                self.opponentCells[i].addOneSeed()
                            
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
                
            elif side == 'rightMiddle':
                nextWin = self.rightLargeCell.getValue()
                
            elif side == 'player':
                nextWin = self.playerCells[nextIndex].getValue()
                
            elif side == 'opponent':
                nextWin = self.opponentCells[nextIndex].getValue()
                
            
            if nextWin == 0:
                return winSeed
            
            winSeed += nextWin    
            side, index, left_to_right = self.leftToRight(side, nextIndex) if left_to_right else self.rightToLeft(side, nextIndex)
            if side == 'leftMiddle' or side == 'rightMiddle':
                break
            zero = self.playerCells[index].value() if side == 'player' else self.opponentCells[index].value()
            
        return winSeed

    def playerMove(self, index: int, direction: str):
        leftLargeBelong = not (self.leftLargeCell.numberLarge > 0)
        rightLargeBelong = not (self.rightLargeCell.numberLarge > 0)
        
        self.noSeedAllCells('player')
        
        if self.playerCells[index].value() == 0:
            raise Exception("Ô không có quân, chọn ô khác")
        
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
                    self.leftLargeCell.addOneSeed()
                    
                    
                elif side == 'rightMiddle':
                    self.rightLargeCell.addOneSeed()
                    
                    
                elif side == 'player':
                    self.playerCells[index].addOneSeed()
                    
                    
                elif side == 'opponent':
                    self.opponentCells[index].addOneSeed()
                    
            
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
            
        if (not leftLargeBelong and self.leftLargeCell.numberLarge == 0 ):
            self.playerLargeSeed += 1
        if (not rightLargeBelong and self.rightLargeCell.numberLarge == 0):
            self.playerLargeSeed += 1

    def opponentMove(self, index: int, direction: str):
        leftLargeBelong = not (self.leftLargeCell.numberLarge > 0)
        rightLargeBelong = not (self.rightLargeCell.numberLarge > 0)
        
        self.noSeedAllCells('opponent')
        
        if self.opponentCells[index].value() == 0:
            raise Exception("Ô không có quân, chọn ô khác")
        
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
                    self.leftLargeCell.addOneSeed()
                    

                elif side == 'rightMiddle':
                    self.rightLargeCell.addOneSeed()
                    
                    
                elif side == 'player':
                    self.playerCells[index].addOneSeed()
                    

                elif side == 'opponent':
                    self.opponentCells[index].addOneSeed()
                    
            
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
        
        if (not leftLargeBelong and self.leftLargeCell.numberLarge == 0 ):
            self.playerLargeSeed += 1
        if (not rightLargeBelong and self.rightLargeCell.numberLarge == 0):
            self.playerLargeSeed += 1
                
    def makeHashString(self):
        playerCellsString = "#".join([playerCell.makeHashString() for playerCell in self.playerCells])
        opponentCellsString = "#".join([opponentCell.makeHashString() for opponentCell in self.opponentCells])
        return "#".join((playerCellsString, opponentCellsString, self.leftLargeCell.makeHashString(), self.rightLargeCell.makeHashString()))
class minimaxNode:
    def __init__(self, level: int = 0, playerTurn: int = 0, index: int = 0, position: int = 0, board: Board = None):
        if board is not None and (board.borrowOpponent >= 36 or board.borrowPlayer >= 36):
            board.leftLargeCell.setSeedZero()
            board.rightLargeCell.setSeedZero()
            
        self.level = level
        self.playerTurn = playerTurn
        self.index = index
        self.position = position

        if playerTurn == 0:
            self.board = Board()
            self.board.initPosition(-1, -1, -1, -1)
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
    
    def makeHashString(self):
        return "+".join((str(self.playerTurn), str(self.index), str(self.position), self.board.makeHashString()))
    
    def hash(self):
        return hash((self.playerTurn, self.index, self.position, self.board))
    
class minimaxTree:
    def __init__(self):
        self.root = minimaxNode(0)
        self.maxLevel = 10**10
        self.build(self.root)

    def build(self, curNode: minimaxNode, visited: set = set()):
        print("Level, playerTurn, playedIndex, playedPosition:", curNode.level, curNode.playerTurn, curNode.index, curNode.position)
        curNode.board.print()
        if curNode.isLeaf():
            print("help")
            return

        #print()
        #if (curNode.level == 2):
            #return
        #build children state
        #if (curNode.makeHashString() in visited):
            #print("cuu")
        #dct[curNode.makeHashString()] = dct.get(curNode.makeHashString(), 0) + 1
        #print()
        
        #print()

        for index in range(5):
            # if (curNode.playerTurn == 1 and not curNode.board.shouldOpponentBorrow() and curNode.board.opponentCells[index].value() == 0) or (curNode.playerTurn == -1 and not curNode.board.shouldPlayerBorrow() and curNode.board.playerCells[index].value() == 0):
            #     continue
            
            if (curNode.playerTurn == 1 and curNode.board.opponentCells[index].value() == 0) or (curNode.playerTurn == -1 and curNode.board.playerCells[index].value() == 0):
                continue
            
            for position in ('left', 'right'):
                board = copy.deepcopy(curNode.board)
                
                if curNode.playerTurn == 0:
                    newNode = minimaxNode(1, 1, index, position, board)
                else:
                    newNode = minimaxNode(curNode.level + 1, -curNode.playerTurn, index, position, board)
                    
                if newNode.makeHashString() not in visited:
                    visited.add(newNode.makeHashString())
                    curNode.children.append(newNode)
                    self.build(newNode, visited)
                    visited.remove(newNode.makeHashString())


orig_stdout = sys.stdout
f = open('out.txt', 'w')
sys.stdout = f
tree = minimaxTree()
sys.stdout = orig_stdout
f.close()
#print(dct)