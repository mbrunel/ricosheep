moves = {"left": (-1, 0), "up": (0, -1), "right": (1, 0), "down": (0, 1)}
sorts = {"left": lambda x: x[0], "up": lambda x: x[1], "right": lambda x: -x[0], "down": lambda x: -x[1]}

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
                self.sheeps.append([len(row), len(self.board)])
            if c == "S" or c == "_":
                row.append(None)
            else:
                row.append(c)
        if len(row):
            self.board.append(row)
        self.height = len(self.board)
        self.width = len(self.board[0])

    def getGameState(self):
        return self.board
    
    def play(self, direction):
        move = moves[direction]
        self.sheeps.sort(key=sorts[direction])
        axe = 0 if move[0] else 1
        maxL = self.height if axe else self.width
        end = maxL if move[axe] > 0 else -1
        cache = [[end, end] for _ in range(max(self.width, self.height))]
        for sheep in self.sheeps:
            i = sheep[abs(axe - 1)]
            end = cache[i][0]
            cache[i][0] = sheep[axe]
            while sheep[axe] != end:
                if (axe == 0 and self.board[i][sheep[axe]] == 'B') or (axe == 1 and self.board[sheep[axe]][i] == 'B'):
                    break
                sheep[axe] += move[axe]
            if sheep[axe] == end:
                sheep[axe] = cache[i][1]
            sheep[axe] -= move[axe]
            cache[i][1] = sheep[axe]
    
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
    game.load("../assets/maps/tests/losable.txt")
    while not game.isWon():
        game.printBoard()
        try:
            game.play(input("Your move : "))
        except KeyError:
            print("You can only enter 'left' 'up' 'down' and 'right'")
        print("*" * game.width * 2)
    game.printBoard()
    print("YOU WON")