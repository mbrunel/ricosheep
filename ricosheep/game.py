from operator import ne

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, o):
        return Dot(self.x + o.x, self.y + o.y)
    
    def __sub__(self, o):
        return Dot(self.x - o.x, self.y - o.y)
    
    def __iadd__(self, o):
        self.x += o.x
        self.y += o.y
        return self
    
    def __isub__(self, o):
        self.x -= o.x
        self.y -= o.y
        return self
    
    def __mul__(self, scal):
        return Dot(self.x * scal, self.y * scal)
    
    def __imul__(self, scal):
        self.x *= scal
        self.y *= scal
        return self
    
    def __eq__(self, o):
        return self.x == o.x and self.y == o.y
    
    def set(self, new):
        self.x = new.x
        self.y = new.y
    
    def __hash__(self):
        return (self.x, self.y).__hash__()


moves = {"left": Dot(-1, 0), "up": Dot(0, -1), "right": Dot(1, 0), "down": Dot(0, 1)}

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
                for direction, move in moves.items():
                    cell = Dot(x, y)
                    while -1 < cell.x < self.width and -1 < cell.y < self.height and not self.board[cell.y][cell.x].is_bush():
                        cell += move
                    self.board[y][x].nearest_bushes[direction] = cell

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
                self.sheeps.append(Dot(len(row), len(self.board)))
            if c == "S" or c == "_":
                row.append(Cell(None))
            else:
                row.append(Cell(c))
        if len(row):
            self.board.append(row)
        self.height = len(self.board)
        self.width = len(self.board[0])
        self.compute_bushes()

    def getGameState(self):
        return self.board
    
    def play(self, direction):
        move = moves[direction]
        cache = {}
        for sheep in self.sheeps:
            nearest_bush = self.board[sheep.y][sheep.x].nearest_bushes[direction]
            if nearest_bush not in cache:
                cache[nearest_bush] = 0
            cache[nearest_bush] += 1
            sheep.set(nearest_bush - move * cache[nearest_bush])

    def isWon(self):
        for sheep in self.sheeps:
            if not self.board[sheep.y][sheep.x].is_grass():
                return False
        return True
    
    def printBoard(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                c = None
                for sheep in self.sheeps:
                    if sheep.x == j and sheep.y == i:
                        if self.board[i][j].is_grass():
                            c = 'H'
                        else:
                            c = 'S'
                        break
                if not c and not self.board[i][j].v:
                    c = '_'
                elif not c:
                    c = self.board[i][j].v
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