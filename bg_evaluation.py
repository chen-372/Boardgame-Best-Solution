from numpy import number
import bg_simulation as bg
import random as r
import matplotlib.pyplot as plt
import csv


# graph1
g1xs = list()
g1ys = list()

total_score = 0
number_score = 0

with open("data/data1.csv") as f:
    reader = csv.DictReader(f)

    for line in reader:
        g1xs.append(line["trail"])
        g1ys.append(line["score"])
        total_score += int(line["score"])
        number_score += 1

g1ys.sort()
fig, ax = plt.subplots(2, 1)

fig.set_figwidth(15)
fig.set_figheight(15)

ax[0].bar(g1xs, g1ys)
ax[0].set_title(
    f"Data Presentation: estimate scores in {number_score} of trails (sorted)"
)
ax[0].set_xlabel("Trails")
ax[0].set_ylabel("Estimate Score")


# graph2
g2xs = list(set(g1ys))
g2xs.sort()

g2ys = list()
for score in g2xs:
    g2ys.append(g1ys.count(score))
# g2xs[g2xs.index(value)] /= 5
# values[values.index(value)] = str(value)

content = "score,frequency"

f = open("data/data1-2.csv", "w")
for score in g2xs:
    content += f"\n{score},{g2ys[g2xs.index(score)]}"

f.write(content)


ax[1].bar(g2xs, g2ys)
ax[1].set_title(f"Data Presentation: the Frequency Against the Different Score")
ax[1].set_xlabel("Score")
ax[1].set_ylabel("Frequency")

plt.tight_layout()

plt.savefig("evaluation.jpg")
plt.close()

# calculation
if False:
    # calculate data
    score, history_board = bg.simulation(board, simulate_times, dices, True, True)

    # process data
    content = "board;dice"
    for i in range(len(dices)):
        content += f"\n{history_board[i]};{dices[i]}"

    f = open("data/data2.csv", "w")
    f.write(content)
    f.close()
