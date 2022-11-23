from aichess import AIChess
from randomchessplayer import RandomChessPlayer
import numpy as np
import matplotlib.pyplot as plt
from minimaxchessplayer import minimaxPlayer

# Testing
title = 'Random Agent VS Minimax Agent - 500 iterations per run'
num_iterations = 50
depth_iterations = [1,2]
wins, losses, draws = np.empty(len(depth_iterations)), np.empty(len(depth_iterations)), np.empty(len(depth_iterations))
baseline = RandomChessPlayer()
testplayers = [minimaxPlayer(depth=depth) for depth in depth_iterations]
aichess = AIChess(iterations=num_iterations, baseline=baseline, testplayers=testplayers)
test_results = aichess.run()
for i, depth_test in enumerate(test_results):
    temp_wins, temp_losses, temp_draws = depth_test.percent_wins_player1, depth_test.percent_wins_player2, depth_test.percent_draws
    wins[i] = np.round(temp_wins, 2) * 100
    losses[i] = np.round(temp_losses, 2) * 100
    draws[i] = np.round(temp_draws, 2) * 100


# Graphs
by_depth = True
if by_depth:
    labels = depth_iterations
else:
    labels = [player.get_name() for player in testplayers]
x = np.arange(len(labels))
width = .15

r1 = np.arange(len(labels))
r2 = [x + width for x in r1]
r3 = [x + width for x in r2]

fig, ax = plt.subplots()
rects1 = ax.bar(r1, wins, width, label='Wins')
rects2 = ax.bar(r2, losses, width, label='Losses')
rects3 = ax.bar(r3, draws, width, label='Draws')

ax.set_ylabel('Percent Wins')
if by_depth:
    ax.set_xlabel('Depth (Number of Moves Look Ahead)')
    ax.set_xlabel('Run #')
else:
    ax.set_xlabel('Player Type')
ax.set_title(title)
ax.set_xticks(x, labels)
ax.legend()

ax.bar_label(rects1, padding=3)
ax.bar_label(rects2, padding=3)
ax.bar_label(rects3, padding=3)
fig.tight_layout()
plt.savefig('charts/' + title)
plt.show()