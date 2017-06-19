"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest

import isolation
import timeit
import game_agent as ga
import sample_players as sp
#from importlib import reload


class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""
    """
    def setUp(self):
        #reload(game_agent)
        self.player1 = "Player1"
        self.player2 = "Player2"
        self.game = isolation.Board(self.player1, self.player2)
    """
    def testSecondPlayerShouldWinIn2x3(self):
        player1 = ga.MinimaxPlayer(search_depth=1, score_fn=sp.open_move_score)
        player2 = ga.MinimaxPlayer(search_depth=1, score_fn=sp.open_move_score)
        game = isolation.Board(player1, player2, 2, 3)
        winner, moves, _ = game.play(100)
        self.assertEqual(winner, player2, "player2 should have won the match")
        self.assertEqual(len(moves), 2, "there should have been two moves, due to the clear win")
        self.assertEqual(moves[0], [2, 1],
                         "player1 should have picked the top left corner since \
                         it's the first node in the tree")
        self.assertEqual(moves[1], [0, 0],
                         "player2 should have picked the opposite corner since \
                         it's the first node that has a direct win")

    def testAlphaBeta(self):
        player1 = ga.AlphaBetaPlayer(search_depth=2, score_fn=sp.open_move_score)
        player2 = ga.AlphaBetaPlayer(search_depth=2, score_fn=sp.open_move_score)
        game = isolation.Board(player1, player2, 9, 9)
        game._board_state = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 42, 14]
        print(game.to_string())
        time_millis = lambda: 1000 * timeit.default_timer()
        move_start = time_millis()
        time_left = lambda: 1000 - (time_millis() - move_start)
        player1.time_left = time_left
        m = player1.alphabeta(game, 2)
        self.assertEqual(m, (6, 3))

    def testAlphaBeta2(self):
        player1 = ga.AlphaBetaPlayer(search_depth=2, score_fn=sp.open_move_score)
        player2 = sp.RandomPlayer()
        game = isolation.Board(player1, player2, 3, 3)
        game.play(150)

if __name__ == '__main__':
    unittest.main()
