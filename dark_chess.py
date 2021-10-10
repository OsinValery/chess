
from kivy.graphics import Rectangle,Ellipse,Color
from kivy.uix.bubble import Bubble,BubbleButton
from kivy.uix.gridlayout import GridLayout

import os

from sounds import Music
from settings import Settings
from translater import Get_text
import global_constants
import core_game_logik

import classic
import dark_figure


class Game_logik(core_game_logik.CoreGameLogik):
    def build_game(self):
        super().build_game()
        self.Figure = dark_figure.Figure
        classic.init_chess(self)

    def init_game(self):
        super().init_game()
        global_constants.Main_Window.wid.canvas.clear()
        self.draw_board()
    
    def delete_tips(self):
        if self.tips_drawed :
            global_constants.Main_Window.wid.canvas.clear()
            self.draw_board()

    def create_tips(self,a,b,board):
        Game = global_constants.game
        Sizes = global_constants.Sizes
        if Game.state_game == 'one' and self.color_do_hod_now != board[a][b].figure.color:
            return
        if Game.state_game != 'one' and board[a][b].figure.color != Game.play_by:
            return
        list1 = self.find_fields(board,board[a][b].figure)
        top_x= Sizes.x_top + Sizes.x_top_board
        top_y = Sizes.y_top + Sizes.y_top_board
        field = Sizes.field_size
        color = [0,1,0,.8 ]
        r = Sizes.field_size // 6
        with global_constants.Main_Window.wid.canvas:
            Color(*color,mode='rgba')
        self.tips_drawed = True

        for el in list1:
            x, y = el
            global_constants.Main_Window.wid.canvas.add(Ellipse(
                pos=[top_x - r/2 +(x+0.5)*field,top_y -r/2 +(y+0.5)*field],
                size=[r,r]
            ))
        with global_constants.Main_Window.wid.canvas:
            Color(1,1,1,1,mode='rgba')

    def find_fields(self,board,figure):
        list2 = figure.first_list(board)
        if figure.type == 'king' and not figure.do_hod_before :
            c = figure.y
            #короткая рокировка
            if board[6][c].figure.type == 'empty' and board[5][c].figure.type == 'empty':
                if board[7][c].figure.type == 'rook' and not board[7][c].figure.do_hod_before:
                    list2.append([6,c])
            #длинная
            if board[1][c].figure.type == 'empty' and board[2][c].figure.type == 'empty':
                if board[3][c].figure.type == 'empty':
                    if board[0][c].figure.type == 'rook' and not board[0][c].figure.do_hod_before:
                        list2.append([2,c])
        return list2

    def is_end_of_game(self, board):
        have = False
        for line in board:
            for field in line:
                fig = field.figure
                if fig.type == 'king' and fig.color == self.color_do_hod_now:
                    have = True
                    break

        if not have :
            global_constants.game.ind = False
            if global_constants.game.with_time:
                self.time.cancel()
            self.interfase.info.text = Get_text(f'game_{self.color_do_hod_now}_lose')
        if global_constants.game.ind :
            if self.color_do_hod_now == 'white' and self.want_draw['black']:
                self.draw()
            elif  self.color_do_hod_now == 'black' and self.want_draw['white']:
                self.draw()

    def move_figure(self,board,x,y,options=None):
        self.message = f'move {self.choose_figure.x} {self.choose_figure.y} {x} {y}'
        Music.move()
        if self.choose_figure.color == 'white':
            self.made_moves += 1

        if self.choose_figure.type == 'pawn':
            if x != self.choose_figure.x:
                if board[x][y].figure.type == 'empty':
                    board[x][self.choose_figure.y].figure.destroy()


        if self.choose_figure.type == 'king' and not self.choose_figure.do_hod_before:
            board = self.do_rocking(board,x,y,self.choose_figure)
        else:
            a , b = self.choose_figure.x , self.choose_figure.y
            board[a][b].figure = self.Figure('',0,0,'empty')
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
                if global_constants.game.ind:
                    global_constants.Main_Window.wid.canvas.clear()
                    self.draw_board()
                else:
                    self.draw_full_board()
            else:
                self.do_transformation(self.color_do_hod_now,x,y,options)
        else:
            if global_constants.game.state_game != 'one' and self.color_do_hod_now == global_constants.game.play_by:
                self.message += f" {self.players_time['white']} {self.players_time['black']}"
                global_constants.Connection_manager.send(self.message)
                self.message = ''
            self.choose_figure = self.Figure('',0,0,'empty')
            self.change_color(options)
            self.is_end_of_game(board)       
            if global_constants.game.ind:
                global_constants.Main_Window.wid.canvas.clear()
                self.draw_board()
            else:
                self.draw_full_board()
        
        self.delete_tips()
        self.green_line.show_field(x=-1,y=-1)
        for a in range(8):
            for b in range(8):
                if board[a][b].figure.type == 'pawn':
                    if board[a][b].figure.color == self.color_do_hod_now:
                        board[a][b].figure.do_hod_now = False
        self.list_of_hod_field = []
        return board

    def do_transformation(self,color,x,y,options=None):
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
            if global_constants.game.ind:
                global_constants.Main_Window.wid.canvas.clear()
                self.draw_board()
            else:
                self.draw_full_board()
        
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
        box = GridLayout(
            rows=2,
            cols=2,
            padding = [Sizes.field_size*0.05]*4
        )
        if color == 'white':
            names = ['qw.png','bw.png','hw.png','rw.png']
        else:
            names = ['qb.png','bb.png','hb.png','rb.png']
        commands = [change_q,change_b,change_h,change_r]
        d = os.path.sep
        folder = Settings.get_folder() + f'pictures{d}fig_set1{d}'
        for x in range(4):
            box.add_widget(BubbleButton(
                text='',
                background_normal=folder + names[x],
                size=[Sizes.field_size]*2,
                on_press = commands[x]
            ))

        self.bub.add_widget(box)
        global_constants.Main_Window.add_widget(self.bub)

    def draw_full_board(self):
        global_constants.Main_Window.wid.canvas.clear()
        Sizes = global_constants.Sizes
        rect = Rectangle(
            source=Settings.get_board_picture(global_constants.game.type_of_chess),
            pos=[Sizes.x_top_board,Sizes.y_top_board],
            size=Sizes.board_size)
        global_constants.Main_Window.wid.canvas.add(rect)
        for line in self.board:
            for field in line:
                if field.figure.type != 'empty':
                    global_constants.Main_Window.wid.canvas.add(field.figure.rect)

    def draw_board(self):
        if not global_constants.game.ind:
            self.draw_full_board()
            return
        Sizes = global_constants.Sizes
        global_constants.Main_Window.wid.canvas.add(Rectangle(
            source=Settings.get_board_picture(global_constants.game.type_of_chess),
            pos=[Sizes.x_top_board,Sizes.y_top_board],
            size=Sizes.board_size
        ))
        self.tips_drawed = False
        draw_color = self.color_do_hod_now 
        if global_constants.game.state_game != 'one':
            draw_color = global_constants.game.play_by

        for line in self.board:
            for field in line:
                field.attacked = False
        for line in self.board:
            for field in line:
                if field.figure.type !='empty'and field.figure.color == draw_color:
                    field.figure.do_attack(self.board)
        for x in range(8):
            for y in range(8):
                fig = self.board[x][y].figure
                if fig.type != 'empty' and (fig.color == draw_color or self.board[x][y].attacked):
                    global_constants.Main_Window.wid.canvas.add(self.board[x][y].figure.rect)
                elif fig.type == 'empty' and self.board[x][y].attacked:
                    pass
                else:
                    # draw darkness
                    size = Sizes
                    pos_x = x * size.field_size + size.x_top + size.x_top_board
                    pos_y = y * size.field_size + size.y_top + size.y_top_board
                    with global_constants.Main_Window.wid.canvas:
                        Color(0,0,0)
                        Rectangle(
                            pos = [pos_x,pos_y],
                            size = [size.field_size]*2
                        )
                        Color(1,1,1,1)
        if self.choose_figure.type != 'empty':
            x,y = self.choose_figure.x, self.choose_figure.y
            self.green_line.show_field(x,y)
