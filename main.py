from aichess import AIChess, Results
from chessplayer import ChessPlayer
from dataclasses import dataclass
from enum import Enum
from heuristics import Heuristic
import matplotlib.pyplot as plt
import numpy as np
from minimaxchessplayer import MinimaxPlayer
from randomchessplayer import RandomChessPlayer
import time
from typing import Any, List

@dataclass
class ResultsPerMatchup:
    results_per_matchup: List[Any]
    label: str

class Main:
    def run(self) -> None:
        # self.__run_minimax_with_heuristics_vs_random()
        # self.__run_heuristics_ablation_study()
        self.__compare_runtimes_of_basic_configs()

    def __run_and_plot_one_experiment(self, iterations: int, baselines: List[ChessPlayer], testplayers: List[ChessPlayer]) -> None:
        test_results: List[List[Results]] = AIChess(iterations=iterations, baselines=baselines, testplayers=testplayers).run()
        print("test_results: ", test_results)
        for i, results_per_baseline in enumerate(test_results):
            baseline = baselines[i]
            print ("results_per_baseline:", results_per_baseline)
            test_player_wins, baseline_wins, draws, process_time_player1, process_time_player2, moves_per_game = [], [], [], [], [], []
            for results in results_per_baseline:
                print("results: ", results)
                self.__append_as_percent(results_by_type=test_player_wins, percent=results.percent_wins_player1)
                self.__append_as_percent(results_by_type=baseline_wins, percent=results.percent_wins_player2)
                self.__append_as_percent(results_by_type=draws, percent=results.percent_draws)
                process_time_player1.append(results.average_decision_time_player1)
                process_time_player2.append(results.average_decision_time_player2)

            win_results = [
                ResultsPerMatchup(test_player_wins, "Test Player Wins"),
                ResultsPerMatchup(baseline_wins, "Baseline Wins"),
                ResultsPerMatchup(draws, "Draws")
            ]
            time_results = [
                ResultsPerMatchup(process_time_player1, "Test Player"),
                ResultsPerMatchup(process_time_player2, "Baseline Player")
            ]
            self.__plot_results(
                baseline=baseline,
                testplayers=testplayers,
                iterations=iterations, 
                matchupresults=win_results,
                ylabel='Percent Wins or Draws'
            )
            self.__plot_results(
                baseline=baseline,
                testplayers=testplayers,
                iterations=iterations, 
                matchupresults=time_results,
                ylabel='Average Processing Time Per Move in Seconds'
            )

    def __append_as_percent(self, results_by_type: np.array(float), percent: float) -> None:
        results_by_type.append(np.round(percent, 2) * 100)

    def __plot_results(
        self,
        baseline: ChessPlayer,
        testplayers: List[ChessPlayer],
        iterations: int,
        matchupresults: List[ResultsPerMatchup],
        ylabel: str
    ) -> None:
        title = 'Baseline: ' + baseline.get_name() + '\n' + str(iterations) + \
            ' iterations per run'
        labels = [player.get_name() for player in testplayers]
        x = np.arange(len(labels))
        width = .15

        r1 = np.arange(len(labels))
        r2 = [x + width for x in r1]
        r3 = [x + width for x in r2]
        x_locations = [r1, r2, r3]

        fig, ax = plt.subplots(figsize=((len(labels)*1.85),6))
        rects = [ax.bar(
            x_locations[i], 
            matchupresults[i].results_per_matchup, 
            width, 
            label=matchupresults[i].label
        ) for i in range(len(matchupresults))]

        ax.set_ylabel(ylabel)
        ax.set_xlabel('Player Type')
        ax.set_title(title)
        ax.set_xticks(x, labels)
        ax.legend(bbox_to_anchor=(.2,1.2,0,0))

        for rect in rects:
            ax.bar_label(rect, padding=3)

        fig.tight_layout()
        plt.savefig('charts/' + title)
        plt.show()

    def __run_heuristics_by_depth_experiments(self) -> None:
        num_iterations = 50
        depth_iterations = [1, 2, 3, 4, 5]
        baselines =  [MinimaxPlayer(
            time=time,
            depth=depth, 
            heuristics=[Heuristic.Distance_From_Starting_Location, Heuristic.Maximize_Number_Of_Pieces],
            run_alpha_beta=True) \
                for depth in depth_iterations]
        testplayers = [
            MinimaxPlayer(
                time=time,
                depth=depth, 
                heuristics=[
                    Heuristic.Piece_Could_Be_Captured,
                    Heuristic.Distance_From_Starting_Location,
                    Heuristic.Keep_Pawns_Diagonally_Supported,
                    Heuristic.Stacked_Pawns,
                    Heuristic.Maximize_Number_Of_Pieces
                ],
                run_alpha_beta=True
            ) for depth in depth_iterations]
        self.__run_and_plot_one_experiment(iterations=num_iterations, baselines=baselines, testplayers=testplayers)

    def __run_heuristics_ablation_study(self) -> None:
        num_iterations = 100
        depth = 4
        all_heuristics = list(Heuristic)
        baselines =  [MinimaxPlayer(
            time=time,
            depth=depth, 
            heuristics=[],
            run_alpha_beta=True
        ), MinimaxPlayer(
            time=time, 
            depth=depth, 
            heuristics=all_heuristics, 
            run_alpha_beta=True
        )]
        testplayers = [MinimaxPlayer(
            time=time, 
            depth=depth, 
            heuristics=[heuristic],
            run_alpha_beta=True
        ) for heuristic in all_heuristics] + \
            [MinimaxPlayer(
                time=time, 
                depth=depth, 
                heuristics=[heuristic for heuristic in all_heuristics if all_heuristics.index(heuristic) != index],
                run_alpha_beta=True
            ) for index in range(len(all_heuristics))]
        self.__run_and_plot_one_experiment(iterations=num_iterations, baselines=baselines, testplayers=testplayers)

    def __run_minimax_with_heuristics_vs_random(self) -> None:
        num_iterations = 100
        baselines = [RandomChessPlayer(time=time)]
        testplayers = [MinimaxPlayer(
            time=time, 
            depth=depth, 
            heuristics=list(Heuristic), 
            run_alpha_beta=True
        ) for depth in range(3)]
        self.__run_and_plot_one_experiment(iterations=num_iterations, baselines=baselines, testplayers=testplayers)

    def __compare_runtimes_of_basic_configs(self) -> None:
        depth = 3
        baselines = [RandomChessPlayer(time=time)]
        testplayers = [
            RandomChessPlayer(time=time),
            MinimaxPlayer(
                time=time,
                depth=depth,
                heuristics=[],
                run_alpha_beta=False
            ),
            MinimaxPlayer(
                time=time,
                depth=depth,
                heuristics=list(Heuristic),
                run_alpha_beta=False
            ),
            MinimaxPlayer(
                time=time,
                depth=depth,
                heuristics=list(Heuristic),
                run_alpha_beta=True
            )
        ]
        self.__run_and_plot_one_experiment(iterations=100, baselines=baselines, testplayers=testplayers)

Main().run()

