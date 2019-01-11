
import pygame as pg
import copy
import tkinter as tk
from tkinter import *
import PIL
from PIL import Image
import cv2
from Game_final import GameBoard

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

class setup_window:
    initialised=False
    def __init__(self, master):
        self.master = master
        master.geometry("400x500") #You want the size of the app to be 500x500
        master.resizable(0, 0) #Don't allow resizing in the x or y direction

        master.title("Connect Set Up")
        self.frame_board_settings=Frame(master)
        self.label=Label(self.frame_board_settings, text="Set up the game!")
        self.label.grid(columnspan=2)


        self.rows=IntVar(None,6)
        self.columns=IntVar(None,7)
        self.connects=IntVar(None,4)
        self.rows_label=Label(self.frame_board_settings,text="Rows")
        self.cols_label=Label(self.frame_board_settings,text="Columns")
        self.connects_label=Label(self.frame_board_settings,text="Connects to win")

        self.rows_label_input=Entry(self.frame_board_settings,justify='center',textvariable=self.rows)
        self.cols_label_input=Entry(self.frame_board_settings,justify='center',textvariable=self.columns)
        self.connects_label_input=Entry(self.frame_board_settings,justify='center',textvariable=self.connects)

        self.rows_label.grid(row=1,column=0,sticky="E")
        self.cols_label.grid(row=2,column=0,sticky="E")
        self.connects_label.grid(row=3,column=0,sticky="E")

        self.rows_label_input.grid(row=1,column=1)
        self.cols_label_input.grid(row=2,column=1)
        self.connects_label_input.grid(row=3,column=1)

        self.frame_board_settings.pack()


        self.frame_player_setting=Frame(master,bd=5)



        self.label_p1=Label(self.frame_player_setting,text="Player 1")
        self.label_p2=Label(self.frame_player_setting,text="Player 2")
        self.label_p1.grid(row=1,column=0)
        self.label_p2.grid(row=1,column=1)

        self.p1human=BooleanVar(None,0)
        self.p2human=BooleanVar(None,0)



        self.frame_vision_1=Frame(self.frame_player_setting)
        self.frame_vision_2=Frame(self.frame_player_setting)

        self.button_height=20
        self.button_width=self.button_height

        self.UpPhoto=PhotoImage(file="open.png")
        self.DownPhoto=PhotoImage(file="close.png")

        self.player1vision= IntVar(None, 2)
        self.player2vision= IntVar(None, 2)
        self.player1vision_label=Label(self.frame_vision_1,textvariable=self.player1vision)
        self.player2vision_label=Label(self.frame_vision_2,textvariable=self.player2vision)

        self.player1vision_intro=Label(self.frame_vision_1,text="AI Vision")
        self.player2vision_intro=Label(self.frame_vision_2,text="AI Vision")

        self.p1_Vision_down=Button(self.frame_vision_1,image=self.DownPhoto,command=lambda: self.update_player_vision(1,-1),height = self.button_height, width = self.button_width)
        self.p1_Vision_up=Button(self.frame_vision_1,image=self.UpPhoto,command=lambda: self.update_player_vision(1,1),height = self.button_height, width = self.button_width)
        self.p2_Vision_down=Button(self.frame_vision_2,image=self.DownPhoto,command=lambda: self.update_player_vision(2,-1),height = self.button_height, width = self.button_width)
        self.p2_Vision_up=Button(self.frame_vision_2,image=self.UpPhoto,command=lambda: self.update_player_vision(2,1),height = self.button_height, width = self.button_width)

        self.player1vision_intro.grid(row=0,column=0,columnspan=3)
        self.p1_Vision_down.grid(row=1,column=0,sticky="W")
        self.player1vision_label.grid(row=1,column=1)
        self.p1_Vision_up.grid(row=1,column=2,sticky="E")

        self.player2vision_intro.grid(row=0,column=0,columnspan=3)
        self.p2_Vision_down.grid(row=1,column=0,sticky="E")
        self.player2vision_label.grid(row=1,column=1)
        self.p2_Vision_up.grid(row=1,column=2,sticky="W")

        self.dummylabel3=Label(self.frame_player_setting,text="      ")
        self.dummylabel3.grid(row=5,column=0,columnspan=2)

        self.frame_vision_1.grid(row=6,column=0)
        self.frame_vision_2.grid(row=6,column=1)

        self.dummylabel3=Label(self.frame_player_setting,text="      ")
        self.dummylabel3.grid(row=7,column=0,columnspan=2)

        self.frame_simulations_1=Frame(self.frame_player_setting)
        self.frame_simulations_2=Frame(self.frame_player_setting)

        self.player1sims_intro_frame=Frame(self.frame_simulations_1)
        self.player2sims_intro_frame=Frame(self.frame_simulations_2)

        self.player1sims=IntVar(None,1000)
        self.player1sims_intro=Label(self.frame_simulations_1,text="AI Simulations")
        self.player1sims_input=Entry(self.player1sims_intro_frame,textvariable=self.player1sims,justify='center')
        #self.player1sims_input.insert(0,1000)
        self.player1sims_intro.grid(row=0,column=0)
        self.player1sims_input.pack()

        self.player2sims=IntVar(None,1000)
        self.player2sims_intro=Label(self.frame_simulations_2,text="AI Simulations")
        self.player2sims_input=Entry(self.player2sims_intro_frame,textvariable=self.player2sims,justify='center')

        self.player2sims_intro.grid(row=0,column=0)
        self.player2sims_input.pack()

        self.player1sims_intro_frame.grid(row=1,column=0)
        self.player2sims_intro_frame.grid(row=1,column=0)

        self.frame_simulations_1.grid(row=4,column=0)
        self.frame_simulations_2.grid(row=4,column=1)

        self.p1_human=Radiobutton(self.frame_player_setting,text="Human",variable=self.p1human,value=1,command=lambda: self.toggle_view(1,0))
        self.p1_AI=Radiobutton(self.frame_player_setting,text="AI",variable=self.p1human,value=0,command=lambda: self.toggle_view(1,1))
        self.p1_AI.grid(sticky="W",row=2,column=0)
        self.p1_human.grid(sticky="W",row=3,column=0)
        self.p2_AI=Radiobutton(self.frame_player_setting,text="AI",variable=self.p2human,value=0,command=lambda: self.toggle_view(2,1))
        self.p2_human=Radiobutton(self.frame_player_setting,text="Human",variable=self.p2human,value=1,command=lambda: self.toggle_view(2,0))
        self.p2_AI.grid(sticky="W",row=2,column=1)
        self.p2_human.grid(sticky="W",row=3,column=1)
        self.frame_player_setting.pack()
        self.frame_player_setting.grid_columnconfigure(0, minsize=140)
        self.frame_player_setting.grid_columnconfigure(1, minsize=140)

        self.frame_sliders = Frame(self.frame_player_setting)
        self.frame_sliders.grid(row=8,columnspan=2)
        self.frame_sliders.grid_columnconfigure(0, minsize=140)
        self.frame_sliders.grid_columnconfigure(1, minsize=140)

        self.player1_frame_slider= Frame(self.frame_sliders)
        self.player2_frame_slider= Frame(self.frame_sliders)



        self.player1_frame_slider.grid(row=0,column=0,sticky="S")
        self.player2_frame_slider.grid(row=0,column=1,sticky="S")

        self.player1_LTO_label_intro=Label(self.player1_frame_slider, text="Long term orientation")
        self.player1_LTO = IntVar(None,90)
        self.player1_LTO_slider= Scale(self.player1_frame_slider, from_=0, to=100, orient=HORIZONTAL, variable=self.player1_LTO)

        #self.player1_LTO_slider.set(90

        self.player1_LTO_label_intro.grid(row=0,column=0,sticky="S")
        self.player1_LTO_slider.grid(row=1,column=0,sticky="N")

        self.player2_LTO_label_intro=Label(self.player2_frame_slider, text="Long term orientation")
        self.player2_LTO = IntVar(None,90)
        self.player2_LTO_slider= Scale(self.player2_frame_slider, from_=0, to=100, orient=HORIZONTAL, variable=self.player2_LTO)
        self.player2_LTO_slider.set(90)

        self.player2_LTO_label_intro.grid(row=0,column=0,sticky="S")
        self.player2_LTO_slider.grid(row=1,column=0,sticky="N")


        self.sliders_explanation = Message(self.frame_sliders,text="Lower long term orientation means less weight is put on outcomes further away in the future compared to ones closer to the player's current state.",width=300)
        self.sliders_explanation.grid(row=2,column=0,columnspan=2,sticky="NSEW")




        self.frame_end_buttons=Frame(master,width=500)
        self.frame_end_buttons.grid_columnconfigure(0, minsize=140)
        self.frame_end_buttons.grid_columnconfigure(1, minsize=140)
        self.dummylabel=Label(self.frame_end_buttons,text="     ")
        self.dummylabel.grid(row=0)
        self.validate_button=Button(self.frame_end_buttons,text="Validate",command=self.validate,height = 1, width = 10)
        self.play_button=Button(self.frame_end_buttons,text="Play",command=self.play,height = 1, width = 10)
        self.validate_button.grid(row=1,column=0,sticky="NSEW")
        self.play_button.grid(row=1,column=1,sticky="NSEW")
        self.frame_end_buttons.pack()


        """
        self.greet_button=Button(master, text="Greet", command=self.greet)
        self.greet_button.()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

        self.frame1=Frame()
        self.greet_button2=Button(self.frame1, text="Greet", command=self.greet)

        self.frame1.pack()
        """
        #self.close_button2=Button(self.frame1, text="Close", command=master.quit)


    def update_player_vision(self,player,action):

        if player==1:
            vision=self.player1vision
            lto=self.player1_frame_slider
        else:
            vision=self.player2vision
            lto=self.player2_frame_slider
        if vision.get()<5 and action==1:
            vision.set(vision.get()+action)
            if vision.get()>1:
                lto.grid(row=0,column=player-1)
        elif vision.get()>0 and action==-1:
            vision.set(vision.get()+action)
            if vision.get()<2:
                lto.grid_forget()


    def toggle_view(self,player,action):
        if player==1:
            frame_vision=self.frame_vision_1
            frame_sims=self.frame_simulations_1
            lto=self.player1_frame_slider
        else:
            frame_vision=self.frame_vision_2
            frame_sims=self.frame_simulations_2
            lto=self.player2_frame_slider
        if action==0:
            frame_sims.grid_forget()
            frame_vision.grid_forget()
            lto.grid_forget()
        else:
            frame_vision.grid(row=6,column=player-1)
            frame_sims.grid(row=4,column=player-1)
            lto.grid(row=0,column=player-1)

    def play(self):
        self.validate()
        if self.validated==True:
            self.initialised=True
            self.master.destroy()
        else:
            print("Get yo shit together son")

    def validate(self):
        warnings=""
        c=0

        numeric=True
        for x in self.rows_label_input.get()+self.cols_label_input.get()+self.connects_label_input.get()+self.player1sims_input.get()+self.player2sims_input.get():
            if x not in '0123456789':
                numeric=False

        if numeric==True:
            for input in [self.rows_label_input.get(),self.cols_label_input.get(),self.connects_label_input.get(),self.player1sims_input.get(),self.player2sims_input.get()]:
                try:
                    int(input)
                except ValueError:
                    c+=1
                    warnings+="%s. Please ensure all manual inputs are positive integers." % c
                    break
        else:
            c+=1
            warnings+="%s. Please ensure all manual inputs are valid positive integers." % c


        if int(self.rows_label_input.get())<1:
            c+=1
            warnings+="%s. You cannot have less than one row" % c
        elif int(self.rows_label_input.get())>10 and int(self.cols_label_input.get())+int(self.rows_label_input.get())>=15:
            c+=1
            warnings+="%s. Please reduce the number of rows in order to keep the game smooth. In general you should not have more than 10 rows unless your rows and columns add up to less than 15." % c

        if int(self.cols_label_input.get())<1:
            c+=1
            warnings+="%s. You cannot have less than one column" % c
        elif int(self.cols_label_input.get())>10 and int(self.cols_label_input.get())+int(self.rows_label_input.get())>=15:
            c+=1
            warnings+="%s. Please reduce the number of columns in order to keep the game smooth. In general you should not have more than 10 columns unless your rows and columns add up to less than 15." % c

        if int(self.cols_label_input.get())<3 or int(self.cols_label_input.get())>10:
            c+=1
            warnings+="%s. Please input between 3 and 10 connects as a winning condition." % c

        if max([int(self.cols_label_input.get()),int(self.rows_label_input.get())])<=int(self.connects_label_input.get()):
            pass

        if self.player1vision.get()>4 or self.player2vision.get()>4:
            c+=1
            warnings+="%s. Please be careful with inputting high Vision values - computation time increases exponentially with each increment of this parameter." % c


        if warnings=="":
            print("Everything looks good!")
            self.validated=True
        else:
            print(warnings)


