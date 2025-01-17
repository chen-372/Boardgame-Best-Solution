import random as r
import copy
from typing import Callable
import matplotlib.pyplot as plt
import os

rule = {
    "s_five": 80,
    "s_four": 40,
    "s_three": 15,
    "s_two": 5,
    "s_sequence": 50,
    "s_three_two": 30,
    "s_two_two": 10,
}


def place(x: str, y: str, value: int, board: list[list[int]]) -> list[list[int]]:
    """place "value" at "x", "y" corrdinate in the "board"

    retrun the new board"""

    new_board = copy.deepcopy(board)

    if new_board[y][x] == 0:
        new_board[y][x] = value

    return new_board


def s_five(line: list[int]) -> bool:
    """retrun weather the given "line" contain a FIVE"""
    return len(set(line)) == 1


def s_four(line: list[int]) -> bool:
    """retrun weather the given "line" contain a FOUR"""
    set_line = set(line)
    element = list(set_line)
    return len(set_line) == 2 and (
        line.count(element[0]) == 4 or line.count(element[1]) == 4
    )


def s_three(line: list[int]) -> bool:
    """retrun weather the given "line" contain a THREE"""
    set_line = set(line)
    element = list(set_line)
    return len(set_line) == 3 and (
        line.count(element[0]) == 3
        or line.count(element[1]) == 3
        or line.count(element[2]) == 3
    )


def s_two(line: list[int]) -> bool:
    """retrun weather the given "line" contain a TWO"""
    return len(set(line)) == 4


def s_sequence(line: list[int]) -> bool:
    """retrun weather the given "line" contain a SEQUENCE"""
    set_line = set(line)
    return len(set_line) == 5 and (1 not in set_line or 6 not in set_line)


def s_three_two(line: list[int]) -> bool:
    """retrun weather the given "line" contain a THREE PLUS TWO"""
    set_line = set(line)
    element = list(set_line)
    return len(set_line) == 2 and (
        line.count(element[0]) == 3 or line.count(element[1] == 3)
    )


def s_two_two(line: list[int]) -> bool:
    """retrun weather the given "line" contain a TWO PLUS TWO"""
    set_line = set(line)
    element = list(set_line)
    return len(set_line) == 3 and (
        line.count(element[0]) == 2 or line.count(element[1])
    )


def check_score(line: list[int], score: Callable) -> bool:
    """retrun weather the given "line" contain the given "score"""
    return score(line)


def line_score(line: list[int]) -> list:
    """retrun the score of the given "line" and the name of that score"""

    line_score = 0
    score_name = ""
    for test in [s_five, s_four, s_three, s_two, s_sequence, s_three_two, s_two_two]:
        if check_score(line, test):
            test_name = str(test)[10:]
            test_name = test_name[: (test_name.index(" "))]
            if rule[test_name] > line_score:
                line_score = rule[test_name]
                score_name = test_name

    return [line_score, score_name]


def board_score(board: list[list[int]]) -> list:
    """retrun the total score of the given "board" and it's statistic"""

    board_score = 0
    board_stat = {
        "s_five": 0,
        "s_four": 0,
        "s_three": 0,
        "s_two": 0,
        "s_sequence": 0,
        "s_three_two": 0,
        "s_two_two": 0,
        "": 0,
    }

    for index in range(5):
        tools = line_score(board[index])
        board_score += tools[0]
        board_stat[tools[1]] += 1

        tools = line_score([board[i][index] for i in range(5)])
        board_score += tools[0]
        board_stat[tools[1]] += 1

    return [board_score, board_stat]


def files_number(path: str) -> int:
    """retrun a correct graph files name according to the numbers of graphs in the folder"""
    return int(os.popen(f'cd {path} & dir /b /a-d | find /v /c ""').read()) + 1


