
from grid import *
from collections import deque
import re
import pdb
"""
implements Player, Play, and Pivot(Play) classes
"""

class Player():

    def __init__(self, grid, numPlayers, pN):
        self.grid = grid
        self.pN = pN # player number
        self.plays = [] # Each player's opportunities for offensive attacks: a list of Play objects
        self.combos = {"straight5": [(fr'{pN}{{5}}', -1, 0, 0)],
                       "closed4": [(fr'[^0{pN}]{pN}{{4}}0', 5, 1, 0), (fr'[^0{pN}]{pN}{{3}}0{pN}', 4, 1, 0), (fr'[^0{pN}]{pN}{pN}0{pN}{pN}', 3, 1, 0), (fr'[^0{pN}]{pN}0{pN}{{3}}', 2, 1, 0), (fr'[^0{pN}]0{pN}{{4}}', 1, 1, 0),
                                   (fr'0{pN}{{4}}[^0{pN}]', 0, 0, -1), (fr'{pN}0{pN}{{3}}[^0{pN}]', 1, 0, -1), (fr'{pN}{pN}0{pN}{pN}[^0{pN}]', 2, 0, -1), (fr'{pN}{{3}}0{pN}[^0{pN}]', 3, 0, -1), (fr'{pN}{{4}}0[^0{pN}]', 4, 0, -1)],
                       "semiopen3": [(fr'0{pN}0{pN}{pN}0', 2, 0, -1), (fr'0{pN}{pN}0{pN}0', 3, 0, -1)],
                       "open3": [(fr'0{pN}{{3}}0', 0, 0, 0), (fr'0{pN}{{3}}0', 4, 0, 0)],
                       "closed3": [(fr'[^0{pN}]{pN}{{3}}00', 4, 1, 0), (fr'[^0{pN}]{pN}{pN}0{pN}0', 3, 1, 0), (fr'[^0{pN}]{pN}{pN}00{pN}', 3, 1, 0), (fr'[^0{pN}]{pN}0{pN}0{pN}', 2, 1, 0), (fr'[^0{pN}]{pN}0{pN}0{pN}', 4, 1, 0), (fr'[^0{pN}]{pN}0{pN}{pN}0', 2, 1, 0), (fr'[^0{pN}]{pN}0{pN}{pN}0', 5, 1, 0),
                                   (fr'00{pN}{{3}}[^0{pN}]', 1, 0, -1), (fr'0{pN}0{pN}{pN}[^0{pN}]', 2, 0, -1), (fr'{pN}00{pN}{pN}[^0{pN}]', 2, 0, -1), (fr'{pN}0{pN}0{pN}[^0{pN}]', 3, 0, -1), (fr'{pN}0{pN}0{pN}[^0{pN}]', 1, 0, -1), (fr'0{pN}{pN}0{pN}[^0{pN}]', 3, 0, -1), (fr'0{pN}{pN}0{pN}[^0{pN}]', 0, 0, -1),
                                   (fr'[^0{pN}]0{pN}{{3}}0[^0{pN}]', 5, 1, -1), (fr'[^0{pN}]0{pN}{{3}}0[^0{pN}]', 1, 1, -1)],
                       "semiopen2": [(fr'0{pN}0{pN}0', 2, 0, 0), (fr'0{pN}00{pN}0', 2, 1, 0)],
                       "open2": [(fr'0{pN}{pN}00', 3, 0, 0), (fr'00{pN}{pN}0', 1, 0, 0)],
                       "remaining": [(fr'{pN}0{{4}}', 1, 0, 0), (fr'0{pN}0{{3}}', 2, 0, 0), (fr'00{pN}00', 1, 0, 0), (fr'0{{3}}{pN}0', 2, 0, 0), (fr'0{{4}}{pN}', 3, 0, 0), ],
                       } # Dict[str, List[(str, int, int, int)]]

    def getStates(self, square):
        """
        returns list of 4 lists representing the states in all 4 directions around a given square
        """
        funcs = ((Square.get_left, Square.get_right),
                 (Square.get_below, Square.get_above),
                 (Square.get_diag_left_down, Square.get_diag_right_up),
                 (Square.get_diag_left_up, Square.get_diag_right_down))
        states = []
        for f1, f2 in funcs:
            state = deque([square])
            open, closed = 0, 0
            curr = f1(square)
            while open < 3 and closed < 1 and curr:
                state.appendleft(curr)
                if curr.isFilled == 0:
                    open += 1
                elif curr.isFilled != self.pN:
                    closed += 1
                curr = f1(curr)
            open, closed = 0, 0
            curr = f2(square)
            while open < 3 and closed < 1 and curr:
                state.append(curr)
                if curr.isFilled == 0:
                    open += 1
                elif curr.isFilled != self.pN:
                    closed += 1
                curr = f2(curr)
            states.append(list(state))
        return states

    def possible_plays(self, state: "List[Square]"):
        """
        returns list of possible plays given a state (sequence of squares)
        """
        plays = []
        state_as_str = "".join(str(sq.isFilled) for sq in state)
        strength = 7
        for combos in self.combos.values():
            if strength == 0 and plays:
                return plays
            for reg, i, l, r in combos: # i is the index of the play, l is the index of the first square in the line, and r is a negative index of the first square after the line's end (0 if last square is the end)
                for match in re.finditer(reg, state_as_str):
                    start, end = match.start(0), match.end(0)
                    play = Play(state[start + i], (state[start+l], state[end-1+r]), strength)
                    if not any(play.isEqual(p) for p in self.plays):
                        # DEBUGGING CODE
                        l1, l2 = [sq.pos for sq in (state[start+l], state[end-1+r])]
                        if l1[0] - l2[0] not in (-4, 4) and l1[1] - l2[1] not in (-4, 4):
                            pdb.set_trace()
                        if end-1+r - (start+l) > 4: # line should be 5 and only 5 squares
                            pdb.set_trace()
                        plays.append(play)
            strength -= 1

        return plays

    def update(self, square):
        """
        updates and sorts the list of plays (self.plays)
        TODO: Find strength 0 plays when list of plays is empty
        """
        self.plays = [p for p in self.plays if not p.contains(square)] # remove plays containing most recently played square (so they can be re-evaluated)
        states = self.getStates(square)
        state_as_str = ["".join(str(sq.isFilled) for sq in state) for state in states]
        for state in states:
            plays = self.possible_plays(state)
            self.plays.extend(plays)
        self.merge_pivots() # find and merge plays which share the same square (play)
        self.sort_plays() # sort plays in order of decreasing strength

    def merge_pivots(self): # Do I need to handle pivots of 3+ lines?
        temp = {}
        for i, p in enumerate(self.plays):
            if p.play in temp and temp[p.play][1] != p.direction:
                q = temp[p.play][0]
                self.plays[q] = Pivot(self.plays[i].play, self.plays[i].line, self.plays[q].line, 6)
                del self.plays[i]
            else:
                temp[p.play] = i, p.direction

    def sort_plays(self): # sorts list of Plays in decreasing order of strength
        self.plays.sort(key=lambda p : p.strength, reverse=True)
        if self.plays and self.plays[0].strength > 0:
            self.plays = [play for play in self.plays if play.strength > 0] # remove strength 0 plays from list

    def print_plays(self):
        print(f"Player {self.pN}'s Plays:")
        for p in self.plays:
            p.printPlay()
        print()

