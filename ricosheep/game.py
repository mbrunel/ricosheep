moves = {"left": (-1, 0), "up": (0, 1), "right": (1, 0), "down": (0, 1)}

class Game:
    def __init__(self, board, sheeps):
        self.board = board
        self.sheeps = sheeps
        self.width = len(board)
        self.length = len(board[0])

    def getGameState(self):
        return self.board
    
    def play(self, direction):
        move = moves[direction]
        for x, y in self.sheeps:
            newx = x + move[0]
            newy = y + move[1]
            while 0 <= newx < self.width and 0 <= newy < self.length:
                if self.board[newy][newx] == "G":
                    break
                x = newx
                y = newy
                newx += move[0]
                newy += move[1]
            self.board[y][x] = "S"
            self.sheeps = (x, y)
    
    def printBoard(self):
        for row in self.board:
            for case in row:
                print(case, end=" ")
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
            row.append(c)
        except:
            print("corrupted map")
            return None
    return board, sheeps

if __name__ == "__main__":
    game = Game(*parser("../assets/maps/big/big1.txt"))
    game.printBoard()
    game.play("left")
    print("********************************")
    game.printBoard()