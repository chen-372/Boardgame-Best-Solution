from jinja2 import Template
import bg_simulation as bg
import csv

content = str()
dices = list()


def board_convert(board: list[list[int]]) -> str:
    html_board = bg.display(board)
    html_board = html_board.replace("\n", "</br>", 10)
    html_board = html_board.replace(" ", "&nbsp;", html_board.count(" "))
    # print(html_board)
    return html_board


with open("templates/template.html") as f:
    _template = Template(f.read())

with open("data/data2.csv") as f:
    reader = csv.DictReader(f, delimiter=";")

    for line in reader:
        dices.append(line["dice"])
        temp_board = line["board"][2:-2].split("], [")

        board = list()
        for y in range(5):
            row = temp_board[y].split(", ")
            for x in range(5):
                row[x] = int(row[x])
            board.append(row)

        content += _template.render(
            board=board_convert(board),
            dice=line["dice"],
            img=f"<img src = 'E:/a_study/DP/Computer_Science/Python_files/simulation/board_game/graph/est_place{len(dices)}.jpg' alt = '' width='1000' height='250'>",
        )

with open("templates/head.html") as f:
    _head = Template(f.read())

with open("data/data1.csv") as f:
    reader = csv.DictReader(f)

    for line in reader:
        print(line["mean"])
        print(line["standard_deviation"])
        content = (
            (
                _head.render(
                    original_board=board_convert(
                        [[0 for _ in range(5)] for _ in range(5)]
                    ),
                    dices=dices,
                    eva_img="<img src = 'E:/a_study/DP/Computer_Science/Python_files/simulation/board_game/graph/evaluation.jpg' alt = ' ' width='750' height='750'>",
                    mean=f"Mean: {str(line['mean'])}",
                    standard_deviation=f"Standar Diveation: {str(line['standard_deviation'])}",
                )
            )
            + "\n"
            + content
        )
print(content)
with open("templates/tail.html") as f:
    content += f.read()


f = open("evaluation.html", "w")
f.write(content)
f.close()
