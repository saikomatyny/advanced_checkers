from db import connect_database

from board import *
from game_logic import *

import asyncio

from websockets.asyncio.server import serve
import websockets.exceptions

connected = {}
players = {}
setup_event = asyncio.Event()

async def send_message_to_player(player, message):
    if player in connected:
        await connected[player].send(message)

async def game_setup():
    player_names = list(connected.keys())
    ws1 = connected[player_names[0]]
    ws2 = connected[player_names[1]]

    # name
    await ws1.send("Enter your name:")
    player1 = await ws1.recv()

    await ws2.send("Enter your name:")
    while True:
        player2 = await ws2.recv()
        if player2 != player1:
            break
        await ws2.send(f"Name '{player2}' already taken. Enter a different name:")

    connected[player1] = ws1
    connected[player2] = ws2
    del connected[player_names[0]]
    del connected[player_names[1]]

    # side
    await ws1.send(f"{player1}, enter a single letter to represent your side (e.g. 'x'):")
    while True:
        side1 = await ws1.recv()
        side1 = side1.strip().lower()
        if len(side1) == 1 and side1.isalpha():
            break
        await ws1.send("Invalid input. Please enter a single letter (a–z).")

    await ws2.send(f"{player1} chose side '{side1}'. {player2}, enter a different letter to represent your side:")
    while True:
        side2 = await ws2.recv()
        side2 = side2.strip().lower()
        if len(side2) == 1 and side2.isalpha() and side2 != side1:
            break
        await ws2.send(f"Invalid or duplicate input. Please enter a different letter than '{side1}'.")

    await ws1.send(f"{player2} chose side '{side2}'.")

    # time
    await ws1.send(f"{player1}, enter your time (in minutes):")
    time1 = int(await ws1.recv())

    await ws2.send(f"{player2}, enter your time (in minutes):")
    time2 = int(await ws2.recv())

    players[side1] = Side(time1, player1, side1)
    players[side2] = Side(time2, player2, side2)

    board = initialize_board()

    rows = int(input("Enter number of rows: "))
    cols = int(input("Enter number of columns: "))
    board.create_board(rows, cols)

    count1 = int(input(f"Enter rows of checkers for {player1} (max {rows // 2 - 1}): "))
    count2 = int(input(f"Enter rows of checkers for {player2} (max {rows // 2 - 1}): "))
    board.place_checkers(count1, count2)

    return board, side1, side2


async def handler(websocket):

    while len(connected) < 2:
        await asyncio.sleep(1)

    for player in connected:
        await send_message_to_player(player, "Both players connected. Starting game...")

    if websocket == connected[0]:
        board, s1, s2 = await game_setup()

        await send_message_to_player(s1, f"Game started. You are {players[s1].name}.")
        await send_message_to_player(s2, f"Game started. You are {players[s2].name}.")

        while not is_game_ended(board, players[s1], players[s2]):
            await send_message_to_player(s1, str(board))
            await send_message_to_player(s2, str(board))
            await asyncio.sleep(1)

async def main():
    async with serve(handler, "", 8001) as server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
