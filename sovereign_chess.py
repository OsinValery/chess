
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Ellipse, Color, Line
from kivy.uix.button import Button
from kivy.uix.bubble import BubbleButton, Bubble, GridLayout
from kivy.uix.scrollview import ScrollView
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
import sovereign

import sovereign_figure
Figure = sovereign_figure.Figure


class Game_rect(Widget):
    def on_touch_down(self, touch):
        Game.do_sf(touch)

    def __del__(self):
        self.canvas.clear()
        self.clear_widgets()


class Green_line(Line):
    def __init__(self):
        super(Green_line, self).__init__()
        self.width = 3
        self.close = True

    def get_canv(self, canvas):
        with canvas:
            Color(0, 1, 0, 1)
            canvas.add(self)
            Color(1,1,1,1)

    def show_field(self, x, y):
        if x < 0 or y < 0:
            self.points = [-1000, -1000, -1000, -1000]
        else:
            pad_x = Sizes.x_top
            pad_y = Sizes.y_top
            pad = Sizes.field_size
            self.points = (
                pad_x + pad * x, pad_y + pad * y,
                pad_x + pad * (x+1), pad_y + pad * y,
                pad_x + pad * (x+1), pad_y + pad * (y+1),
                pad_x + pad * x, pad_y + pad * (y + 1)
            )


###############################################
# game logik
##############################################

def is_chax(board, player):
    res = False
    for a in range(16):
        for b in range(16):
            if (board[a][b].figure.type == 'king') and (board[a][b].attacked):
                if Game.game_state.get_owner(board[a][b].figure.color) == player:
                    res = True
                    break
    return res


def able_to_do_hod(board, player):
    Res = False
    for a in board:
        for field in a:
            if field.figure.type != 'empty' and Game.game_state.get_owner(field.figure.color) == player:
                if find_fields(board, field.figure) != []:
                    Res = True
                    break
    return Res


def find_fields(board, figure):
    time_list = figure.first_list(board,global_constants.game.game_state)
    if figure.type == 'king':
        time_list += sovereign.find_rocking(figure,board,Game.game_state.copy())
    list2 = []

    for element in time_list:
        board2 = copy_board(board)
        new_state = Game.game_state.copy()
        for a in board2:
            for b in a:
                b.attacked = False

        new_state.check_control([figure.x,figure.y,*element],figure.color)
        # как будто был сделан туда ход, и нет ли шаха королю ходящего цвета
        board2[figure.x][figure.y].figure.type = 'empty'
        board2[figure.x][figure.y].figure.color = ''
        board2[element[0]][element[1]].figure.type = copy.copy(figure.type)
        board2[element[0]][element[1]].figure.color = copy.copy(figure.color)

        for a in range(16):
            for b in range(16):
                if board2[a][b].figure.type != 'empty':
                    if new_state.get_owner(board2[a][b].figure.color) != Game.color_do_hod_now:
                        if board2[a][b].figure.type == board[a][b].figure.type:
                            board2 = board[a][b].figure.do_attack(board2,new_state)

        if not is_chax(board2, Game.color_do_hod_now):
            list2.append(element)

    return list2


def is_end_of_game(board):
    is_mate = False
    board2 = copy_board(board)
    for x in range(16):
        for y in range(16):
            if Game.game_state.get_owner(board2[x][y].figure.color) != Game.color_do_hod_now:
                board2 = board[x][y].figure.do_attack(board2,Game.game_state)
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


