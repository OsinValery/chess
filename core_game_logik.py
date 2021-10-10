from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Ellipse, Color, Line
from kivy.uix.button import Button
from kivy.uix.bubble import Bubble, BubbleButton
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock

import copy
import os

import global_constants
import interface
from Window_info import Window
from sounds import Music
from settings import Settings
from translater import Get_text

import help_chess


class Game_rect(Widget):
    def on_touch_down(self, touch):
        global_constants.game.Game_logik.do_sf(touch)

    def __del__(self):
        self.canvas.clear()
        self.clear_widgets()


class Field():
    def __init__(self):
        self.attacked = False
        self.figure = None

    def __str__(self):
        return str(self.figure)


class Green_line(Line):
    def __init__(self):
        super(Green_line, self).__init__()
        self.width = 3
        self.close = True
        self.drawed = False

    def get_canv(self, canvas):
        self.canvas = canvas

    def show_field(self, x, y):
        if self.drawed:
            self.canvas.remove(self)
            self.drawed = False
        if x != -1:
            pad_x = global_constants.Sizes.x_top_board + global_constants.Sizes.x_top
            pad_y = global_constants.Sizes.y_top_board + global_constants.Sizes.y_top
            pad = global_constants.Sizes.field_size
            self.points = (
                pad_x + pad * x, pad_y + pad * y,
                pad_x + pad * (x+1), pad_y + pad * y,
                pad_x + pad * (x+1), pad_y + pad * (y+1),
                pad_x + pad * x, pad_y + pad * (y + 1)
            )
            with self.canvas:
                Color(0, 1, 0, 1)
                self.canvas.add(self)
                self.drawed = True
                Color(1, 1, 1, 1)


