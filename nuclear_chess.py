
import copy

from translater import Get_text
from sounds import Music
import global_constants
import core_game_logik

import nuclear
import kamikadze_figure


class Game_logik(core_game_logik.CoreGameLogik):
    def build_game(self):
        super().build_game()
        self.Figure = kamikadze_figure.Figure
        nuclear.init_chess(self)

    def is_end_of_game(self, board):
        if not have_king(board, self.color_do_hod_now):
            global_constants.game.ind = False
            self.interfase.do_info(Get_text(f'game_boom_{self.color_do_hod_now}_king'))
            return
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

    def find_fields(self, board, figure):
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
            burst = False
            # взятие на проходе
            if figure.type == 'pawn':
                if board2[element[0]][element[1]].figure.type == 'empty':
                    if figure.x != element[0]:
                        board2[element[0]][figure.y].figure.type = 'empty'
                        board2[element[0]][figure.y].figure.color = ''
                        burst = True
            if board2[element[0]][element[1]].figure.type != 'empty':
                burst = True
            if burst:
                board2[element[0]][element[1]].figure.type = 'empty'
                board2[element[0]][element[1]].figure.color = ''
                for dx in -1, 0, 1:
                    for dy in -1, 0, 1:
                        nx, ny = dx + element[0], dy + element[1]
                        if nx > -1 and nx < 8 and ny > -1 and ny < 8:
                            if board2[nx][ny].figure.type not in ['empty', 'pawn']:
                                board2[nx][ny].figure.type = 'empty'
                                board2[nx][ny].figure.color = ''
            else:
                board2[element[0]][element[1]].figure.type = copy.copy(figure.type)
                board2[element[0]][element[1]].figure.color = copy.copy(figure.color)

            if not have_king(board2, figure.color):
                continue

            color = 'white'
            if figure.color == color:
                color = 'black'

            if not have_king(board2, color):
                list2.append(element)
            else:
                for a in range(8):
                    for b in range(8):
                        if board2[a][b].figure.type != 'empty':
                            if board2[a][b].figure.color != self.color_do_hod_now:
                                if board2[a][b].figure.type == board[a][b].figure.type:
                                    board2 = board[a][b].figure.do_attack(board2)

                if not self.is_chax(board2, self.color_do_hod_now):
                    list2.append(element)

        if figure.type == 'king' and not figure.do_hod_before:
            list2 = self.can_do_rocking(self, board, figure, list2)

        return list2

    def move_figure(self, board, x, y, options=None):
        self.message = f'move {self.choose_figure.x} {self.choose_figure.y} {x} {y}'
        Music.move()
        if self.choose_figure.color == 'white':
            self.made_moves += 1

        burst = False
        if self.choose_figure.type == 'pawn':
            if x != self.choose_figure.x:
                if board[x][y].figure.type == 'empty':
                    burst = True
                    board[x][self.choose_figure.y].figure.destroy()
        if board[x][y].figure.type != 'empty':
            burst = True

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

        if burst:
            self.choose_figure.destroy()
            for dx in -1, 0, 1:
                for dy in -1, 0, 1:
                    nx, ny = dx + x, dy + y
                    if nx > -1 and nx < 8 and ny > -1 and ny < 8:
                        if board[nx][ny].figure.type not in ['empty', 'pawn']:
                            board[nx][ny].figure.destroy()

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
                global_constants.Connection_manager.send(self.message)
                self.message = ''
            self.choose_figure = self.Figure('', 0, 0, 'empty')
            self.change_color(options)
            self.is_end_of_game(board)

        self.delete_tips()
        self.green_line.show_field(x=-1, y=-1)
        for a in range(8):
            for b in range(8):
                if board[a][b].figure.type == 'pawn':
                    if board[a][b].figure.color == self.color_do_hod_now:
                        board[a][b].figure.do_hod_now = False
        self.list_of_hod_field = []
        return board


def have_king(board, color):
    for line in board:
        for field in line:
            fig = field.figure
            if fig.type == 'king' and fig.color == color:
                return True
    return False