def do_hod(x, y, board):
    global choose_figure
    if (choose_figure.type != 'empty') and (choose_figure is board[x][y].figure):
        # кликнули на выббранную фигуру
        if choose_figure.type == 'king':
            desertion(x,y,board)
        else:
            choose_figure = Figure('', 0, 0, 'empty')
            gr_line.show_field(-1, y)
            Game.list_of_hod_field = []
            if Game.make_tips:
                delete_tips()
    elif (board[x][y].figure.type != 'empty') and (Game.game_state.get_owner(board[x][y].figure.color) != Game.color_do_hod_now) and not([x, y] in Game.list_of_hod_field):
        # попросить подсказку хода для врага
        if Game.make_tips:
            delete_tips()
            create_tips(x, y, board)
    elif Game.game_state.get_owner(board[x][y].figure.color) == Game.color_do_hod_now:
        # выбрать фигуру
        choose_figure = board[x][y].figure
        Game.list_of_hod_field = find_fields(board, choose_figure)
        gr_line.show_field(x, y)
        if Game.make_tips:
            delete_tips()
            create_tips(x, y, board)
    elif choose_figure.type != 'empty':
        # move figure
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
    Game.game_state.check_control([a,b,x,y],choose_figure.color)
    board[a][b].figure = Figure('', 0, 0, 'empty')
    board[x][y].figure.destroy()
    board[x][y].figure = choose_figure
    board[x][y].figure.set_coords_on_board(x, y)
    if board[x][y].figure.type == 'king':
        sovereign.do_rocking(a,b,x,y,board)

    if choose_figure.type == 'pawn' and board[x][y].figure.pawn_on_last_line():
        if Game.state_game != 'one' and Game.color_do_hod_now != Game.play_by:
            n, m = choose_figure.x, choose_figure.y
            Game.board[n][m].figure.transform_to(options[1])
            if options[1] == 'king':
                
                transform_to_king(n,m,board)
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


def desertion(x,y,board):
    global choose_figure
    game = Game
    colors = game.game_state.friend_colors(board[x][y].figure.color)
    if game.game_state.is_control_point(x,y):
        color = game.game_state.get_control_point_color([x,y])
        if color in colors:
            colors.remove(color)
    new_board = sovereign.copy_board(board)
    for a in range(16):
        for b in range(16):
            if game.game_state.get_owner(board[a][b].figure.color) != game.color_do_hod_now:
                new_board = board[a][b].figure.do_attack(new_board,game.game_state)
    if is_chax(new_board, game.color_do_hod_now) or len(colors) == 1:
        choose_figure = Figure('', 0, 0, 'empty')
        gr_line.show_field(-1, y)
        Game.list_of_hod_field = []
        if Game.make_tips:
            delete_tips()
        return


    def change_color_player(color):
        color = color.text
        game.need_change_figure = False
        global_constants.Main_Window.remove_widget(bub)
        if color == board[x][y].figure.color:
            return
        game.game_state.update_player_color(board[x][y].figure.color,color)
        board[x][y].figure.change_color(color)

        if Game.state_game != 'one':
            Game.message = f'move {x} {y} {x} {y} = {color}'
            Game.message += f" {Game.players_time['white']} {Game.players_time['black']}"
            Connection.messages += [Game.message]
        Game.message = ''
        choose_figure = Figure('', 0, 0, 'empty')
        change_color()
        delete_tips()
        gr_line.show_field(x=-1, y=-1)
        Game.list_of_hod_field = []

    grid = GridLayout(cols=3)
    bub = Bubble(
        pos = [global_constants.Main_Window.wid.center[0],global_constants.Sizes.y_top_board + global_constants.Main_Window.wid.center[1]],
        size = [global_constants.Sizes.board_size[0] / 3]*2
    )
    bub.add_widget(grid)
    global_constants.Main_Window.add_widget(bub)
    for color in colors:
        grid.add_widget(BubbleButton(
            text = color,
            on_press = change_color_player
        ))
    game.need_change_figure = True


