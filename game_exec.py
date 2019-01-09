from GUI import *
from Game_final import *
from tkinter import *

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
            self.playgame_AIvAI()
        elif self.player1.AI==True or self.player2.AI==True:
            self.playgame_PlayervAI()
        else:
            self.playgame_PvP()

    def get_game_setup(self):
        self.root=Tk()
        setup=setup_window(self.root)
        self.root.mainloop()

        self.player1.AI=not setup.p1human.get()
        self.player1.vision=setup.player1vision
        self.player1.lto=float(setup.player1_LTO.get())/100
        self.player1.numsims=setup.player1sims_input.get()

        self.player2.AI=not setup.p2human.get()
        self.player2.vision=setup.player2vision
        self.player2.lto=float(setup.player2_LTO.get())/100
        self.player2.numsims=setup.player2sims_input.get()

        self.rows=int(setup.rows_label_input.get())
        self.columns=int(setup.cols_label_input.get())
        self.connects=int(setup.connects_label_input.get())

    def playgame_AIvAI(self):
        #Initialise GUI
        self.GUI.initialise_game()

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
        while win==False and draw==False and lost==False and done==False:
            # --- Main event loop
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True

            if not disk_dropping:
                if player1_turn==True:
                    #Control the value of the vision parameter while the game is still in the initial stages, as its processing load is maximal and information added minimal early on.
                    if round<self.game.connects*3:
                        vision=min(self.player1.vision,2)
                    else:
                        vision=self.player1.vision
                    win,draw,row,column=self.player1.make_AI_play(self.game,self.player1,vision)
                    #Have these display AFTER game is over
                    if win==True:
                        print("Player 1 is the winner.")
                    elif draw==True:
                        print("The game ended in a draw. Neither player wins.")
                    player1_turn=False
                else:
                    if round<self.game.connects*3:
                        vision=min(self.player2.vision,2)
                    else:
                        vision=self.player2.vision
                    lost,draw,row,column=self.player2.make_AI_play(self.game,self.player2,vision)
                    if lost==True:
                        print("Player 2 is the winner.")
                    elif draw==True:
                        print("The game ended in a draw. Neither player wins.")
                    player1_turn=True
                if not win and not lost:
                    disk_dropping=True
                    current_coord,end_coord=GUI.get_disk_trajectory(row,column)
                #Increment round tracker
                round+=1

            self.screen.fill(BLACK)
            #Highlight column if moused over
            for j in range(self.columns):
                if self.GUI.highlights[j][1].collidepoint(pg.mouse.get_pos()):
                    screen.blit(*highlights[j])

            #Draw main board
            for i in range(self.rows):
                for j in range(self.columns):
                    screen.blit(self.GUI.grid_space[i][j][0],self.grid_space_rects[i][j])
                    if self.grid_space[i][j][1]==1:
                        pg.draw.ellipse(screen,RED,self.grid_space_rects[i][j])
                    elif self.grid_space[i][j][1]==2:
                        pg.draw.ellipse(screen,BLUE,self.grid_space_rects[i][j])

            #Disk dropping animation
            if disk_dropping==True:
                if current_coord[1]<end_coord[1]-8:
                    current_coord[1]+=8
                else:
                    disk_dropping=False
                pg.draw.ellipse(screen,ball_color,current_coord)
            elif updated_board==False:
                if p1_turn:
                    self.grid_space[action_row][column][1]=1
                else:
                    self.grid_space[action_row][column][1]=2
                updated_board=True
                p1_turn=not(p1_turn)


            pg.display.flip()

            clock.tick(60)
        pg.quit()



    """
    def playgame_PlayervAI(self):

        #Initialise game loop
        player1_turn=True
        win=False
        draw=False
        lost=False

        while win==False and draw==False and lost==False:
            if player1_turn==True:
                if self.player1.AI==True:

                #Control the value of the vision parameter while the game is still in the initial stages, as its processing load is maximal and information added minimal early on.
                if self.round<self.game.connects*3:
                    vision=min(self.player1.vision,2)
                else:
                    vision=self.player1.vision
                win,draw=self.player1.make_AI_play(self.game,self.player1,vision)
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
                lost,draw=self.player2.make_AI_play(self.game,self.player2,vision)
                if lost==True:
                    print("Player 2 is the winner.")
                elif draw==True:
                    print("The game ended in a draw. Neither player wins.")
                player1_turn=True
            #Increment round tracker
            self.round+=1

            #Update graphical display
        """
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
