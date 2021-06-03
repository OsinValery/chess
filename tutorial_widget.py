from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.graphics import Rectangle,Ellipse,Color

from settings import Settings
from translater import Get_text
import global_constants

import help_chess
import permutation_figure
import figure_alamos
import garner_figure
import circle_figure
import bizantion_figure
import glin_figure
import kuej_figure
import garner_figure
import horde_figure
import kamikadze_figure
import bad_figure
import schatranj_figure
import rasing_figure
Figure = None

import rasing
import math



class Field():
    def __init__(self,x,y,tip,color):
        global Figure
        self.attacked = False
        self.figure = Figure(color,x,y,tip)


class Tutorial_Widget(Widget):
    """ this class help tutorial, do interactive it"""
    def __init__(self,size,pos,game,figures=list(),options=[]):
        """ 
        game - type of chess
        figures - list, in format [type,color,x,y]
        """
        global Figure
        self.app_size = global_constants.Sizes 
        self.pos = pos
        self.size = size
        self.type_of_chess = game.type_of_chess
        self.figures = figures
        self.current = None
        self.options = options
        super(Tutorial_Widget,self).__init__()

        self.canvas.add(Rectangle(
            size = self.app_size.board_size,
            pos = [self.app_size.x_top_board,self.app_size.y_top_board],
            source = Settings.get_board_picture(game.type_of_chess)
        ))
        if game.type_of_chess in ['classic','fisher','horse_battle','magik','week','haotic']:
            help_chess.get_widget(self,self.app_size)
            Figure = help_chess.Figure   
            self.board = [ [Field(x,y,'empty','') for y in range(8)] for x in range(8)]
        
        # this code make funcions show standart material with features thoose type of chess
        # for example, board 8x8 -> 6x6 for los_alamos if user goes from tutorial los alamos to 
        # tutorial of classic chess
        elif self.type_of_chess == 'permutation':
            permutation_figure.get_widget(self,self.app_size)
            Figure = permutation_figure.Figure
            self.board = [ [Field(x,y,'empty','') for y in range(8)] for x in range(8)]
        
        elif self.type_of_chess == 'los_alamos':
            figure_alamos.get_widget(self,self.app_size)
            Figure = figure_alamos.Figure
            self.board = [ [Field(x,y,'empty','') for y in range(6)] for x in range(6)]
        
        elif self.type_of_chess == 'circle_chess':
            circle_figure.get_widget(self,self.app_size)
            Figure = circle_figure.Figure
            self.board = [[ Field(x,y,'empty','') for x in range(16) ] for y in range(4) ]
        
        elif self.type_of_chess == 'bizantion':
            bizantion_figure.get_widget(self,self.app_size)
            Figure = bizantion_figure.Figure
            self.board = [[ Field(x,y,'empty','') for x in range(16) ] for y in range(4) ]

        elif self.type_of_chess == 'glinskiy':
            glin_figure.get_widget(self,self.app_size)
            Figure = glin_figure.Figure
            self.board = [[ Field(a,t,'empty','') for t in range(11)] for a in range(11)]
        
        elif self.type_of_chess == 'kuej':
            kuej_figure.get_widget(self,self.app_size)
            Figure = kuej_figure.Figure
            self.board = [[ Field(a,t,'empty','') for t in range(11)] for a in range(11)]
        
        elif self.type_of_chess == 'garner':
            garner_figure.get_widget(self,self.app_size)
            Figure = garner_figure.Figure
            self.board = [[Field(t,a,'empty','') for t in range(5)] for a in range(5)]

        elif self.type_of_chess == 'horde':
            horde_figure.get_widget(self,self.app_size)
            Figure = horde_figure.Figure
            self.board = [ [Field(x,y,'empty','') for y in range(8)] for x in range(8)]
        
        elif self.type_of_chess == 'kamikadze':
            kamikadze_figure.get_widget(self,self.app_size)
            Figure = kamikadze_figure.Figure
            self.board = [ [Field(x,y,'empty','') for y in range(8)] for x in range(8)]
        
        elif self.type_of_chess == 'bad_chess':
            bad_figure.get_widget(self,self.app_size)
            Figure = bad_figure.Figure
            self.board = [ [Field(x,y,'empty','') for y in range(8)] for x in range(8)]
        
        elif self.type_of_chess == 'rasing':
            rasing_figure.get_widget(self,self.app_size)
            Figure = rasing_figure.Figure
            self.board = [ [Field(x,y,'empty','') for y in range(8)] for x in range(8)]
        
        elif self.type_of_chess == 'schatranj':
            schatranj_figure.get_widget(self,self.app_size)
            Figure = schatranj_figure.Figure
            self.board = [ [Field(x,y,'empty','') for y in range(8)] for x in range(8)]



        for fig in figures:
            x,y = fig[2:4]
            if self.type_of_chess in ['circle_chess','bizantion'] and fig[0] == 'pawn':
                direct = fig[-1]
                self.board[x][y].figure = Figure(fig[1],x,y,fig[0],direct)
            else :
                self.board[x][y].figure = Figure(fig[1],x,y,fig[0])

        self.add_widget(Label(
            text = Get_text('tutorial_move'),
            pos = [self.app_size.x_top_board,self.app_size.y_top_board - 0.1 * self.size[1]],
            size = [self.app_size.board_size[0],self.app_size.board_size[1]/10]
        ))

    def on_touch_down(self,click):
        global Figure
        super(Tutorial_Widget,self).on_touch_down(click)
        pos = [*click.pos]
        eight_fields = [
            'classic','fisher','horse_battle','magik',
            'permutation','horde','week','kamikadze',
            'bad_chess', 'rasing','haotic','schatranj'
            ]
        if self.type_of_chess in eight_fields:
            pos[0] -= (self.app_size.x_top_board + self.app_size.x_top)
            pos[1] -= (self.app_size.y_top_board + self.app_size.y_top)
            if pos[0] < 0 or pos[1] < 0:
                return
            f = self.app_size.field_size
            if pos[0] > f * 8 or pos[1] > f * 8:
                return
            coord = [int(pos[0] // f),int(pos[1] // f)]

        # it applyes changes, described in the last methood
        elif self.type_of_chess == 'los_alamos':
            pos[0] -= (self.app_size.x_top_board + self.app_size.x_top)
            pos[1] -= (self.app_size.y_top_board + self.app_size.y_top)
            if pos[0] < 0 or pos[1] < 0:
                return
            f = self.app_size.field_size
            if pos[0] > f * 6 or pos[1] > f * 6:
                return
            coord = [int(pos[0] // f),int(pos[1] // f)]

        elif self.type_of_chess in ['circle_chess','bizantion'] :
            coord = fit_field(click,self.app_size)
            if -1 in coord:
                return

        elif self.type_of_chess in ['glinskiy','kuej']:
            coord = fit_field_gekso(click,self.app_size)
            if -1 in coord:
                return
            
        elif self.type_of_chess == 'garner':
            pos[0] -= (self.app_size.x_top_board + self.app_size.x_top)
            pos[1] -= (self.app_size.y_top_board + self.app_size.y_top)
            if pos[0] < 0 or pos[1] < 0:
                return
            f = self.app_size.field_size
            if pos[0] > f * 5 or pos[1] > f * 5:
                return
            coord = [int(pos[0] // f),int(pos[1] // f)]

        x,y = coord
        if self.current == None:
            if self.board[x][y].figure.type != 'empty':
                self.current = self.board[x][y].figure
                may = self.current.first_list(self.board)
                if 'check' in self.options:
                    may = rasing.find_fields(self.board, self.current)
                # all squared boards
                squared = [
                    'classic','fisher','horse_battle','magik',
                    'permutation','los_alamos','garner','horde',
                    'week','kamikadze','bad_chess','rasing','haotic',
                    'schatranj'
                ]
                if self.type_of_chess in squared :
                    simple_tips(self.app_size,self.canvas,may)
                if self.type_of_chess in ['circle_chess','bizantion'] :
                    round_tips(self.app_size,self.canvas,may)
                if self.type_of_chess in ['kuej','glinskiy']:
                    gekso_tips(self.app_size,self.canvas,may)

        elif self.board[x][y].figure.type == 'empty' or self.current.color != self.board[x][y].figure.color:
            may = self.current.first_list(self.board)
            if 'check' in self.options:
                may = rasing.find_fields(self.board, self.current)
            if [x,y] in may:
                self.canvas.clear()
                self.canvas.add(Rectangle(
                    size = self.app_size.board_size,
                    pos = [self.app_size.x_top_board,self.app_size.y_top_board],
                    source = Settings.get_board_picture(self.type_of_chess)
                ))
                for line in self.board:
                    for field in line:
                        if field.figure.type != 'empty':
                            self.canvas.add(field.figure.rect)
                a,b = self.current.x, self.current.y
                self.current = None

                self.board[a][b].figure.set_coords_on_board(x,y)
                self.board[x][y].figure = self.board[a][b].figure
                self.board[a][b].figure = Figure('',a,b,'empty')
            
                if self.type_of_chess == 'permutation' and 'rotate' in self.options:
                    self.board[x][y].figure.swap()

    def __del__(self):
        del self.board
        self.canvas.clear()
        self.clear_widgets()



# it is for circle chesses
def fit_field(event,size):
    x,y = 0,0
    e_x,e_y = event.x,event.y
    s = size
    r = (e_x - s.center[0])**2 + (e_y - s.center[1])**2
    if r < s.r_min**2:
        return -1,-1
    elif r > s.r_max**2 :
        return -1,-1
    else:
        e_x -= s.center[0]
        e_y -= s.center[1]
        r **=.5
        a = abs(math.asin(e_y/r))
        if e_y >= 0 and e_x >= 0 :
            ch = 1
        if e_x >= 0 and e_y <= 0 :
            ch = 4
        if e_x <= 0 and e_y >= 0 :
            ch = 2
        if e_y <= 0 and e_x <= 0 :
            ch = 3
        egle = math.degrees(a)
        if ch == 1:
            pass
        elif ch == 2:
            egle = 180 - egle
        elif ch == 3:
            egle += 180
        else:
            egle = 360 - egle
        while egle > 22.5:
            y += 1
            egle -= 22.5

        r -= s.r_min
        while r > s.r:
            x+=1
            r -= s.r
        return x,y

def in_gekso(x,y,Zx,Zy,size):
    if y < Zy or y > Zy + size.field_h:
        return False
    if x < Zx - .5 * size.field_len:
        return False
    if x > Zx + 1.5 * size.field_len:
        return False
    x -= (Zx - .5 * size.field_len)
    y -= Zy
    if x > size.field_len :
        x = size.field_len * 2 - x
    if y > size.field_h // 2:
        y = size.field_h - y
    if x >= size.field_len:
        return True
    dx = .5 * size.field_len - x
    return y > dx * 3**.5

def fit_field_gekso(event,size):
    e_x,e_y = event.x,event.y
    s = size
    if e_x <= s.x_top_board or e_y <= s.y_top_board:
        return -1,-1
    elif (e_y >= s.y_top_board + s.board_size[0]) or (e_x >= s.x_top_board + s.board_size[0] ) :
        return -1,-1
    else:
        for i in range(11):
            for j in range(11+abs(5-i)):
                Zx = s.x_top_board + .5 * (s.board_size[0] - s.field_len)
                Zy = s.y_top_board + 0.5 * s.field_h * abs(5-i) + j * s.field_h
                Zx += (i-5) * 1.5 * s.field_len
                if in_gekso(e_x,e_y,Zx,Zy,size):
                    return i,j
        return -1,-1



def simple_tips(size,canvas,where): 
    "create tips on rectangle board"
    with canvas:
        Color(0,1,0,1)
        for x,y in where:
            canvas.add(Ellipse(
                size = [11,11],
                pos = [(x + .5) * size.field_size + size.x_top + size.x_top_board - 5,
                            size.field_size * (y + .5) + size.y_top + size.y_top_board - 5]
            ))
    with canvas:
        Color(0,0,0,0)

def round_tips(size,canvas,where):
    with canvas:
        Color(0,1,0,1)
    tip_r = size.r // 3
    for el in where:
        x , y = el[0] , el[1]
        agle = y * 22.5 + 11.25
        r = size.r_min + size.r * x + size.r * .5
        bx = math.cos(math.radians(agle))*r - 2 + size.center[0]
        by = math.sin(math.radians(agle))*r - 2 + size.center[1]
        r = tip_r
        canvas.add(Ellipse(
            pos=[bx - r/2 ,by -r/2 ],
            size=(r,r)     
        ))

    with canvas:
        Color(1,1,1,0,mode='rgba')

def gekso_tips(size,canvas,where):
    field = size.field_len
    r = field // 3
    with canvas:
        Color(0,1,0,1)

    for el in where:
        x , y = el[0] , el[1]
        pos_x = size.x_top_board + (x * 1.5 + 1) * field - r/2 
        pos_y = size.y_top_board + (y+0.5) * size.field_h + abs(5-x) * .5 * size.field_h -r/2
        canvas.add(Ellipse(
            pos=[pos_x,pos_y],
            size=(r,r)     
        ))

    with canvas:
        Color(1,1,1,0,mode='rgba')




