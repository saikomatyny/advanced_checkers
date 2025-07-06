from exceptions import BoardExceptions

class Board:
    def __init__(self):
        self.board = []
        self.rows : int
        self.cols : int

    def create_board(self, rows : int, cols : int):
        if rows < 4 and cols < 3:
            raise BoardExceptions.MinimumSize("Board is too small! Minimum count rows: 4, cols: 3")

        self.rows = rows
        self.cols = cols
        for i in range(rows):
            row = ['_' for _ in range(cols)]
            self.board.append(row)

    def place_checkers(self, checkers_white : int, checkers_black : int):

        if checkers_white < 1 or checkers_black < 1:
            raise BoardExceptions.InvalidAmount("Invalid amount of checkers.")

        if checkers_white > self.rows / 2 - 1:
            raise BoardExceptions.MaxCountCheckers(f"Maximum count rows of white checkers: {self.rows // 2 - 1}, users count: {checkers_white}")

        if checkers_black > self.rows / 2 - 1:
            raise BoardExceptions.MaxCountCheckers(f"Maximum count rows of black checkers: {self.rows // 2 - 1}, users count: {checkers_black}")

        for i in range(checkers_white):
            for j in range(self.cols):
                if (i + j) % 2 == 0:
                    self.board[self.rows - i - 1][j] = 'w'

        for i in range(checkers_black):
            for j in range(self.cols):
                if (i + j) % 2 != 0:
                    self.board[i][j] = 'b'


    def __str__(self):
        string = ''
        for row in self.board:
            string += ' '.join(row) + '\n'

        return string

    def __repr__(self):
        return "Board()"


class Timer:
    def __init__(self, time : int):
        self.time = time
        self.time_is_up = False

    def __str__(self):
        return f"time: {self.time}"

class Player:
    def __init__(self, name, side):
        self.name = name
        self.is_won = False
        self.side = side

    def __str__(self):
        return f"player: {self.name}\nis_won: {self.is_won}\nside: {self.side}"

    def __repr__(self):
        return f"Player({self.name})"

class Side:
    def __init__(self, time, name, side):
        self.timer = Timer(time * 10)
        self.player = Player(name, side)

    def __str__(self):
        return f"player: {self.player.name}\nis_won: {self.player.is_won}\nside: {self.player.side}\ntime: {self.timer.time}"
