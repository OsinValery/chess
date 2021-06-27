from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Ellipse, Color, Line
from kivy.uix.button import Button
from kivy.clock import Clock

import math
import copy

import interface
from Window_info import Window
from sounds import Music
from settings import Settings
from translater import Get_text
from connection import Connection
import global_constants

import circle_figure
import bizantion_figure
Figure = circle_figure.Figure


class Game_rect(Widget):
    def on_touch_down(self, touch):
        Game.do_sf(touch)

    def __del__(self):
        self.canvas.clear()


class Field():
    def __init__(self):
        self.attacked = False
        self.figure = None

    def __str__(self):
        return str(self.figure)


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


def back(touch):
    # close game
    global choose_figure, interfase, Sizes, gr_line

    Main_Window.wid.canvas.clear()
    if len(Main_Window.wid.children) > 0:
        Main_Window.wid.clear_widgets()
    del Main_Window.wid

    if Game.with_time:
        Game.time.cancel()
        del Game.time
    del Game.board
    del interfase
    del Game.color_do_hod_now
    del Game.fit_field
    del Game.list_of_hod_field
    del Game.do_hod
    del Game.tips_drawed
    del choose_figure
    del Sizes
    del gr_line
    if Game.state_game != 'one':
        Connection.messages += ['leave']
    Game.renew()
    Main_Window.canvas.clear()
    Main_Window.create_start_game(touch)


def return_board(press):
    # exit from pause
    global but
    if not Game.pause:
        return
    if Game.state_game != 'one':
        Connection.messages += [
            f'pause off {Game.players_time["white"]} {Game.players_time["black"]}']
    Main_Window.remove_widget(but)
    del but
    rect = Rectangle(source=Settings.get_board_picture(Game.type_of_chess),
                     pos=[Sizes.x_top_board, Sizes.y_top_board],
                     size=Sizes.board_size)
    Main_Window.wid.canvas.add(rect)
    Game.tips_drawed = False
    for x in range(len(Game.board)):
        for y in range(len(Game.board[x])):
            if Game.board[x][y].figure.type != 'empty':
                Main_Window.wid.canvas.add(Game.board[x][y].figure.rect)
    if Game.with_time:
        Game.time = Clock.schedule_interval(tick, 1)
    if choose_figure.type != 'empty':
        x, y = choose_figure.x, choose_figure.y
        gr_line.show_field(x, y)
    Game.pause = False


def pause(touch):
    global but
    if not Game.ind:
        return
    # antibug with many buttons "return"
    if not Game.pause and not Game.need_change_figure:
        Game.pause = True
        if Game.state_game != 'one':
            Connection.messages += [
                f'pause on {Game.players_time["white"]} {Game.players_time["black"]}']
        if Game.with_time:
            Game.time.cancel()
        Main_Window.wid.canvas.clear()
        gr_line.show_field(-1, 0)
        but = Button(
            size=(0.5*Sizes.window_size[0], 0.1*Sizes.window_size[0]),
            pos=(0.25*Sizes.window_size[0], 0.4*Sizes.window_size[1]),
            text=Get_text('game_return'),
            color=(1, 0, 1, 0.5),
            background_normal='',
            background_color=(0, 1, 0, 0.5),
            on_press=return_board,
            font_name = global_constants.Settings.get_font(),
            font_size=40
        )
        Main_Window.add_widget(but)


def create_tips(a, b, board):
    list1 = find_fields(board, board[a][b].figure)
    if len(list1) > 0:
        Game.tips_drawed = True

    color = [0, 1, 0, 0.5]
    if board[a][b].figure.color != Game.color_do_hod_now:
        color = [1, 0, 0, 0.5]
    if Game.state_game != 'one' and Game.color_do_hod_now != Game.play_by:
        color = [1, 0, 0, .8]
    with Main_Window.wid.canvas:
        Color(*color)
    tip_r = Sizes.r // 6
    for el in list1:
        x, y = el[0], el[1]
        agle = y * 22.5 + 11.25
        r = Sizes.r_min + Sizes.r * x + Sizes.r * .5
        bx = math.cos(math.radians(agle))*r - 2 + Sizes.center[0]
        by = math.sin(math.radians(agle))*r - 2 + Sizes.center[1]
        r = tip_r
        Main_Window.wid.canvas.add(Ellipse(
            pos=[bx - r/2, by - r/2],
            size=(r, r)))

    with Main_Window.wid.canvas:
        Color(1, 1, 1, 1, mode='rgba')


