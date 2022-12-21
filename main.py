import math
import time
from level import TILE_TYPES, Level
import os


class Robot:
    def __init__(self, level):
        self.level = level
        self.pos = level.start_point
        self.facing = 0  # angle 0, pi/2, pi, 3pi/2,

    def fd(self):
        dx = int(math.cos(self.facing))
        dy = int(-math.sin(self.facing))
        new_pos = self.pos[0] + dy, self.pos[1] + dx
        if self.check(new_pos):
            self.pos = new_pos

        else:
            print("you can't go there")
            time.sleep(1)

    def lt(self):
        self.facing += math.pi / 2
        self.facing %= math.pi * 2

    def rt(self):
        self.facing -= math.pi / 2
        self.facing %= math.pi * 2

    def draw(self):
        board = self.level.num_board

        board[self.pos[0]][self.pos[1]] = "p"
        for i in board:
            print(*[get_code(j) for j in i], sep=" ")

        if self.facing == 0:
            dircet = "→"
        elif self.facing == math.pi / 2:
            dircet = "↑"
        elif self.facing == math.pi:
            dircet = "←"
        elif self.facing == (math.pi * 3) / 2:
            dircet = "↓"

        print(f"you are facing {dircet}")

    def check(self, pos):
        level = self.level.level
        if level[pos[0]][pos[1]] == TILE_TYPES.NONE:
            return False

        return True

    def graverty_idk(self):
        level = self.level.level
        if self.pos[0] < len(level) - 1:
            
            if level[self.pos[0]+1][self.pos[1]] != TILE_TYPES.NONE:
                self.pos = (self.pos[0]+1, self.pos[1])
    
    def do(self, func):
        self.graverty_idk()
        func(self)
    
def get_code(char):
    char = str(char)
    if char == "0":
        return "\u001b[47;1m \u001b[0m"
    elif char == "p":
        return "\u001b[41m \u001b[0m"
    elif char == "3":
        return "\u001b[42m \u001b[0m"
    else:
        return " "

def get_code(char):
    char = str(char)
    if char == "0":
        return " "
    elif char == "1":
        return "■"
    elif char == "3":
        return "■"
    elif char == "p":
        return "p"
    else:
        return " "

def _get_input(message, ans_type, vals):
    while True:
        try:
            val = input(message)
            val = ans_type(val)
            if val in vals:
                return val

        except IndexError:
             print(f"you have {len(vals)} opptions why did you go and choose that one")
        

def convert_type(inp):
    return str(inp)[0]


def get_input():
    
    moves = {"a": "go forward", "b": "turn left", "c": "turn right"}
    print("What do you want to do?")
    QUESTION = ""
    for i in moves:
        QUESTION+=(f"{i}: {moves[i]}\n")

    ans = _get_input(QUESTION, convert_type, list(moves.keys()))
    vals = {
        "a": Robot.fd,
        "b": Robot.lt,
        "c": Robot.rt,
    }

    return vals[ans.lower()]


def main():

    level = Level("./levels/level_one.json")
    r = Robot(level)

    while True:
        # os.system("clear")
        r.draw()
        r.do(get_input())


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Bye!!")
