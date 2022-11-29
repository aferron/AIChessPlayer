from aichess import AIChess
from randomchessplayer import RandomChessPlayer
import numpy as np
import matplotlib.pyplot as plt
from minimaxchessplayer import MinimaxPlayer
from heuristics import Heuristic

# Testing
num_iterations = 1
depth_iterations = [1, 2, 3]
wins, losses, draws = [], [], []
baselines =  [MinimaxPlayer(depth=depth, heuristics=[Heuristic.Distance_From_Starting_Location, Heuristic.Maximize_Number_Of_Pieces], run_alpha_beta=True) for depth in depth_iterations]
testplayers = [MinimaxPlayer(depth=depth, heuristics=[Heuristic.Piece_Could_Be_Captured, Heuristic.Distance_From_Starting_Location, Heuristic.Keep_Pawns_Diagonally_Supported, Heuristic.Stacked_Pawns, Heuristic.Maximize_Number_Of_Pieces], run_alpha_beta=True) for depth in depth_iterations]
test_results = AIChess(iterations=num_iterations, baselines=baselines, testplayers=testplayers).run()
for i, depth_tests in enumerate(test_results):
    wins.append([]), losses.append([]), draws.append([])
    for depth_test in depth_tests:
        temp_wins, temp_losses, temp_draws = depth_test.percent_wins_player1, depth_test.percent_wins_player2, depth_test.percent_draws
        wins[i].append( np.round(temp_wins, 2) * 100)
        losses[i].append( np.round(temp_losses, 2) * 100)
        draws[i].append( np.round(temp_draws, 2) * 100)

# Graphs
for (win, loss, draw, baseline) in zip(wins, losses, draws, baselines):
    title = 'Baseline -' + baseline.get_name()+ '.png'
    by_depth = False
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
    rects1 = ax.bar(r1, win, width, label='Wins')
    rects2 = ax.bar(r2, loss, width, label='Losses')
    rects3 = ax.bar(r3, draw, width, label='Draws')

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
#    plt.savefig('charts/' + title)
    plt.show()