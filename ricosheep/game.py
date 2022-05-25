from collections import deque
from random import randrange, choice

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hash = None
    
    def __add__(self, o):
        return Dot(self.x + o.x, self.y + o.y)
    
    def __sub__(self, o):
        return Dot(self.x - o.x, self.y - o.y)
    
    def __mul__(self, scal):
        return Dot(self.x * scal, self.y * scal)
    
    def __eq__(self, o):
        return self.x == o.x and self.y == o.y
    
    def __ne__(self, o):
        return not self == o
    
    def __hash__(self):
        if not self.hash:
            self.hash = (self.x, self.y).__hash__()
        return self.hash
    
    def set(self, other):
        self.x = other.x
        self.y = other.y
        self.hash = other.hash
    
    def clone(self):
        new_dot = Dot(self.x, self.y)
        new_dot.hash = self.hash
        return new_dot

MOVES = {"left": Dot(-1, 0), "up": Dot(0, -1), "right": Dot(1, 0), "down": Dot(0, 1)}

class Cell:
    def __init__(self, v, pos):
        self.v = v
        self.pos = pos
        self.nearest_bushes = {"left": None, "up": None, "right": None, "down": None}
    
    def is_bush(self):
        return self.v == "B"
    
    def is_grass(self):
        return self.v == "G"

class Parser:
    def __init__(self, file):
        self.file = file
    
    def load(self):
        '''return a list representing the board and a list of sheeps from a map'''
        file = open(self.file)
        board = []
        sheeps = []
        row = []
        x = 0
        y = 0
        for c in file.read():
            pos = Dot(x, y)
            if c == "\n":
                if board and len(row) != len(board[-1]):
                    raise Exception("Invalid board")
                board.append(row)
                row = []
                y += 1
                x = 0
                continue
            elif c == "S":
                row.append(Cell(None, pos))
                sheeps.append(pos.clone())
            elif c == "_":
                row.append(Cell(None, pos))
            else:
                row.append(Cell(c, pos))
            x += 1
        if len(row):
            if board and len(row) != len(board[-1]):
                raise Exception("Invalid board")
            board.append(row)
        return board, sheeps

class Board:
    def __init__(self, board=None, width=0, height=0):
        '''create a new Board instance from either a list or dimensions'''
        self.board = board
        if not self.board:
            self.__generate_board(width, height)
        self.width = len(self.board[0])
        self.height = len(self.board)
        self.nbGrass = 0
        self.__compute_bushes()

    def __getitem__(self, pos):
        return self.board[pos.y][pos.x]

    def __compute_bushes(self):
        '''precompute the nearest bushes for each cell to speed up the sheep's movements'''
        def find_nearest_bush(self, pos, direction):
            cell = self[pos]
            if cell.is_bush():
                cell.nearest_bushes[direction] = cell.pos
            else:
                nearest = pos + MOVES[direction]
                if -1 < nearest.x < self.width and -1 < nearest.y < self.height:
                    cell.nearest_bushes[direction] = self[nearest].nearest_bushes[direction]
                else:
                    cell.nearest_bushes[direction] = cell.pos

        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                pos = Dot(x, y)
                if self[pos].is_grass():
                    self.nbGrass += 1
                find_nearest_bush(self, pos, "left")
                find_nearest_bush(self, pos, "up")
        for y in reversed(range(len(self.board))):
            for x in reversed(range(len(self.board[y]))):
                pos = Dot(x, y)
                find_nearest_bush(self, pos, "right")
                find_nearest_bush(self, pos, "down")
        
    def __generate_board(self, width, height):
        '''randomly generate a board of width and height'''
        self.board = []
        self.width = width
        self.height = height
        proba_bush = randrange(5, 8)
        prng = ['_' for _ in range(proba_bush)]
        prng[0] = 'B'
        for y in range(self.height):
            row = []
            for x in range(self.width):
                c = prng[randrange(proba_bush)]
                row.append(Cell(c, Dot(x, y)))
            self.board.append(row)

