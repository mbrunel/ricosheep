moves = {"left": (-1, 0), "up": (0, -1), "right": (1, 0), "down": (0, 1)}
sorts = {"left": lambda x: x[0], "up": lambda x: x[1], "right": lambda x: -x[0], "down": lambda x: -x[1]}

class Cell:
    def __init__(self, v):
        self.v = v
        self.nearest_bushes = {"left": None, "up": None, "right": None, "down": None}
    
    def is_bush(self):
        return self.v == "B"
    
    def is_grass(self):
        return self.v == "G"


class Game:

    def compute_bushes(self):
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                for direction in moves:
                    while 0 < x < self.width and 0 < y < self.height:
                        if self.board[y][x].is_bush():
                            self.board[y][x].nearest_bushes[direction] = (x, y)

    def load(self, filename):
        file = open(filename)
        self.board = []
        self.sheeps = []
        row = []
        for c in file.read():
            if c == "\n":
                self.board.append(row)
                row = []
                continue
            if c == "S":
                self.sheeps.append([len(row), len(self.board)])
            if c == "S" or c == "_":
                row.append(Cell(None))
            else:
                row.append(Cell(None))
        if len(row):
            self.board.append(row)
        self.height = len(self.board)
        self.width = len(self.board[0])
        self.compute_bushes()

    def getGameState(self):
        return self.board
    
    def play(self, direction):
        move = moves[direction]
        self.sheeps.sort(key=sorts[direction])
        cache = {}
        for sheep in self.sheeps:
             nearest_bush = self.board[sheep[0]][sheep[1]].nearest_bushes[direction]
             if nearest_bush in cache:
    def isWon(self):
        for x, y in self.sheeps:
            if self.board[y][x] != 'G':
                return False
        return True
    
    def printBoard(self):
        c = ''
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if [j, i] in self.sheeps:
                    if self.board[i][j] == 'G':
                        c = 'H'
                    else:
                        c = 'S'
                elif self.board[i][j] == None:
                    c = '_'
                else:
                    c = self.board[i][j]
                print(c, end=' ')
            print()

if __name__ == "__main__":
    game = Game()
    game.load("../assets/maps/big/huge.txt")
    while not game.isWon():
        game.printBoard()
        try:
            game.play(input("Your move : "))
        except KeyError:
            print("You can only enter 'left' 'up' 'down' and 'right'")
        print("*" * game.width * 2)
    game.printBoard()
    print("YOU WON")