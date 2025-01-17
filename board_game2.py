import random as r
import copy
from typing import Callable
import PySimpleGUI as pg


player_board = [[0 for _ in range(5)] for _ in range(5)]

computer_board = [[0 for _ in range(5)] for _ in range(5)]

simulate_times = 100
throws = 0
throw_die = False
die = r.randint(1, 6)


rules = {
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
            if rules[test_name] > line_score:
                line_score = rules[test_name]
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


def computer_simulate(
    board: list[list[int]], x: int, y: int, die: int, throws: int
) -> float:
    """simulate many times for "die" in ("x", "y") block under the given "board"

    return the average possible score"""

    total_score = 0
    for _ in range(simulate_times * throws + 500):
        sim_throw = throws
        sim_x = 0
        sim_y = 0
        sim_board = copy.deepcopy(board)
        sim_board[y][x] = die

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

    return total_score / simulate_times


player_layout = [
    [pg.Button(button_text="    ", key=f"-BUTTON{x}{y}-") for x in range(5)]
    for y in range(5)
]

data_layout = [
    [pg.Text(text=f"Die Number: {die}", key="-DIE-")],
    [
        pg.Text(text="Player Score", visible=False, key="-PLAYERSCORE-"),
    ],
    [
        pg.Text(text="Computer Score", visible=False, key="-COMSCORE-"),
    ],
]

computer_layout = [
    [pg.Button(button_text="    ", key=f"-COMBUTTON{x}{y}-") for x in range(5)]
    for y in range(5)
]

main = pg.Window(
    title="board game",
    layout=[
        [
            pg.Frame(title="Player Board", layout=player_layout),
            pg.Frame(title="Data", layout=data_layout),
            pg.Frame(title="Computer Board", layout=computer_layout),
        ]
    ],
)


while True:

    main_event, main_value = main.read()

    if main_event == pg.WIN_CLOSED:
        break

    if main_event[:7] == "-BUTTON":

        x = int(main_event[7])
        y = int(main_event[8])

        new_board = place(x, y, die, player_board)
        if player_board == new_board:
            print("Error, input again...")
        else:
            # print(f"{die} is placed in {x}{y}")
            player_board = new_board
            throw_die = True
            throws += 1
            main[f"-BUTTON{x}{y}-"].update(f" {player_board[y][x]} ")
            best_coord = [0, 0]
            best_score = 0

            x = 0
            y = 0

            # try every block that can fit a new number
            for _ in range(25):
                if computer_board[y][x] == 0:
                    sim_score = computer_simulate(computer_board, x, y, die, throws)
                    if sim_score > best_score:
                        best_score = sim_score
                        best_coord = [x, y]
                if x == 4:
                    y += 1
                    x = 0
                else:
                    x += 1
            x = best_coord[0]
            y = best_coord[1]
            computer_board = place(x, y, die, computer_board)
            main[f"-COMBUTTON{x}{y}-"].update(f" {computer_board[y][x]} ")

    if throws == 25:
        throws = 0
        score = board_score(player_board)
        player_score = score[0]
        player_stat = score[1]

        score = board_score(computer_board)
        computer_score = score[0]
        computer_stat = score[1]

        main["-PLAYERSCORE-"].update(
            f"Player Score: {player_score}\n{player_stat}", visible=True
        )

        main["-COMSCORE-"].update(
            f"Computer Score: {computer_score}\n{computer_stat}", visible=True
        )

    if throw_die:
        throw_die = False
        die = r.randint(1, 6)
        main["-DIE-"].update(f"Die Number: {die}")


main.close()
