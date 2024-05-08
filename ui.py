import sys, pygame
import random
from state import *

pygame.init()

WIDTH = 1200
HEIGHT = 720

CELL_HEIGHT = HEIGHT // 4
CELL_WIDTH = WIDTH // 8

BASE_X = (WIDTH - CELL_WIDTH*7) // 2
BASE_Y = (HEIGHT - CELL_HEIGHT*2) // 2

size = width, height = 1200, 720

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

def fontText(text):
    text = str(text)
    return pygame.font.SysFont('Corbel', 20) .render(text , True , (0, 0, 0))

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
        screen.blit(fontText(board.opponentCells[_].numberOfSeed()) , (baseX + 70, baseY + 16))
        drawNormalSeed(board.opponentNormalPosition[_])
        
        pygame.draw.rect(screen, (170, 170, 170), [baseX + 50, baseY + CELL_HEIGHT, 50, 50]) 
        screen.blit(fontText(board.playerCells[_].numberOfSeed()) , (baseX + 70, baseY + CELL_HEIGHT + 16))
        drawNormalSeed(board.playerNormalPosition[_])
        
    baseX += CELL_WIDTH
    pygame.draw.rect(screen, (170, 170, 170), [baseX, baseY + CELL_HEIGHT*2 - 50, 50, 50]) 
    screen.blit(fontText(board.leftLargeCell.numberOfSeed()) , (baseX + 20, baseY + CELL_HEIGHT*2 - 34))
    if board.leftLargeCell.numberLarge != 0:
        screen.blit(seedImages("large"), (baseX + 20, baseY + 120))
    drawNormalSeed(board.rightNormalPosition)

mainBoard = Board()
mainBoard.initPosition(BASE_X + CELL_WIDTH, BASE_Y, CELL_WIDTH, CELL_HEIGHT)

while True:
    screen.fill((0, 255, 255))
    drawBoard()
    drawSeed(mainBoard)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()
            
            
    pygame.display.update()