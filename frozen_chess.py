

from kivy.uix.bubble import Bubble,BubbleButton
from kivy.uix.gridlayout import GridLayout

import copy
import os


from sounds import Music
from settings import Settings
from translater import Get_text
from connection import Connection
import global_constants
import core_game_logik

import frozen
import frozen_figure


class Game_logik(core_game_logik.CoreGameLogik):
    def copy_board(self, board):
        Field = core_game_logik.Field
        new_board = [[Field() for t in range(8)] for a in range(8)]
        for a in range(8):
            for b in range(8):
                new_board[a][b].figure = self.Figure('white',0,0,'')
                new_board[a][b].figure.color = copy.copy(board[a][b].figure.color)
                new_board[a][b].figure.type = copy.copy(board[a][b].figure.type)
                new_board[a][b].figure.do_hod_before = copy.copy(board[a][b].figure.do_hod_before)
                new_board[a][b].figure.x = board[a][b].figure.x
                new_board[a][b].figure.y = board[a][b].figure.y
                if board[a][b].figure.type == 'pawn':
                    new_board[a][b].figure.do_hod_now = board[a][b].figure.do_hod_now

        return new_board

    def find_fields(self, board,figure):
        list2 = super().find_fields(board, figure)
        if figure.type == 'king' and not figure.do_hod_before :
            list2 = self.can_do_rocking(self,board,figure,list2)
        return list2
    
    def build_game(self):
        super().build_game()
        self.Figure = frozen_figure.Figure
        frozen.init_chess(self)

    def move_figure(self,board,x,y,options=None):
        self.message = f'move {self.choose_figure.x} {self.choose_figure.y} {x} {y}'
        Music.move()
        if self.choose_figure.color == 'white':
            self.made_moves += 1

        if self.choose_figure.type == 'pawn':
            # taking on the pass
            if x != self.choose_figure.x:
                if board[x][y].figure.type == 'empty':
                    board[x][self.choose_figure.y].figure.destroy()

        if self.choose_figure.type == 'king' and not self.choose_figure.do_hod_before:
            board = self.do_rocking(board,x,y,self.choose_figure)
        else:
            a , b = self.choose_figure.x , self.choose_figure.y
            board[a][b].figure = self.Figure('',a,b,'empty')
            board[x][y].figure.destroy()
            board[x][y].figure = self.choose_figure
            board[x][y].figure.set_coords_on_board(x,y)
                
        if self.choose_figure.type == 'pawn' and abs(y-b) == 2:
            self.choose_figure.do_hod_now = True
        board[x][y].figure.do_hod_before = True

        if self.choose_figure.type == 'pawn' and board[x][y].figure.pawn_on_last_line():
            if global_constants.game.state_game != 'one' and self.color_do_hod_now != global_constants.game.play_by:
                n , m = self.choose_figure.x , self.choose_figure.y
                self.board[n][m].figure.transform_to(options[1])
                self.choose_figure = self.Figure('',0,0,'empty')
                options = options[2:]
                self.change_color(options)
                self.is_end_of_game(board)
                self.after_movement(board,options)
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
            self.after_movement(board,options)

        self.delete_tips()
        self.green_line.show_field(x=-1,y=-1)
        self.list_of_hod_field = []

        return board

    def do_transformation(self,color,x,y,options=None):
        d = os.sep
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
                Connection.messages += [self.message]
            self.message = ''
            self.change_color(options)
            self.is_end_of_game(self.board)
            # it is new line
            self.after_movement(self.board,options)
        
        # for buttons
        def change_q(click):
            complete('queen')
        def change_h(click):
            complete('horse')
        def change_b(click):
            complete('bishop')
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
            names = ['qw.png','bw.png','hw.png','rw.png']
        else:
            names = ['qb.png','bb.png','hb.png','rb.png']
        commands = [change_q,change_b,change_h,change_r]
        folder = Settings.get_folder() + 'pictures{0}fig_set1{0}'.format(d)
        for x in range(4):
            but = BubbleButton(
                text='',
                background_normal=folder + names[x],
                size=[Sizes.field_size]*2)
            but.bind(on_press=commands[x])
            box.add_widget(but)

        self.bub.add_widget(box)
        global_constants.Main_Window.add_widget(self.bub)

    def after_movement(self,board,options):
        if self.color_do_hod_now == 'black':
            return board
        if self.made_moves % global_constants.game.frozen_moves != 0:
            return board
        if not global_constants.game.ind:
            return board
        kings = [1,1]
        for line in board:
            for field in line:
                if field.figure.type not in ['frozen','empty']:
                    if is_isolated(field.figure,board):
                        if field.figure.type == 'king':
                            if field.figure.color == 'white':
                                kings[0] = 0
                            else:
                                kings[1] = 0
                        field.figure.freeze()
        for line in board:
            for field in line:
                if field.figure.type == 'empty' and is_deisolated(field.figure,board):
                    field.figure.freeze()

        if 0 in kings:
            global_constants.game.ind = False
        if kings == [0,0]:
            self.interfase.do_info(Get_text('game_both_frozen'))
        if kings == [1, 0]:
            self.interfase.do_info(Get_text('game_black_frozen'))
        if kings == [0, 1]:
            self.interfase.do_info(Get_text('game_white_frozen'))
        self.is_end_of_game(board)
        return board



def is_isolated(figure,board):
    x, y = figure.x, figure.y
    empty = ['empty', 'frozen']
    if x != 0:
        if board[x-1][y].figure.type not in empty:
            return False
        if y != 0 and board[x-1][y-1].figure.type not in empty:
            return False
        if y != 7 and board[x-1][y+1].figure.type not in empty:
            return False
    if y != 0:
        if board[x][y-1].figure.type not in empty:
            return False
    if y != 7:
        if board[x][y+1].figure.type not in empty:
            return False
    if x != 7:
        if board[x+1][y].figure.type not in empty:
            return False
        if y != 0 and board[x+1][y-1].figure.type not in empty:
            return False
        if y != 7 and board[x+1][y+1].figure.type not in empty:
            return False
    return True

def is_deisolated(figure,board):
    x, y = figure.x, figure.y
    empty = ['frozen', 'empty']
    if x != 0 and board[x-1][y].figure.type in empty:
        return True
    if x != 7 and board[x+1][y].figure.type in empty:
        return True
    if y != 0 and board[x][y-1].figure.type in empty:
        return True
    if y != 7 and board[x][y+1].figure.type in empty:
        return True
    return False






    
