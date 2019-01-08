import random
import numpy as np
from tabulate import tabulate
import copy
import pygame as pg

class Slot:
    red=False
    blue=False
    def __init__(self, rect, **kwargs):
        self.process_kwargs(kwargs)
        self.rect = pg.Rect(rect)
        self.image = pg.Surface(self.rect.size).convert()
        #self.function = command
        self.text = self.font.render(self.text,True,self.font_color)
        self.text_rect = self.text.get_rect(center=self.rect.center)


    def red_play(self,Surface):
        self.red=True

    def blue_play(self,Surface):
        self.blue=True

    def process_kwargs(self, kwargs):
        settings = {
            'color'         :pg.Color('white'),
            'text'          :'default',
            'font'          :pg.font.SysFont('Arial', 16),
            'hover_color'   :(200,0,0),
            'font_color'    :pg.Color('white'),
            'border_color'  :pg.Color('black')
        }
        for kwarg in kwargs:
            if kwarg in settings:
                settings[kwarg] = kwargs[kwarg]
            else:
                raise AttributeError("{} has no keyword: {}".format(self.__class__.__name__, kwarg))
        self.__dict__.update(settings)

    def is_hovering(self):
        if self.rect.collidepoint(pg.mouse.get_pos()):
            return True

    def draw(self, surf):
        if self.is_hovering():
            self.image.fill(self.hover_color)
        else:
            self.image.fill(self.color)
        surf.blit(self.text, self.text_rect)
        surf.blit(self.image, self.rect)
        if self.red==True:
            pg.draw.ellipse(surf,pg.Color("red"),self.rect)
            pg.display.update()
        if self.blue==True:
            pg.draw.ellipse(surf,pg.Color("blue"),self.rect)
            pg.display.update()


class GameBoard:
    #Current round tracker
    cr=0

    def __init__(self,rows=6,columns=7,connects=4):
        self.rows=rows
        self.columns=columns
        self.connects=connects
        self.board=np.zeros((rows,columns))
        self.diag_win_min=connects*(connects+1)/2

    #The play function takes an action argument, checks its validity, updates the board accordingly, and checks whether a winning condition was met
    def play(self,column,tick):
        #Check if action is feasible
        if self.board[0,column]!=0:
            print("Cannot take this action")
            return False, False
        self.cr+=1
        #Take action
        for row in reversed(range(self.rows)):
            if self.board[row,column]==0:
                self.board[row,column]=tick
                break
        return row,column
        #Takes value True if this move won the game, 0 otherwise


    def check_win(self,tick,row,column):
        "Checks if the current player won"

        #If not enough rounds were played for a player to have won, return fasle
        """print(self.cr)
        if self.cr<self.connects*2-2:
            return False
        """
        dE=min(self.columns-1,column+self.connects-1)
        dN=max(0,row-self.connects+1)
        dW=max(0,column-self.connects+1)
        dS=min(self.rows-1,row+self.connects-1)
        #print("Row col: ",row,column)
        #print("ENWS: ",dE,dN,dW,dS)

        dNE=min(row-dN,dE-column)
        dNW=min(row-dN,column-dW)
        dSW=min(dS-row,column-dW)
        dSE=min(dS-row,dE-column)

        #print("NE %s NW %s SW %s SE %s" % (dNE, dNW, dSW, dSE))

        checks=[]

        if dE-dW+1>=self.connects:
            checks.append(self.board[row,dW:dE+1])
        if dS-dN+1>=self.connects:
            checks.append(self.board[dN:dS+1,column])
        if dNW+dSE+1>=self.connects:
            checks.append([])
            for i in range(dNW+dSE+1):
                checks[-1].append(self.board[row-dNW+i,column-dNW+i])
        if dNE+dSW+1>=self.connects:
            checks.append([])
            for i in range(dNE+dSW+1):
                checks[-1].append(self.board[row-dNE+i,column+dNE-i])
        for array in checks:
            counter=0
            for slot in array:
                if slot==tick:
                    counter+=1
                else:
                    counter=0
                if counter==self.connects:
                    return True
        return False


    def get_valid_actions(self):
        actions=list(range(self.columns))
        for action in actions[:]:
            if self.board[0,action]!=0:
                actions.remove(action)
        return actions

    def print_game_state(self):
        print("**********************************")
        print(self.board)

    def check_draw(self):
        for col in range(self.columns):
            if self.board[0,col]==0:
                return False
        return True

    def get_row_of_action(self,action):
        "Gets the row where a slot would be dropped given a certain action. Assumes the action passed to it is valid (eg the column is not full)"
        row=''
        candidate=self.rows-1
        while row=='':
            if self.board[candidate,action]==0:
                row=candidate
            else:
                candidate-=1
        return row


