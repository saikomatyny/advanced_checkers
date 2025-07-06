from db import connect_database

from board import *
from game_logic import *

import asyncio

from websockets.asyncio.server import serve
import websockets.exceptions

connected = []
players = []

async def send_message_to_player(player, message):
    if player in connected:
        await player.send(message)

async def game_setup():
    ws1 = connected[0]
    ws2 = connected[1]

    # name
    await ws1.send("Enter your name:")
    player1 = await ws1.recv()

    await ws2.send("Enter your name:")
    while True:
        player2 = await ws2.recv()
        if player1 == player2:
            await ws2.send(f"Name '{player2}' already taken. Enter a different name:")
        else:
            break

    # side
    await ws1.send(f"{player1}, enter a single letter to represent your side (Ex. 'x'):")
    while True:
        side1 = await ws1.recv()
        side1 = side1.strip().lower()
        if len(side1) != 1 and not side1.isalpha():
            await ws1.send("Invalid input. Please enter a single letter (a–z).")
        else:
            break

    await ws2.send(f"{player1} chose side '{side1}'. {player2}, enter a different letter to represent your side:")
    while True:
        side2 = await ws2.recv()
        side2 = side2.strip().lower()
        if len(side2) != 1 and not side2.isalpha():
            await ws2.send("Invalid input. Please enter a single letter (a–z).")
        else:
            break

    await ws1.send(f"{player2} chose side '{side2}'.")

    # time
    await ws1.send(f"{player1}, enter your time (in minutes):")
    time1 = int(await ws1.recv())

    await ws2.send(f"{player2}, enter your time (in minutes):")
    time2 = int(await ws2.recv())

    players.append(Side(time1, player1, side1))
    players.append(Side(time2, player2, side2))

    board = initialize_board()

    # rows = int(input("Enter number of rows: "))
    # cols = int(input("Enter number of columns: "))
    rows = 10
    cols = 10
    board.create_board(rows, cols)

    # count1 = int(input(f"Enter rows of checkers for {player1} (max {rows // 2 - 1}): "))
    # count2 = int(input(f"Enter rows of checkers for {player2} (max {rows // 2 - 1}): "))
    count1 = 4
    count2 = 3
    board.place_checkers(count1, count2)

    return board, side1, side2

async def main_game_loop(board, user1, user2):
    while not game_is_over(board, players[0], players[1]):
        await user1.send(f"\n{str(board)}")
        await user2.send(f"\n{str(board)}")


async def handler(websocket):
    if websocket not in connected:
        connected.append(websocket)

    while len(connected) < 2:
        await websocket.send("Waiting for second player...")
        await asyncio.sleep(1)

    user1 = connected[0]
    user2 = connected[1]

    if websocket is connected[0]:
        for player in connected:
            await player.send("Both players connected. Starting game...")

        board, s1, s2 = await game_setup()

        await user1.send(f"Game started. You are {s1}.")
        await user2.send(f"Game started. You are {s2}.")

        await main_game_loop(board, user1, user2)

        await user1.close()
        await user2.close()
        connected.clear()
        players.clear()
    else:
        await asyncio.Future()


async def main():
    async with serve(handler, "", 8001) as server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())

# websockets ws://localhost:8001/
