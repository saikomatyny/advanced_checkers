from board import Board, Side
from exceptions import MoveExceptions

def initialize_board() -> Board:
    board = Board()

    return board


def main_loop():
    name1 = input("Enter name of first player: ")
    name2 = input("Enter name of second player: ")
    while name1 == name2:
        name2 = input(f"Name {name1} is already chosen. Type something different: ")

    side1 = input(f"Enter letter of your side, {name1}. Ex: 'w': ")
    side2 = input(f"Enter letter of your side, {name2}. Ex: 'b': ")
    while side1 == side2:
        side2 = input(f"Side {side1} is already chosen. Type something different: ")

    time1 = int(input(f"Enter time in minutes for player {name1}: "))
    time2 = int(input(f"Enter time in minutes for player {name2}: "))

    player1 = Side(time1, name1, side1)
    player2 = Side(time2, name2, side2)

    board = initialize_board()

    rows, cols = int(input("Rows: ")), int(input("Cols: "))
    board.create_board(rows, cols)

    checkers_count_1 = int(input(f"Enter rows count of checkers for player {name1} (maximum is {rows // 2 - 1}): "))
    checkers_count_2 = int(input(f"Enter rows count of checkers for player {name2} (maximum is {rows // 2 - 1}): "))

    board.place_checkers(checkers_count_1, checkers_count_2)

    current_side = player1
    while not game_is_over(board, player1, player2):
        print(board)
        x = int(input(f"{current_side.player.name}, enter checker X coordinate: "))
        y = int(input(f"{current_side.player.name}, enter checker Y coordinate: "))
        move = input("Enter move (DR, DL, UR, UL): ")

        try:
            if can_capture_from(board, x, y, move):
                do_capture(board, x, y, move)

                nx, ny = get_destination(x, y, move)
                while True:
                    next_moves = available_captures(board, nx, ny)
                    if not next_moves:
                        break
                    print(f"Additional captures available: {next_moves}")
                    move = input(f"{current_side.player.name}, choose next capture: ")
                    if move not in next_moves:
                        print("Invalid capture move, ending chain.")
                        break
                    do_capture(board, nx, ny, move)
                    nx, ny = get_destination(nx, ny, move)
            else:
                move_checker(board, x, y, move)
        except MoveExceptions.InvalidMoveValue as e:
            print(e)
            continue
        except MoveExceptions.OutOfBoundaries as e:
            print(e)
            continue

        if current_side == player1:
            current_side = player2
        else:
            current_side = player1

    print(board)
    if player1.player.is_won:
        print(f"{player1.player.name} wins!")
    elif player2.player.is_won:
        print(f"{player2.player.name} wins!")
    else:
        print("Time's up!")



def game_is_over(board : Board, white_side : Side, black_side : Side) -> bool:

    base_cases_of_ending_game(white_side, black_side)

    if black_side.timer.time <= 0:
        black_side.timer.time_is_up = True
        return True

    if white_side.timer.time <= 0:
        white_side.timer.time_is_up = True
        return True

    if not checkers_on_board(board, white_side.player.side):
        black_side.player.is_won = True
        return True

    if not checkers_on_board(board, black_side.player.side):
        white_side.player.is_won = True
        return True

    return False

def base_cases_of_ending_game(white_side : Side, black_side : Side) -> bool:
    if white_side.player.is_won:
        return True
    if black_side.player.is_won:
        return True
    if white_side.timer.time_is_up:
        return True
    if black_side.timer.time_is_up:
        return True

    return False

def checkers_on_board(board : Board, side : str) -> int:
    return str(board).count(side.lower())

def move_checker(board : Board, x : int, y : int, move : str):
    if move != "DR" and move != "DL" and move != "UR" and move != "UL":
        raise MoveExceptions.InvalidMoveValue(move)

    check_boundaries(board, x, y, move)

    default_move(board, x, y, move)

def can_capture_from(board: Board, x: int, y: int, move: str) -> bool:
    if not is_checker_ahead(board, x, y, move):
        return False

    nx, ny = get_destination(x, y, move, jump=True)
    if not (0 <= nx < board.cols and 0 <= ny < board.rows):
        return False
    return board.board[ny][nx] == '_'


def available_captures(board: Board, x: int, y: int) -> list[str]:
    moves = []

    if can_capture_from(board, x, y, "DR"):
        moves.append("DR")
    if can_capture_from(board, x, y, "DR"):
        moves.append("DL")
    if can_capture_from(board, x, y, "DR"):
        moves.append("UR")
    if can_capture_from(board, x, y, "DR"):
        moves.append("UL")

    return moves


def get_destination(x : int, y : int, move : str):
    if move == "DR":
        return x + 2, y + 2
    elif move == "DL":
        return x - 2, y + 2
    elif move == "UR":
        return x + 2, y - 2
    elif move == "UL":
        return x - 2, y - 2

    return 0, 0


def do_capture(board: Board, x: int, y: int, move: str):
    if move != "DR" and move != "DL" and move != "UR" and move != "UL":
        raise MoveExceptions.InvalidMoveValue(move)

    nx, ny = get_destination(x, y, move)
    if nx < 0 or nx >= board.cols or ny < 0 or ny >= board.rows:
        raise MoveExceptions.OutOfBoundaries(move)

    mx, my = get_destination(x, y, move)
    board.board[my][mx] = '_'

    board.board[ny][nx] = board.board[y][x]
    board.board[y][x] = '_'

def is_checker_ahead(board : Board, x : int, y : int, move : str) -> bool:
    if move == "DR":
        if board.board[y + 1][x + 1] != '_':
            return True
    elif move == "DL":
        if board.board[y + 1][x - 1] != '_':
            return True
    elif move == "UR":
        if board.board[y - 1][x + 1] != '_':
            return True
    elif move == "UL":
        if board.board[y - 1][x - 1] != '_':
            return True
    return False

def default_move(board : Board, x : int, y : int, move : str):
    if move == "DR":
        board.board[y + 1][x + 1] = board.board[y][x]
        board.board[y][x] = '_'
    elif move == "DL":
        board.board[y + 1][x - 1] = board.board[y][x]
        board.board[y][x] = '_'
    elif move == "UR":
        board.board[y - 1][x + 1] = board.board[y][x]
        board.board[y][x] = '_'
    elif move == "UL":
        board.board[y - 1][x - 1] = board.board[y][x]
        board.board[y][x] = '_'

def check_boundaries(board : Board, x : int, y : int, move : str) -> None:
    match move:
        case "DR":
            if x + 1 >= board.cols or y + 1 >= board.rows:
                raise MoveExceptions.OutOfBoundaries(move)
        case "DL":
            if x - 1 < 0 or y + 1 >= board.rows:
                raise MoveExceptions.OutOfBoundaries(move)
        case "UR":
            if x + 1 >= board.cols or y - 1 < 0:
                raise MoveExceptions.OutOfBoundaries(move)
        case "UL":
            if x - 1 < 0 or y - 1 < 0:
                raise MoveExceptions.OutOfBoundaries(move)


if __name__ == '__main__':
    white_player = Side(1800, 'Artur', 'w')
    black_player = Side(1200, 'Dmitry', 'b')
    board = initialize_board()
    board.create_board(10, 8)
    board.place_checkers(4, 4)
    print(board)

    main_loop()
