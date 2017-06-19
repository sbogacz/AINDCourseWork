"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random
import math


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


class InvalidDepth(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    # prioritize own moves - opponent moves, and have a term for the
    # distance from the center
    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    w, h = game.width / 2., game.height / 2.
    y, x = game.get_player_location(player)
    dist = math.sqrt(float((h - y)**2 + (w - x)**2))
    return float(own_moves - opp_moves - dist)


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    # prioritize own moves - opponent moves, and have a term for the
    # distance from the center
    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    w, h = game.width / 2., game.height / 2.
    y, x = game.get_player_location(player)
    dist = math.sqrt(float((h - y)**2 + (w - x)**2))
    return float(own_moves**2 - opp_moves**2 - dist)


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    # stay near the opposite player while maximizing moves
    w, h = game.get_player_location(game.get_opponent(player))
    y, x = game.get_player_location(player)
    dist = math.sqrt(float((h - y)**2 + (w - x)**2))
    return dist + \
        float(len(game.get_legal_moves(player)))


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """
    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        best_move = (-1, -1)
        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if not game.get_legal_moves():
            return (-1, -1)

        # pick a random move in case we can't come up with an anser in time
        best_move = random.choice(game.get_legal_moves())
        # as per the algorithm, choose the action with the best value given
        # a minimizing opponent having the next turn
        try:
            _, move = self.max_value(game, depth)
            if move != (-1, -1):
                best_move = move
        except Exception as e:
            return best_move

        return best_move

    def min_value(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # if we're under specified depth, that means we've gone too far
        if depth < 1:
            raise InvalidDepth()

        legal_moves = game.get_legal_moves()
        # if there are no legal moves, min lost
        if not legal_moves:
            return float("inf"), (-1, -1)

        if depth == 1:
            val, move = min([(self.score(game.forecast_move(m), self), m)
                             for m in legal_moves])
            return val, move

        # set min to positive infinity
        min_val = float("inf")
        move = (-1, -1)
        for m in legal_moves:
            try:
                res, _ = self.max_value(game.forecast_move(m), depth - 1)
            except Exception as e:
                if move == (-1, -1):
                    raise
                return min_val, move
            if res < min_val:
                if res == float("-inf"):
                    return res, m
                min_val, move = res, m
        return min_val, move

    def max_value(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # if we're under specified depth, that means we've gone too far
        if depth < 1:
            raise InvalidDepth()

        legal_moves = game.get_legal_moves()
        # if there are no legal moves, max lost
        if not legal_moves:
            return float("-inf"), (-1, -1)

        if depth == 1:
            val, move = max([(self.score(game.forecast_move(m), self), m)
                             for m in legal_moves])
            return val, move

        max_val = float("-inf")
        move = (-1, -1)
        for m in legal_moves:
            try:
                res, _ = self.min_value(game.forecast_move(m), depth - 1)
            except Exception as e:
                if move == (-1, -1):
                    raise
                return max_val, move
            if res > max_val:
                if res == float("inf"):
                    return res, m
                max_val, move = res, m
        return max_val, move


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """
    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        if not game.get_legal_moves():
            return (-1, -1)

        best_move = random.choice(game.get_legal_moves())
        try:
            iterative_depth = 1
            while True:
                move = self.alphabeta(game, iterative_depth)
                if move == (-1, -1):
                    continue
                best_move = move
                score = self.score(game.forecast_move(best_move), self)
                if score == float("-inf") or score == float("inf"):
                    break
                iterative_depth += 1
        except Exception:
            pass

        # Return the best move from the last completed search iteration
        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        try:
            _, best_move = self.max_value(game, depth, alpha, beta)
        except Exception:
            pass
        return best_move

    def min_value(self, game, depth, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # if we're under specified depth, that means we've gone too far
        if depth < 1:
            raise InvalidDepth()

        legal_moves = game.get_legal_moves()
        # if there are no legal moves, return
        if not legal_moves:
            return float("inf"), (-1, -1)

        # set min to positive infinity
        min_val = float("inf")
        move = (-1, -1)
        for m in legal_moves:
            if depth == 1:
                res = self.score(game.forecast_move(m), self)
            elif depth > 1:
                try:
                    res, _ = self.max_value(game.forecast_move(m), depth - 1,
                                            alpha, beta)
                except Exception as e:
                    if move == (-1, -1):
                        raise
                    return min_val, move
            # alpha test, if result is less than alpha, then the short circuit
            if res <= alpha:
                return res, m
            if res < min_val:
                min_val, move = res, m
            beta = min(beta, min_val)
        return min_val, move

    def max_value(self, game, depth, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # if we're under specified depth, that means we've gone too far
        if depth < 1:
            raise InvalidDepth()

        legal_moves = game.get_legal_moves()
        # if there are no legal moves, return
        if not legal_moves:
            return float("-inf"), (-1, -1)

        max_val = float("-inf")
        move = (-1, -1)
        for m in legal_moves:
            if depth == 1:
                res = self.score(game.forecast_move(m), self)
            elif depth > 1:
                try:
                    res, _ = self.min_value(game.forecast_move(m), depth - 1,
                                            alpha, beta)
                except Exception as e:
                    if move == (-1, -1):
                        raise
                    return max_val, move
            # beta test, if res is greater than beta, then we don't need
            # to search further
            if res >= beta:
                return res, m
            if res > max_val:
                max_val, move = res, m
            alpha = max(alpha, max_val)
        return max_val, move
