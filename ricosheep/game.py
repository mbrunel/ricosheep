GRASS = 1
BUSH = 1 << 1
SHEEP = 1 << 2

moves = {"left": (-1, 0), "up": (0, -1), "right": (1, 0), "down": (0, 1)}
sorts = {"left": lambda x: x[0], "up": lambda x: x[1], "right": lambda x: -x[0], "down": lambda x: -x[1]}
filetoi = {"_": 0, "G": GRASS, "B": BUSH, "S": SHEEP, "H": GRASS|SHEEP}
itofile = {y:x for x,y in filetoi.items()}

class Game:
    def __init__(self, board, sheeps):
        self.board = board
        self.sheeps = sheeps
        self.height = len(board)
        self.width = len(board[0])

    def getGameState(self):
        return self.board
    
    def play(self, direction):
        move = moves[direction]
        self.sheeps.sort(key=sorts[direction])
        for i, sheep in enumerate(self.sheeps):
            x, y = sheep
            self.board[y][x] ^= SHEEP
            while 0 <= x < self.width and 0 <= y < self.height and not self.board[y][x] & BUSH|SHEEP:
                x += move[0]
                y += move[1]
            x -= move[0]
            y -= move[1]
            self.board[y][x] ^= SHEEP
            self.sheeps[i] = (x, y)
    
    def isWon(self):
        for x, y in self.sheeps:
            if ~self.board[y][x] & GRASS|SHEEP:
                return False
        return True
    
    def printBoard(self):
        for row in self.board:
            for case in row:
                print(itofile[case], end=" ")
            print()

def parser(filename):
    file = open(filename)
    board = []
    sheeps = []
    row = []
    for c in file.read():
        if c == "\n":
            board.append(row)
            row = []
            continue
        if c == "S":
            sheeps.append((len(row), len(board)))
        try:
            row.append(filetoi[c])
        except:
            print("corrupted map")
            return None
    board.append(row)
    return board, sheeps

if __name__ == "__main__":
    game = Game(*parser("../assets/maps/big/huge.txt"))
    while not game.isWon():
        game.printBoard()
        try:
            game.play(input("Your move : "))
        except KeyError:
            print("You can only enter 'left' 'up' 'down' and 'right'")
        print("*" * game.width * 2)
    game.printBoard()
    print("YOU WON")