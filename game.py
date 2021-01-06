
from grid import *
from collections import deque
import re

class Player():

    def __init__(self, grid, numPlayers, pN):
        self.grid = grid
        self.pN = pN # player number
        self.plays = [] # Each player's opportunities for offensive attacks: a list of Play objects
        self.combos = {"closed4": [(fr'[^0{pN}]{pN}{{4}}0', 5), (fr'[^0{pN}]{pN}{{3}}0{pN}', 4), (fr'[^0{pN}]{pN}{pN}0{pN}{pN}', 3), (fr'[^0{pN}]{pN}0{pN}{{3}}', 2), (fr'[^0{pN}]0{pN}{{4}}', 1)],
                       "semiopen3": [(fr'0{pN}0{pN}{pN}0', 2), (fr'0{pN}{pN}0{pN}0', 3)],
                       "open3": [(fr'0{pN}{{3}}0', 0), (fr'0{pN}{{3}}0', 4)],
                       "closed3": [(fr'[^0{pN}]{pN}{{3}}00', 4), (fr'[^0{pN}]{pN}{pN}0{pN}0', 3), (fr'[^0{pN}]{pN}{pN}00{pN}', 3), (fr'[^0{pN}]{pN}0{pN}0{pN}', 2), (fr'[^0{pN}]{pN}0{pN}0{pN}', 4), (fr'[^0{pN}]{pN}0{pN}{pN}0', 2), (fr'[^0{pN}]{pN}0{pN}{pN}0', 5),
                                   (fr'00{pN}{{3}}[^0{pN}]', 1), (fr'0{pN}0{pN}{pN}[^0{pN}]', 2), (fr'{pN}00{pN}{pN}[^0{pN}]', 2), (fr'{pN}0{pN}0{pN}[^0{pN}]', 3), (fr'{pN}0{pN}0{pN}[^0{pN}]', 1), (fr'0{pN}{pN}0{pN}[^0{pN}]', 3), (fr'0{pN}{pN}0{pN}[^0{pN}]', 0),
                                   (fr'[^0{pN}]0{pN}{{3}}0[^0{pN}]', 5), (fr'[^0{pN}]0{pN}{{3}}0[^0{pN}]', 1)],
                       "semiopen2": [(fr'0{pN}0{pN}0', 2)],
                       "open2": [(fr'0{pN}{pN}00', 3), (fr'00{pN}{pN}0', 1)],} # Dict[str, List[(str, int)]]

    def sort_plays(self):
        self.plays.sort(key=lambda p : p.strength, reverse=True)

    def getStates(self, square):
        """
        returns list of 4 lists of strings representing the states in all 4 directions
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
            while open <= 3 and closed <= 1 and curr:
                state.appendleft(curr)
                if curr.isFilled == 0:
                    open += 1
                elif curr.isFilled != self.pN:
                    closed += 1
                curr = f1(curr)
            open, closed = 0, 0
            curr = f2(square)
            while open <= 3 and closed <= 1 and curr:
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
        strength = 6
        for attack_type, combos in self.combos.items():
            for reg, i in combos:
                for match in re.finditer(reg, state_as_str):
                    start, end = match.start(0), match.end(0)
                    plays.append(Play(state[start + i], (state[start], state[end-1]), strength))
            strength -= 1
        return plays

    def update(self, square):
        """
        updates and sorts the list of plays
        """
        self.plays = [p for p in self.plays if not p.contains(square)]
        for state in self.getStates(square):
            plays = self.possible_plays(state)
            self.plays.extend(plays)
        self.sort_plays()

    def print_plays(self):
        print(f"Player {self.pN}'s Plays:")
        for p in self.plays:
            print(f"\tPlay(play={p.play.pos}, line={[sq.pos for sq in p.line]}, strength={p.strength}), {p.direction}")
        print()

class Play():
    def __init__(self, play, line, strength):
        self.play = play
        self.line = line # tuple of 2 squares - the beginning and end of the line, inclusive
        self.strength = strength
        self.direction = self.__getDirection()

    def __getDirection(self):
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
        if self.direction == "horizontal":
            return l.x <= square.x <= r.x and square.y == l.y
        elif self.direction == "vertical":
            return l.y >= square.y >= r.x and square.x == l.x
        elif self.direction == "diagonal up":
            return square.x - l.x == l.y - square.y
        elif self.direction == "diagonal down":
            return square.x - l.x == square.y - l.y

    def isEqual(self, other):
        return self.play == other.play and self.line == other.line
