from array import *
from chessplayer import ChessPlayer
from dataclasses import dataclass
from game import Game
from tqdm import tqdm


@dataclass
class Results:
    player1_name: str
    player2_name: str
    percent_wins_player1: float
    percent_wins_player2: float
    percent_draws: float
    average_decision_time_player1: float
    average_decision_time_player2: float
    average_moves_per_game: float
    iterations: int

    def __str__(self) -> str:
        return self.player1_name + " win percent:" + str(self.percent_wins_player1) + '\n' + \
            self.player2_name + " win percent:" + str(self.percent_wins_player2) + '\n' + \
            "draws percent:" + str(self.percent_draws) + '\n' +\
            "number iterations:" + str(self.iterations) + '\n'

class AIChess:
    def __init__(self, iterations: int, baselines: ChessPlayer, testplayers: array, visual: bool=False, verbose: bool=False) -> None:
        self.__iterations: int = iterations
        self.__visual: bool = visual
        self.__verbose: bool = verbose
        self.__results: array[array[Results]] = []
        self.__baselines: array[ChessPlayer] = baselines
        self.__testplayers: array[ChessPlayer] = testplayers

    def run(self) -> array:
        counter: int = 0
        for baseline in self.__baselines:
            for player in self.__testplayers:
                self.__run_one_set_of_opponents(player1=player, player2=baseline, current_index=counter)
            counter += 1
        return self.__results

    def __run_one_set_of_opponents(self, player1: ChessPlayer, player2: ChessPlayer, current_index: int) -> None:
        player1_wins = 0
        draws = 0
        total_moves = 0
        player1_starts = True

        for i in tqdm(range(self.__iterations)):
            
            game = Game(
                white=player1 if player1_starts else player2,
                black=player2 if player1_starts else player1,
                visual=self.__visual,
                verbose=self.__verbose
            )

            winner = game.run()
            if winner is None:
                draws += 1

            # If winner is True and player1_starts is True, player1 won
            # If winner is False and player1_starts is False, player1 won
            elif winner == player1_starts:
                player1_wins += 1

            total_moves += game.player_white.total_moves + game.player_black.total_moves

            player1_starts != player1_starts
        
        percent_wins_player1 = player1_wins / self.__iterations
        percent_draws = draws / self.__iterations
        percent_wins_player2 = 1 - (percent_wins_player1 + percent_draws)
        if(len(self.__results) != current_index + 1):
            self.__results.append([])
        self.__results[current_index].append(
            Results(
                player1.get_name(),
                player2.get_name(),
                percent_wins_player1,
                percent_wins_player2,
                percent_draws,
                player1.average_time_to_get_move,
                player2.average_time_to_get_move,
                total_moves / self.__iterations,
                self.__iterations
            )
        )

    def get_results(self) -> Results:
        return self.__results
