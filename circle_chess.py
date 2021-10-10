
from help_chess import Figure
from kivy.graphics import Ellipse, Color, Line

import math
import copy

from sounds import Music
from translater import Get_text
import global_constants
import core_game_logik

import circle_figure
import bizantion_figure


class Green_line(Line):
    def __init__(self):
        super(Green_line, self).__init__()
        self.width = 2
        self.close = True
        self.drawed = False
        self.color = [0, 0, 1, 1]

    def __del__(self):
        if self.drawed:
            self.canvas.clear()

    def get_canv(self, canvas):
        self.canvas = canvas

    def get_circle(self, y):
        mas = []
        d = 3 - 2 * y
        x = 0
        while(x <= y):
            mas.append([x, y])
            if d < 0:
                d += 4 * x + 6
            else:
                d += 4 * (x - y) + 10
                y -= 1
            x += 1
        mas2 = mas[::-1]
        for el in mas2:
            mas.append([el[1], el[0]])
        mas2 = mas[::-1]
        for el in mas2:
            mas.append([el[0], -el[1]])
        mas2 = mas[::-1]
        for el in mas2:
            mas.append([-el[0], el[1]])
        return mas

    def show_field(self, x, y):
        Sizes = global_constants.Sizes
        if self.drawed:
            self.canvas.remove(self)
            self.drawed = False
        if x != -1:
            size = Sizes.r // 2
            agle = y * 22.5 + 11.25
            r = Sizes.r_min + Sizes.r * x + Sizes.r * .5
            bx = math.cos(math.radians(agle))*r + Sizes.center[0]
            by = math.sin(math.radians(agle))*r + Sizes.center[1]
            circle = self.get_circle(size)
            self.points = []
            for [x, y] in circle:
                self.points.append(x + bx)
                self.points.append(y+by)
            with self.canvas:
                Color(*self.color)
                self.canvas.add(self)
                self.drawed = True
                Color(1, 1, 1, 1)