def score_estimate(
    board: list[list[int]],
    x: int,
    y: int,
    dice: int,
    throws: int,
    simulate_times,
    graph: bool = False,
) -> float:
    """simulate many times for "dice" in ("x", "y") block under the given "board"\\
    draw a line graph is "graph" activated\\
    return the average possible score"""

    total_score = 0
    xs = list[int]()
    ys = list[float]()

    for i in range(simulate_times):
        sim_throw = throws
        sim_x = 0
        sim_y = 0
        sim_board = copy.deepcopy(board)
        sim_board[y][x] = dice

        while True:
            if sim_throw == 25:
                break
            if sim_board[sim_y][sim_x] == 0:
                sim_board[sim_y][sim_x] = r.randint(1, 6)
                sim_throw += 1

            if sim_x == 4:
                sim_y += 1
                sim_x = 0
            else:
                sim_x += 1

        total_score += board_score(sim_board)[0]

        if graph:
            xs.append(i + 1)
            ys.append(total_score / (i + 1))

    if graph:
        fig, ax = plt.subplots(1, 1)

        fig.set_figwidth(10)
        fig.set_figheight(5)
        ax.plot(
            xs,
            ys,
            label="Simulated",
        )
        ax.set_title(
            f"Estimating dice {dice} on block ({x},{y}) for {simulate_times} simulations"
        )
        ax.set_xlabel("Simulations")
        ax.set_ylabel("Estimate")
        plt.savefig(f"graph/estimate{files_number('graph')}.jpg")
        plt.close()
    return total_score / simulate_times


def best_place(
    board: list[list[int]],
    dice: int,
    throws: int,
    simulate_times: int,
    graph: bool = False,
) -> list:
    """retrun the best place (x, y) to put "dice" on the "board"\\
    draw a bar graph is "graph" activated"""
    best_coord = [0, 0]
    best_score = 0

    xs = list[int]()
    ys = list[float]()

    x = 0
    y = 0
    # try every block that can fit a new number
    for i in range(25):
        if board[y][x] == 0:
            sim_score = score_estimate(board, x, y, dice, throws, simulate_times)
            if sim_score > best_score:
                best_score = sim_score
                best_coord = [x, y]

            if graph:
                xs.append(str([x, y]))
                ys.append(sim_score)

        # move to next block
        if x == 4:
            y += 1
            x = 0
        else:
            x += 1

    if graph:
        fig, ax = plt.subplots(1, 1)

        fig.set_figwidth(20)
        fig.set_figheight(5)
        ax.bar(
            xs,
            ys,
            label="Simulated",
        )
        ax.set_title(
            f"Estimating dice {dice} best place on board for {simulate_times} simulations"
        )
        ax.set_xlabel("Place")
        ax.set_ylabel("Estimate")
        plt.savefig(f"graph/est_place{throws}.jpg")
        plt.close()

    return best_coord


def display(board) -> str:
    """return the given "board" """

    output = ""
    output += "·---·---·---·---·---·\n"
    for y in board:
        output += "| "
        for x in y:
            output += str(x) if x != 0 else " "
            output += " | "
        output += "\n·---·---·---·---·---·\n"
    return output


def simulation(
    board: list[list[int]],
    simulate_times: int,
    dices: list[int],
    graph: bool = False,
    history_board: bool = False,
) -> tuple:
    """run the whole computer simulation\\
    return the score\\
    save bar graphs if "graph" is activied\\
    return board history if "history_board" is activied"""

    throws = 25 - len(dices)
    history = []
    while throws < 25:
        throws += 1

        best = best_place(board, dices[throws - 1], throws, simulate_times, graph)
        board = place(best[0], best[1], dices[throws - 1], board)

        history.append(board)
        # print(display(board))
        # print(f"number {dices[throws - 1]} placed in ({best[0]}, {best[1]})\n{'-'*50}")

    score = board_score(board)
    computer_score = score[0]
    # print(computer_score)

    # computer_stat = score[1]
    # print(computer_stat)

    return (computer_score, history) if history_board else computer_score


# board = [[0 for _ in range(5)] for _ in range(5)]
# dices = [1, 1, 5, 3, 3, 6, 4, 3, 4, 5, 4, 1, 3, 6, 6, 2, 3, 2, 1, 1, 3, 4, 3, 1, 5]
# simulation(board, 1000, dices)
