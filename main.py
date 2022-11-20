from aichess import AIChess
import numpy as np
import matplotlib.pyplot as plt

# Testing
title = 'Random Agent VS Random Agent - 500 iterations per run'
num_iterations = 500
depth_iterations = [1,2,3,4,5]
wins, losses, draws = np.empty(len(depth_iterations)), np.empty(len(depth_iterations)), np.empty(len(depth_iterations))
for i, depth_test in enumerate(depth_iterations):
    temp_wins, temp_losses, temp_draws = AIChess(iterations=num_iterations, visual=False, verbose=True, depth = depth_test).run()
    wins[i] = np.round(temp_wins, 2) * 100
    losses[i] = np.round(temp_losses, 2) * 100
    draws[i] = np.round(temp_draws, 2) * 100

# Graphs
labels = depth_iterations
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
ax.set_xlabel('Depth (Number of Moves Look Ahead)')
ax.set_xlabel('Run #')
ax.set_title(title)
ax.set_xticks(x, labels)
ax.legend()

ax.bar_label(rects1, padding=3)
ax.bar_label(rects2, padding=3)
ax.bar_label(rects3, padding=3)
fig.tight_layout()
plt.savefig('charts/' + title)
plt.show()