class Game_logik(core_game_logik.CoreGameLogik):
    def build_game(self):
        super().build_game()
        self.Figure = bizantion_figure.Figure
        if global_constants.game.type_of_chess == 'circle_chess':
            self.Figure = circle_figure.Figure
        self.board = create_round_board()
    
    def init_game(self):
        Main_Window = global_constants.Main_Window
        self.create_interface(Main_Window, global_constants.Sizes)
        global_constants.current_figure_canvas = Main_Window.wid.canvas
        self.build_game()
        self.choose_figure = self.Figure('white', 0, 0, 'empty')        
        self.green_line = Green_line()
        self.green_line.get_canv(Main_Window.canvas)

    def copy_board(self, board):
        x = len(board)
        y = len(board[0])
        Field = core_game_logik.Field
        new_board = [[Field() for t in range(y)] for a in range(x)]
        for a in range(x):
            for b in range(y):
                new_board[a][b].figure = self.Figure('white', a, b, '')
                new_board[a][b].figure.color = copy.copy(board[a][b].figure.color)
                new_board[a][b].figure.type = copy.copy(board[a][b].figure.type)
                if board[a][b].figure.type == 'pawn':
                    new_board[a][b].figure.moving = board[a][b].figure.moving

        return new_board

    def create_tips(self, a, b, board):
        list1 = self.find_fields(board, board[a][b].figure)
        Sizes = global_constants.Sizes
        if len(list1) > 0:
            self.tips_drawed = True

        color = [0, 1, 0, 0.5]
        if board[a][b].figure.color != self.color_do_hod_now:
            color = [1, 0, 0, 0.5]
        if global_constants.game.state_game != 'one' and self.color_do_hod_now != global_constants.game.play_by:
            color = [1, 0, 0, .8]
        with global_constants.Main_Window.wid.canvas:
            Color(*color)
        tip_r = Sizes.r // 6
        for el in list1:
            x, y = el[0], el[1]
            agle = y * 22.5 + 11.25
            r = Sizes.r_min + Sizes.r * x + Sizes.r * .5
            bx = math.cos(math.radians(agle))*r - 2 + Sizes.center[0]
            by = math.sin(math.radians(agle))*r - 2 + Sizes.center[1]
            r = tip_r
            global_constants.Main_Window.wid.canvas.add(Ellipse(
                pos=[bx - r/2, by - r/2],
                size=(r, r)))

        with global_constants.Main_Window.wid.canvas:
            Color(1, 1, 1, 1, mode='rgba')

    def move_figure(self, board, x, y, options=None):
        if global_constants.game.state_game != 'one' and self.color_do_hod_now == global_constants.game.play_by:
            global_constants.Connection_manager.send(
                f"move {self.choose_figure.x} {self.choose_figure.y} {x} {y} {self.players_time['white']} {self.players_time['black']}")
        Music.move()
        if self.choose_figure.color == 'white':
            self.made_moves += 1

        a, b = self.choose_figure.x, self.choose_figure.y
        board[a][b].figure = Figure('', 0, 0, 'empty')
        board[x][y].figure.destroy()
        board[x][y].figure = self.choose_figure
        board[x][y].figure.set_coords_on_board(x, y)

        self.choose_figure = Figure('', 0, 0, 'empty')
        self.change_color(options)
        self.is_end_of_game(board)
        self.delete_tips()
        self.green_line.show_field(x=-1, y=-1)
        self.list_of_hod_field = []

        return board

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
        if not is_mate:
            if not self.able_to_do_hod(board, self.color_do_hod_now):
                if self.color_do_hod_now == 'white':
                    self.interfase.do_info(Get_text('game_white_pat_lose'))
                else:
                    self.interfase.do_info(Get_text('game_black_pat_lose'))
                is_mate = True

        if not is_mate:
            if not have_figs(board, self.color_do_hod_now):
                if self.color_do_hod_now == 'white':
                    self.interfase.do_info(Get_text('game_white_lost_figs'))
                else:
                    self.interfase.do_info(Get_text('game_black_lost_figs'))
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

    def fit_field(self, event):
        x, y = 0, 0
        e_x, e_y = event.x, event.y
        s = global_constants.Sizes
        r = (e_x - s.center[0])**2 + (e_y - s.center[1])**2
        if r < s.r_min**2:
            return -1, -1
        elif r > s.r_max**2:
            return -1, -1
        else:
            e_x -= s.center[0]
            e_y -= s.center[1]
            r **= .5
            a = abs(math.asin(e_y/r))
            if e_y >= 0 and e_x >= 0:
                ch = 1
            if e_x >= 0 and e_y <= 0:
                ch = 4
            if e_x <= 0 and e_y >= 0:
                ch = 2
            if e_y <= 0 and e_x <= 0:
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
                x += 1
                r -= s.r
            return x, y



def create_round_board():
    Figure = global_constants.game.Game_logik.Figure
    Field = core_game_logik.Field
    board = [[Field() for x in range(16)] for y in range(4)]
    king = ['king', 'bishop', 'horse', 'rook']
    queen = ['queen', 'bishop', 'horse', 'rook']

    for x in range(4):
        board[x][2].figure = Figure('black', x, 2, 'pawn', 'down')
        board[x][3].figure = Figure('black', x, 3, queen[x])
        board[x][4].figure = Figure('black', x, 4, king[x])
        board[x][5].figure = Figure('black', x, 5, 'pawn', 'up')

        board[x][10].figure = Figure('white', x, 10, 'pawn', 'down')
        board[x][12].figure = Figure('white', x, 12, queen[x])
        board[x][11].figure = Figure('white', x, 11, king[x])
        board[x][13].figure = Figure('white', x, 13, 'pawn', 'up')
        for y in 0, 1, 6, 7, 8, 9, 14, 15:
            board[x][y].figure = Figure('', x, y, 'empty', '')

    return board

def have_figs(board, color):
    res = False
    for line in board:
        for field in line:
            if field.figure.type not in ['', 'king', 'empty']:
                if field.figure.color == color:
                    res = True
                    break
    return res