class connectGUI:
    #Ensure the screen does not become excessively big for a large number of rows/columns
    max_dimension=400
    #Ensure a minimum size for the screen in case few rows/columns are passed
    max_square_edge=40
    edge_margin_ratio=0.1

    def __init__(self,rows,columns):
        self.rows=rows
        self.columns=columns
        self.width,self.height,self.edge=self.get_dimensions(rows,columns)
        self.margin=self.edge*self.edge_margin_ratio
        self.grid=[[0 for x in range(columns)] for y in range(rows)]
        self.size=self.width, self.height

    def get_dimensions(self,rows,columns):
        "Gets the shape of the output, the edge of the squares, and the margins"
        edge_margin_ratio=self.edge_margin_ratio
        max_val=max([rows,columns])
        min_val=min([rows,columns])
        if max_val>9:
            edge=int(self.max_dimension/(max_val+(max_val+1)*edge_margin_ratio)//2*2)
            bigdim=self.max_dimension
            lildim=edge*(min_val+edge_margin_ratio*(1+min_val))
        else:
            edge=self.max_square_edge
            bigdim=edge*(max_val+edge_margin_ratio*(1+max_val))
            lildim=edge*(min_val+edge_margin_ratio*(1+min_val))
        if rows>columns:
            width=lildim
            height=bigdim
        elif rows==columns:
            width=bigdim
            height=bigdim
        else:
            width=bigdim
            height=lildim
        return int(width), int(height), edge

    def get_disk_trajectory(self,row,column):
        end_coord=self.grid_space_rects[row][column]
        start_coord=copy.deepcopy(end_coord)
        start_coord[1]=0
        return start_coord,end_coord

    def initialise_game(self,game):
        pg.init()
        # Set the width and height of the screen [width, height]
        self.screen = pg.display.set_mode(self.size)
        pg.display.set_caption("Connect-"+str(game.connects))

        # Used to manage how fast the screen updates
        self.clock = pg.time.Clock()

        #Generate images_rects of objects:
        self.grid_space=[]
        self.grid_space_rects=[]
        self.highlights=[]
        for i in range(self.rows):
            self.grid_space.append([])
            self.grid_space_rects.append([])
            for j in range(self.columns):
                rect=pg.Rect(self.margin+j*(self.margin+self.edge),self.margin+i*(self.margin+self.edge),self.edge,self.edge)
                self.grid_space_rects[i].append(rect)
                image=pg.Surface(rect.size).convert()
                image.fill(WHITE)
                tagged=0
                self.grid_space[i].append([image,tagged])
        for i in range(self.columns):
            highlight_rect=pg.Rect(self.margin+i*(self.margin+self.edge)-self.margin/2,self.margin,self.edge+self.margin,self.height)
            highlight_image=pg.Surface(highlight_rect.size).convert()
            highlight_image.fill(YELLOW)
            self.highlights.append([highlight_image,highlight_rect])

        """
        # -------- Main Program Loop -----------
        disk_dropping=False
        updated_board=True
        p1_turn=True
        # Loop until the user clicks the close button.
        done = False
        while not done:
            # --- Main event loop
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if disk_dropping==False:
                        location=pg.mouse.get_pos()
                        column=int((location[0]-self.margin)//(self.margin+self.edge))
                        action_row=-1
                        for row in reversed(range(self.rows)):
                            if self.grid_space[row][column][1]==0:
                                action_row=row
                                end_coord=self.grid_space_rects[row][column]
                                break
                        if action_row>-1:
                            current_coord=copy.deepcopy(end_coord)
                            current_coord[1]=0
                            print(current_coord)
                            disk_dropping=True
                            updated_board=False
                            if p1_turn:
                                ball_color=RED
                            else:
                                ball_color=BLUE
            self.screen.fill(BLACK)
            #Background - highlight column is moused over
            for j in range(self.columns):
                if self.highlights[j][1].collidepoint(pg.mouse.get_pos()):
                    self.screen.blit(*self.highlights[j])
            for i in range(self.rows):
                for j in range(self.columns):
                    self.screen.blit(self.grid_space[i][j][0],self.grid_space_rects[i][j])
                    if self.grid_space[i][j][1]==1:
                        pg.draw.ellipse(self.screen,RED,self.grid_space_rects[i][j])
                    elif self.grid_space[i][j][1]==2:
                        pg.draw.ellipse(self.screen,BLUE,self.grid_space_rects[i][j])

            if disk_dropping==True:
                if current_coord[1]<end_coord[1]-8:
                    current_coord[1]+=8
                else:
                    disk_dropping=False
                pg.draw.ellipse(self.screen,ball_color,current_coord)
            elif updated_board==False:
                if p1_turn:
                    self.grid_space[action_row][column][1]=1
                else:
                    self.grid_space[action_row][column][1]=2
                updated_board=True
                p1_turn=not(p1_turn)


            pg.display.flip()

            self.clock.tick(60)
        pg.quit()
        """
"""
root=Tk()
my_gui=setup_window(root)
root.mainloop()
print("I'm donez :D")


GUI=connectGUI(7,6)
GUI.start_game()
"""
