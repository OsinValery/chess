from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Ellipse, Color, Line
from kivy.uix.button import Button
from kivy.uix.bubble import BubbleButton, Bubble, GridLayout
from kivy.clock import Clock

import copy
import os

import interface
from Window_info import Window
from sounds import Music
from settings import Settings
from translater import Get_text
from connection import Connection
import global_constants

import legan_figure
Figure = legan_figure.Figure


class Game_rect(Widget):
    def on_touch_down(self, touch):
        Game.do_sf(touch)

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
            pad_x = Sizes.x_top_board + Sizes.x_top
            pad_y = Sizes.y_top_board + Sizes.y_top
            pad = Sizes.field_size
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


def create_start_game_board():
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


def back(touch):
    global choose_figure, interfase, gr_line

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
    del gr_line
    if Game.state_game != 'one':
        Connection.messages += ['leave']
    Game.renew()
    Main_Window.canvas.clear()
    Main_Window.create_start_game(touch)


def return_board(press):
    global but
    if not Game.pause or Game.voyaje_message:
        return
    if Game.state_game != 'one':
        Connection.messages += [
            f'pause off {Game.players_time["white"]} {Game.players_time["black"]}']
    try:
        Main_Window.remove_widget(but)
        del but
    except:
        pass
    rect = Rectangle(source=Settings.get_board_picture(Game.type_of_chess),
                     pos=[Sizes.x_top_board, Sizes.y_top_board],
                     size=Sizes.board_size)
    Main_Window.wid.canvas.add(rect)
    Game.tips_drawed = False
    for x in range(8):
        for y in range(8):
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
    if Game.ind == False:
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
            font_name = global_constants.Settings.get_font(),
            font_size=40,
            text=Get_text('game_return'),
            color=(1, 0, 1, 0.5),
            background_normal='',
            background_color=(0, 1, 0, 0.5),
            on_press=return_board
        )
        Main_Window.add_widget(but)


def create_tips(a, b, board):
    list1 = find_fields(board, board[a][b].figure)
    top_x = Sizes.x_top + Sizes.x_top_board
    top_y = Sizes.y_top + Sizes.y_top_board
    field = Sizes.field_size
    color = [0, 1, 0, .8]
    if Game.color_do_hod_now != board[a][b].figure.color:
        color = [1, 0, 0, .8]
    if Game.state_game != 'one' and Game.color_do_hod_now != Game.play_by:
        color = [1, 0, 0, .8]
    r = Sizes.field_size // 6
    with Main_Window.wid.canvas:
        Color(*color, mode='rgba')
    for el in list1:
        Game.tips_drawed = True
        x, y = el[0], el[1]
        Main_Window.wid.canvas.add(Ellipse(
            pos=[top_x - r/2 + (x+0.5)*field, top_y - r/2 + (y+0.5)*field],
            size=[r, r]))
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
        for x in range(8):
            for y in range(8):
                if Game.board[x][y].figure.type != 'empty':
                    Main_Window.wid.canvas.add(Game.board[x][y].figure.rect)


def copy_board(board):
    new_board = [[Field() for t in range(8)] for a in range(8)]
    for a in range(8):
        for b in range(8):
            new_board[a][b].figure = Figure('white', 0, 0, '')
            new_board[a][b].figure.color = copy.copy(board[a][b].figure.color)
            new_board[a][b].figure.type = copy.copy(board[a][b].figure.type)

    return new_board


def is_chax(board, color):
    res = False
    for a in range(8):
        for b in range(8):
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
        board2 = copy_board(board)
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
                    if board2[a][b].figure.color != Game.color_do_hod_now:
                        if board2[a][b].figure.type == board[a][b].figure.type:
                            board2 = board[a][b].figure.do_attack(board2)

        if not is_chax(board2, Game.color_do_hod_now):
            list2.append(element)

    return list2


