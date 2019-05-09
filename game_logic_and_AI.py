import random
import numpy as np
from tabulate import tabulate
import copy
import pygame as pg


class GameBoard:
    # Current round tracker
    cr = 0

    def __init__(self, rows=6, columns=7, connects=4):
        self.rows = rows
        self.columns = columns
        self.connects = connects
        self.board = np.zeros((rows, columns))
        self.diag_win_min = connects * (connects + 1) / 2

    # The play function takes an action argument, checks its validity, updates the board accordingly, and checks
    # whether a winning condition was met
    def play(self, column, tick):
        # Check if action is feasible
        if self.board[0, column] != 0:
            print("Cannot take this action")
            return False, False
        self.cr += 1

        # Take action
        for row in reversed(range(self.rows)):
            if self.board[row, column] == 0:
                self.board[row, column] = tick
                break
        return row, column

    def check_win(self, tick, row, column):
        """Checks if the current player won
        tick - unique identifier of the player making the move and of the slots currently claimed by them
        row - row of the latest move
        column - column of the latest move
        """

        direction_east = min(self.columns - 1, column + self.connects - 1)
        direction_north = max(0, row - self.connects + 1)
        direction_west = max(0, column - self.connects + 1)
        direction_south = min(self.rows - 1, row + self.connects - 1)

        direction_north_east = min(row - direction_north, direction_east - column)
        direction_north_west = min(row - direction_north, column - direction_west)
        direction_south_west = min(direction_south - row, column - direction_west)
        direction_south_east = min(direction_south - row, direction_east - column)

        checks = []

        # Generate a list of the arrays where a win is possible to have occured given the latest move
        if direction_east - direction_west + 1 >= self.connects:
            checks.append(self.board[row, direction_west:direction_east + 1])
        if direction_south - direction_north + 1 >= self.connects:
            checks.append(self.board[direction_north:direction_south + 1, column])
        if direction_north_west + direction_south_east + 1 >= self.connects:
            checks.append([])
            for i in range(direction_north_west + direction_south_east + 1):
                checks[-1].append(self.board[row - direction_north_west + i, column - direction_north_west + i])
        if direction_north_east + direction_south_west + 1 >= self.connects:
            checks.append([])
            for i in range(direction_north_east + direction_south_west + 1):
                checks[-1].append(self.board[row - direction_north_east + i, column + direction_north_east - i])

        # For each array, check if the player has won, in which case return True. If no condition was met, return False
        for array in checks:
            counter = 0
            for slot in array:
                if slot == tick:
                    counter += 1
                else:
                    counter = 0
                if counter == self.connects:
                    return True
        return False

    def get_valid_actions(self):
        """"
        Returns a list of the valid actions available to the current player.
        """
        actions = list(range(self.columns))
        for action in actions[:]:
            if self.board[0, action] != 0:
                actions.remove(action)
        return actions

    def print_game_state(self):
        print("**********************************")
        print(self.board)

    def check_draw(self):
        """"Check if the game_state is a draw"""
        for column in range(self.columns):
            if self.board[0, column] == 0:
                return False
        return True

    def get_row_of_action(self, action):
        """Gets the row where a slot would be dropped given a certain column chosen to drop it in.
        Assumes the action passed to it is valid (eg the column is not full)"""
        row = ''
        candidate = self.rows - 1
        while row == '':
            if self.board[candidate, action] == 0:
                row = candidate
            else:
                candidate -= 1
        return row


