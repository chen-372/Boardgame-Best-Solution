import bg_simulation as bg

dices = [1, 1, 5, 3, 3, 6, 4, 3, 4, 5, 4, 1, 3, 6, 6, 2, 3, 2, 1, 1, 3, 4, 3, 1, 5]
board = [[0 for _ in range(5)] for _ in range(5)]
simulate_times = 100
evaluate_times = 200

f = f = open("data/data1.csv")
content = f.read()
if not content:
    content = "trail,score"
f.close()

f = open("data/data1.csv", "w+")

print(content)

for i in range(evaluate_times):
    score = bg.simulation(board, simulate_times, dices)
    content += f"\n{content.count(',')},{score}"
    print(i)


print(content)
f.write(content)

f.close()