#Player object with two attributes - the Monte Carlo simulations performed before computing each action. This is a measure of the "inteligence" of the AI.
class Player:
    "Tick = unique numeric identifier (suggested: 1 and -1). Vision = how many turns ahead will the AI check before making a move. LTO = cumulative discount for outcome of end-states, making further away outcomes less (un)preferred than nearer ones."
    def __init__(self,tick,vision=2,long_term_orientation=0.9,numsims=100):
        self.tick=tick
        self.vision=vision
        self.lto=long_term_orientation
        self.numsims=numsims

    def make_naive_play(self,game):
        "Makes a naive play that picks randomly from feasible options. Very fast computation-wise"
        actionlist=game.get_valid_actions()
        if actionlist==[]:
            action_outcome=False
            return action_outcome,False,False
        chosen_action=np.random.choice(actionlist)
        row,column=game.play(chosen_action,self.tick)
        action_outcome=True
        return action_outcome,row,column

    def make_intelligent_play(self,game,opponent,vision):
        "Makes a more intelligent play by looking ahead for a number of turns equal to the player's vision. Can get very computation-intensive for players with a large vision parameter."
        #For the first iteration, check if there is any winning move and return that, otherwise either look deeper if appropriate or return a random action.
        if vision==0:
            action_outcome,row,column=self.make_naive_play(game)
            return action_outcome,row,column
        action_outcome=True
        #Get valid actions and quit if there are none.
        actionlist=game.get_valid_actions()
        print(actionlist)
        if actionlist==[]:
            action_outcome=False
            row=False
            column=False
            return action_outcome, row, column
        #Check if any valid action results in a win, in which case choose that
        for action in actionlist:
            simgame=copy.deepcopy(game)
            simrow,simcol=simgame.play(action,self.tick)
            print(simgame.check_win(self.tick,simrow,simcol))
            if simgame.check_win(self.tick,simrow,simcol)==True:
                row_played,column_played=game.play(action, self.tick)
                return action_outcome,row_played,column_played

        #If there are no winning actions, if player vision is higher than one then proceed to evaluate the game-state at one level deeper, otherwise pick an action at random.
        if self.vision==1:
            action=np.random.choice(actionlist)
            row_played,column_played=game.play(action, self.tick)
            return action_outcome, row_played, column_played
        else:
            action_value=np.zeros_like(actionlist)
            for index, action in enumerate(actionlist):
                    simgame=copy.deepcopy(game)
                    simrow,simcol=simgame.play(action,self.tick)
                    if simgame.check_draw()==True:
                        action_value[index]=-1
                    else:
                        action_value[index]=-opponent.state_valuation(game=simgame,level=2,vision=self.vision,opponent=self,lto=self.lto)
            #In case multiple actions are equally favourable (likely in sparse game-states), pick a random action out of those tied for most favourable to prevent the AI from being biased towards the left-most column
            #print(actionlist,action_value.tolist())
            action_chosen=actionlist[np.random.choice(np.argwhere(action_value.tolist()==np.amax(action_value)).flatten().tolist())]
            row_played,column_played=game.play(action_chosen, self.tick)
            return action_outcome, row_played, column_played

    def state_valuation(self,game,level,vision,opponent,lto):
        "Returns the value of the game-state. Evaluation sophistication is a function of the level and vision parameters - the function will recur until a possible end-state was reached or until the levels equal vision."
        actionlist=game.get_valid_actions()
        #The value of being in a draw state is -1 (preferable to losing (negative value) but inferior to winning (positive value)).
        if actionlist==[]:
            return -1

        #Get state-action outcomes
        action_outcomes=np.zeros_like(actionlist)
        for index, action in enumerate(actionlist):
            simgame=copy.deepcopy(game)
            simrow,simcol=simgame.play(action,self.tick)
            win=simgame.check_win(self.tick,simrow,simcol)
            draw=simgame.check_draw()
            if win==True:
                action_outcomes[index]=2
            elif draw==True:
                action_outcomes[index]=1
        num_winning_moves=np.count_nonzero(action_outcomes==2)

        #A state where the player has multiple winning moves is extremely valuable, as it is basically a guaranteed win
        if num_winning_moves>1:
            return 100

        #A state where the player has a single winning move is still valuable, albeit less so as the opponent is more likely to be able to block this move. That is unless the winning move is inevitable.
        elif num_winning_moves==1:
            if len(actionlist)==1:
                return 100
            else:
                return 10

        #If the player has no winning moves at this level but his vision goes deeper than the current level, go one level deeper to evaluate
        elif level<vision:
            action_value=np.zeros_like(actionlist)
            for index, action in enumerate(actionlist):
                #draw outcomes are slightly unfavourable, although preferred to loss outcomes
                if action_outcomes[index]==1:
                    action_value[index]=-1
                else:
                    simgame=copy.deepcopy(game)
                    simrow,simcol=simgame.play(action,self.tick)
                    action_value[index]=-lto*opponent.state_valuation(simgame,level+1,vision,self,lto)
            #The value of being in this state is equal to the value netted by the most valuable action available to the player
            return max(action_value)

        #If this is as deep as the player's vision goes, and none of the other if conditions were met, return a value of 0 (no potential win move was seen for either player, so we are neutral to this end state)
        else:
            return 0

    def makeplay(self,game,opponent,vision):
        "Computes an optimal play via Monte Carlo sampling of complete game outcomes. Assumes players make plays of varying sophistication, controlled by the Vision parameter of the player class"
        #The function updates the game with the player's move and returns whether the player won or ended in a draw
        actionlist=game.get_valid_actions()
        if actionlist==[]:
            action_outcome=False
            return action_outcome
        #Ensure all actions are equally explored. If the number of simulations is not divisible,
        #by the number of actions, ensure the actions trialed one additional time compared to the
        #minimally explored action are randomly chosen.
        num_trials_per_action=np.ones(len(actionlist))*self.numsims//len(actionlist)
        extra=self.numsims%len(actionlist)
        for i in np.random.choice(range(len(actionlist)),extra,replace=False):
            num_trials_per_action[i]+=1

        #Run Monte Carlo simulations and track the number of wins recorded for each potential action
        wins=np.zeros_like(actionlist)
        draws=np.zeros_like(actionlist)
        loses=np.zeros_like(actionlist)
        for actionind, sims in enumerate(num_trials_per_action):
            print("CURRENT ACTION IS ",actionlist[actionind])
            for i in range(int(sims)):
                #Create local copies of objects
                game_simulation=copy.deepcopy(game)
                #Play action
                row_played,column_played=game_simulation.play(actionlist[actionind],self.tick)
                #Check player status
                win=game_simulation.check_win(self.tick,row_played,column_played)
                draw=game_simulation.check_draw()
                lost=False
                my_turn=False
                #Simulate rest of game
                #print("*********************************\nSimulation is on\n******************************************")
                while win==False and draw==False and lost==False:
                    if my_turn==True:
                        #We pick a random feasible action
                        play_outcome,row_played,column_played=self.make_intelligent_play(game_simulation,opponent,vision)
                        if play_outcome==False:
                            win=False
                            draw=True
                            lost=False
                            break
                        win=game_simulation.check_win(self.tick,row_played,column_played)
                        #draw=game_simulation.check_draw()
                        my_turn=False
                    else:
                        #We pick a random feasible action
                        play_outcome,row_played,column_played=opponent.make_intelligent_play(game_simulation,self,vision)
                        if play_outcome==False:
                            win=False
                            draw=True
                            lost=False
                            break
                        lost=game_simulation.check_win(opponent.tick,row_played,column_played)
                        #draw=game_simulation.check_draw()
                        my_turn=True
                    #print(game_simulation.board)
                if win==True:
                    wins[actionind]+=1
                elif draw==True:
                    draws[actionind]+=1
                elif lost==True:
                    loses[actionind]+=1
        print("*********************")
        print("I am player ",self.tick)
        print(wins)
        print(loses)
        print(draws)
        ideal=wins-1.5*loses
        action=actionlist[np.argmax(ideal)]
        row_played,column_played=game.play(action,self.tick)

        win=game.check_win(self.tick,row_played,column_played)
        draw=game.check_draw()
        game.print_game_state()
        return win, draw