def delete_tips():
    if Game.tips_drawed:
        Main_Window.wid.canvas.clear()
        rect = Rectangle(source=Settings.get_board_picture(Game.type_of_chess),
                         pos=[Sizes.x_top_board, Sizes.y_top_board],
                         size=Sizes.board_size)
        Main_Window.wid.canvas.add(rect)
        Game.tips_drawed = False
        for x in range(len(Game.board)):
            for y in range(len(Game.board[x])):
                if Game.board[x][y].figure.type != 'empty':
                    Main_Window.wid.canvas.add(Game.board[x][y].figure.rect)


def copy_board(board):
    x = len(board)
    y = len(board[0])
    new_board = [[Field() for t in range(y)] for a in range(x)]
    for a in range(x):
        for b in range(y):
            new_board[a][b].figure = Figure('white', a, b, '')
            new_board[a][b].figure.color = copy.copy(board[a][b].figure.color)
            new_board[a][b].figure.type = copy.copy(board[a][b].figure.type)
            if board[a][b].figure.type == 'pawn':
                new_board[a][b].figure.moving = board[a][b].figure.moving

    return new_board


def is_chax(board, color):
    res = False
    for a in range(len(board)):
        for b in range(len(board[0])):
            if (board[a][b].figure.type == 'king') and (board[a][b].figure.color == color) and (board[a][b].attacked):
                res = True
    return res


def able_to_do_hod(board, color):
    Res = False
    for a in board:
        for field in a:
            if field.figure.type != 'empty' and field.figure.color == color:
                if find_fields(board, field.figure) != []:
                    Res = True
                    break
    return Res


def find_fields(board, figure):
    time_list = figure.first_list(board)
    list2 = []

    for element in time_list:
        board2 = []
        board2 = copy_board(board)
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
                    if board2[a][b].figure.color != Game.color_do_hod_now:
                        if board2[a][b].figure.type == board[a][b].figure.type:
                            board2 = board[a][b].figure.do_attack(board2)

        if not is_chax(board2, Game.color_do_hod_now):
            list2.append(element)

    return list2


def have_figs(board, color):
    res = False
    for line in board:
        for field in line:
            if field.figure.type not in ['', 'king', 'empty']:
                res = True
                break
    return res


def is_end_of_game(board):
    is_mate = False
    board2 = copy_board(board)
    for x in range(len(board)):
        for y in range(len(board[0])):
            if board2[x][y].figure.color != Game.color_do_hod_now:
                board2 = board[x][y].figure.do_attack(board2)
    if Game.color_do_hod_now == 'white':
        if is_chax(board2, 'white'):
            if not able_to_do_hod(board, 'white'):
                is_mate = True
                interfase.do_info(Get_text('game_white_mate'))
            else:
                interfase.do_info(Get_text('game_white_chax'))
    else:
        if is_chax(board2, 'black'):
            if not able_to_do_hod(board, 'black'):
                interfase.do_info(Get_text('game_black_mate'))
                is_mate = True
            else:
                interfase.do_info(Get_text('game_black_chax'))
    if not is_mate:
        if not able_to_do_hod(board, Game.color_do_hod_now):
            if Game.color_do_hod_now == 'white':
                interfase.do_info(Get_text('game_white_pat_lose'))
            else:
                interfase.do_info(Get_text('game_black_pat_lose'))
            is_mate = True

    if not is_mate:
        if not have_figs(board, Game.color_do_hod_now):
            if Game.color_do_hod_now == 'white':
                interfase.do_info(Get_text('game_white_lost_figs'))
            else:
                interfase.do_info(Get_text('game_black_lost_figs'))
            is_mate = True

    if is_mate:
        Game.ind = False
        if Game.with_time:
            Game.time.cancel()

    if Game.ind:
        if Game.color_do_hod_now == 'white' and Game.want_draw['black']:
            draw()
        elif Game.color_do_hod_now == 'black' and Game.want_draw['white']:
            draw()
    del board2


