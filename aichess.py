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
    iterations: int

    def __str__(self) -> str:
        return self.player1_name + " win percent:" + str(self.percent_wins_player1) + '\n' + \
            self.player2_name + " win percent:" + str(self.percent_wins_player2) + '\n' + \
            "draws percent:" + str(self.percent_draws) + '\n' +\
            "number iterations:" + str(self.iterations) + '\n'

class AIChess:
    def __init__(self, iterations: int, baseline: ChessPlayer, testplayers: array, visual: bool=False, verbose: bool=False) -> None:
        self.__iterations: int = iterations
        self.__visual: bool = visual
        self.__verbose: bool = verbose
        self.__results: array = []
        self.__baseline: ChessPlayer = baseline
        self.__testplayers: array[ChessPlayer] = testplayers

    def run(self) -> array:
        for player in self.__testplayers:
            self.__run_one_set_of_opponents(player1=player, player2=self.__baseline)
        return self.__results

    def __run_one_set_of_opponents(self, player1: ChessPlayer, player2: ChessPlayer) -> None:
        player1_wins = 0
        draws = 0
        for i in tqdm(range(self.__iterations)):
            game = Game(
                white=player1,
                black=player2,
                visual=self.__visual,
                verbose=self.__verbose
            )

            winner = game.run()
            if winner is None:
                draws += 1

            # If winner is True, white won (player1)
            elif winner:
                player1_wins += 1

        percent_wins_player1 = player1_wins / self.__iterations
        percent_draws = draws / self.__iterations
        percent_wins_player2 = 1 - (percent_wins_player1 + percent_draws)
        self.__results.append(
            Results(
                player1.get_name(),
                player2.get_name(),
                percent_wins_player1,
                percent_wins_player2,
                percent_draws,
                self.__iterations
            )
        )

    def get_results(self) -> Results:
        return self.__results

      # How to use:
        # baseline = RandomChessPlayer()
        # testplayers = [
        #     RandomChessPlayer(),
        #     minimaxPlayer(depth=1),
        #     minimaxPlayer(depth=2)
        # ]
        # aichess = AIChess(
        #     iterations=100, 
        #     baseline=baseline,
        #     testplayers=testplayers
        # )
        # aichess.run()
        # results = aichess.get_results()
        # for result in results:
        #     print(result)
