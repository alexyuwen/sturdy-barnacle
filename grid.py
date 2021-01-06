
import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (127, 0, 255)
GREEN = (0, 153, 0)
ORANGE = (255, 128, 0)

SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 720

class Grid():
    def __init__(self, surface, cellSize, marginSize):
        self.surface = surface
        self.colNb = SCREEN_WIDTH // cellSize - 2
        self.rowNb = SCREEN_HEIGHT // cellSize - 2
        self.cellSize = cellSize
        self.marginSize = marginSize
        self.rightBound = self.marginSize + (self.colNb - 1) * self.cellSize
        self.bottomBound = self.marginSize + (self.rowNb - 1) * self.cellSize
        self.grid = [[Square(self, i, j) for j in range(self.rowNb)] for i in range(self.colNb)] # i and j are column and row numbers, not the exact coordinates
        self.shapes = [set(), set()] # list of sets of tuples containing coordinates of top left corner of squares with shapes in them

    def draw(self):
        for li in range(self.rowNb):
            liCoord = self.marginSize + li * self.cellSize
            pygame.draw.line(self.surface, BLACK, (self.marginSize, liCoord), (self.rightBound, liCoord))
        for co in range(self.colNb):
            colCoord = self.marginSize + co * self.cellSize
            pygame.draw.line(self.surface, BLACK, (colCoord, self.marginSize), (colCoord, self.bottomBound))

        thickness = 2
        crossMargin = self.cellSize // 5
        for xp, yp in self.shapes[0]:
            center = (xp + self.cellSize / 2, yp + self.cellSize / 2)
            pygame.draw.line(self.surface, RED, (xp + crossMargin, yp + crossMargin), (xp + self.cellSize - crossMargin, yp + self.cellSize - crossMargin), thickness) # downward diagonal
            pygame.draw.line(self.surface, RED, (xp + self.cellSize - crossMargin, yp + crossMargin), (xp + crossMargin, yp + self.cellSize - crossMargin), thickness) # upward diagonal
        radius = self.cellSize // 3
        for xp, yp in self.shapes[1]:
            center = (xp + self.cellSize / 2, yp + self.cellSize / 2)
            pygame.draw.circle(self.surface, BLUE, center, radius, thickness)

    def printGrid(self):
        for a in self.grid:
            for b in a:
                print("\t", end="")
                b.printSquare()
            print("--------------------------------------------------------------------")


class Square():
    def __init__(self, grid, x, y): # x and y are the column and row numbers, not the exact coordinates
        self.grid = grid
        self.x = x
        self.y = y
        self.pos = (x, y)
        self.coord = (self.x * grid.cellSize + grid.marginSize, self.y * grid.cellSize + grid.marginSize)
        self.isFilled = 0 # 0 means unfilled, 1 means filled by Player 1, 2 means filled by Player 2, etc...

    def printSquare(self):
        print(f"Square({self.pos}, isFilled={self.isFilled})")

    def get_left(self):
        if self.x == 0:
            return None
        return self.grid.grid[self.x - 1][self.y]

    def get_right(self):
        if self.x + 1 == self.grid.colNb:
            return None
        return self.grid.grid[self.x + 1][self.y]

    def get_above(self):
        if self.y == 0:
            return None
        return self.grid.grid[self.x][self.y - 1]

    def get_below(self):
        if self.y + 1 == self.grid.rowNb:
            return None
        return self.grid.grid[self.x][self.y + 1]

    def get_diag_left_up(self):
        if self.x == 0 or self.y == 0:
            return None
        return self.grid.grid[self.x - 1][self.y - 1]

    def get_diag_right_up(self):
        if self.x + 1 == self.grid.colNb or self.y == 0:
            return None
        return self.grid.grid[self.x + 1][self.y - 1]

    def get_diag_left_down(self):
        if self.x == 0 or self.y + 1 == self.grid.rowNb:
            return None
        return self.grid.grid[self.x - 1][self.y + 1]

    def get_diag_right_down(self):
        if self.x + 1 == self.grid.colNb or self.y + 1 == self.grid.rowNb:
            return None
        return self.grid.grid[self.x + 1][self.y + 1]
