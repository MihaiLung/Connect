from GUI import *
from Game_final import *
from tkinter import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

class Simulation:
    #The player AI needs two variables to be initialised - which instance of the GameBoard object it sees and acts upon, and
    #what is the number of Monte Carlo simulations it will run before it will settle on an action to take.
    def __init__(self):
        self.player1=Player(1)
        self.player2=Player(-1)
        self.get_game_setup()
        self.game=GameBoard(self.rows,self.columns,self.connects)
        self.GUI=connectGUI(self.rows,self.columns)
        if self.player1.AI==True and self.player2.AI==True:
            self.play_game()
        elif self.player1.AI==True or self.player2.AI==True:
            self.play_game()
        else:
            self.playgame_PvP()

    def get_game_setup(self):
        self.root=Tk()
        setup=setup_window(self.root)
        self.root.mainloop()

        self.player1.AI=not setup.p1human.get()
        self.player1.vision=setup.player1vision.get()
        self.player1.lto=float(setup.player1_LTO.get())/100
        self.player1.numsims=int(setup.player1sims.get())

        self.player2.AI=not setup.p2human.get()
        self.player2.vision=setup.player2vision.get()
        self.player2.lto=float(setup.player2_LTO.get())/100
        self.player2.numsims=setup.player2sims.get()

        self.rows=int(setup.rows.get())
        self.columns=int(setup.columns.get())
        self.connects=int(setup.connects.get())

        """
    def play_game(self):
        #Initialise GUI
        self.GUI.initialise_game(self.game)

        #Initialise game loop
        player1_turn=True
        win=False
        draw=False
        lost=False
        done=False
        disk_dropping=False
        updated_board=True
        player1_turn=True
        round=1
        board=copy.deepcopy(self.game.board)
        GUI_refreshed=True
        while (win==False and draw==False and lost==False) or disk_dropping:
            # --- Main event loop
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True

            if not disk_dropping and updated_board and GUI_refreshed:
                if player1_turn==True:
                    #Control the value of the vision parameter while the game is still in the initial stages, as its processing load is maximal and information added minimal early on.
                    if round<self.game.connects*3:
                        vision=min(self.player1.vision,2)
                    else:
                        vision=self.player1.vision
                    win,draw,row,column=self.player1.make_AI_play(self.game,self.player2,vision)
                    #Have these display AFTER game is over
                    if win==True:
                        print("Player 1 is the winner.")
                    elif draw==True:
                        print("The game ended in a draw. Neither player wins.")
                else:
                    if round<self.game.connects*3:
                        vision=min(self.player2.vision,2)
                    else:
                        vision=self.player2.vision
                    lost,draw,row,column=self.player2.make_AI_play(self.game,self.player1,vision)
                    if lost==True:
                        print("Player 2 is the winner.")
                    elif draw==True:
                        print("The game ended in a draw. Neither player wins.")
                disk_dropping=True
                updated_board=False
                if player1_turn:
                    ball_color=RED
                else:
                    ball_color=BLUE
                current_coord,end_coord=self.GUI.get_disk_trajectory(row,column)
                player1_turn=not player1_turn
                #Increment round tracker
                round+=1

            self.GUI.screen.fill(BLACK)
            #Highlight column if moused over
            for j in range(self.columns):
                if self.GUI.highlights[j][1].collidepoint(pg.mouse.get_pos()):
                    self.GUI.screen.blit(*self.GUI.highlights[j])

            #Draw main board
            for i in range(self.rows):
                for j in range(self.columns):
                    self.GUI.screen.blit(self.GUI.grid_space[i][j][0],self.GUI.grid_space_rects[i][j])
                    if board[i][j]==1:
                        pg.draw.ellipse(self.GUI.screen,RED,self.GUI.grid_space_rects[i][j])
                    elif board[i][j]==-1:
                        pg.draw.ellipse(self.GUI.screen,BLUE,self.GUI.grid_space_rects[i][j])
            GUI_refreshed=True

            #Disk dropping animation
            if disk_dropping==True:
                if current_coord[1]<end_coord[1]-8:
                    current_coord[1]+=8
                else:
                    disk_dropping=False
                pg.draw.ellipse(self.GUI.screen,ball_color,current_coord)
            elif updated_board==False:
                board=copy.deepcopy(self.game.board)
                updated_board=True
                GUI_refreshed=False

            pg.display.flip()

            self.GUI.clock.tick(60)
        while not done:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
            #Highlight column if moused over
            for j in range(self.columns):
                if self.GUI.highlights[j][1].collidepoint(pg.mouse.get_pos()):
                    self.GUI.screen.blit(*self.GUI.highlights[j])

            #Draw main board
            for i in range(self.rows):
                for j in range(self.columns):
                    self.GUI.screen.blit(self.GUI.grid_space[i][j][0],self.GUI.grid_space_rects[i][j])
                    if board[i][j]==1:
                        pg.draw.ellipse(self.GUI.screen,RED,self.GUI.grid_space_rects[i][j])
                    elif board[i][j]==-1:
                        pg.draw.ellipse(self.GUI.screen,BLUE,self.GUI.grid_space_rects[i][j])
        pg.quit()

"""


    def play_game(self):

        #Initialise GUI
        self.GUI.initialise_game(self.game)

        #Initialise game loop
        player1_turn=True
        win=False
        draw=False
        lost=False
        done=False
        disk_dropping=False
        updated_board=True
        player1_turn=True
        round=1
        board=copy.deepcopy(self.game.board)
        GUI_refreshed=True

        while (win==False and draw==False and lost==False) or not GUI_refreshed:
            #Replace disk_dropping with board updated flag
            # --- Main event loop
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if player1_turn:
                        currplayer=self.player1
                    else:
                        currplayer=self.player2
                    if not disk_dropping and not currplayer.AI:
                        location=pg.mouse.get_pos()
                        column=int((location[0]-self.GUI.margin)//(self.GUI.margin+self.GUI.edge))
                        action_row=-1
                        for row in reversed(range(self.rows)):
                            if self.game.board[row,column]==0:
                                action_row=row
                                break
                        if action_row>-1:
                            current_coord,end_coord=self.GUI.get_disk_trajectory(action_row,column)
                            disk_dropping=True
                            updated_board=False
                            self.game.board[action_row,column]=currplayer.tick
                            if player1_turn:
                                ball_color=RED
                            else:
                                ball_color=BLUE
                            player1_turn=not player1_turn


            if not disk_dropping and updated_board and GUI_refreshed:
                if player1_turn and self.player1.AI:
                    #Control the value of the vision parameter while the game is still in the initial stages, as its processing load is maximal and information added minimal early on.
                    if round<self.game.connects*3:
                        vision=min(self.player1.vision,2)
                    else:
                        vision=self.player1.vision
                    win,draw,row,column=self.player1.make_AI_play(self.game,self.player2,vision)
                    #Have these display AFTER game is over
                    if win==True:
                        print("Player 1 is the winner.")
                    elif draw==True:
                        print("The game ended in a draw. Neither player wins.")
                    disk_dropping=True
                    updated_board=False
                    ball_color=RED
                    current_coord,end_coord=self.GUI.get_disk_trajectory(row,column)
                    player1_turn=not player1_turn
                elif (not player1_turn) and self.player2.AI:
                    if round<self.game.connects*3:
                        vision=min(self.player2.vision,2)
                    else:
                        vision=self.player2.vision
                    lost,draw,row,column=self.player2.make_AI_play(self.game,self.player1,vision)
                    if lost==True:
                        print("Player 2 is the winner.")
                    elif draw==True:
                        print("The game ended in a draw. Neither player wins.")
                    disk_dropping=True
                    updated_board=False
                    ball_color=BLUE
                    current_coord,end_coord=self.GUI.get_disk_trajectory(row,column)
                    player1_turn=not player1_turn
                #Increment round tracker
                round+=1

            self.GUI.screen.fill(BLACK)
            #Highlight column if moused over
            for j in range(self.columns):
                if self.GUI.highlights[j][1].collidepoint(pg.mouse.get_pos()):
                    self.GUI.screen.blit(*self.GUI.highlights[j])

            #Draw main board
            for i in range(self.rows):
                for j in range(self.columns):
                    self.GUI.screen.blit(self.GUI.grid_space[i][j][0],self.GUI.grid_space_rects[i][j])
                    if board[i][j]==1:
                        pg.draw.ellipse(self.GUI.screen,RED,self.GUI.grid_space_rects[i][j])
                    elif board[i][j]==-1:
                        pg.draw.ellipse(self.GUI.screen,BLUE,self.GUI.grid_space_rects[i][j])
            GUI_refreshed=True

            #Disk dropping animation
            if disk_dropping==True:
                if current_coord[1]<end_coord[1]-8:
                    current_coord[1]+=8
                else:
                    disk_dropping=False
                pg.draw.ellipse(self.GUI.screen,ball_color,current_coord)
            elif updated_board==False:
                board=copy.deepcopy(self.game.board)
                updated_board=True
                GUI_refreshed=False

            pg.display.flip()

            self.GUI.clock.tick(60)
        while not done:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
            #Highlight column if moused over
            for j in range(self.columns):
                if self.GUI.highlights[j][1].collidepoint(pg.mouse.get_pos()):
                    self.GUI.screen.blit(*self.GUI.highlights[j])

            #Draw main board
            for i in range(self.rows):
                for j in range(self.columns):
                    self.GUI.screen.blit(self.GUI.grid_space[i][j][0],self.GUI.grid_space_rects[i][j])
                    if board[i][j]==1:
                        pg.draw.ellipse(self.GUI.screen,RED,self.GUI.grid_space_rects[i][j])
                    elif board[i][j]==-1:
                        pg.draw.ellipse(self.GUI.screen,BLUE,self.GUI.grid_space_rects[i][j])
        pg.quit()

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

sim=Simulation()
