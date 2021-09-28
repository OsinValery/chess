
from kivy.uix.bubble import Bubble, BubbleButton
from kivy.uix.gridlayout import GridLayout

import copy
import os

from sounds import Music
from settings import Settings
from translater import Get_text
from connection import Connection
import global_constants
import core_game_logik

import magik
import help_chess


class Game_logik(core_game_logik.CoreGameLogik):
    def build_game(self):
        super().build_game()
        self.Figure = help_chess.Figure
        magik.init_chess(self)

    def copy_board(self, board):
        Field = core_game_logik.Field 
        new_board = [[Field() for t in range(8)] for a in range(8)]
        for a in range(8):
            for b in range(8):
                new_board[a][b].figure = self.Figure('white', 0, 0, '')
                new_board[a][b].figure.color = copy.copy(board[a][b].figure.color)
                new_board[a][b].figure.type = copy.copy(board[a][b].figure.type)
                new_board[a][b].figure.do_hod_before = copy.copy(
                    board[a][b].figure.do_hod_before)
                new_board[a][b].figure.x = board[a][b].figure.x
                new_board[a][b].figure.y = board[a][b].figure.y
                if board[a][b].figure.type == 'pawn':
                    new_board[a][b].figure.do_hod_now = board[a][b].figure.do_hod_now

        return new_board

    def find_fields(self, board, figure):
        list2 = super().find_fields(board, figure)
        if figure.type == 'king' and not figure.do_hod_before:
            list2 = self.can_do_rocking(self, board, figure, list2)
        return list2

    def move_figure(self, board, x, y, options=None):
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
            board = self.do_rocking(board, x, y, self.choose_figure)
        else:
            a, b = self.choose_figure.x, self.choose_figure.y
            board[a][b].figure = self.Figure('', 0, 0, 'empty')
            board[x][y].figure.destroy()
            board[x][y].figure = self.choose_figure
            board[x][y].figure.set_coords_on_board(x, y)

        if self.choose_figure.type == 'pawn' and abs(y-b) == 2:
            self.choose_figure.do_hod_now = True
        board[x][y].figure.do_hod_before = True
        self.case = magik.magia_for_network_gen(board)

        if self.choose_figure.type == 'pawn' and board[x][y].figure.pawn_on_last_line():
            if global_constants.game.state_game != 'one' and self.color_do_hod_now != global_constants.game.play_by:
                n, m = self.choose_figure.x, self.choose_figure.y
                self.board[n][m].figure.transform_to(options[1])
                self.choose_figure = self.Figure('', 0, 0, 'empty')
                options = options[2:]
                self.change_color(options)
                self.is_end_of_game(board)
                self.after_movement(board, options)
            else:
                self.do_transformation(self.color_do_hod_now, x, y, options)
        else:
            if global_constants.game.state_game != 'one' and self.color_do_hod_now == global_constants.game.play_by:
                self.message += f" {self.players_time['white']} {self.players_time['black']}"
                self.message += f' {self.case}'
                Connection.messages += [self.message]
                self.message = ''
            self.choose_figure = self.Figure('', 0, 0, 'empty')
            self.change_color(options)
            self.is_end_of_game(board)
            self.after_movement(board, options)

        self.delete_tips()
        self.green_line.show_field(x=-1, y=-1)
        self.list_of_hod_field = []

        return board

    def after_movement(self, board, options):
        # effects of magik chess there
        for a in range(8):
            for b in range(8):
                if board[a][b].figure.type == 'pawn':
                    if board[a][b].figure.color == self.color_do_hod_now:
                        board[a][b].figure.do_hod_now = False
        if not global_constants.game.ind:
            return board
        if self.made_moves % global_constants.game.magia_moves == 0 and self.color_do_hod_now == 'white':
            case = self.case
            if global_constants.game.state_game == 'one':
                magik.magik(self.board)
            elif options != None:
                case = options[-1]
                magik.magia_for_network_run(self.board, case)
            else:
                magik.magia_for_network_run(self.board, case)

            #       check   mate
            white = [False, False]
            black = [False, False]

            # check white
            board2 = self.copy_board(board)
            for x in range(8):
                for y in range(8):
                    if board2[x][y].figure.color == 'black':
                        board2 = board[x][y].figure.do_attack(board2)

            white[0] = self.is_chax(board2, 'white')
            if white[0]:
                white[1] = self.is_mate(board2, 'white')

            # check black
            board2 = self.copy_board(board)
            for x in range(8):
                for y in range(8):
                    if board2[x][y].figure.color == 'white':
                        board2 = board[x][y].figure.do_attack(board2)

            black[0] = self.is_chax(board2, 'black')
            if black[0]:
                black[1] = self.is_mate(board2, 'black')

            Game = global_constants.game
            if black[1] and white[1]:
                Game.ind = False
                self.interfase.do_info(Get_text('game_both_mate'))
            elif white[1]:
                Game.ind = False
                self.interfase.do_info(Get_text('game_white_mate'))
            elif black[1]:
                Game.ind = False
                self.interfase.do_info(Get_text('game_black_mate'))
            elif black[0] and white[0]:
                self.interfase.do_info(Get_text('game_both_chax'))
            elif black[0]:
                edd = Get_text('game_magik_black_chax')
                self.interfase.do_info(Get_text('game_black_chax') + edd)
                self.change_color()
            elif white[0]:
                self.interfase.do_info(Get_text('game_white_chax'))
            else:
                # nothing
                self.interfase.do_info(Get_text('game_white_move'))
                # it is possible that figure, that take chax, will be moved here, and
                # it is not chax, but in is_end_of_game it was detected

        return board

    def is_mate(self, board, color):
        for line in board:
            for field in line:
                if field.figure.color == color:
                    if self.have_move(board, field.figure):
                        return False
        return True

    def have_move(self, board, figure):
        first = figure.first_list(board)
        for element in first:
            board2 = self.copy_board(board)
            # как будто был сделан туда ход, и нет ли шаха королю ходящего цвета
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

            if not self.is_chax(board2, figure.color):
                return True
        return False

    def do_transformation(self, color, x, y, options=None):
        d = os.path.sep

        def complete(ftype):
            x, y = self.choose_figure.x, self.choose_figure.y
            self.board[x][y].figure.transform_to(ftype)
            self.choose_figure = self.Figure('', 0, 0, 'empty')
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
            self.after_movement(self.board, options)

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
        wid = (x - 1) * Sizes.field_size + Sizes.x_top + Sizes.x_top_board
        height = (y + 0.8) * Sizes.field_size + Sizes.y_top + Sizes.y_top_board

        self.bub = Bubble(
            pos=[wid, height],
            size=[3*Sizes.field_size]*2
        )
        box = GridLayout(rows=2, cols=2)
        box.padding = [Sizes.field_size*0.05]*4
        if color == 'white':
            names = ['qw.png', 'bw.png', 'hw.png', 'rw.png']
        else:
            names = ['qb.png', 'bb.png', 'hb.png', 'rb.png']
        commands = [change_q, change_b, change_h, change_r]
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


