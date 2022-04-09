import queue

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

MOVES = {"left": Dot(-1, 0), "up": Dot(0, -1), "right": Dot(1, 0), "down": Dot(0, 1)}

class Cell:
    def __init__(self, v):
        self.v = v
        self.nearest_bushes = {"left": None, "up": None, "right": None, "down": None}
    
    def is_bush(self):
        return self.v == "B"
    
    def is_grass(self):
        return self.v == "G"


class Game:

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

    def compute_bushes(self):
        def find_nearest_bush(self, x, y, direction, MOVES):
            cell = Dot(x, y)
            if self.board[y][x].is_bush():
                self.board[y][x].nearest_bushes[direction] = cell
            else:
                cell += MOVES[direction]
                if -1 < cell.x < self.width and -1 < cell.y < self.height:
                    self.board[y][x].nearest_bushes[direction] = self.board[cell.y][cell.x].nearest_bushes[direction]
                else:
                    self.board[y][x].nearest_bushes[direction] = cell

        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                find_nearest_bush(self, x, y, "left", MOVES)
                find_nearest_bush(self, x, y, "up", MOVES)
        for y in reversed(range(len(self.board))):
            for x in reversed(range(len(self.board[y]))):
                find_nearest_bush(self, x, y, "right", MOVES)
                find_nearest_bush(self, x, y, "down", MOVES)

    def move(self, direction):
        move = MOVES[direction]
        cache = {}
        for sheep in self.sheeps:
            nearest_bush = self.board[sheep.y][sheep.x].nearest_bushes[direction]
            if nearest_bush not in cache:
                cache[nearest_bush] = 0
            cache[nearest_bush] += 1
            sheep.set(nearest_bush - move * cache[nearest_bush])

    def isWon(self, sheeps):
        for sheep in sheeps:
            if not self.board[sheep.y][sheep.x].is_grass():
                return False
        return True

    def solve(self):
        visited = []
        to_treat_queue = queue.Queue(self.sheeps, None)
        while len(to_treat_queue):
            to_treat = to_treat_list.pop()
            if self.isWon(to_treat[0]):
                return to_treat[1]
            


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
            game.move(input("Your move : "))
        except KeyError:
            print("You can only enter 'left' 'up' 'down' and 'right'")
        print("*" * game.width * 2)
    game.printBoard()
    print("YOU WON")