def change_color(time=None):
    if Game.with_time:
        Game.time.cancel()
        if time != None:
            if Game.color_do_hod_now != Game.play_by:
                Game.players_time['white'] = int(time[0])
                Game.players_time['black'] = int(time[1])
        Game.time = Clock.schedule_interval(tick, 1)
        Game.players_time[Game.color_do_hod_now] += Game.add_time
    if Game.color_do_hod_now == 'white':
        if Game.ind:
            interfase.do_info(Get_text('game_black_move'))
        Game.color_do_hod_now = 'black'
    elif Game.color_do_hod_now == 'black':
        if Game.ind:
            interfase.do_info(Get_text('game_white_move'))
        Game.color_do_hod_now = 'white'
    if Game.with_time:
        interfase.set_time(Game.players_time)


def do_hod(x, y, board):
    global choose_figure
    if (choose_figure.type != 'empty') and (choose_figure is board[x][y].figure):
        choose_figure = Figure('', 0, 0, 'empty')
        gr_line.show_field(-1, y)
        Game.list_of_hod_field = []
        if Game.make_tips:
            delete_tips()
    elif (board[x][y].figure.type != 'empty') and (board[x][y].figure.color != Game.color_do_hod_now) \
            and not([x, y] in Game.list_of_hod_field):
        if Game.make_tips:
            delete_tips()
            create_tips(x, y, board)
    elif board[x][y].figure.color == Game.color_do_hod_now:
        choose_figure = board[x][y].figure
        Game.list_of_hod_field = find_fields(board, choose_figure)
        gr_line.show_field(x, y)
        if Game.make_tips:
            delete_tips()
            create_tips(x, y, board)
    elif choose_figure.type != 'empty':
        if [x, y] in Game.list_of_hod_field:
            if Game.state_game != 'one' and Game.color_do_hod_now != Game.play_by:
                return board
            board = move_figure(board, x, y)
    return board


def move_figure(board, x, y, options=None):
    global choose_figure
    if Game.state_game != 'one' and Game.color_do_hod_now == Game.play_by:
        Connection.messages += [
            f"move {choose_figure.x} {choose_figure.y} {x} {y} {Game.players_time['white']} {Game.players_time['black']}"]
    Music.move()
    if choose_figure.color == 'white':
        Game.made_moves += 1

    a, b = choose_figure.x, choose_figure.y
    board[a][b].figure = Figure('', 0, 0, 'empty')
    board[x][y].figure.destroy()
    board[x][y].figure = choose_figure
    board[x][y].figure.set_coords_on_board(x, y)

    choose_figure = Figure('', 0, 0, 'empty')
    change_color(options)
    is_end_of_game(board)
    delete_tips()
    gr_line.show_field(x=-1, y=-1)
    Game.list_of_hod_field = []

    return board


def fit_field(event):
    x, y = 0, 0
    e_x, e_y = event.x, event.y
    s = Sizes
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


def draw():
    if not Game.ind:
        return

    def no(press=None):
        Game.want_draw['black'] = False
        Game.want_draw['white'] = False

    def yes(press=None):
        Game.ind = False
        if Game.with_time:
            Game.time.cancel()
        interfase.do_info(Get_text('game_draw_ok'))

    Window(
        btn_texts=[Get_text('game_no'), Get_text('game_yes')],
        btn_commands=[no, yes],
        text=Get_text('game_want_draw'),
        title=Get_text('game_draw_title'),
        size=[Sizes.board_size[0], .5 * Sizes.board_size[1]],
        title_color=[.1, 0, 1, 1],
        background_color=[.1, 1, .1, .15]
    ).open()


def tick(cd):
    Game.players_time[Game.color_do_hod_now] -= 1
    interfase.set_time(Game.players_time)
    if Game.players_time[Game.color_do_hod_now] == 0:
        Game.ind = False
        Music.time_passed()
        text = Get_text('game_end_time')+'!\n'
        if Game.color_do_hod_now == 'white':
            text += Get_text('game_white_lose')
        else:
            text += Get_text('game_black_lose')
        interfase.do_info(text)
        Game.time.cancel()


def build_game(game):
    game.fit_field = fit_field
    game.color_do_hod_now = 'white'
    game.list_of_hod_field = []
    game.board = create_round_board()
    game.do_hod = do_hod
    game.tips_drawed = False
    if game.with_time:
        game.time = Clock.schedule_interval(tick, 1)
    return game


def create_round_board():
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