# Player object with two attributes - the Monte Carlo simulations performed before computing each action. This is a measure of the "inteligence" of the AI.
class Player:
    """
    Tick = unique numeric identifier (suggested: 1 and -1).
    Vision = how many turns ahead will the AI check before making a move.
    Long-term-orientation = cumulative discount for outcome of end-states. Lower values means less importance is
    assigned to win or loss scenarios many plays in the future.
    """

    def __init__(self, tick, vision=2, long_term_orientation=0.9, num_sims=100):
        self.tick = tick
        self.vision = vision
        self.lto = long_term_orientation
        self.num_sims = num_sims

    def make_naive_play(self, game):
        """Makes a naive play that picks randomly from feasible options. Very fast computation-wise"""
        action_list = game.get_valid_actions()
        if action_list == []:
            action_outcome = False
            return action_outcome, False, False
        chosen_action = np.random.choice(action_list)
        row, column = game.play(chosen_action, self.tick)
        action_outcome = True
        return action_outcome, row, column

    def make_intelligent_play(self, game, opponent, vision):
        "Makes a more intelligent play by looking ahead for a number of turns equal to the player's vision. Can get very computation-intensive for players with a large vision parameter."
        # If vision is 0 (purely random AI), do an arbitrary play.
        if vision == 0:
            action_successful, row, column = self.make_naive_play(game)
            return action_successful, row, column
        action_successful = True
        # Get valid actions and quit if there are none.
        action_list = game.get_valid_actions()
        # print(actionlist)
        if not action_list:
            action_successful = False
            row = False
            column = False
            return action_successful, row, column
        # Check if any valid action results in a win, in which case choose that
        for action in action_list:
            game_simulation = copy.deepcopy(game)
            row_sim, col_sim = game_simulation.play(action, self.tick)
            if game_simulation.check_win(self.tick, row_sim, col_sim):
                row_played, column_played = game.play(action, self.tick)
                return action_successful, row_played, column_played

        # If there are no winning actions, proceeds one level deeper into evaluation.
        # If player vision is 1, take a random action (vision 1 means only evaluate one action ahead)
        if self.vision == 1:
            action = np.random.choice(action_list)
            row_played, column_played = game.play(action, self.tick)
            return action_successful, row_played, column_played
        else:
            action_value = np.zeros_like(action_list)
            # Evaluate each action ahead
            for index, action in enumerate(action_list):
                # For each action, check if it is a draw (we already checked before for winning actions)
                game_simulation = copy.deepcopy(game)
                _, _ = game_simulation.play(action, self.tick)
                if game_simulation.check_draw():
                    # If the action is a draw, assign the value -1 to it
                    action_value[index] = -1
                # If the action does not end the game, proceed to evaluate it from the opponent's perspective.
                else:
                    action_value[index] = -opponent.state_valuation(game=game_simulation, level=2, vision=self.vision,
                                                                    opponent=self, long_term_orientation=self.lto,
                                                                    player_is_opponent=True)
            # Pick the most valuable action, as evaluated above
            # Pick randomly if multiple actions tied for most valuable (frequent situation in sparse game-states)
            action_chosen = action_list[
                np.random.choice(np.argwhere(action_value.tolist() == np.amax(action_value)).flatten().tolist())]
            row_played, column_played = game.play(action_chosen, self.tick)
            return action_successful, row_played, column_played

    def state_valuation(self, game, level, vision, opponent, long_term_orientation, player_is_opponent):
        """
        Returns the value of the game-state.
        game = instance of a game object
        level = how many levels deep into the recurrent state valuation process the program is at the point when
        this function is called
        vision = vision parameter of the root player. Tracks how deep the evaluation recursion will go.
        long_term_orientation = parameter controlling the degree of the AI's preference for immediate
        over delayed reward.
        player_is_opponent = boolean indicating whether the player from who's perspective the game-state is evaluated
        at this stage is the root player or their opponent
        """
        actionlist = game.get_valid_actions()
        # If there are no valid actions, the game is a draw
        # The value of this state is -1 - negative but less so than losing.
        if not actionlist:
            return -1

        # Get state-action outcomes
        action_outcomes = np.zeros_like(actionlist)
        for index, action in enumerate(actionlist):
            simgame = copy.deepcopy(game)
            simrow, simcol = simgame.play(action, self.tick)
            win = simgame.check_win(self.tick, simrow, simcol)
            draw = simgame.check_draw()
            if win == True:
                action_outcomes[index] = 2
            elif draw == True:
                action_outcomes[index] = 1
        num_winning_moves = np.count_nonzero(action_outcomes == 2)

        # Next we value moves that result in a player winning the game entirely.
        # We want the AI to be risk averse - it puts higher weight on avoiding potential losses than on chasing
        # potential wins. As such, losing outcomes are valued 1.5 times higher in absolute terms.

        # A state where the player has multiple winning moves is extremely valuable, as it is basically a guaranteed win
        if num_winning_moves > 1:
            if player_is_opponent:
                return 150
            else:
                return 100

        # States with one single winning move are valuable but less so than the above scenario. The AI assumes
        # their opponent will block before they can win should there be a single winning move. As such this is weighted
        # 10 times lower than the above scenario
        elif num_winning_moves == 1:
            if player_is_opponent:
                return 15
            else:
                return 10

        # If the player's vision allows, evaluate one level deeper
        elif level < vision:
            action_value = np.zeros_like(actionlist)
            for index, action in enumerate(actionlist):
                # draw outcomes are slightly unfavourable, although preferred to loss outcomes
                if action_outcomes[index] == 1:
                    action_value[index] = -1
                else:
                    simgame = copy.deepcopy(game)
                    simrow, simcol = simgame.play(action, self.tick)
                    action_value[index] = -long_term_orientation * opponent.state_valuation(simgame, level + 1, vision, self, long_term_orientation,
                                                                                            not player_is_opponent)
            # return the value of the state to the player.
            return sum(action_value) / len(action_value)

        # If the player's vision only goes as deep as this and none of the above conditions triggered, return 0
        else:
            return 0

    def make_AI_play(self, game, opponent, vision):
        """Computes an optimal play for the current player via Monte Carlo sampling of complete game outcomes.
        Sophistication is controlled by the vision parameter."""
        # The function updates the game with the player's move and returns whether the player won or ended in a draw
        actionlist = game.get_valid_actions()

        # Ensure all actions are equally explored. If the number of simulations is not divisible,
        # by the number of actions, ensure the actions trialed one additional time compared to the
        # minimally explored action are randomly chosen.
        num_trials_per_action = np.ones(len(actionlist)) * self.num_sims // len(actionlist)
        extra = self.num_sims % len(actionlist)
        for i in np.random.choice(range(len(actionlist)), extra, replace=False):
            num_trials_per_action[i] += 1

        # Run Monte Carlo simulations and track the number of wins recorded for each potential action
        wins = np.zeros_like(actionlist)
        draws = np.zeros_like(actionlist)
        loses = np.zeros_like(actionlist)
        for action_ind, sims in enumerate(num_trials_per_action):
            print("CURRENT ACTION IS ", actionlist[action_ind])
            for i in range(int(sims)):
                # Create local copies of objects
                game_simulation = copy.deepcopy(game)
                # Play action
                row_played, column_played = game_simulation.play(actionlist[action_ind], self.tick)
                # Check player status
                win = game_simulation.check_win(self.tick, row_played, column_played)
                draw = game_simulation.check_draw()
                lost = False
                my_turn = False
                # Simulate rest of game
                while not (win or draw or lost):
                    if my_turn:
                        # We pick a random feasible action
                        play_successful, row_played, column_played = self.make_intelligent_play(game_simulation, opponent,
                                                                                             vision)
                        if not play_successful:
                            win = False
                            draw = True
                            lost = False
                            break
                        win = game_simulation.check_win(self.tick, row_played, column_played)
                        my_turn = False
                    else:
                        # We pick a random feasible action
                        play_successful, row_played, column_played = opponent.make_intelligent_play(game_simulation, self,
                                                                                                 vision)
                        if not play_successful:
                            win = False
                            draw = True
                            lost = False
                            break
                        lost = game_simulation.check_win(opponent.tick, row_played, column_played)
                        my_turn = True
                if win:
                    wins[action_ind] += 1
                elif draw:
                    draws[action_ind] += 1
                elif lost:
                    loses[action_ind] += 1
        print("*"*21)
        print("Current player: {}".format(self.tick))
        print(wins)
        print(loses)
        print(draws)
        ideal = wins - 1.5 * loses
        action = actionlist[np.argmax(ideal)]
        row_played, column_played = game.play(action, self.tick)

        win = game.check_win(self.tick, row_played, column_played)
        draw = game.check_draw()
        game.print_game_state()
        return win, draw, row_played, column_played