class CoreGameLogik:
    def __init__(self) -> None:
        self.Figure = help_chess.Figure
        self.green_line = Green_line()
        self.interfase = None
        self.board = []
        self.list_of_hod_field = []
        self.choose_figure = None

        self.tips = []
        self.players_time = {'white': -1, 'black': -1}
        self.want_draw = {'white': False, 'black': False}
        self.color_do_hod_now = 'white'
        self.time = None
        self.tips_drawed = False
        # this button returns board  after the pause
        self.pause_button = None
        # states
        self.pause = False
        self.need_change_figure = False
        self.voyaje_message = False
        self.want_surrend = False
    
        self.message = ''
        self.made_moves = 0
    
    def init_game(self):
        Main_Window = global_constants.Main_Window
        self.create_interface(Main_Window, global_constants.Sizes)
        global_constants.current_figure_canvas = Main_Window.wid.canvas
        self.build_game()
        self.choose_figure = self.Figure('white', 0, 0, 'empty')        
        self.green_line = Green_line()
        self.green_line.get_canv(Main_Window.canvas)

    def create_interface(self,Main_Window, Sizes):
        Game = global_constants.game
        def set_draw(press):
            if not Game.ind:
                return
            if self.made_moves > 3 or (self.color_do_hod_now == 'white' and self.made_moves == 3):
                draw_message()
            else:
                create_message(Get_text('game_cant_draw'))

        self.interfase = interface.Graphical_interfase(
            global_constants.game, Sizes, [back, self.pause_command, self.surrend, set_draw])

        wid = Game_rect(size=Sizes.board_size)
        rect = Rectangle(
            source=Settings.get_board_picture(Game.type_of_chess),
            pos=[Sizes.x_top_board, Sizes.y_top_board],
            size=Sizes.board_size
        )
        wid.canvas.add(rect)
        Main_Window.add_widget(wid)
        Main_Window.wid = wid

    def build_game(self):
        """
        this methood create game 
         you must use super().build_game()  and create self.board and self.Figure
        and other objacts
        """
        if global_constants.game.with_time:
            self.time = Clock.schedule_interval(self.tick, 1)

    def tick(self,cd):
        self.players_time[self.color_do_hod_now] -= 1
        self.interfase.set_time(self.players_time)
        if self.players_time[self.color_do_hod_now] == 0:
            global_constants.game.ind = False
            Music.time_passed()
            text = Get_text('game_end_time') + '!\n'
            if self.color_do_hod_now == 'white':
                text += Get_text('game_white_lose')
            else:
                text += Get_text('game_black_lose')
            self.interfase.do_info(text)
            self.time.cancel()

    def change_color(self,time=None):
        if global_constants.game.with_time:
            self.time.cancel()
            self.time = Clock.schedule_interval(self.tick, 1)
            if time != None:
                if self.color_do_hod_now != global_constants.game.play_by:
                    self.players_time['white'] = int(time[0])
                    self.players_time['black'] = int(time[1])
            self.players_time[self.color_do_hod_now] += global_constants.game.add_time
        if self.color_do_hod_now == 'white':
            if global_constants.game.ind:
                self.interfase.do_info(Get_text('game_black_move'))
            self.color_do_hod_now = 'black'
        elif self.color_do_hod_now == 'black':
            if global_constants.game.ind:
                self.interfase.do_info(Get_text('game_white_move'))
            self.color_do_hod_now = 'white'
        if global_constants.game.with_time:
            self.interfase.set_time(self.players_time)

    def pause_command(self,touch,second_device=False):
        if global_constants.game.ind == False or self.pause:
            return
        # antibug with many buttons "return"
        if not self.pause and not self.need_change_figure:
            self.pause = True
            if global_constants.game.state_game != 'one' and not second_device:
                global_constants.Connection_manager.send(
                    f'pause on {self.players_time["white"]} {self.players_time["black"]}')
            if global_constants.game.with_time:
                self.time.cancel()
            global_constants.Main_Window.wid.canvas.clear()
            self.green_line.show_field(-1, 0)
            Sizes = global_constants.Sizes
            self.pause_button = Button(
                size=(0.5*Sizes.window_size[0], 0.1*Sizes.window_size[0]),
                pos=(0.25*Sizes.window_size[0], 0.4*Sizes.window_size[1]),
                text=Get_text('game_return'),
                color=(1, 0, 1, 0.5),
                background_normal='',
                background_color=(0, 1, 0, 0.5),
                on_press=self.return_board,
                font_name =global_constants.Settings.get_font(),
                font_size = 50,
            )
            global_constants.Main_Window.add_widget(self.pause_button)

    def return_board(self,press):
        if not self.pause or self.voyaje_message:
            return
        if global_constants.game.state_game != 'one':
            global_constants.Connection_manager.send(
                f'pause off {self.players_time["white"]} {self.players_time["black"]}')
        try:
            global_constants.Main_Window.remove_widget(self.pause_button)
            self.pause_button = None
        except:
            pass
        self.draw_board()
        if global_constants.game.with_time:
            self.time = Clock.schedule_interval(self.tick, 1)
        self.pause = False

    def draw_board(self):
        Sizes = global_constants.Sizes
        rect = Rectangle(
            source=Settings.get_board_picture(global_constants.game.type_of_chess),
            pos=[Sizes.x_top_board, Sizes.y_top_board],
            size=Sizes.board_size)
        global_constants.Main_Window.wid.canvas.add(rect)
        self.tips_drawed = False
        for x in range(len(self.board)):
            for y in range(len(self.board[0])):
                if self.board[x][y].figure.type != 'empty':
                    global_constants.Main_Window.wid.canvas.add(self.board[x][y].figure.rect)
        if self.choose_figure.type != 'empty':
            x, y = self.choose_figure.x, self.choose_figure.y
            self.green_line.show_field(x, y)

    def create_tips(self, a, b, board):
        list1 = self.find_fields(board, board[a][b].figure)
        Sizes = global_constants.Sizes

        top_x = Sizes.x_top + Sizes.x_top_board
        top_y = Sizes.y_top + Sizes.y_top_board
        field = Sizes.field_size
        r = Sizes.field_size // 6

        color = [0, 1, 0, .8]
        if self.color_do_hod_now != board[a][b].figure.color:
            color = [1, 0, 0, .8]
        if global_constants.game.state_game != 'one' and self.color_do_hod_now != global_constants.game.play_by:
            color = [1, 0, 0, .8]
        with global_constants.Main_Window.wid.canvas:
            Color(*color, mode='rgba')
        self.tips_drawed = True

        for el in list1:
            x, y = el
            global_constants.Main_Window.wid.canvas.add(Ellipse(
                pos=[top_x - r/2 + (x+0.5)*field, top_y - r/2 + (y+0.5)*field],
                size=[r, r]
            ))
        with global_constants.Main_Window.wid.canvas:
            Color(1, 1, 1, 1, mode='rgba')

    def delete_tips(self):
        Sizes = global_constants.Sizes
        if self.tips_drawed:
            global_constants.Main_Window.wid.canvas.clear()
            rect = Rectangle(
                source=Settings.get_board_picture(global_constants.game.type_of_chess),
                pos=[Sizes.x_top_board, Sizes.y_top_board],
                size=Sizes.board_size)
            global_constants.Main_Window.wid.canvas.add(rect)
            self.tips_drawed = False
            for x in range(len(self.board)):
                for y in range(len(self.board[0])):
                    if self.board[x][y].figure.type != 'empty':
                        global_constants.Main_Window.wid.canvas.add(self.board[x][y].figure.rect)

    def fit_field(self, event):
        x, y = 0, 0
        e_x, e_y = event.x, event.y
        s = global_constants.Sizes
        if e_x <= s.x_top + s.x_top_board or e_y <= s.y_top + s.y_top_board:
            return -1, -1
        elif (e_y >= s.y_top + s.y_top_board + s.field_size * 8) or \
                (e_x >= s.x_top + s.x_top_board + s.field_size * 8):
            return -1, -1
        else:
            e_x -= (s.x_top + s.x_top_board)
            x = e_x // s.field_size
            e_y -= (s.y_top + s.y_top_board)
            y = e_y // s.field_size
            x = round(x)
            y = round(y)
            return x, y

    def do_sf(self, touch):
        def draw():
            if self.color_do_hod_now == 'white' and self.want_draw['black']:
                return True
            if self.color_do_hod_now == 'black' and self.want_draw['white']:
                return True
            return False
        end_game = global_constants.game.ind
        if end_game and not self.need_change_figure and not self.pause and not \
                self.want_surrend and not draw() and not self.voyaje_message:
            x, y = self.fit_field(touch)
            if x != -1 and y != -1:
                self.board = self.do_hod(x, y, self.board)

    def copy_board(self, board):
        new_board = [[Field() for b in range(len(board[0]))] for a in range(len(board))]
        for a in range(len(board)):
            for b in range(len(board[0])):
                new_board[a][b].figure = self.Figure('white', 0, 0, '')
                new_board[a][b].figure.color = copy.copy(board[a][b].figure.color)
                new_board[a][b].figure.type = copy.copy(board[a][b].figure.type)
                new_board[a][b].figure.do_hod_before = copy.copy(
                    board[a][b].figure.do_hod_before)

        return new_board

    # after this line is realized chess logik

    def is_chax(self, board, color):
        for a in range(len(board)):
            for b in range(len(board[0])):
                if (board[a][b].figure.type == 'king'):
                    if (board[a][b].figure.color == color) and (board[a][b].attacked):
                        return True
        return False

    def able_to_do_hod(self, board, color):
        Res = False
        for a in board:
            for field in a:
                if field.figure.type != 'empty' and field.figure.color == color:
                    if self.find_fields(board, field.figure) != []:
                        Res = True
                        break
        return Res

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
        """this function finds all moves of the figure without rocking for king"""
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
            # взятие на проходе
            if figure.type == 'pawn':
                if board2[element[0]][element[1]].figure.type == 'empty':
                    if figure.x != element[0]:
                        board2[element[0]][figure.y].figure.type = 'empty'
                        board2[element[0]][figure.y].figure.color = ''
            board2[element[0]][element[1]].figure.type = copy.copy(figure.type)
            board2[element[0]][element[1]].figure.color = copy.copy(figure.color)

            for a in range(len(board)):
                for b in range(len(board[0])):
                    if board2[a][b].figure.type != 'empty':
                        if board2[a][b].figure.color != self.color_do_hod_now:
                            if board2[a][b].figure.type == board[a][b].figure.type:
                                board2 = board[a][b].figure.do_attack(board2)

            if not self.is_chax(board2, self.color_do_hod_now):
                list2.append(element)

        return list2        

    def do_hod(self, x, y, board):
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

    def move_figure(self, board, x, y, options=None):
        self.message = f'move {self.choose_figure.x} {self.choose_figure.y} {x} {y}'
        Music.move()
        if self.choose_figure.color == 'white':
            self.made_moves += 1

        if self.choose_figure.type == 'pawn':
            if x != self.choose_figure.x:
                if board[x][y].figure.type == 'empty':
                    board[x][self.choose_figure.y].figure.destroy()

        a, b = self.choose_figure.x, self.choose_figure.y
        board[a][b].figure = self.Figure('', 0, 0, 'empty')
        board[x][y].figure.destroy()
        board[x][y].figure = self.choose_figure
        board[x][y].figure.set_coords_on_board(x, y)

        if self.choose_figure.type == 'pawn' and abs(y-b) == 2:
            self.choose_figure.do_hod_now = True
        board[x][y].figure.do_hod_before = True

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
        for a in range(len(board)):
            for b in range(len(board[0])):
                if board[a][b].figure.type == 'pawn':
                    if board[a][b].figure.color == self.color_do_hod_now:
                        board[a][b].figure.do_hod_now = False
        self.list_of_hod_field = []
        return board

    def do_transformation(self, color, x, y, options=None):
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
                global_constants.Connection_manager.send(self.message)
            self.message = ''
            self.change_color(options)
            self.is_end_of_game(self.board)

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
        box = GridLayout(
            rows=2,
            cols=2,
            padding=[Sizes.field_size*0.05]*4
        )
        if color == 'white':
            names = ['qw.png', 'bw.png', 'hw.png', 'rw.png']
        else:
            names = ['qb.png', 'bb.png', 'hb.png', 'rb.png']
        commands = [change_q, change_b, change_h, change_r]
        d = os.path.sep
        folder = Settings.get_folder() + f'pictures{d}fig_set1{d}'
        for x in range(4):
            box.add_widget(BubbleButton(
                text='',
                background_normal=folder + names[x],
                size=[Sizes.field_size]*2,
                on_press=commands[x]
            ))

        self.bub.add_widget(box)
        global_constants.Main_Window.add_widget(self.bub)

    def draw(self):
        if not global_constants.game.ind:
            return
        Sizes = global_constants.Sizes

        def no(press=None):
            self.want_draw['black'] = False
            self.want_draw['white'] = False

        def yes(press=None):
            global_constants.game.ind = False
            if global_constants.game.with_time:
                self.time.cancel()
            self.interfase.do_info(Get_text('game_draw_ok'))

        Window(
            btn_texts=[Get_text('game_no'), Get_text('game_yes')],
            btn_commands=[no, yes],
            text=Get_text('game_want_draw'),
            title=Get_text('game_draw_title'),
            size=[Sizes.board_size[0], .5 * Sizes.board_size[1]],
            title_color=[.1, 0, 1, 1],
            background_color=[.1, 1, .1, .15]
        ).open()

    def surrend(self, click):
        if not global_constants.game.ind:
            return
        Sizes = global_constants.Sizes

        def yes():
            global_constants.game.ind = False
            if global_constants.game.state_game == 'one':
                if self.color_do_hod_now == 'white':
                    f = Get_text('game_white_surrend')
                else:
                    f = Get_text('game_black_surrend')
            else:
                f = Get_text('game_you_surrend')
            self.interfase.do_info(f)
            if global_constants.game.with_time:
                self.time.cancel()
            if global_constants.game.state_game != 'one':
                global_constants.Connection_manager.send(self.message)

        def no():
            self.want_surrend = False

        if self.made_moves < 4 or (self.made_moves == 3 and self.color_do_hod_now == 'black'):
            create_message(Get_text('game_cant_surrend'))
        elif not self.pause and not self.need_change_figure and not self.want_surrend:
            self.want_surrend = True
            Window(
                btn_texts=[Get_text('game_want_surrend'), Get_text('game_not_surrend')],
                btn_commands=[yes, no],
                text=Get_text('game_agree?'),
                title=Get_text('game_press_surrend'),
                size=[Sizes.board_size[0], .5 * Sizes.board_size[1]],
                title_color=[.1, 0, 1, 1]
            ).open()

    def get_game_config_message(self, game):
        text = f'start\ntype:{game.type_of_chess}\ncolor:'
        if game.play_by == 'white':
            text += 'black'
            game.name1 = global_constants.Connection_manager.my_nick
            game.name2 = global_constants.Connection_manager.friend_nick
        else:
            text += 'white'
            game.name2 = global_constants.Connection_manager.my_nick
            game.name1 = global_constants.Connection_manager.friend_nick
        text += f'\ntime:{game.time_mode}\nadd:{game.add_time}\ntips:'
        if game.make_tips:
            text += 't'
        else:
            text += 'f'
        if game.type_of_chess == 'magik':
            text += f'\nmagic:{game.magia_moves}'

        return text




