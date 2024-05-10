import sys, pygame
from state import *

CHOOSEN = (220, 20, 60)
NOT_CHOOSEN = (170, 170, 170)

pygame.init()

size = width, height = 1200, 800

pygame.display.set_caption("Ô ĂN QUAN")
icon = pygame.image.load("assets/large-seed.png")
pygame.display.set_icon(icon)
screen = pygame.display.set_mode(size)

def cellImages(type):
    image = pygame.image.load(f"assets/{type}-cell.png")
    image = pygame.transform.scale(image, (CELL_WIDTH, CELL_HEIGHT*2 if "large" in type else CELL_HEIGHT))
    return image

def seedImages(type):
    image = pygame.image.load(f"assets/{type}-seed.png")
    return image

def arrowImages(type):
    image = pygame.image.load(f"assets/{type}-arrow.png")
    return image

def fontText(text):
    text = str(text)
    return pygame.font.SysFont('Corbel', 20) .render(text , True , (0, 0, 0))

def selectMode(mode: str):
    pygame.draw.rect(screen, CHOOSEN if mode == "EASY" else NOT_CHOOSEN, [50, 5, 200, 40]) 
    screen.blit(fontText("EASY") , (70, 15))
    
    pygame.draw.rect(screen, CHOOSEN if mode == "MEDIUM" else NOT_CHOOSEN, [50, 50, 200, 40]) 
    screen.blit(fontText("MEDIUM") , (70, 60))
    
    pygame.draw.rect(screen, CHOOSEN if mode == "HARD" else NOT_CHOOSEN, [50, 95, 200, 40]) 
    screen.blit(fontText("HARD") , (70, 105))
    
def resetBoard(player: int):
    pygame.draw.rect(screen, CHOOSEN if player == 1 else NOT_CHOOSEN, [300, 5, 200, 40]) 
    screen.blit(fontText("PLAYER") , (320, 15))
    
    pygame.draw.rect(screen, CHOOSEN if player == -1 else NOT_CHOOSEN, [300, 50, 200, 40]) 
    screen.blit(fontText("OPPONENT") , (320, 60))
    
def startGame():
    pygame.draw.rect(screen, CHOOSEN if start else NOT_CHOOSEN, [550, 5, 200, 40]) 
    screen.blit(fontText("START") , (570, 15))

def drawBoard():
    baseX = BASE_X
    baseY = BASE_Y
    
    screen.blit(cellImages("left-large"), (baseX, baseY))
        
    for _ in range(5):
        baseX += CELL_WIDTH 
        screen.blit(cellImages("normal"),(baseX, baseY))
        screen.blit(cellImages("normal"),(baseX, baseY + CELL_HEIGHT))
        
    screen.blit(cellImages("right-large"), (baseX + CELL_WIDTH, baseY)) 

def drawNormalSeed(postion: list[tuple[int, int]]):
    for post in postion:
        screen.blit(seedImages("normal"), (post[0], post[1]))

def drawSeed(board: Board):
    baseX = BASE_X
    baseY = BASE_Y
    
    pygame.draw.rect(screen, (170, 170, 170), [baseX + CELL_WIDTH - 50, baseY, 50, 50]) 
    screen.blit(fontText(board.leftLargeCell.numberOfSeed()) , (baseX + CELL_WIDTH - 30, baseY + 16))
    if board.leftLargeCell.numberLarge != 0:
        screen.blit(seedImages("large"), (baseX + 30 , baseY + 120))
    drawNormalSeed(board.leftNormalPosition)
    
    for _ in range(5):
        baseX += CELL_WIDTH

        pygame.draw.rect(screen, (170, 170, 170), [baseX + 50, baseY, 50, 50])
        screen.blit(fontText(board.opponentCells[4 - _].numberOfSeed()) , (baseX + 70, baseY + 16))
        drawNormalSeed(board.opponentNormalPosition[4 - _])
        
        pygame.draw.rect(screen, (170, 170, 170), [baseX + 50, baseY + CELL_HEIGHT, 50, 50]) 
        screen.blit(fontText(board.playerCells[_].numberOfSeed()) , (baseX + 70, baseY + CELL_HEIGHT + 16))
        drawNormalSeed(board.playerNormalPosition[_])
        
    baseX += CELL_WIDTH
    pygame.draw.rect(screen, (170, 170, 170), [baseX, baseY + CELL_HEIGHT*2 - 50, 50, 50]) 
    screen.blit(fontText(board.rightLargeCell.numberOfSeed()) , (baseX + 20, baseY + CELL_HEIGHT*2 - 34))
    if board.rightLargeCell.numberLarge != 0:
        screen.blit(seedImages("large"), (baseX + 20, baseY + 120))
    drawNormalSeed(board.rightNormalPosition)
    
    baseX = BASE_X
    baseY = BASE_Y
    screen.blit(arrowImages("left"), (baseX + 2.5*CELL_WIDTH , baseY + 400))
    screen.blit(arrowImages("right"), (baseX + 4*CELL_WIDTH , baseY + 400))

