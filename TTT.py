
import pdb
from game import *
from grid import *
from computer import *
import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    KEYUP,
    K_g,
    K_h,
    K_p,
    QUIT,
    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP,
    MOUSEMOTION,
)

pygame.init()
pygame.font.init()

def home_screen():
    screen.fill(WHITE)
    font = pygame.font.SysFont('Comic Sans MS', 24)
    title = font.render('PLAY THIS GAME!', True, ORANGE)
    font2 = pygame.font.SysFont('Comic Sans MS', 14)
    text = font2.render('Press any key to continue', True, ORANGE)
    screen.blit(title, (20, 20))
    screen.blit(text, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

def gameOverScreen(screen):
    font = pygame.font.SysFont('Comic Sans MS', 32)
    text = font.render('GAME OVER', True, PURPLE)
    font2 = pygame.font.SysFont('Comic Sans MS', 16)
    text2 = font2.render("To return to the home screen, press 'h'. To play again, press the space bar", True, PURPLE)
    screen.blit(text, (100, 100))
    screen.blit(text2, (180, 200))

hasGameStarted = False
isGameOver = False

singlePlayer = True
twoPlayer = False

while twoPlayer:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    grid = Grid(surface=screen, cellSize=30, marginSize=20)
    numPlayers = 2
    whoseTurn = 1
    comp = Computer(grid, numPlayers, numPlayers)
    strategy = comp.strategy
    inSameGame = True
    while inSameGame:
        pygame.display.flip()
        event_list = pygame.event.get()
        for event in event_list:
            if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == QUIT:
                grid.printGrid()
                pygame.quit()
                exit()
        if not hasGameStarted:
            home_screen()
            for event in event_list:
                if event.type == KEYDOWN:
                    hasGameStarted = True
        elif isGameOver:
            gameOverScreen(screen)
            for event in event_list:
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        isGameOver = False
                        inSameGame = False
                    elif event.key == K_h:
                        hasGameStarted = False
                        isGameOver = False
                        inSameGame = False
        else:
            for event in event_list:
                if event.type == MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if grid.marginSize < pos[0] < grid.rightBound and grid.marginSize < pos[1] < grid.bottomBound:
                        x = (pos[0] - grid.marginSize) // grid.cellSize
                        y = (pos[1] - grid.marginSize) // grid.cellSize
                        square = grid.grid[x][y]
                        if square.isFilled == 0: # if player clicked an empty square
                            coord = (x * grid.cellSize + grid.marginSize, y * grid.cellSize + grid.marginSize)
                            grid.shapes[whoseTurn - 1].add(coord)
                            square.isFilled = whoseTurn
                            for player in strategy:
                                print(["".join(str(sq.isFilled) for sq in state) for state in player.getStates(square)], end="\n") # DEBUGGING LINE
                                player.update(square)
                                if player.plays and player.plays[0].strength == 7:
                                    print("GAME OVER: ", end="")
                                    player.plays[0].printPlay()
                                    isGameOver = True
                                    break
                            print()
                            whoseTurn = (whoseTurn % numPlayers) + 1
                # FOR DEBUGGING
                if event.type == KEYDOWN:
                    if event.key == K_p:
                        comp.print_plays()
                    if event.key == K_g:
                        grid.printGrid()

            screen.fill(WHITE)
            grid.draw()


while singlePlayer:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    grid = Grid(surface=screen, cellSize=30, marginSize=20)
    numPlayers = 2
    computerTurn = 2
    whoseTurn = 2 # computer goes first
    isFirstMove = True
    comp = Computer(grid, numPlayers, numPlayers)
    strategy = comp.strategy
    inSameGame = True
    while inSameGame:
        pygame.display.flip()
        event_list = pygame.event.get()
        for event in event_list:
            if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == QUIT:
                grid.printGrid()
                pygame.quit()
                exit()
        if not hasGameStarted:
            home_screen()
            for event in event_list:
                if event.type == KEYDOWN:
                    hasGameStarted = True
        elif isGameOver:
            gameOverScreen(screen)
            for event in event_list:
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        isGameOver = False
                        inSameGame = False
                    elif event.key == K_h:
                        hasGameStarted = False
                        isGameOver = False
                        inSameGame = False
        elif whoseTurn == computerTurn: # NEEDS TO FIRST CHECK IF OPPONENT HAS PLAY OF STRENGTH 4+ !!!
            if isFirstMove:
                best_move = grid.grid[grid.colNb // 2 - 1][grid.rowNb // 2 - 1]
                isFirstMove = False
            else:
                best_move = strategy[1].plays[0].play # returns a Square, given that list of plays is non-empty
            x, y = best_move.x, best_move.y
            square = grid.grid[x][y]
            coord = (x * grid.cellSize + grid.marginSize, y * grid.cellSize + grid.marginSize)
            grid.shapes[whoseTurn - 1].add(coord)
            square.isFilled = whoseTurn
            for player in strategy:
                print(["".join(str(sq.isFilled) for sq in state) for state in player.getStates(square)], end="\n") # DEBUGGING LINE
                player.update(square)
                if player.plays and player.plays[0].strength == 7:
                    print("GAME OVER: ", end="")
                    player.plays[0].printPlay()
                    isGameOver = True
                    break
                player.print_plays()
            print()
            whoseTurn = (whoseTurn % numPlayers) + 1
        else:
            for event in event_list:
                if event.type == MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if grid.marginSize < pos[0] < grid.rightBound and grid.marginSize < pos[1] < grid.bottomBound:
                        x = (pos[0] - grid.marginSize) // grid.cellSize
                        y = (pos[1] - grid.marginSize) // grid.cellSize
                        square = grid.grid[x][y]
                        if square.isFilled == 0: # if player clicked an empty square
                            coord = (x * grid.cellSize + grid.marginSize, y * grid.cellSize + grid.marginSize)
                            grid.shapes[whoseTurn - 1].add(coord)
                            square.isFilled = whoseTurn
                            for player in strategy:
                                print(["".join(str(sq.isFilled) for sq in state) for state in player.getStates(square)], end="\n") # DEBUGGING LINE
                                player.update(square)
                                if player.plays and player.plays[0].strength == 7:
                                    print("GAME OVER: ", end="")
                                    player.plays[0].printPlay()
                                    isGameOver = True
                                    break
                                player.print_plays()
                            print()
                            whoseTurn = (whoseTurn % numPlayers) + 1
                # FOR DEBUGGING
                if event.type == KEYDOWN:
                    if event.key == K_p:
                        comp.print_plays()
                    if event.key == K_g:
                        grid.printGrid()

            screen.fill(WHITE)
            grid.draw()

comp.print_plays()
grid.printGrid()
