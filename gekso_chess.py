from kivy.graphics import Color, Line, Ellipse
import copy

from sounds import Music
from translater import Get_text
from connection import Connection
import global_constants
import core_game_logik

# import types of chess
import gen_glinskiy
import gen_kuej

import glin_figure 
import kuej_figure


class Game_logik(core_game_logik.CoreGameLogik):
    def build_game(self):
        super().build_game()
        Game = global_constants.game
        if Game.type_of_chess == 'kuej':
            self.Figure = kuej_figure.Figure
            gen_kuej.init_chess(self)
        else:
            self.Figure = glin_figure.Figure
            gen_glinskiy.init_chess(self)
        
    def init_game(self):
        Main_Window = global_constants.Main_Window
        self.create_interface(Main_Window, global_constants.Sizes)
        global_constants.current_figure_canvas = Main_Window.wid.canvas
        self.build_game()
        self.choose_figure = self.Figure('white', 0, 0, 'empty')        
        self.green_line = Green_line()
        self.green_line.get_canv(Main_Window.canvas)

    def copy_board(self, board):
        Field = core_game_logik.Field
        x = len(board)
        y = len(board[0])
        new_board = [[Field() for t in range(y)] for a in range(x)]
        for a in range(x):
            for b in range(y):
                new_board[a][b].figure = self.Figure('white',0,0,'')
                new_board[a][b].figure.color = copy.copy(board[a][b].figure.color)
                new_board[a][b].figure.type = copy.copy(board[a][b].figure.type)

        return new_board

    def fit_field(self, event):
        e_x,e_y = event.x,event.y
        s = global_constants.Sizes
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
                    if in_gekso(e_x,e_y,Zx,Zy):
                        return i,j
            return -1,-1

    def is_end_of_game(self, board):
        is_mate = False
        board2 = self.copy_board(board)
        for x in range(len(board)):
            for y in range(len(board[0])):
                if board2[x][y].figure.color != self.color_do_hod_now:
                    board2 = board[x][y].figure.do_attack(board2)
        if self.color_do_hod_now == 'white':
            if self.is_chax(board2,'white'):
                if not self.able_to_do_hod(board,'white'):
                    is_mate = True
                    self.interfase.do_info(Get_text('game_white_mate'))
                else:
                    self.interfase.do_info(Get_text('game_white_chax'))
        else:
            if self.is_chax(board2,'black'):
                if not self.able_to_do_hod(board,'black'):
                    self.interfase.do_info(Get_text('game_black_mate'))
                    is_mate = True
                else:
                    self.interfase.do_info(Get_text('game_black_chax') )   
        if not is_mate:
            if not self.able_to_do_hod(board,self.color_do_hod_now):
                self.interfase.do_info(Get_text(description='game_pat',
                        params=self.color_do_hod_now if global_constants.game.type_of_chess == 'glinskiy' else None))
                is_mate = True
        if is_mate :
            global_constants.game.ind = False
        if not global_constants.game.ind:
            if global_constants.game.with_time:
                self.time.cancel()
        if global_constants.game.ind :
            if self.color_do_hod_now == 'white' and self.want_draw['black']:
                self.draw()
            elif  self.color_do_hod_now == 'black' and self.want_draw['white']:
                self.draw()
        del board2

    def find_fields(self, board,figure):
        time_list = figure.first_list(board)
        list2 = []
        if figure.type == 'pawn':
            if global_constants.game.type_of_chess == 'glinskiy':
                time_list += taking_on_pass_glinskiy(board,figure)
            else:
                time_list += taking_on_pass_kuej(board,figure)
        for element in time_list:
            board2 = self.copy_board(board)
            for a in board2:
                for b in a:
                    b.attacked = False      
            #как будто был сделан туда ход, и нет ли шаха королю ходящего цвета
            board2[figure.x][figure.y].figure.type = 'empty'
            board2[figure.x][figure.y].figure.color = ''
            board2[element[0]][element[1]].figure.type = copy.copy(figure.type)
            board2[element[0]][element[1]].figure.color = copy.copy(figure.color)
            
            for a in range(len(board)):
                for b in range(len(board[0])):
                    if board2[a][b].figure.type != 'empty':
                        if board2[a][b].figure.color != self.color_do_hod_now:
                            if board2[a][b].figure.type == board[a][b].figure.type:
                                board2 = board[a][b].figure.do_attack(board2)

            if not self.is_chax(board2,self.color_do_hod_now):
                list2.append(element)
        return list2

    def move_figure(self,board,x,y,options=None):
        self.message = f'move {self.choose_figure.x} {self.choose_figure.y} {x} {y}'
        Music.move()
        if self.choose_figure.color == 'white':
            self.made_moves += 1

        if self.choose_figure.type == 'pawn':
            a = -1
            if self.choose_figure.color == 'black':
                a = 1
            if x != self.choose_figure.x:
                if board[x][y].figure.type == 'empty':
                    board[x][y+a].figure.destroy()

        a , b = self.choose_figure.x , self.choose_figure.y
        board[a][b].figure = self.Figure('',0,0,'empty')
        board[x][y].figure.destroy()
        board[x][y].figure = self.choose_figure
        board[x][y].figure.set_coords_on_board(x,y)

        if self.choose_figure.type == 'pawn' and abs(y-b) == 2:
            self.choose_figure.do_hod_now = True

        if self.choose_figure.type == 'pawn' and board[x][y].figure.pawn_on_last_line():
            if global_constants.game.state_game != 'one' and self.color_do_hod_now != global_constants.game.play_by:
                n , m = self.choose_figure.x , self.choose_figure.y
                self.board[n][m].figure.transform_to(options[1])
                self.choose_figure = self.Figure('',0,0,'empty')
                options = options[2:]
                self.change_color(options)
                self.is_end_of_game(board)
            else:
                self.do_transformation(self.color_do_hod_now,x,y,options)
        else:
            if global_constants.game.state_game != 'one' and self.color_do_hod_now == global_constants.game.play_by:
                self.message += f" {self.players_time['white']} {self.players_time['black']}"
                Connection.messages += [self.message]
                self.message = ''
            self.choose_figure = self.Figure('',0,0,'empty')
            self.change_color(options)
            self.is_end_of_game(board)

        self.delete_tips()
        self.green_line.show_field(x=-1,y=-1)
        self.list_of_hod_field = []    
        for a in range(len(board)):
            for b in range(len(board[0])):
                if board[a][b].figure.type == 'pawn':
                    if board[a][b].figure.color == self.color_do_hod_now:
                        board[a][b].figure.do_hod_now = False
        return board

    def create_tips(self,a,b,board):
        list1 = self.find_fields(board,board[a][b].figure)
        Sizes = global_constants.Sizes
        field = Sizes.field_len
        r = field // 6
        color = [0, 1, 0, .8 ]
        if self.color_do_hod_now != board[a][b].figure.color:
            color = [1, 0, 0, .8 ]
        if global_constants.game.state_game != 'one' and self.color_do_hod_now != global_constants.game.play_by:
            color = [1,0,0,.8]
        with global_constants.Main_Window.wid.canvas:
            Color(*color,mode='rgba')
        self.tips_drawed = True if len(list1) != 0 else False

        for el in list1:
            x , y = el[0] , el[1]
            pos_x = Sizes.x_top_board + (x * 1.5 + 1) * field - r/2 
            pos_y = Sizes.y_top_board + (y+0.5) * Sizes.field_h + abs(5-x) * .5 * Sizes.field_h -r/2
            global_constants.Main_Window.wid.canvas.add(Ellipse(
                        pos=[pos_x,pos_y],
                        size=(r,r)     ))

        with global_constants.Main_Window.wid.canvas:
            Color(1,1,1,1,mode='rgba')