class Simulation:
    #The player AI needs two variables to be initialised - which instance of the GameBoard object it sees and acts upon, and
    #what is the number of Monte Carlo simulations it will run before it will settle on an action to take.
    def __init__(self,player1,player2,game):
        self.player1=player1
        self.player2=player2
        self.game=game
        self.round=1

    def playgame(self):

        #Initialise graphical interface
        rows=self.game.rows
        columns=self.game.columns
        pg.init()
        screen=pg.display.set_mode((700,700))
        width=700
        height=600
        x_location=10
        y_location=100
        edge=min(width/rows,height/columns)
        slots=[]
        for i in range(rows):
            slots.append([])
            for j in range(columns):
                rect=x_location+edge*j+3*j,y_location+edge*i+3*i,edge,edge
                newslot=Slot(rect)
                slots[i].append(newslot)
        for event in pg.event.get():
            if event.type==pg.QUIT:
                done=True
        for i in range(rows):
            for j in range(columns):
                slots[i][j].draw(screen)
        pg.display.update()

        #Initialise game loop
        player1_turn=True
        win=False
        draw=False
        lost=False
        while win==False and draw==False and lost==False:
            if player1_turn==True:
                #Control the value of the vision parameter while the game is still in the initial stages, as its processing load is maximal and information added minimal in the early stages.
                if self.round<self.game.connects*3:
                    vision=min(self.player1.vision,2)
                else:
                    vision=self.player1.vision
                win,draw=self.player1.makeplay(self.game,self.player1,vision)
                if win==True:
                    print("Player 1 is the winner.")
                elif draw==True:
                    print("The game ended in a draw. Neither player wins.")
                player1_turn=False
            else:
                if self.round<self.game.connects*3:
                    vision=min(self.player2.vision,2)
                else:
                    vision=self.player2.vision
                lost,draw=self.player2.makeplay(self.game,self.player2,vision)
                if lost==True:
                    print("Player 2 is the winner.")
                elif draw==True:
                    print("The game ended in a draw. Neither player wins.")
                player1_turn=True
            #Increment round tracker
            self.round+=1

            #Update graphical display
            slots=self.update_board(game.board,slots)
            for event in pg.event.get():
                if event.type==pg.QUIT:
                    done=True
            for i in range(rows):
                for j in range(columns):
                    slots[i][j].draw(screen)
            pg.display.update()



    def update_board(self,board,slots):
        rows=len(board)
        cols=len(board[0])
        newslots=slots
        for i in range(rows):
            for j in range(cols):
                if board[i,j]==1:
                    newslots[i][j].red=True
                elif board[i,j]==-1:
                    newslots[i][j].blue=True
        return newslots

A=Player(1,3,100)
B=Player(-1,1,100)
game=GameBoard(6,7,4)
sim=Simulation(A,B,game)

game.board=np.array([
 [ 0,  0,  0,  0,  0,  0,  0,],
 [ 0,  0,  0,  0,  0,  0,  0,],
 [ 1,  0,  0,  1,  0,  0,  0,],
 [ 1,  0,  0, -1,  0,  0,  0,],
 [-1,  1, -1, -1,  0, -1,  0,],
 [ 1, -1,  1,  1,  0, -1,  0,]]
)
#Player 1 is he will ALWAYS lose if he plays 1, 3 or 4. Why?
random.seed(1)
A.makeplay(game,B,3)
print(game.board)


"""
sim.playgame()
running = True
while running:
  for event in pg.event.get():
    if event.type == pg.QUIT:
      running = False
"""