def back(touch):
    Game = global_constants.game
    global_constants.Main_Window.wid.canvas.clear()
    if len(global_constants.Main_Window.wid.children) > 0:
        global_constants.Main_Window.wid.clear_widgets()
    del global_constants.Main_Window.wid

    if Game.with_time:
        Game.Game_logik.time.cancel()
        del Game.Game_logik.time

    if Game.state_game != 'one':
        global_constants.Connection_manager.send('leave')
    Game.renew()
    global_constants.Main_Window.canvas.clear()
    global_constants.Main_Window.create_start_game(touch)



def create_message(text):
    Sizes = global_constants.Sizes
    Game = global_constants.game
    def ok():
        Game.Game_logik.voyaje_message = False
    Game.Game_logik.voyaje_message = True
    Window(
        btn_texts=[Get_text('game_ok')],
        btn_commands=[ok],
        text=str(text),
        title=Get_text('game_error'),
        size=[Sizes.board_size[0], .5 * Sizes.board_size[1]],
        title_color=[.1, 0, 1, 1]
    ).open()


def draw_message():
    Game = global_constants.game
    def yes():
        if Game.state_game == 'one':
            Game.Game_logik.want_draw[Game.Game_logik.color_do_hod_now] = True
            Game.Game_logik.voyaje_message = False
        else:
            global_constants.Connection_manager.send('draw offer')
            if global_constants.game.with_time:
                Game.Game_logik.time.cancel()
            global_constants.Main_Window.wid.canvas.clear()
            global_constants.game.Game_logik.green_line.show_field(-1, 0)

    def no():
        global_constants.game.Game_logik.voyaje_message = False

    global_constants.game.Game_logik.voyaje_message = True
    Sizes = global_constants.Sizes
    Window(
        btn_texts=[Get_text(f'game_{i}') for i in ['no', 'yes']],
        btn_commands=[no, yes],
        text=Get_text('game_offer_draw?'),
        size=[Sizes.board_size[0], .5 * Sizes.board_size[1]],
        title_color=[.1, 0, 1, 1],
        title=Get_text('game_draw?')
    ).open()






