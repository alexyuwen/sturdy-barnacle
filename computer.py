from game import *

class Computer():

    def __init__(self, grid, numPlayers, playerNum):
        self.grid = grid
        self.numPlayers = numPlayers
        self.playerNum = playerNum
        self.strategy = [Player(grid, numPlayers, playerNum) for playerNum in range(1, numPlayers + 1)]

    def next_move(self):
        pass

    def print_plays(self):
        for player in self.strategy:
            player.print_plays()