class Game:
    def __init__(self, board, sheeps=None, nbSheeps=0):
        '''onstruct a new game instance'''
        self.board = board
        if sheeps:
            self.sheeps = sheeps
            self.hash = None
            self.moves = []
            self.states = [[s.clone() for s in self.sheeps]]
        else:
            self.new_sheeps(nbSheeps)

    def move(self, direction):
        '''moves sheeps on the board according to direction'''
        move = MOVES[direction]
        cache = {}
        for sheep in self.sheeps:
            nearest_bush = self.board[sheep].nearest_bushes[direction]
            if nearest_bush not in cache:
                if self.board[nearest_bush].is_bush():
                    cache[nearest_bush] = 0
                else:
                    cache[nearest_bush] = -1
            cache[nearest_bush] += 1
            sheep.set(self.board[nearest_bush - move * cache[nearest_bush]].pos)
        self.hash = None
        self.moves.append(direction)
        self.states.append([s.clone() for s in self.sheeps])

    def isWon(self):
        '''return true if the game is won'''
        nbHidden = 0
        for sheep in self.sheeps:
            if self.board[sheep].is_grass():
                nbHidden += 1
            if nbHidden == self.board.nbGrass:
                return True
        return False

    def solve(self):
        '''return the shortest list of input possible to solve the game'''

        visited = {self}
        pending = deque([self])
        first = True
        while pending:
            current = pending.popleft()
            if current.isWon():
                return current.moves
            for key, value in MOVES.items():
                if current.moves and not first:
                    first = False
                    prev = MOVES[current.moves[-1]]
                else:
                    prev = Dot(0, 0)
                if value == prev or value == prev * -1:
                    continue
                next = current.clone()
                next.move(key)
                if next not in visited:
                    pending.append(next)
                    visited.add(next)
        return None

    def generate_solution(self, solution_depth):
        '''put bushes on the the board so that the map has a minimal solution of at most solution_depth'''
        visited = {self.__hash__()}
        clone = self.clone()
        prev = Dot(0, 0)
        nb_retry = 0
        while solution_depth > 0:
            if clone.moves:
                prev = MOVES[clone.moves[-1]]
            clone.move(choice([key for key, value in MOVES.items() if value != prev and value != prev * -1]))
            if clone.__hash__() not in visited:
                visited.add(clone.__hash__())
                solution_depth -= 1
            else:
                clone.rewind(-1)
                nb_retry += 1
                if nb_retry > 100:
                    return False
        for sheep in clone.sheeps:
            self.board[sheep].v = 'G'
        self.board.nbGrass = len(self.sheeps)
        return True

    def new_sheeps(self, nbSheeps):
        '''correctly put nbSheeps sheeps on the board'''
        self.sheeps = []
        self.moves = []
        self.hash = None
        sheeps = {}
        for _ in range(nbSheeps):
            nb_iteration = 0
            while nb_iteration < self.board.width * self.board.height:
                nb_iteration += 1
                pos = Dot(randrange(self.board.width), randrange(self.board.height))
                if not self.board[pos].is_bush() and pos not in sheeps:
                    break
            if nb_iteration == self.board.width * self.board.height:
                return self.new_sheeps(nbSheeps - 1)
            self.sheeps.append(pos)
            sheeps[pos] = pos
        self.states = [[s.clone() for s in self.sheeps]]
        return self.sheeps

    def __hash__(self):
        if not self.hash:
            self.hash = 0
            for sheep in self.sheeps:
                self.hash ^= sheep.__hash__()
        return self.hash
    
    def __eq__(self, o):
        return self.__hash__() == o.__hash__()

    def clone(self):
        '''copy the game state'''
        new_game = Game(self.board, [s.clone() for s in self.sheeps])
        new_game.moves = self.moves.copy()
        new_game.hash = self.hash
        return new_game

    def rewind(self, nbMoves):
        '''go back nbMoves if nbMoves < 0 else go back to the nbMoves move'''
        if not self.moves:
            return
        n = (0 if nbMoves >= 0 else len(self.moves)) + nbMoves
        self.sheeps = [s.clone() for s in self.states[n]]
        for _ in range(n, len(self.moves)):
            self.moves.pop()
            self.states.pop()

    def printBoard(self):
        '''
        print board in terminal
        '''
        for i in range(self.board.height):
            for j in range(self.board.width):
                cell = self.board[Dot(j, i)]
                if cell.pos in self.sheeps:
                    if cell.is_grass():
                        c = 'H'
                    else:
                        c = 'S'
                elif cell.is_grass() or cell.is_bush():
                    c = cell.v
                else:
                    c = '_'
                print(c, end=' ')
            print()
        print("*" * (self.board.width * 2 + 1))

if __name__ == "__main__":
    while True:
        board = Board(width=10, height=10)
        game = Game(board, nbSheeps=4)
        game.generate_solution(5)
        solution = game.solve()
        while not game.isWon():
            game.printBoard()
            print(solution)
            try:
                game.move(input("Your move : "))
            except KeyError:
                print("You can only enter 'left' 'up' 'down' and 'right'")
        print("You won !")