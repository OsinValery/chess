import copy

from sounds import Music
from translater import Get_text
from connection import Connection
import global_constants
import core_game_logik

import rasing_figure 


def get_start_position():
    Field = core_game_logik.Field
    Figure = global_constants.game.Game_logik.Figure
    board = [[Field() for t in range(8)] for a in range(8)]
    for x in range(8):
        for y in range(8):
            board[x][y].figure = Figure('',0,0,'empty')
            board[x][y].attacked = False

    figs1 = ['king','rook','bishop','horse']
    figs2 = ['queen'] + figs1[1:]
    for a in range(4):
        board[a][1].figure = Figure('black',a,1,figs1[a])
        board[7-a][1].figure = Figure('white',7-a,1,figs1[a])
        board[a][0].figure = Figure('black',a,0,figs2[a])
        board[7-a][0].figure = Figure('white',7-a,0,figs2[a])
    return board


class Game_logik(core_game_logik.CoreGameLogik):
    def build_game(self):
        super().build_game()
        self.Figure = rasing_figure.Figure
        self.board = get_start_position()

    def copy_board(self, board):
        Field = core_game_logik.Field
        new_board = [[Field() for t in range(8)] for a in range(8)]
        for a in range(8):
            for b in range(8):
                new_board[a][b].figure = self.Figure('white',a,b,'')
                new_board[a][b].figure.color = copy.copy(board[a][b].figure.color)
                new_board[a][b].figure.type = copy.copy(board[a][b].figure.type)
                new_board[a][b].figure.x = a
                new_board[a][b].figure.y = b
        return new_board

    def find_fields(self,board,figure):
        time_list = figure.first_list(board)
        list2 = []

        for element in time_list:
            board2 = self.copy_board(board)
            #как будто был сделан туда ход, и нет ли шаха королю ходящего цвета
            board2[figure.x][figure.y].figure.type = 'empty'
            board2[figure.x][figure.y].figure.color = ''
            board2[element[0]][element[1]].figure.type = copy.copy(figure.type)
            board2[element[0]][element[1]].figure.color = copy.copy(figure.color)
            # check that both dont give check
            for a in range(8):
                for b in range(8):
                    if board2[a][b].figure.type != 'empty':
                        if board2[a][b].figure.color == 'white':
                            board2 = board2[a][b].figure.do_attack(board2)
            if self.is_chax(board2,'black'):
                continue
            for a in range(8):
                for b in range(8):
                    board2[a][b].attacked = False
            for a in range(8):
                for b in range(8):
                    if board2[a][b].figure.type != 'empty':
                        if board2[a][b].figure.color == 'black':
                            board2 = board2[a][b].figure.do_attack(board2)
            if not self.is_chax(board2,'white'):
                list2.append(element)
        return list2
 
    def is_end_of_game(self, board):
        is_end = False
        if self.color_do_hod_now == 'white':
            # is kings on last line ?
            kings = []
            for x in range(8):
                if board[x][7].figure.type == 'king':
                    kings.append(board[x][7].figure.color)
            if len(kings) > 0:
                is_end = True
                if len(kings) == 1:
                    self.interfase.do_info(Get_text(f'game_{kings[0]}_king'))
                else:
                    self.interfase.do_info(Get_text('game_both_king'))
        # pate
        if not is_end:
            for line in board:
                for el in line:
                    el.attacked = False
            for line in board:
                for field in line:
                    if field.figure.type != 'empty' and \
                                field.figure.color != self.color_do_hod_now:
                        field.figure.do_attack(board)
            
            if not self.able_to_do_hod(board,self.color_do_hod_now):
                self.interfase.do_info(Get_text('game_pat'))
                is_end = True
        global_constants.game.ind = not is_end

    def move_figure(self,board,x,y,options=None):
        self.message = f'move {self.choose_figure.x} {self.choose_figure.y} {x} {y}'
        Music.move()
        if self.choose_figure.color == 'white':
            self.made_moves += 1

        a , b = self.choose_figure.x , self.choose_figure.y
        board[a][b].figure = self.Figure('',0,0,'empty')
        board[x][y].figure.destroy()
        board[x][y].figure = self.choose_figure
        board[x][y].figure.set_coords_on_board(x,y)
                
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
        return board

