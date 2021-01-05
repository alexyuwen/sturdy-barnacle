import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    KEYUP,
    QUIT,
    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP,
    MOUSEMOTION,
)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (127, 0, 255)
GREEN = (0, 153, 0)
ORANGE = (255, 128, 0)

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 720
CELL_SIZE = 24
GRID_MARGIN_SIZE = 20 # size of left and upper margins
RIGHT_BOUNDARY = CELL_SIZE * ((SCREEN_WIDTH - 2 *  GRID_MARGIN_SIZE) // CELL_SIZE)
BOTTOM_BOUNDARY = GRID_MARGIN_SIZE + ((SCREEN_HEIGHT // CELL_SIZE - 2) - 1) * CELL_SIZE

class Grid():
    def __init__(self, surface, cellSize):
        self.surface = surface
        self.colNb = (surface.get_width() - 2 *  GRID_MARGIN_SIZE) // cellSize
        self.lineNb = surface.get_height() // cellSize - 2
        self.cellSize = cellSize
        self.grid = [[0 for i in range(self.colNb)] for j in range(self.lineNb)]
        self.circles = set() # set of tuples containing coordinates of top left corner of squares with O's in them
        self.crosses = set() # set of tuples containing coordinates of top left corner of squares with X's in them

    def draw(self):
        for li in range(self.lineNb):
            liCoord = GRID_MARGIN_SIZE + li * self.cellSize
            pygame.draw.line(self.surface, BLACK, (GRID_MARGIN_SIZE, liCoord), (RIGHT_BOUNDARY, liCoord))
        for co in range(self.colNb):
            colCoord = GRID_MARGIN_SIZE + co * self.cellSize
            pygame.draw.line(self.surface, BLACK, (colCoord, GRID_MARGIN_SIZE), (colCoord, BOTTOM_BOUNDARY))

        thickness = 2
        radius = self.cellSize // 3
        for xp, yp in self.circles:
            center = (xp + self.cellSize / 2, yp + self.cellSize / 2)
            pygame.draw.circle(self.surface, BLUE, center, radius, thickness)
        crossMargin = self.cellSize // 5
        for xp, yp in self.crosses:
            center = (xp + self.cellSize / 2, yp + self.cellSize / 2)
            pygame.draw.line(self.surface, RED, (xp + crossMargin, yp + crossMargin), (xp + self.cellSize - crossMargin, yp + self.cellSize - crossMargin), thickness) # downward diagonal
            pygame.draw.line(self.surface, RED, (xp + self.cellSize - crossMargin, yp + crossMargin), (xp + crossMargin, yp + self.cellSize - crossMargin), thickness) # upward diagonal

def home_screen():
    screen.fill(WHITE)
    font = pygame.font.SysFont('Comic Sans MS', 20)
    surf = font.render('HELLO, PLAY THIS GAME!', False, ORANGE)
    screen.blit(surf, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
grid = Grid(screen, CELL_SIZE)

running = True
isPlayer1sTurn = True
hasGameStarted = False
isGameOver = False

while running:
    event_list = pygame.event.get()

    for event in event_list:
        if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == QUIT:
            running = False
    if not running:
        pygame.quit()
        break

    if not hasGameStarted:
        home_screen()
        for event in event_list:
            if event.type == KEYUP:
                hasGameStarted = True

    elif isGameOver:
        pass

    else:
        for event in event_list:
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if GRID_MARGIN_SIZE < pos[0] < RIGHT_BOUNDARY and GRID_MARGIN_SIZE < pos[1] < BOTTOM_BOUNDARY:
                    xp = ((pos[0] - GRID_MARGIN_SIZE) // CELL_SIZE) * CELL_SIZE + GRID_MARGIN_SIZE
                    yp = ((pos[1] - GRID_MARGIN_SIZE) // CELL_SIZE) * CELL_SIZE + GRID_MARGIN_SIZE
                    if isPlayer1sTurn and (xp, yp) not in grid.circles:
                        grid.crosses.add((xp, yp))
                    elif not isPlayer1sTurn and (xp, yp) not in grid.crosses:
                        grid.circles.add((xp, yp))
                    isPlayer1sTurn = not isPlayer1sTurn

        screen.fill(WHITE)
        grid.draw()

    pygame.display.flip()