def surrend(click):
    if not Game.ind:
        return

    def yes():
        Game.ind = False
        if Game.state_game == 'one':
            if Game.color_do_hod_now == 'white':
                f = Get_text('game_white_surrend')
            else:
                f = Get_text('game_black_surrend')
        else:
            f = Get_text('game_you_surrend')
        interfase.do_info(f)
        if Game.with_time:
            Game.time.cancel()
        if Game.state_game != 'one':
            Connection.messages += ['surrend']

    def no():
        Game.want_surrend = False

    if Game.made_moves < 4 or (Game.made_moves == 3 and Game.color_do_hod_now == 'black'):
        create_message(Get_text('game_cant_surrend'))
    elif not Game.pause and not Game.need_change_figure and not Game.want_surrend:
        Game.want_surrend = True
        Window(
            btn_texts=[Get_text('game_want_surrend'),
                       Get_text('game_not_surrend')],
            btn_commands=[yes, no],
            text=Get_text('game_agree?'),
            title=Get_text('game_press_surrend'),
            size=[Sizes.board_size[0], .5 * Sizes.board_size[1]],
            title_color=[.1, 0, 1, 1]
        ).open()


def create_interface(main_widget, app_size):
    global interfase

    def set_draw(press):
        if Game.ind == False:
            return
        if Game.made_moves > 3 or (Game.color_do_hod_now == 'white' and Game.made_moves == 3):
            draw_message()
        else:
            create_message(Get_text('game_cant_draw'))

    interfase = interface.Graphical_interfase(
        Game, app_size, [back, pause, surrend, set_draw])

    wid = Game_rect(size=app_size.board_size)
    rect = Rectangle(
        source=Settings.get_board_picture(Game.type_of_chess),
        pos=[app_size.x_top_board, app_size.y_top_board],
        size=app_size.board_size)
    wid.canvas.add(rect)
    main_widget.add_widget(wid)
    main_widget.wid = wid


def init_game():
    global choose_figure, gr_line
    global Figure, Game, Sizes, Main_Window
    Game = global_constants.game
    Sizes = global_constants.Sizes
    Main_Window = global_constants.Main_Window

    if Game.type_of_chess == 'circle_chess':
        Figure = circle_figure.Figure
    else:
        Figure = bizantion_figure.Figure

    create_interface(Main_Window, Sizes)

    global_constants.current_figure_canvas = Main_Window.wid.canvas

    Game = build_game(Game)
    gr_line = Green_line()
    gr_line.get_canv(Main_Window.canvas)
    choose_figure = Figure('white', 0, 0, 'empty')


def create_message(text):
    def ok():
        Game.voyaje_message = False
    Game.voyaje_message = True
    Window(
        btn_texts=[Get_text('game_ok')],
        btn_commands=[ok],
        text=str(text),
        title=Get_text('game_error'),
        size=[Sizes.board_size[0], .5 * Sizes.board_size[1]],
        title_color=[.1, 0, 1, 1]
    ).open()


def draw_message():
    def yes():
        if Game.state_game == 'one':
            Game.want_draw[Game.color_do_hod_now] = True
            Game.voyaje_message = False
        else:
            Connection.messages += ['draw offer']
            if Game.with_time:
                Game.time.cancel()
            Main_Window.wid.canvas.clear()
            gr_line.show_field(-1, 0)

    def no():
        Game.voyaje_message = False

    Game.voyaje_message = True
    Window(
        btn_texts=[Get_text(f'game_{i}') for i in ['no', 'yes']],
        btn_commands=[no, yes],
        text=Get_text('game_offer_draw?'),
        size=[Sizes.board_size[0], .5 * Sizes.board_size[1]],
        title_color=[.1, 0, 1, 1],
        title=Get_text('game_draw?')
    ).open()


def draw_board():
    rect = Rectangle(source=Settings.get_board_picture(Game.type_of_chess),
                     pos=[Sizes.x_top_board, Sizes.y_top_board],
                     size=Sizes.board_size)
    Main_Window.wid.canvas.add(rect)
    Game.tips_drawed = False
    for line in Game.board:
        for field in line:
            if field.figure.type != 'empty':
                Main_Window.wid.canvas.add(field.figure.rect)
    if choose_figure.type != 'empty':
        x, y = choose_figure.x, choose_figure.y
        gr_line.show_field(x, y)
