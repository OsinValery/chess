
from kivy.graphics import Color, Line
from kivy.uix.bubble import Bubble, BubbleButton
from kivy.uix.gridlayout import GridLayout

from settings import Settings
import global_constants
import core_game_logik


# change it on new module of chess
import figure_alamos

import copy
import os


def create_start_game_board():
    Figure = figure_alamos.Figure
    board = [[Field() for t in range(6)] for a in range(6)]
    for x in range(6):
        for y in range(6):
            board[x][y].figure = Figure('',0,0,'empty')
            board[x][y].attacked = False

    
    figs = ['rook','horse','queen','king','horse','rook']
    for a in range(6):
        board[a][0].figure = Figure('white',a,0,figs[a])
        board[a][5].figure = Figure('black',a,5,figs[a])
        board[a][1].figure = Figure('white',a,1,'pawn')
        board[a][4].figure = Figure('black',a,4,'pawn')

    return board

class Field():
    def __init__(self):
        self.attacked = False
        self.figure = None
    def __str__(self):
        return str(self.figure)


class Green_line(Line):
    def __init__(self):
        super(Green_line,self).__init__()
        self.width = 3
        self.close = True
        self.drawed = False
    
    def get_canv(self,canvas):
        self.canvas = canvas
    
    def show_field(self,x,y):
        if self.drawed:
            self.canvas.remove(self)
            self.drawed = False
        if x != -1:
            Sizes = global_constants.Sizes
            pad_x = Sizes.x_top_board + Sizes.x_top
            pad_y = Sizes.y_top_board + Sizes.y_top
            pad = Sizes.field_size
            self.points=(
                pad_x + pad * x , pad_y + pad * y,
                pad_x + pad * (x+1) , pad_y + pad * y,
                pad_x + pad * (x+1) , pad_y + pad * (y+1),
                pad_x + pad * x , pad_y + pad * (y + 1)
                )
            with self.canvas:
                Color(0,1,0,1)
                self.canvas.add(self)
                self.drawed = True
                Color(1,1,1,1)


class Game_logik(core_game_logik.CoreGameLogik):
    def build_game(self):
        super().build_game()
        self.Figure = figure_alamos.Figure
        self.board = create_start_game_board()
    
    def copy_board(self, board):
        x = len(board)
        y = len(board[0])
        new_board = [[Field() for t in range(y)] for a in range(x)]
        for a in range(x):
            for b in range(y):
                new_board[a][b].figure = self.Figure('white',a,b,'')
                new_board[a][b].figure.color = copy.copy(board[a][b].figure.color)
                new_board[a][b].figure.type = copy.copy(board[a][b].figure.type)
        return new_board

    def fit_field(self, event):
        x,y = 0,0
        e_x,e_y = event.x,event.y
        s = global_constants.Sizes
        if e_x <= s.x_top + s.x_top_board or e_y <= s.y_top + s.y_top_board:
            return -1,-1
        elif (e_y >= s.y_top + s.y_top_board + s.field_size * 6) or \
            (e_x >= s.x_top + s.x_top_board + s.field_size * 6) :
            return -1,-1
        else:
            e_x -= (s.x_top + s.x_top_board)
            x = e_x // s.field_size
            e_y -= (s.y_top + s.y_top_board)
            y = e_y // s.field_size
            x = round(x)
            y = round(y)
            return x,y

    def init_game(self):
        Main_Window = global_constants.Main_Window
        self.create_interface(Main_Window, global_constants.Sizes)
        global_constants.current_figure_canvas = Main_Window.wid.canvas
        self.build_game()
        self.choose_figure = self.Figure('white', 0, 0, 'empty')        
        self.green_line = Green_line()
        self.green_line.get_canv(Main_Window.canvas)

    def do_transformation(self, color,x,y,options=None):

        def complete(ftype):
            x , y = self.choose_figure.x , self.choose_figure.y
            self.board[x][y].figure.transform_to(ftype)
            self.choose_figure = self.Figure('',0,0,'empty')
            global_constants.Main_Window.remove_widget(self.bub)
            del self.bub
            self.need_change_figure = False
            if global_constants.game.state_game != 'one':
                self.message += ' = ' + ftype
                self.message += f" {self.players_time['white']} {self.players_time['black']}"
                global_constants.Connection_manager.send(self.message)
            self.message = ''
            self.change_color(options)
            self.is_end_of_game(self.board)
        
        # for buttons
        def change_q(click):
            complete('queen')
        def change_h(click):
            complete('horse')
        def change_r(click):
            complete('rook')

        self.need_change_figure = True
        Sizes = global_constants.Sizes
        wid = ( x - 1 ) * Sizes.field_size + Sizes.x_top + Sizes.x_top_board
        height = ( y + 0.8 ) * Sizes.field_size + Sizes.y_top + Sizes.y_top_board

        self.bub = Bubble(
            pos = [wid,height],
            size=[3*Sizes.field_size]*2
        )
        box = GridLayout(rows=2,cols=2)
        box.padding = [Sizes.field_size*0.05]*4
        if color == 'white':
            names = ['qw.png','hw.png','rw.png']
        else:
            names = ['qb.png','hb.png','rb.png']
        commands = [change_q,change_h,change_r]
        d = os.path.sep
        folder = Settings.get_folder() + f'pictures{d}fig_set1{d}'
        for x in range(3):
            box.add_widget(BubbleButton(
                text='',
                background_normal=folder + names[x],
                size=[Sizes.field_size]*2,
                on_press=commands[x]
            ))

        self.bub.add_widget(box)
        global_constants.Main_Window.add_widget(self.bub)