class Green_line(Line):
    def __init__(self):
        super(Green_line,self).__init__()
        self.width = 3
        self.close = True
        self.drawed = False
        self.color = [0,1,0,1]
    
    def get_canv(self,canvas):
        self.canvas = canvas
    
    def get_circle(self,y):
        mas = []
        d = 3 - 2 * y
        x = 0
        # Brasenhem's algorithm
        while(x <= y) :
            mas.append([x,y])
            if d < 0 :
                d+= 4 * x + 6
            else : 
                d += 4 * (x - y) + 10
                y -= 1
            x += 1
        mas2 = mas[::-1]
        for el in mas2:
            mas.append( [ el[1] , el[0] ] )
        mas2 = mas[::-1]
        for el in mas2:
            mas.append( [ el[0] , -el[1] ] )
        mas2 = mas[::-1]
        for el in mas2:
            mas.append( [ -el[0] , el[1] ] )
        return mas

    def show_field(self,x,y):
        Sizes = global_constants.Sizes
        if self.drawed:
            self.canvas.remove(self)
            self.drawed = False
        if x != -1: 
            size = Sizes.field_h / 2           
            bx = Sizes.x_top_board + .5 * Sizes.board_size[0] \
                    + (x-5) * 1.5 * Sizes.field_len 
            by = Sizes.y_top_board + (abs(5-x) + 1) * .5 * Sizes.field_h + \
                y * Sizes.field_h
            circle = self.get_circle(size)
            self.points = []
            for [x,y] in circle:
                self.points.append(x + bx)
                self.points.append(y+by)
            with self.canvas:
                Color(*self.color)
                self.canvas.add(self)
                self.drawed = True
                Color(1,1,1,1)