class Simulation:

    def __init__(self, player1, player2, game):
        self.player1 = player1
        self.player2 = player2
        self.game = game
        self.round = 1

    def play_game(self):

        # Initialise graphical interface
        rows = self.game.rows
        columns = self.game.columns
        pg.init()
        screen = pg.display.set_mode((700, 700))
        width = 700
        height = 600
        x_location = 10
        y_location = 100
        edge = min(width / rows, height / columns)
        slots = []
        for i in range(rows):
            slots.append([])
            for j in range(columns):
                rect = x_location + edge * j + 3 * j, y_location + edge * i + 3 * i, edge, edge
                newslot = Slot(rect)
                slots[i].append(newslot)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
        for i in range(rows):
            for j in range(columns):
                slots[i][j].draw(screen)
        pg.display.update()

        # Initialise game loop
        player1_turn = True
        win = False
        draw = False
        lost = False
        while not (win or draw or lost):
            if player1_turn:
                # Early on high vision causes very large memory load with very little effect on the AI's performance.
                # We are putting a cap on it early in the game to improve performance
                if self.round < self.game.connects * 3:
                    vision = min(self.player1.vision, 2)
                else:
                    vision = self.player1.vision
                win, draw = self.player1.make_AI_play(self.game, self.player1, vision)
                if win:
                    print("Player 1 is the winner.")
                elif draw:
                    print("The game ended in a draw. Neither player wins.")
                player1_turn = False
            else:
                if self.round < self.game.connects * 3:
                    vision = min(self.player2.vision, 2)
                else:
                    vision = self.player2.vision
                lost, draw = self.player2.make_AI_play(self.game, self.player2, vision)
                if lost:
                    print("Player 2 is the winner.")
                elif draw:
                    print("The game ended in a draw. Neither player wins.")
                player1_turn = True
            # Increment round tracker
            self.round += 1

            # Update graphical display
            slots = self.update_board(game.board, slots)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
            for i in range(rows):
                for j in range(columns):
                    slots[i][j].draw(screen)
            pg.display.update()

    def update_board(self, board, slots):
        rows = len(board)
        cols = len(board[0])
        new_slots = slots
        for i in range(rows):
            for j in range(cols):
                if board[i, j] == 1:
                    new_slots[i][j].red = True
                elif board[i, j] == -1:
                    new_slots[i][j].blue = True
        return new_slots


