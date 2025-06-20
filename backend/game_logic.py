from board import Board, Side
from exceptions import MoveExceptions

def initialize_board() -> Board:
    board = Board()

    return board

def is_game_ended(board : Board, white_side : Side, black_side : Side) -> bool:

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
    return board.board.count(side.lower()) or board.board.count(side.upper())

def move_checker(board : Board, x : int, y : int, move : str):
    if move != "DR" or move != "DL" or move != "UR" or move != "UL":
        raise MoveExceptions.InvalidMoveValue(move)

    check_boundaries(board, x, y, move)



def check_boundaries(board : Board, x : int, y : int, move : str) -> None:
    match move:
        case "DR":
            if x + 1 >= board.cols or y + 1 >= board.rows:
                raise MoveExceptions.InvalidMove(move)
        case "DL":
            if x - 1 < 0 or y + 1 >= board.rows:
                raise MoveExceptions.InvalidMove(move)
        case "UR":
            if x + 1 >= board.cols or y - 1 < 0:
                raise MoveExceptions.InvalidMove(move)
        case "UL":
            if x - 1 < 0 or y - 1 < 0:
                raise MoveExceptions.InvalidMove(move)

if __name__ == '__main__':
    white_player = Side(1800, 'Artur', 'w')
    black_player = Side(1200, 'Dmitry', 'b')
    board = initialize_board()
    board.create_board(10, 8)
    board.place_checkers(4, 4)
    print(board)