def scoreBoard(playerSeed: int, opponentSeed: int):
    pygame.draw.rect(screen, NOT_CHOOSEN, [BASE_X + 6*CELL_WIDTH, BASE_Y - 50, 100, 40]) 
    screen.blit(fontText(str(opponentSeed)) , (BASE_X + 6*CELL_WIDTH + 20, BASE_Y - 40))
    
    pygame.draw.rect(screen, NOT_CHOOSEN, [BASE_X + CELL_WIDTH - 100, BASE_Y + CELL_HEIGHT*2 + 5, 100, 40]) 
    screen.blit(fontText(str(playerSeed)) , (BASE_X + CELL_WIDTH - 100 + 20, BASE_Y + CELL_HEIGHT*2 + 15))

def getPlayerIndex(x: list[int], y: int, mouse_pos: tuple[int, int]) -> int:
    if x[0] <= mouse_pos[0] <= x[1] and y <= mouse_pos[1] <= y + CELL_HEIGHT: return 0
    if x[1] <= mouse_pos[0] <= x[2] and y <= mouse_pos[1] <= y + CELL_HEIGHT: return 1
    if x[2] <= mouse_pos[0] <= x[3] and y <= mouse_pos[1] <= y + CELL_HEIGHT: return 2
    if x[3] <= mouse_pos[0] <= x[4] and y <= mouse_pos[1] <= y + CELL_HEIGHT: return 3
    if x[4] <= mouse_pos[0] <= x[5] and y <= mouse_pos[1] <= y + CELL_HEIGHT: return 4

def getPlayerDirection(mouse_pos: tuple[int, int]) -> str:
    if BASE_X + 2.5*CELL_WIDTH <= mouse_pos[0] <= BASE_X + 2.5*CELL_WIDTH + 64 and BASE_Y + 400 <= mouse_pos[1] <= BASE_Y + 400 + 64: return "left"
    if BASE_X + 4*CELL_WIDTH <= mouse_pos[0] <= BASE_X + 4*CELL_WIDTH + 64 and BASE_Y + 400 <= mouse_pos[1] <= BASE_Y + 400 + 64: return "right"

def showWinner(winner: str):        
    pygame.draw.rect(screen, (170, 170, 170), [(WIDTH - 200)/2, 50, 200, 50]) 
    screen.blit(fontText(winner + "WIN") , ((WIDTH - 200)/2 + 55, 65))
    
    trophy = pygame.image.load("assets/trophy.png")
    screen.blit(trophy, ((WIDTH - 200)/2, 50))
    
start = False

mainBoard = Board()
minmaxTree = None
modeLevel = 1
mode = "EASY"

firstPlayer = 1

playerIndex = None
playerDirection = None
playerClick = 0

finalSide = None

while True:
    screen.fill((0, 255, 255))
    
    selectMode(mode)
    resetBoard(firstPlayer)
    startGame()
    
    drawBoard()
    drawSeed(mainBoard)
    scoreBoard(mainBoard.playerSeed, mainBoard.opponentSeed)
    
    xAxis = [BASE_X + CELL_WIDTH, BASE_X + 2*CELL_WIDTH, BASE_X + 3*CELL_WIDTH, BASE_X + 4*CELL_WIDTH,  BASE_X + 5*CELL_WIDTH, BASE_X + 6*CELL_WIDTH]
    yAxis = BASE_Y + CELL_HEIGHT
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start and BASE_X <= mouse_pos[0] <= BASE_X + 7*CELL_WIDTH and BASE_Y <= mouse_pos[1] <= BASE_Y + 3*CELL_HEIGHT:
                if playerClick == 0:
                    playerIndex = getPlayerIndex(xAxis, yAxis, mouse_pos)
                    playerClick = 1
                else:
                    playerDirection = getPlayerDirection(mouse_pos)
                    playerClick = 0

                if playerIndex is not None and playerDirection is not None:
                    print("Player Turn")
                    print(playerIndex, playerDirection)
                    mainBoard.playerMove(playerIndex, playerDirection)
                    mainBoard.print()
                    
                    print("Opponent Turn")
                    minmaxTree = minimaxTree(1, modeLevel, mainBoard)
                    opponentIndex, opponentDirection = minmaxTree.findBestMove()
                    print(opponentIndex, opponentDirection)
                    mainBoard.opponentMove(playerIndex, playerDirection)
                    
            
            if 50 <= mouse_pos[0] <= 250 and 5 <= mouse_pos[1] <= 45:
                mode = "EASY"
                modeLevel = 1
            
            if 50 <= mouse_pos[0] <= 250 and 50 <= mouse_pos[1] <= 90:
                mode = "MEDIUM"
                modeLevel = 3
                
            if 50 <= mouse_pos[0] <= 250 and 95 <= mouse_pos[1] <= 135:
                mode = "HARD"
                modeLevel = 5
                
            if 300 <= mouse_pos[0] <= 500 and 5 <= mouse_pos[1] <= 45:
                firstPlayer = 1
                mainBoard = Board()
                
            if 300 <= mouse_pos[0] <= 500 and 50 <= mouse_pos[1] <= 90:
                firstPlayer = -1
                mainBoard = Board()
                
            if 550 <= mouse_pos[0] <= 750 and 5 <= mouse_pos[1] <= 45:
                start = not start
                print(start)

    if mainBoard.isTerminalState(finalSide):
        showWinner(mainBoard.winner())   

    pygame.display.update()