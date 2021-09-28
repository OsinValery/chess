
import core_game_logik
import global_constants
from translater import Get_text
from sounds import Music
from connection import Connection

import classic
import fisher
import horse_battle
import permutation
import gen_horde

import permutation_figure
import help_chess


class Field():
    def __init__(self):
        self.attacked = False
        self.figure = None

    def __str__(self):
        return str(self.figure)


class Game_logik(core_game_logik.CoreGameLogik):
    def find_fields(self, board, figure):
        moves = super().find_fields(board, figure)

        if figure.type == 'king' and not figure.do_hod_before:
            moves = self.can_do_rocking(self, board, figure, moves)

        if global_constants.game.type_of_chess == 'fisher':
            if figure.type == 'rook' and not figure.do_hod_before:
                board2 = self.copy_board(board)
                for line in board:
                    for field in line:
                        if field.figure.type != 'empty' and field.figure.color != figure.color:
                            board2 = field.figure.do_attack(board2)
                if not self.is_chax(board2, figure.color):
                    moves = self.rocking_do_rook(board, figure, moves)
        return moves

    def is_end_of_game(self, board):
        is_mate = False
        board2 = self.copy_board(board)
        for x in range(len(board)):
            for y in range(len(board[0])):
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

        if global_constants.game.type_of_chess == 'horde' and self.color_do_hod_now == 'white':
            n = 0
            for row in self.board:
                for f in row:
                    if f.figure.color == 'white':
                        n += 1
            if n == 0:
                is_mate = True
                self.interfase.do_info(Get_text('game_white_nothing'))

        if not is_mate:
            if not self.able_to_do_hod(board, self.color_do_hod_now):
                self.interfase.do_info(Get_text('game_pat'))
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

    def do_hod(self, x, y, board):
        Game = global_constants.game
        if (self.choose_figure.type != 'empty') and (self.choose_figure is board[x][y].figure):
            self.choose_figure = self.Figure('', 0, 0, 'empty')
            self.green_line.show_field(-1, y)
            self.list_of_hod_field = []
            if global_constants.game.make_tips:
                self.delete_tips()
        elif (board[x][y].figure.type != 'empty') and (board[x][y].figure.color != self.color_do_hod_now) \
                and not([x, y] in self.list_of_hod_field):
            if global_constants.game.make_tips:
                self.delete_tips()
                self.create_tips(x, y, board)
        elif board[x][y].figure.color == self.color_do_hod_now:
            if Game.type_of_chess == 'fisher' and self.choose_figure.type == 'king' and [x, y] in self.list_of_hod_field:
                if Game.state_game != 'one' and self.color_do_hod_now != Game.play_by:
                    return board
                board = self.move_figure(board, x, y)
            else:
                self.choose_figure = board[x][y].figure
                self.list_of_hod_field = self.find_fields(board, self.choose_figure)
                self.green_line.show_field(x, y)
                if global_constants.game.make_tips:
                    self.delete_tips()
                    self.create_tips(x, y, board)
        elif self.choose_figure.type != 'empty':
            Game = global_constants.game
            if [x, y] in self.list_of_hod_field:
                if Game.state_game != 'one' and self.color_do_hod_now != Game.play_by:
                    return board
                board = self.move_figure(board, x, y)
        return board

    def build_game(self):
        super(Game_logik,self).build_game()
        game = global_constants.game
        self.Figure = help_chess.Figure
        if game.type_of_chess == 'permutation':
            self.Figure = permutation_figure.Figure

        if game.type_of_chess in ['classic']:
            classic.init_chess(self)
        elif game.type_of_chess == 'fisher':
            fisher.init_chess(self)
        elif game.type_of_chess == 'horse_battle':
            horse_battle.init_chess(self)
        elif game.type_of_chess == 'permutation':
            permutation.init_chess(self)
        elif game.type_of_chess == 'horde':
            gen_horde.init_chess(self)

    def move_figure(self, board, x, y, options=None):
        self.message = f'move {self.choose_figure.x} {self.choose_figure.y} {x} {y}'
        Music.move()
        if self.choose_figure.color == 'white':
            self.made_moves += 1

        if self.choose_figure.type == 'pawn':
            if x != self.choose_figure.x:
                if board[x][y].figure.type == 'empty':
                    board[x][self.choose_figure.y].figure.destroy()

        if global_constants.game.type_of_chess == 'fisher':
            if self.choose_figure.type == 'rook':
                self.is_it_rocking(self.choose_figure, board, x)

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
        if global_constants.game.type_of_chess == 'permutation':
            self.choose_figure.swap()

        if self.choose_figure.type == 'pawn' and board[x][y].figure.pawn_on_last_line():
            if global_constants.game.type_of_chess == 'horse_battle':
                a, b = self.choose_figure.x, self.choose_figure.y
                self.board[a][b].figure.transform_to('horse')
                self.choose_figure = self.Figure('', 0, 0, 'empty')
                self.change_color(options)
                self.is_end_of_game(board)
            else:
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
        for a in range(len(board)):
            for b in range(len(board[0])):
                if board[a][b].figure.type == 'pawn':
                    if board[a][b].figure.color == self.color_do_hod_now:
                        board[a][b].figure.do_hod_now = False
        self.list_of_hod_field = []
        return board