def taking_on_pass_glinskiy(board,figure):
    list_ = []
    x = figure.x
    y = figure.y
    if figure.color == 'white':
        d = 0
        if x > 4:
            d = 1
        if x != 10 and y == 4 + d :
            if board[x+1][4].figure.type == 'pawn':
                if board[x+1][4].figure.color != figure.color:
                    if board[x+1][4].figure.do_hod_now:
                        list_.append([x+1,5])
        d = 0
        if x < 6:
            d = 1
        if x != 0 and y == 4 + d :
            if board[x-1][4].figure.type == 'pawn':
                if board[x-1][4].figure.color != 'white':
                    if board[x-1][4].figure.do_hod_now:
                        list_.append([x-1,5])
    else:
        d = x+1
        if x >= 5:
            d = 5 - abs(5-x)
        if x != 10 and y == d  :
            if board[x+1][6 - abs(4 - x)].figure.type == 'pawn' :
                if board[x+1][6-abs(4-x)].figure.color != figure.color:
                    if board[x+1][6-abs(4-x)].figure.do_hod_now:
                        list_.append([x+1,5-abs(4-x)])
        d = x
        if x > 5:
            d = 11 - x
        if x != 0 and y == d:
            if board[x-1][6-abs(5-(x-1))].figure.type == 'pawn':
                if board[x-1][6-abs(6-x)].figure.color != figure.color:
                    if board[x-1][6-abs(6-x)].figure.do_hod_now:
                        list_.append([x-1,6-abs(6-x)])
    return list_

def taking_on_pass_kuej(board,figure):
    list_ = []
    x = figure.x
    y = figure.y
    if figure.color == 'white':
        d = 0
        if x > 4:
            d = 1
        if x != 10 and y == 4 + d :
            if board[x+1][5].figure.type == 'pawn':
                if board[x+1][5].figure.color != figure.color:
                    if board[x+1][5].figure.do_hod_now:
                        list_.append([x+1,6])
        d = 0
        if x < 6:
            d = 1
        if x != 0 and y == 4 + d :
            if board[x-1][5].figure.type == 'pawn':
                if board[x-1][5].figure.color != 'white':
                    if board[x-1][5].figure.do_hod_now:
                        list_.append([x-1,6])
    else:
        d = x + 1
        if x >= 5:
            d = 5 - abs(5-x)
        if x != 10 and y == d  :
            if board[x+1][5 - abs(4 - x)].figure.type == 'pawn' :
                if board[x+1][5-abs(4-x)].figure.color != figure.color:
                    if board[x+1][5-abs(4-x)].figure.do_hod_now:
                        list_.append([x+1,4-abs(4-x)])
        d = x 
        if x > 5:
            d = 11 - x
        if x != 0 and y == d:
            if board[x-1][5-abs(5-(x-1))].figure.type == 'pawn':
                if board[x-1][5-abs(6-x)].figure.color != figure.color:
                    if board[x-1][5-abs(6-x)].figure.do_hod_now:
                        list_.append([x-1,5-abs(6-x)])
    return list_

def in_gekso(x,y,Zx,Zy):
    # Z (point) - it is the left bottom angle of 6-angle
    # 6-angle - field, that I check
    Sizes = global_constants.Sizes
    if y < Zy or y > Zy + Sizes.field_h:
        return False
    if x < Zx - .5 * Sizes.field_len:
        return False
    if x > Zx + 1.5 * Sizes.field_len:
        return False
    x -= (Zx - .5 * Sizes.field_len)
    y -= Zy
    if x > Sizes.field_len :
        x = Sizes.field_len * 2 - x
    if y > Sizes.field_h // 2:
        y = Sizes.field_h - y
    if x >= Sizes.field_len:
        return True
    dx = .5 * Sizes.field_len - x
    return y > dx * 3**.5