class Play():
    def __init__(self, play, line, strength):
        self.play = play # square
        self.line = line # tuple of 2 Squares - the beginning and end of the line, inclusive
        self.strength = strength
        self.direction = self.getDirection()

    def getDirection(self): # name mangling
        """
        horizontal: left to right
        vertical: bottom to top (Remember that the y-axis is inverted)
        diagonal up: left to right
        diagonal down: left to right
        """
        if self.line[0].y == self.line[1].y:
            return "horizontal"
        elif self.line[0].x == self.line[1].x:
            return "vertical"
        elif self.line[0].y > self.line[1].y:
            return "diagonal up"
        else:
            return "diagonal down"

    def contains(self, square):
        l, r = self.line
        # 1 extra square checked on both ends
        if self.direction == "horizontal":
            return l.x - 1 <= square.x <= r.x + 1 and square.y == l.y
        elif self.direction == "vertical":
            return l.y + 1 >= square.y >= r.x - 1 and square.x == l.x
        elif self.direction == "diagonal up":
            return square.x - l.x == l.y - square.y
        elif self.direction == "diagonal down":
            return square.x - l.x == square.y - l.y

    def isEqual(self, other):
        return self.play == other.play and self.line == other.line

    def printPlay(self):
        print(f"\tPlay(play={self.play.pos}, line={[sq.pos for sq in self.line]}, strength={self.strength}), {self.direction}")

class Pivot(Play):
    def __init__(self, play, line, line2, strength):
        super().__init__(play, line, 6)
        self.line2 = line2

    # overrides parent function
    def contains(self, square):
        for line in [self.line, self.line2]:
            l, r = line
            # 1 extra square checked on both ends
            if ((self.direction == "horizontal" and l.x - 1 <= square.x <= r.x + 1 and square.y == l.y) or
                (self.direction == "vertical" and l.y + 1 >= square.y >= r.x - 1 and square.x == l.x) or
                (self.direction == "diagonal up" and square.x - l.x == l.y - square.y) or
                (self.direction == "diagonal down" and square.x - l.x == square.y - l.y)):
                return True
        return False

    def next_move(self):
        pass

    def printPlay(self):
        print(f"\tPivot(play={self.play.pos}, lines={[sq.pos for sq in self.line]}, {[sq.pos for sq in self.line2]}, strength={self.strength}), {self.direction}")
