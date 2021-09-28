
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

import haos
import help_chess


class Game_logik(core_game_logik.CoreGameLogik):
    def build_game(self):
        super().build_game()
        self.Figure = help_chess.Figure
        haos.init_chess(self)

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

    def find_fields(self,board,figure):
        time_list = figure.first_list(board)
        list2 = []

        for element in time_list:
            if board[element[0]][element[1]].figure.type == 'king':
                continue
            board2 = []
            board2 = self.copy_board(board)
            for a in board2:
                for b in a:
                    b.attacked = False
                    
            #как будто был сделан туда ход, и нет ли шаха королю ходящего цвета
            board2[figure.x][figure.y].figure.type = 'empty'
            board2[figure.x][figure.y].figure.color = ''
            # взятие на проходе
            if figure.type == 'pawn':
                if board2[element[0]][element[1]].figure.type == 'empty':
                    if figure.x != element[0]:
                        board2[element[0]][figure.y].figure.type = 'empty'
                        board2[element[0]][figure.y].figure.color = ''
            board2[element[0]][element[1]].figure.type = copy.copy(figure.type)
            board2[element[0]][element[1]].figure.color = copy.copy(figure.color)
            
            for a in range(8):
                for b in range(8):
                    if board2[a][b].figure.type != 'empty':
                        if board2[a][b].figure.color != self.color_do_hod_now:
                            if board2[a][b].figure.type == board[a][b].figure.type:
                                board2 = board[a][b].figure.do_attack(board2)

            if not self.is_chax(board2,self.color_do_hod_now):
                list2.append(element)

        if figure.type == 'king' and not figure.do_hod_before :
            list2 = self.can_do_rocking(self,board,figure,list2)
        
        return list2

    def do_hod(self,x,y,board):
        if (self.choose_figure.type != 'empty') and (self.choose_figure is board[x][y].figure):
            self.choose_figure = self.Figure('',0,0,'empty')
            self.green_line.show_field(-1,y)
            self.list_of_hod_field = []
            if global_constants.game.make_tips:
                self.delete_tips()
        elif (board[x][y].figure.type != 'empty') and (board[x][y].figure.color != self.color_do_hod_now) \
            and not([x,y] in self.list_of_hod_field):
            if global_constants.game.make_tips:
                self.delete_tips()
                self.create_tips(x,y,board)
        elif board[x][y].figure.color == self.color_do_hod_now and board[x][y].figure.type != 'empty':
                self.choose_figure = board[x][y].figure
                self.list_of_hod_field = self.find_fields(board,self.choose_figure)
                self.green_line.show_field(x,y)
                if global_constants.game.make_tips:
                    self.delete_tips()
                    self.create_tips(x,y,board)
        elif self.choose_figure.type != 'empty' :
            if [x,y] in self.list_of_hod_field:
                if global_constants.game.state_game != 'one' and self.color_do_hod_now != global_constants.game.play_by:
                    return  board
                board = self.move_figure(board,x,y)
        return board

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
            board[a][b].figure = self.Figure('',0,0,'empty')
            board[x][y].figure.destroy()
            board[x][y].figure = self.choose_figure
            board[x][y].figure.set_coords_on_board(x,y)
                
        if self.choose_figure.type == 'pawn' and abs(y-b) == 2:
            self.choose_figure.do_hod_now = True
        board[x][y].figure.do_hod_before = True
        self.case = haos.magia_for_network_gen(board)

        if self.choose_figure.type == 'pawn' and board[x][y].figure.pawn_on_last_line():
            if global_constants.game.state_game != 'one' and self.color_do_hod_now != global_constants.game.play_by:
                n , m = self.choose_figure.x , self.choose_figure.y
                self.board[n][m].figure.transform_to(options[1])
                options = options[2:]
                self.change_color(options)
                self.is_end_of_game(board)
                self.after_movement(board,options)
            else:
                self.do_transformation(self.color_do_hod_now,x,y,options)
        else:
            if global_constants.game.state_game != 'one' and self.color_do_hod_now == global_constants.game.play_by:
                self.message += f" {self.players_time['white']} {self.players_time['black']}"
                self.message += f' {self.case}'
                Connection.messages += [self.message]
                self.message = ''
            self.change_color(options)
            self.is_end_of_game(board)
            self.after_movement(board,options)

        self.choose_figure = self.Figure('',0,0,'empty')
        self.delete_tips()
        self.green_line.show_field(x=-1,y=-1)
        self.list_of_hod_field = []

        return board

    def after_movement(self,board,options):
        # effects of magik chess there
        for a in range(8):
            for b in range(8):
                if board[a][b].figure.type == 'pawn':
                    if board[a][b].figure.color == self.color_do_hod_now:
                        board[a][b].figure.do_hod_now = False
        if not global_constants.game.ind:
            return board

        if global_constants.game.state_game == 'one':
            haos.magik(self.board)
        elif options != None:
            haos.magia_for_network_run(self.board, options[-1])
        else:
            haos.magia_for_network_run(self.board,self.case)
        
        for y in 0,7:
            for x in range(8):
                if board[x][y].figure.type == 'pawn' and board[x][y].figure.pawn_on_last_line():
                    board[x][y].figure.transform_to('queen')

        # check check and mate, it can be changed, when magia excist
        # 0 - check  1 - mate
        results = {'white':[False,False],'black':[False,False]}
        for color in results:
            board2 = self.copy_board(board)
            for x in range(8):
                for y in range(8):
                    if board2[x][y].figure.color != color:
                        board2 = board[x][y].figure.do_attack(board2)
            results[color][0] = self.is_chax(board2,color)
            if results[color][0]:
                results[color][1] = self.is_mate(board2,color)

        # solution
        Game = global_constants.game
        if results['black'][1] and results['white'][1]:
            Game.ind = False
            self.interfase.do_info(Get_text('game_both_mate'))
        elif results['white'][1]:
            Game.ind = False
            self.interfase.do_info(Get_text(f'game_white_mate'))
        elif results['black'][1]:
            Game.ind = False
            self.interfase.do_info(Get_text('game_black_mate'))
        elif results['black'][0] and results['white'][0]:
            self.interfase.do_info(Get_text('game_both_chax'))

        elif results['black'][0]:
            edd = ''
            if self.color_do_hod_now == 'white':
                edd = Get_text('game_magik_black_chax')
                self.change_color()
            self.interfase.do_info(Get_text('game_black_chax') + edd)

        elif results['white'][0]:
            edd = ''
            if self.color_do_hod_now == 'black':
                edd = Get_text('game_magik_white_chax')
                self.change_color()
            self.interfase.do_info(Get_text('game_white_chax')+edd)
        else:
            # nothing
            if self.color_do_hod_now == 'white':
                self.interfase.do_info(Get_text('game_white_move'))
            else:
                self.interfase.do_info(Get_text('game_black_move'))
            # it is possible that figure, that take chax, will be moved here, and
            # it is not chax, but in is_end_of_game it was detected
        return board

    def is_mate(self,board,color):
        for line in board:
            for field in line:
                if field.figure.color == color:
                    if self.have_move(board,field.figure):
                        return False
        return True
    
    def have_move(self,board,figure):
        first = figure.first_list(board)
        for element in first:
            board2 = self.copy_board(board)
            #как будто был сделан туда ход, и нет ли шаха королю ходящего цвета
            board2[figure.x][figure.y].figure.type = 'empty'
            board2[figure.x][figure.y].figure.color = ''
            # взятие на проходе
            if figure.type == 'pawn':
                if board2[element[0]][element[1]].figure.type == 'empty':
                    if figure.x != element[0]:
                        board2[element[0]][figure.y].figure.type = 'empty'
                        board2[element[0]][figure.y].figure.color = ''
            board2[element[0]][element[1]].figure.type = copy.copy(figure.type)
            board2[element[0]][element[1]].figure.color = copy.copy(figure.color)
            
            for a in range(8):
                for b in range(8):
                    if board2[a][b].figure.type != 'empty':
                        if board2[a][b].figure.color != figure.color:
                            if board2[a][b].figure.type == board[a][b].figure.type:
                                board2 = board[a][b].figure.do_attack(board2)

            if not self.is_chax(board2,figure.color):
                return True
        return False    

    def do_transformation(self,color,x,y,options=None):
        def complete(ftype):
            self.board[x][y].figure.transform_to(ftype)
            global_constants.Main_Window.remove_widget(self.bub)
            del self.bub
            self.need_change_figure = False
            if global_constants.game.state_game != 'one':
                self.message += ' = ' + ftype
                self.message += f" {self.players_time['white']} {self.players_time['black']}"
                self.message += f' {self.case}'
                Connection.messages += [self.message]
            self.message = ''
            self.change_color(options)
            self.is_end_of_game(self.board)
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
        box = GridLayout(rows=2,cols=2,padding = [Sizes.field_size*0.05]*4)
        names = [f'{l}{color[0]}.png' for l in ['q','b','h','r']]
        commands = [change_q,change_b,change_h,change_r]
        folder = os.path.join(Settings.get_folder(),'pictures','fig_set1')
        for n in range(4):
            but = BubbleButton(
                text='',
                background_normal=os.path.join(folder,names[n]),
                size=[Sizes.field_size]*2)
            but.bind(on_press=commands[n])
            box.add_widget(but)

        self.bub.add_widget(box)
        global_constants.Main_Window.add_widget(self.bub)

