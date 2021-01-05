from collections import deque
import re

class Player():

    def __init__(self, grid, numPlayers, pN):
        self.grid = grid
        self.pN = pN # player number
        self.plays = [] # Each player's opportunities for offensive attacks
        self.combos = {"closed3": [(fr'[^01]{pN}{{3}}00', 4), (fr'[^01]{pN}{pN}0{pN}0', 3), (fr'[^01]{pN}{pN}00{pN}', 3), (fr'[^01]{pN}0{pN}0{pN}', 2), (fr'[^01]{pN}0{pN}0{pN}', 4), (fr'[^01]{pN}0{pN}{pN}0', 2), (fr'[^01]{pN}0{pN}{pN}0', 5),
                                   (fr'00{pN}{{3}}[^01]', 1), (fr'0{pN}0{pN}{pN}[^01]', 2), (fr'{pN}00{pN}{pN}[^01]', 2), (fr'{pN}0{pN}0{pN}[^01]', 3), (fr'{pN}0{pN}0{pN}[^01]', 1), (fr'0{pN}{pN}0{pN}[^01]', 3), (fr'0{pN}{pN}0{pN}[^01]', 0)],
                       "semiopen2": [(fr'0{pN}0{pN}0', 2)],
                       "open2": [(fr'0{pN}{pN}00', 3), (fr'00{pN}{pN}0', 1)],} # Dict[str, List[(str, int)]]

    def update(self, square):
        def analyze_state(state: "List[Square]"):
            plays = []
            state_as_str = "".join(str(sq.isFilled) for sq in state)
            strength = 3
            for attack_type, combos in self.combos.items():
                for reg, i in combos:
                    for match in re.finditer(reg, state_as_str):
                        start, end = match.start(0), match.end(0)
                        plays.append(Play(state[start + i], state[start:end], strength))
                strength -= 1
            return plays
            streak = 0
            if streak == 5:
                return # GAME OVER!

        horizState = deque([square])
        open = 0
        closed = 0
        curr = square.get_left()
        while open <= 3 and closed <= 1 and curr:
            horizState.appendleft(curr)
            if curr.isFilled == 0:
                open += 1
            elif curr.isFilled != self.pN:
                closed += 1
            curr = curr.get_left()

        open = 0
        closed = 0
        curr = square.get_right()
        while open <= 3 and closed <= 1 and curr:
            horizState.append(curr)
            if curr.isFilled == 0:
                open += 1
            elif curr.isFilled != self.pN:
                closed += 1
            curr = curr.get_right()

        self.plays = analyze_state(list(horizState)) + self.plays

class Play():
    def __init__(self, play, line, strength):
        self.play = play
        self.line = line
        self.strength = strength

    def isEqual(self, other):
        return self.play == other.play and self.line == other.line