def do_transformation(color, x, y, options=None):
    def complete(ftype):
        global choose_figure
        x, y = choose_figure.x, choose_figure.y
        Game.board[x][y].figure.transform_to(ftype)
        if ftype == 'king':
            transform_to_king(x,y,Game.board)
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
    
    def change_k(click):
        complete('king')

    Game.need_change_figure = True

    wid = (x - 1) * Sizes.field_size + Sizes.x_top + Sizes.x_top_board
    height = (y + 0.8) * Sizes.field_size + Sizes.y_top + Sizes.y_top_board

    Game.bub = Bubble(
        pos=[wid, height],
        size=[3*Sizes.field_size]*2
    )
    box = GridLayout(
        rows=2,
        padding=[Sizes.field_size*0.05]*4
    )
    if color == 'white':
        names = ['qw.png', 'bw.png', 'hw.png', 'rw.png']
    else:
        names = ['qb.png', 'bb.png', 'hb.png', 'rb.png']
    commands = [change_q, change_b, change_h, change_r]
    d = os.path.sep
    folder = Settings.get_folder() + f'pictures{d}fig_set1{d}'

    # add king
    new_board = sovereign.copy_board(Game.board)
    for a in range(16):
        for b in range(16):
            if new_board[a][b].figure.type == 'king':
                if Game.game_state.get_owner(new_board[a][b].figure.color) == color:
                    new_board[a][b].figure.color = ''
                    new_board[a][b].figure.type = 'empty'
    new_board[x][y].figure.type = 'king'
    for a in range(16):
        for b in range(16):
            if Game.game_state.get_owner(new_board[a][b].figure.color) != color:
                new_board = Game.board[a][b].figure.do_attack(new_board,Game.game_state)
    if not new_board[x][y].attacked:
        commands.append(change_k)
        if color == 'white':
            names.append('kw.png')
        else:
            names.append('kb.png')

    for x in range(len(names)):
        box.add_widget(BubbleButton(
            text='',
            background_normal=folder + names[x],
            size=[Sizes.field_size]*2,
            on_press=commands[x]
        ))

    Game.bub.add_widget(box)
    Main_Window.add_widget(Game.bub)


def transform_to_king(x,y,board):
    if board[x][y].figure.color == Game.game_state.white_player:
        for a in range(16):
            for b in range(16):
                if [a,b] != [x,y]:
                    if board[a][b].figure.type == 'king':
                        if board[a][b].figure.color == Game.game_state.white_player:
                            board[a][b].figure.destroy()
    elif board[x][y].figure.color == Game.game_state.black_player:
        for a in range(16):
            for b in range(16):
                if [a,b] != [x,y]:
                    if board[a][b].figure.type == 'king':
                        if board[a][b].figure.color == Game.game_state.black_player:
                            board[a][b].figure.destroy()
    else:
        color = board[x][y].figure.color
        if Game.game_state.get_owner(color) == 'white':
            old_color = Game.game_state.white_player
        else:
            old_color = Game.game_state.black_player
        for a in range(16):
            for b in range(16):
                if board[a][b].figure.color == old_color:
                    if board[a][b].figure.type == 'king':
                        board[a][b].figure.destroy()
        Game.game_state.update_player_color(old_color,color)


def work_network_message(message:str):
    global choose_figure
    data = message.split()
    print(data)
    x0 = int(data[0])
    y0 = int(data[1])
    x1 = int(data[2])
    y1 = int(data[3])
    options = data[4:]
    if [x0,y0] != [x1,y1]:
        choose_figure = Game.board[x0][y0].figure
        Game.board = move_figure(Game.board, x1, y1, options)
    else:
        print(x0,y0,x1,y1)
        print(options)
        color = options[1]
        Game.game_state.update_player_color(Game.board[x0][y0].figure.color,color)
        Game.board[x0][y0].figure.change_color(color)
        change_color(options[2:])
        delete_tips()
        gr_line.show_field(x=-1, y=-1)
        Game.list_of_hod_field = []


############################################################
# start game logik
############################################################

def build_game(game):
    game.fit_field = fit_field
    game.color_do_hod_now = 'white'
    game.list_of_hod_field = []
    game.board = sovereign.create_start_game_board()
    game.do_hod = do_hod
    game.tips_drawed = False
    game.game_state = sovereign.Game_State()
    if game.with_time:
        game.time = Clock.schedule_interval(tick, 1)
    return game


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

    wid = Game_rect(size=app_size.virtual_board_size)
    wid.canvas.add(Rectangle(
        source=Settings.get_board_picture(Game.type_of_chess),
        size=app_size.virtual_board_size))
    scroll = ScrollView(
        size = global_constants.Sizes.board_size,
        pos = [global_constants.Sizes.x_top_board, global_constants.Sizes.y_top_board],
    )
    scroll.add_widget(wid)
    wid.size_hint = [None] * 2
    main_widget.add_widget(scroll)
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
    gr_line.get_canv(Main_Window.wid.canvas)



