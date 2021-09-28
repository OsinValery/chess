
import copy
from help_chess import Figure

from sounds import Music
from translater import Get_text
from connection import Connection
import global_constants
import core_game_logik

import legan_figure


class Game_logik(core_game_logik.CoreGameLogik):
    def build_game(self):
        super().build_game()
        self.Figure = legan_figure.Figure
        self.board = create_start_game_board()

    def copy_board(self,board):
        Field = core_game_logik.Field
        new_board = [[Field() for t in range(8)] for a in range(8)]
        for a in range(8):
            for b in range(8):
                new_board[a][b].figure = legan_figure.Figure('white', 0, 0, '')
                new_board[a][b].figure.color = copy.copy(board[a][b].figure.color)
                new_board[a][b].figure.type = copy.copy(board[a][b].figure.type)
        return new_board

    def find_fields(self,board, figure):
        time_list = figure.first_list(board)
        list2 = []
        for element in time_list:
            board2 = self.copy_board(board)
            for a in board2:
                for b in a:
                    b.attacked = False
            # как будто был сделан туда ход, и нет ли шаха королю ходящего цвета
            board2[figure.x][figure.y].figure.type = 'empty'
            board2[figure.x][figure.y].figure.color = ''
            board2[element[0]][element[1]].figure.type = copy.copy(figure.type)
            board2[element[0]][element[1]].figure.color = copy.copy(figure.color)

            for a in range(8):
                for b in range(8):
                    if board2[a][b].figure.type != 'empty':
                        if board2[a][b].figure.color != self.color_do_hod_now:
                            if board2[a][b].figure.type == board[a][b].figure.type:
                                board2 = board[a][b].figure.do_attack(board2)

            if not self.is_chax(board2, self.color_do_hod_now):
                list2.append(element)
        return list2

    def is_end_of_game(self,board):
        is_mate = False
        board2 = self.copy_board(board)
        for x in range(8):
            for y in range(8):
                if board2[x][y].figure.color != self.color_do_hod_now:
                    board2 = board[x][y].figure.do_attack(board2)
        if self.color_do_hod_now == 'white':
            if self.is_chax(board2, 'white'):
                if not self.able_to_do_hod(board, 'white'):
                    is_mate = True
                    self.interfase.do_info(Get_text('game_white_mate'))
                else:
                    self.interfase.do_info(Get_text('game_white_chax'))
        else:
            if self.is_chax(board2, 'black'):
                if not self.able_to_do_hod(board, 'black'):
                    self.interfase.do_info(Get_text('game_black_mate'))
                    is_mate = True
                else:
                    self.interfase.do_info(Get_text('game_black_chax'))

        if not is_mate:
            if not self.able_to_do_hod(board, self.color_do_hod_now):
                self.interfase.do_info(
                    Get_text('game_pat', params=self.color_do_hod_now))
                is_mate = True
        if is_mate:
            global_constants.game.ind = False
            if global_constants.game.with_time:
                self.time.cancel()
        if global_constants.game.ind:
            if self.color_do_hod_now == 'white' and self.want_draw['black']:
                self.draw()
            elif self.color_do_hod_now == 'black' and self.want_draw['white']:
                self.draw()
        del board2

    def move_figure(self, board, x, y, options=None):
        self.message = f'move {self.choose_figure.x} {self.choose_figure.y} {x} {y}'
        Music.move()
        if self.choose_figure.color == 'white':
            self.made_moves += 1

        a, b = self.choose_figure.x, self.choose_figure.y
        board[a][b].figure = self.Figure('', 0, 0, 'empty')
        board[x][y].figure.destroy()
        board[x][y].figure = self.choose_figure
        board[x][y].figure.set_coords_on_board(x, y)

        if self.choose_figure.type == 'pawn' and board[x][y].figure.pawn_on_last_line():
            if global_constants.game.state_game != 'one' and self.color_do_hod_now != global_constants.game.play_by:
                n, m = self.choose_figure.x, self.choose_figure.y
                self.board[n][m].figure.transform_to(options[1])
                self.choose_figure = self.Figure('', 0, 0, 'empty')
                options = options[2:]
                self.change_color(options)
                self.is_end_of_game(board)
            else:
                self.do_transformation(self.color_do_hod_now, x, y, options)
        else:
            if global_constants.game.state_game != 'one' and self.color_do_hod_now == global_constants.game.play_by:
                self.message += f" {self.players_time['white']} {self.players_time['black']}"
                Connection.messages += [self.message]
                self.message = ''
            self.choose_figure = self.Figure('', 0, 0, 'empty')
            self.change_color(options)
            self.is_end_of_game(board)

        self.delete_tips()
        self.green_line.show_field(x=-1, y=-1)
        self.list_of_hod_field = []
        return board


def create_start_game_board():
    Field = core_game_logik.Field
    Figure = global_constants.game.Game_logik.Figure
    board = [[Field() for t in range(8)] for a in range(8)]
    for x in range(8):
        for y in range(8):
            board[x][y].figure = Figure('', 0, 0, 'empty')

    for a in range(5):
        board[3+a][a].figure = Figure('white',3+a,a,'pawn')
        board[a][3+a].figure = Figure('black',a,3+a,'pawn')
    board[4][3].figure = Figure('white',4,3,'pawn')
    board[3][4].figure = Figure('black',3,4,'pawn')

    for a in 0,1:
        board[a+1][5+a].figure = Figure(x=a+1,y=5+a,fig_type='pawn',color='black')
        board[5+a][a+1].figure = Figure('white',a+5,a+1,'pawn')
    def color(x):
        if x > 3:  return 'white'
        return 'black'
    
    for x,y in [[4,0], [0,4], [3,7], [7,3]]:
        board[x][y].figure = Figure(color(x),x,y,'rook')
    board[0][7].figure = Figure('black',0,7,'king')
    board[7][0].figure = Figure('white',7,0,'king')

    for x,y in [[5,0], [7,1], [0,6], [2,7]]:
        board[x][y].figure = Figure(color(x),x,y,'bishop')
    board[1][6].figure = Figure('black',1,6,'queen')
    board[6][1].figure = Figure('white',6,1,'queen')

    for x,y in [[0,5], [1,7], [6,0], [7,2]]:
        board[x][y].figure = Figure(color(x),x,y,'horse')

    return board