def is_end_of_game(board):
    is_mate = False
    board2 = copy_board(board)
    for x in range(8):
        for y in range(8):
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
            interfase.do_info(
                Get_text('game_pat', params=Game.color_do_hod_now))
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
        Game.time = Clock.schedule_interval(tick, 1)
        if time != None:
            if Game.color_do_hod_now != Game.play_by:
                Game.players_time['white'] = int(time[0])
                Game.players_time['black'] = int(time[1])
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
    Game.message = f'move {choose_figure.x} {choose_figure.y} {x} {y}'
    Music.move()
    if choose_figure.color == 'white':
        Game.made_moves += 1

    a, b = choose_figure.x, choose_figure.y
    board[a][b].figure = Figure('', 0, 0, 'empty')
    board[x][y].figure.destroy()
    board[x][y].figure = choose_figure
    board[x][y].figure.set_coords_on_board(x, y)

    if choose_figure.type == 'pawn' and board[x][y].figure.pawn_on_last_line():
        if Game.state_game != 'one' and Game.color_do_hod_now != Game.play_by:
            n, m = choose_figure.x, choose_figure.y
            Game.board[n][m].figure.transform_to(options[1])
            choose_figure = Figure('', 0, 0, 'empty')
            options = options[2:]
            change_color(options)
            is_end_of_game(board)
        else:
            do_transformation(Game.color_do_hod_now, x, y, options)
    else:
        if Game.state_game != 'one' and Game.color_do_hod_now == Game.play_by:
            Game.message += f" {Game.players_time['white']} {Game.players_time['black']}"
            Connection.messages += [Game.message]
            Game.message = ''
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
        text = Get_text('game_end_time') + '!\n'
        if Game.color_do_hod_now == 'white':
            text += Get_text('game_white_lose')
        else:
            text += Get_text('game_black_lose')
        interfase.do_info(text)
        Game.time.cancel()


def do_transformation(color, x, y, options=None):
    def complete(ftype):
        global choose_figure
        x, y = choose_figure.x, choose_figure.y
        Game.board[x][y].figure.transform_to(ftype)
        choose_figure = Figure('', 0, 0, 'empty')
        Main_Window.remove_widget(Game.bub)
        del Game.bub
        Game.need_change_figure = False
        if Game.state_game != 'one':
            Game.message += ' = ' + ftype
            Game.message += f" {Game.players_time['white']} {Game.players_time['black']}"
            Connection.messages += [Game.message]
        Game.message = ''
        change_color(options)
        is_end_of_game(Game.board)

    # for buttons
    def change_q(click):
        complete('queen')

    def change_h(click):
        complete('horse')

    def change_b(click):
        complete('bishop')

    def change_r(click):
        complete('rook')

    Game.need_change_figure = True

    wid = (x - 1) * Sizes.field_size + Sizes.x_top + Sizes.x_top_board
    height = (y + 0.8) * Sizes.field_size + Sizes.y_top + Sizes.y_top_board

    Game.bub = Bubble(
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

    Game.bub.add_widget(box)
    Main_Window.add_widget(Game.bub)



def build_game(game):
    game.fit_field = fit_field
    game.color_do_hod_now = 'white'
    game.list_of_hod_field = []
    game.board = create_start_game_board()
    game.do_hod = do_hod
    game.tips_drawed = False
    if game.with_time:
        game.time = Clock.schedule_interval(tick, 1)
    return game


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


def create_interface(main_widget, app_size, Game):
    global interfase

    def set_draw(press):
        if not Game.ind:
            return
        if Game.made_moves > 3 or (Game.color_do_hod_now == 'white' and Game.made_moves == 3):
            draw_message()
        else:
            create_message(Get_text('game_cant_draw'))

    interfase = interface.Graphical_interfase(
        Game, app_size, [back, pause, surrend, set_draw])

    wid = Game_rect(size=app_size.board_size)
    wid.canvas.add(Rectangle(
        source=Settings.get_board_picture(Game.type_of_chess),
        pos=[app_size.x_top_board, app_size.y_top_board],
        size=app_size.board_size))
    main_widget.add_widget(wid)
    main_widget.wid = wid


def init_game():
    global choose_figure, gr_line
    global Game, Main_Window, Sizes
    Game = global_constants.game
    Main_Window = global_constants.Main_Window
    Sizes = global_constants.Sizes

    choose_figure = Figure('white', 0, 0, 'empty')
    create_interface(Main_Window, Sizes, Game)
    global_constants.current_figure_canvas = Main_Window.wid.canvas
    Game = build_game(Game)
    gr_line = Green_line()
    gr_line.get_canv(Main_Window.canvas)


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
    for x in range(8):
        for y in range(8):
            if Game.board[x][y].figure.type != 'empty':
                Main_Window.wid.canvas.add(Game.board[x][y].figure.rect)
    if choose_figure.type != 'empty':
        x, y = choose_figure.x, choose_figure.y
        gr_line.show_field(x, y)