#############################################################
# interface logik
#############################################################


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


def draw_board():
    rect = Rectangle(
        source=Settings.get_board_picture(Game.type_of_chess),
        size=Sizes.virtual_board_size)
    Main_Window.wid.canvas.add(rect)
    Game.tips_drawed = False
    for x in range(16):
        for y in range(16):
            if Game.board[x][y].figure.type != 'empty':
                Main_Window.wid.canvas.add(Game.board[x][y].figure.rect)
    if choose_figure.type != 'empty':
        x, y = choose_figure.x, choose_figure.y
        gr_line.show_field(x, y)


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
    del Game.game_state
    del choose_figure
    del gr_line
    if Game.state_game != 'one':
        Connection.messages += ['leave']
    Game.renew()
    Main_Window.canvas.clear()
    Main_Window.create_start_game(touch)


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
    with Main_Window.wid.canvas:
        Rectangle(
            source=Settings.get_board_picture(Game.type_of_chess),
            size=Sizes.board_size
            )
    Game.tips_drawed = False
    for x in range(16):
        for y in range(16):
            if Game.board[x][y].figure.type != 'empty':
                Main_Window.wid.canvas.add(Game.board[x][y].figure.rect)
    if Game.with_time:
        Game.time = Clock.schedule_interval(tick, 1)
    if choose_figure.type != 'empty':
        x, y = choose_figure.x, choose_figure.y
        gr_line.show_field(x, y)
    with Main_Window.wid.canvas:
        Color(0,1,0,1)
        Main_Window.wid.canvas.add(gr_line)
        Color(1,1,1,1)
    Game.pause = False


##############################################################
#  standart logik
##############################################################


def fit_field(event):
    x, y = 0, 0
    e_x, e_y = event.x, event.y
    s = Sizes
    if e_x <= s.x_top  or e_y <= s.y_top:
        return -1, -1
    elif (e_y >= s.y_top + s.field_size * 16) or (e_x >= s.x_top + s.field_size * 16):
        return -1, -1
    else:
        e_x -= s.x_top 
        x = e_x // s.field_size
        e_y -= s.y_top
        y = e_y // s.field_size
        x = round(x)
        y = round(y)
        return x, y


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


def copy_board(board):
    new_board = [[sovereign.Field() for _ in range(16)] for a in range(16)]
    for a in range(16):
        for b in range(16):
            new_board[a][b].figure = Figure('white', 0, 0, '')
            new_board[a][b].figure.color = copy.copy(board[a][b].figure.color)
            new_board[a][b].figure.type = copy.copy(board[a][b].figure.type)

    return new_board


def create_tips(a, b, board):
    list1 = find_fields(board, board[a][b].figure)
    field = Sizes.field_size
    color = [0, 1, 0, .8]
    if Game.color_do_hod_now != Game.game_state.get_owner(board[a][b].figure.color):
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
            pos=[Sizes.x_top - r/2 + (x+0.5)*field, Sizes.y_top - r/2 + (y+0.5)*field],
            size=[r, r]))
    with Main_Window.wid.canvas:
        Color(1, 1, 1, 1, mode='rgba')


def delete_tips():
    if Game.tips_drawed:
        Main_Window.wid.canvas.clear()
        with Main_Window.wid.canvas:
            Rectangle(
                source=Settings.get_board_picture(Game.type_of_chess),
                size=Sizes.virtual_board_size)
        Game.tips_drawed = False
        for x in range(16):
            for y in range(16):
                if Game.board[x][y].figure.type != 'empty':
                    Main_Window.wid.canvas.add(Game.board[x][y].figure.rect)
        with Main_Window.wid.canvas:
            Color(0,1,0,1)
            Main_Window.wid.canvas.add(gr_line)
            Color(1,1,1,1)





