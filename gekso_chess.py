from kivy.uix.widget import Widget
from kivy.graphics import Rectangle,Ellipse,Color,Line
from kivy.uix.button import Button
from kivy.uix.bubble import Bubble,BubbleButton
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock

import copy

import interface
from Window_info import Window
from sounds import Music
from settings import Settings
from translater import Get_text
from connection import Connection
import global_constants

# import types of chess
import gen_glinskiy
import gen_kuej

import glin_figure 
import kuej_figure
Figure = glin_figure.Figure

class Game_rect(Widget):
    def on_touch_down(self,touch):
        Game.do_sf(touch)


class Field():
    def __init__(self):
        self.attacked = False
        self.figure = None
    def __str__(self):
        return str(self.figure)


class Green_line(Line):
    def __init__(self):
        super(Green_line,self).__init__()
        self.width = 3
        self.close = True
        self.drawed = False
        self.color = [0,1,0,1]
    
    def get_canv(self,canvas):
        self.canvas = canvas
    
    def get_circle(self,y):
        mas = []
        d = 3 - 2 * y
        x = 0
        # Brasenhem's algorithm
        while(x <= y) :
            mas.append([x,y])
            if d < 0 :
                d+= 4 * x + 6
            else : 
                d += 4 * (x - y) + 10
                y -= 1
            x += 1
        mas2 = mas[::-1]
        for el in mas2:
            mas.append( [ el[1] , el[0] ] )
        mas2 = mas[::-1]
        for el in mas2:
            mas.append( [ el[0] , -el[1] ] )
        mas2 = mas[::-1]
        for el in mas2:
            mas.append( [ -el[0] , el[1] ] )
        return mas

    def show_field(self,x,y):
        if self.drawed:
            self.canvas.remove(self)
            self.drawed = False
        if x != -1: 
            size = Sizes.field_h / 2           
            bx = Sizes.x_top_board + .5 * Sizes.board_size[0] \
                    + (x-5) * 1.5 * Sizes.field_len 
            by = Sizes.y_top_board + (abs(5-x) + 1) * .5 * Sizes.field_h + \
                y * Sizes.field_h
            circle = self.get_circle(size)
            self.points = []
            for [x,y] in circle:
                self.points.append(x + bx)
                self.points.append(y+by)
            with self.canvas:
                Color(*self.color)
                self.canvas.add(self)
                self.drawed = True
                Color(1,1,1,1)


def back(touch):
    # close game 
    global choose_figure,interfase,gr_line

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
    # exit from pause
    global but
    if not Game.pause :
        return
    if Game.state_game != 'one':
        Connection.messages += [f'pause off {Game.players_time["white"]} {Game.players_time["black"]}']
    Main_Window.remove_widget(but)
    del but
    rect = Rectangle(source=Settings.get_board_picture(Game.type_of_chess),
            pos=[Sizes.x_top_board,Sizes.y_top_board],
            size=Sizes.board_size)
    Main_Window.wid.canvas.add(rect)
    Game.tips_drawed = False
    for x in range(len(Game.board)):
        for y in range(len(Game.board[x])):
            if Game.board[x][y].figure.type != 'empty':
                Main_Window.wid.canvas.add(Game.board[x][y].figure.rect)
    if Game.with_time:
        Game.time = Clock.schedule_interval(tick,1)
    if choose_figure.type != 'empty':
        x,y = choose_figure.x,choose_figure.y
        gr_line.show_field(x,y)
    Game.pause = False

def pause(touch,second_device=False):
    global but
    if Game.ind == False:
        return
    # antibug with many buttons "return"
    if not Game.pause and not Game.need_change_figure :
        Game.pause = True
        if Game.state_game != 'one' and not second_device:
            Connection.messages += [f'pause on {Game.players_time["white"]} {Game.players_time["black"]}']
        if Game.with_time:
            Game.time.cancel()
        Main_Window.wid.canvas.clear()
        gr_line.show_field(-1,0)
        but = Button(
            size = (0.5*Sizes.window_size[0],0.1*Sizes.window_size[0]),
            pos  = (0.25*Sizes.window_size[0],0.4*Sizes.window_size[1]),
            font_name = global_constants.Settings.get_font(),
            font_size = 40,
            text = Get_text('game_return'),
            color = (1,0,1,0.5),
            background_normal = '',
            background_color = (0,1,0,0.5),
            on_press = return_board
        )
        Main_Window.add_widget(but)

def create_tips(a,b,board):
    list1 = find_fields(board,board[a][b].figure)
    field = Sizes.field_len
    r = field // 6
    color = [0, 1, 0, .8 ]
    if Game.color_do_hod_now != board[a][b].figure.color:
        color = [1, 0, 0, .8 ]
    if Game.state_game != 'one' and Game.color_do_hod_now != Game.play_by:
        color = [1,0,0,.8]
    with Main_Window.wid.canvas:
        Color(*color,mode='rgba')
    Game.tips_drawed = True if len(list1) != 0 else False

    for el in list1:
        x , y = el[0] , el[1]
        pos_x = Sizes.x_top_board + (x * 1.5 + 1) * field - r/2 
        pos_y = Sizes.y_top_board + (y+0.5) * Sizes.field_h + abs(5-x) * .5 * Sizes.field_h -r/2
        Main_Window.wid.canvas.add(Ellipse(
                    pos=[pos_x,pos_y],
                    size=(r,r)     ))

    with Main_Window.wid.canvas:
        Color(1,1,1,1,mode='rgba')
    
def delete_tips():
    if Game.tips_drawed :
        Main_Window.wid.canvas.clear()
        rect = Rectangle(source=Settings.get_board_picture(Game.type_of_chess),
            pos=[Sizes.x_top_board,Sizes.y_top_board],
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
            new_board[a][b].figure = Figure('white',0,0,'')
            new_board[a][b].figure.color = copy.copy(board[a][b].figure.color)
            new_board[a][b].figure.type = copy.copy(board[a][b].figure.type)

    return new_board

def is_chax(board,color):
    res = False
    for line in board:
        for field in line:
            if (field.figure.type == 'king') and (field.figure.color == color) and (field.attacked):
                res = True
    return res

def able_to_do_hod(board,color):
    Res = False
    for a in board:
        for field in a:
            if field.figure.type != 'empty' and field.figure.color == color:
                if find_fields(board,field.figure) != []:
                    Res = True
                    break
    return Res 

def taking_on_pass_glinskiy(board,figure):
    list_ = []
    x = figure.x
    y = figure.y
    if figure.color == 'white':
        d = 0
        if x > 4:
            d = 1
        if x != 10 and y == 4 + d :
            if board[x+1][4].figure.type == 'pawn':
                if board[x+1][4].figure.color != figure.color:
                    if board[x+1][4].figure.do_hod_now:
                        list_.append([x+1,5])
        d = 0
        if x < 6:
            d = 1
        if x != 0 and y == 4 + d :
            if board[x-1][4].figure.type == 'pawn':
                if board[x-1][4].figure.color != 'white':
                    if board[x-1][4].figure.do_hod_now:
                        list_.append([x-1,5])
    else:
        d = x+1
        if x >= 5:
            d = 5 - abs(5-x)
        if x != 10 and y == d  :
            if board[x+1][6 - abs(4 - x)].figure.type == 'pawn' :
                if board[x+1][6-abs(4-x)].figure.color != figure.color:
                    if board[x+1][6-abs(4-x)].figure.do_hod_now:
                        list_.append([x+1,5-abs(4-x)])
        d = x
        if x > 5:
            d = 11 - x
        if x != 0 and y == d:
            if board[x-1][6-abs(5-(x-1))].figure.type == 'pawn':
                if board[x-1][6-abs(6-x)].figure.color != figure.color:
                    if board[x-1][6-abs(6-x)].figure.do_hod_now:
                        list_.append([x-1,6-abs(6-x)])
    return list_

def taking_on_pass_kuej(board,figure):
    list_ = []
    x = figure.x
    y = figure.y
    if figure.color == 'white':
        d = 0
        if x > 4:
            d = 1
        if x != 10 and y == 4 + d :
            if board[x+1][5].figure.type == 'pawn':
                if board[x+1][5].figure.color != figure.color:
                    if board[x+1][5].figure.do_hod_now:
                        list_.append([x+1,6])
        d = 0
        if x < 6:
            d = 1
        if x != 0 and y == 4 + d :
            if board[x-1][5].figure.type == 'pawn':
                if board[x-1][5].figure.color != 'white':
                    if board[x-1][5].figure.do_hod_now:
                        list_.append([x-1,6])
    else:
        d = x + 1
        if x >= 5:
            d = 5 - abs(5-x)
        if x != 10 and y == d  :
            if board[x+1][5 - abs(4 - x)].figure.type == 'pawn' :
                if board[x+1][5-abs(4-x)].figure.color != figure.color:
                    if board[x+1][5-abs(4-x)].figure.do_hod_now:
                        list_.append([x+1,4-abs(4-x)])
        d = x 
        if x > 5:
            d = 11 - x
        if x != 0 and y == d:
            if board[x-1][5-abs(5-(x-1))].figure.type == 'pawn':
                if board[x-1][5-abs(6-x)].figure.color != figure.color:
                    if board[x-1][5-abs(6-x)].figure.do_hod_now:
                        list_.append([x-1,5-abs(6-x)])
    return list_

def find_fields(board,figure):
    time_list = figure.first_list(board)
    list2 = []
    if figure.type == 'pawn':
        if Game.type_of_chess == 'glinskiy':
            time_list += taking_on_pass_glinskiy(board,figure)
        else:
            time_list += taking_on_pass_kuej(board,figure)
    for element in time_list:
        board2 = copy_board(board)
        for a in board2:
            for b in a:
                b.attacked = False      
        #как будто был сделан туда ход, и нет ли шаха королю ходящего цвета
        board2[figure.x][figure.y].figure.type = 'empty'
        board2[figure.x][figure.y].figure.color = ''
        board2[element[0]][element[1]].figure.type = copy.copy(figure.type)
        board2[element[0]][element[1]].figure.color = copy.copy(figure.color)
        
        for a in range(len(board)):
            for b in range(len(board[0])):
                if board2[a][b].figure.type != 'empty':
                    if board2[a][b].figure.color != Game.color_do_hod_now:
                        if board2[a][b].figure.type == board[a][b].figure.type:
                            board2 = board[a][b].figure.do_attack(board2)

        if not is_chax(board2,Game.color_do_hod_now):
            list2.append(element)
    return list2

def is_end_of_game(board):
    is_mate = False
    board2 = copy_board(board)
    for x in range(len(board)):
        for y in range(len(board[0])):
            if board2[x][y].figure.color != Game.color_do_hod_now:
                board2 = board[x][y].figure.do_attack(board2)
    if Game.color_do_hod_now == 'white':
        if is_chax(board2,'white'):
            if not able_to_do_hod(board,'white'):
                is_mate = True
                interfase.do_info(Get_text('game_white_mate'))
            else:
                interfase.do_info(Get_text('game_white_chax'))
    else:
        if is_chax(board2,'black'):
            if not able_to_do_hod(board,'black'):
                interfase.do_info(Get_text('game_black_mate'))
                is_mate = True
            else:
                interfase.do_info(Get_text('game_black_chax') )   
    if not is_mate:
        if not able_to_do_hod(board,Game.color_do_hod_now):
            interfase.do_info(Get_text(description='game_pat',
                    params=Game.color_do_hod_now if Game.type_of_chess == 'glinskiy' else None))
            is_mate = True
    if is_mate :
        Game.ind = False
    if not Game.ind:
        if Game.with_time:
            Game.time.cancel()
    if Game.ind :
        if Game.color_do_hod_now == 'white' and Game.want_draw['black']:
            draw()
        elif  Game.color_do_hod_now == 'black' and Game.want_draw['white']:
            draw()
    del board2

def change_color(time=None):
    if Game.with_time:
        Game.time.cancel()
        if time != None:
            if Game.color_do_hod_now != Game.play_by:
                Game.players_time['white'] = int(time[0])
                Game.players_time['black'] = int(time[1])
        Game.time = Clock.schedule_interval(tick,1)
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

def do_hod(x,y,board):
    global choose_figure
    if (choose_figure.type != 'empty') and (choose_figure is board[x][y].figure):
        choose_figure = Figure('',0,0,'empty')
        gr_line.show_field(-1,y)
        Game.list_of_hod_field = []
        if Game.make_tips:
            delete_tips()
    elif (board[x][y].figure.type != 'empty') and (board[x][y].figure.color != Game.color_do_hod_now) \
           and not([x,y] in Game.list_of_hod_field):
        if Game.make_tips:
            delete_tips()
            create_tips(x,y,board)
    elif board[x][y].figure.color == Game.color_do_hod_now:
            choose_figure = board[x][y].figure
            Game.list_of_hod_field = find_fields(board,choose_figure)
            gr_line.show_field(x,y)
            if Game.make_tips:
                delete_tips()
                create_tips(x,y,board)
    elif choose_figure.type != 'empty' :
        if [x,y] in Game.list_of_hod_field:
            if Game.state_game != 'one' and Game.color_do_hod_now != Game.play_by:
                return  board
            board = move_figure(board,x,y)
    return board

def move_figure(board,x,y,options=None):
    global choose_figure
    Game.message = f'move {choose_figure.x} {choose_figure.y} {x} {y}'
    Music.move()
    if choose_figure.color == 'white':
        Game.made_moves += 1

    if choose_figure.type == 'pawn':
        a = -1
        if choose_figure.color == 'black':
            a = 1
        if x != choose_figure.x:
            if board[x][y].figure.type == 'empty':
                board[x][y+a].figure.destroy()

    a , b = choose_figure.x , choose_figure.y
    board[a][b].figure = Figure('',0,0,'empty')
    board[x][y].figure.destroy()
    board[x][y].figure = choose_figure
    board[x][y].figure.set_coords_on_board(x,y)

    if choose_figure.type == 'pawn' and abs(y-b) == 2:
        choose_figure.do_hod_now = True

    if choose_figure.type == 'pawn' and board[x][y].figure.pawn_on_last_line():
        if Game.state_game != 'one' and Game.color_do_hod_now != Game.play_by:
            n , m = choose_figure.x , choose_figure.y
            Game.board[n][m].figure.transform_to(options[1])
            choose_figure = Figure('',0,0,'empty')
            options = options[2:]
            change_color(options)
            is_end_of_game(board)
        else:
            do_transformation(Game.color_do_hod_now,x,y,options)
    else:
        if Game.state_game != 'one' and Game.color_do_hod_now == Game.play_by:
            Game.message += f" {Game.players_time['white']} {Game.players_time['black']}"
            Connection.messages += [Game.message]
            Game.message = ''
        choose_figure = Figure('',0,0,'empty')
        change_color(options)
        is_end_of_game(board)

    delete_tips()
    gr_line.show_field(x=-1,y=-1)
    Game.list_of_hod_field = []    
    for a in range(len(board)):
        for b in range(len(board[0])):
            if board[a][b].figure.type == 'pawn':
                if board[a][b].figure.color == Game.color_do_hod_now:
                    board[a][b].figure.do_hod_now = False
    return board

def in_gekso(x,y,Zx,Zy):
    # Z (point) - it is the left bottom angle of 6-angle
    # 6-angle - field, that I check
    if y < Zy or y > Zy + Sizes.field_h:
        return False
    if x < Zx - .5 * Sizes.field_len:
        return False
    if x > Zx + 1.5 * Sizes.field_len:
        return False
    x -= (Zx - .5 * Sizes.field_len)
    y -= Zy
    if x > Sizes.field_len :
        x = Sizes.field_len * 2 - x
    if y > Sizes.field_h // 2:
        y = Sizes.field_h - y
    if x >= Sizes.field_len:
        return True
    dx = .5 * Sizes.field_len - x
    return y > dx * 3**.5

def fit_field(event):
    e_x,e_y = event.x,event.y
    s = Sizes
    if e_x <= s.x_top_board or e_y <= s.y_top_board:
        return -1,-1
    elif (e_y >= s.y_top_board + s.board_size[0]) or (e_x >= s.x_top_board + s.board_size[0] ) :
        return -1,-1
    else:
        for i in range(11):
            for j in range(11+abs(5-i)):
                Zx = Sizes.x_top_board + .5 * (Sizes.board_size[0] - Sizes.field_len)
                Zy = Sizes.y_top_board + 0.5 * Sizes.field_h * abs(5-i) + j * Sizes.field_h
                Zx += (i-5) * 1.5 * Sizes.field_len
                if in_gekso(e_x,e_y,Zx,Zy):
                    return i,j
        return -1,-1

def do_transformation(color,x,y,options):

    def complete(ftype):
        global choose_figure
        x , y = choose_figure.x , choose_figure.y
        Game.board[x][y].figure.transform_to(ftype)
        choose_figure = Figure('',0,0,'empty')
        Main_Window.remove_widget(Game.bub)
        del Game.bub
        Game.need_change_figure = False
        if Game.state_game != 'one':
            Connection.messages += [Game.message + ' = ' + ftype + \
            f" {Game.players_time['white']} {Game.players_time['black']}"]
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
    size = Sizes

    wid = (-.5 + 1.5 * x) * size.field_len +size.x_top_board
    height = (1 + y) * size.field_h + size.y_top_board + abs(5-x) * .5 * size.field_h

    Game.bub = Bubble(
        pos = [wid,height],
        size=[3*Sizes.field_len]*2
    )
    box = GridLayout(rows=2,cols=2)
    if color == 'white':
        names = ['qw.png','bw.png','hw.png','rw.png']
    else:
        names = ['qb.png','bb.png','hb.png','rb.png']
    commands = [change_q,change_b,change_h,change_r]
    folder = Settings.get_folder()
    d = folder[-1]
    folder += 'pictures{0}fig_set1{0}'.format(d)
    for x in range(4):
        but = BubbleButton(
            text='',
            background_normal=folder + names[x],
            size=[Sizes.field_len]*2)
        but.bind(on_press=commands[x])
        box.add_widget(but)

    Game.bub.add_widget(box)
    Main_Window.add_widget(Game.bub)

def draw():
    if not Game.ind:
        return
    def no():
        Game.want_draw['black'] = False
        Game.want_draw['white'] = False
    
    def yes():
        Game.ind = False
        if Game.with_time:
            Game.time.cancel()
        interfase.do_info(Get_text('game_draw_ok'))

    Window(
            btn_texts=[Get_text('game_no'), Get_text('game_yes') ],
            btn_commands=[no,yes],
            text = Get_text('game_want_draw'),
            title = Get_text('game_draw_title'),
            size = [Sizes.board_size[0], .5 * Sizes.board_size[1] ],
            title_color = [.1,0,1,1],
            background_color = [.1,1,.1,.15]
    ).open()

def tick(cd):
    Game.players_time[Game.color_do_hod_now]-=1
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
    game.do_hod = do_hod
    game.color_do_hod_now = 'white'
    game.list_of_hod_field = []
    game.tips_drawed = False
    if game.with_time:
        game.time = Clock.schedule_interval(tick,1) 

    if game.type_of_chess == 'glinskiy':
        gen_glinskiy.init_chess(game)
    elif game.type_of_chess == 'kuej':
        gen_kuej.init_chess(game)
    return game

def surrend(click):
    if Game.ind == False:
        return
    def yes(press=None):
        Game.ind = False
        if Game.state_game == 'one':
            if Game.color_do_hod_now == 'white' :  
                f = Get_text('game_white_surrend')
            else :  
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
    
    if Game.made_moves <4 or (Game.made_moves == 3 and Game.color_do_hod_now == 'black'):
        create_message(Get_text('game_cant_surrend'))
    elif not Game.pause and not Game.need_change_figure and not Game.want_surrend:
        Game.want_surrend = True
        Window(
            btn_texts=[Get_text('game_want_surrend'),Get_text('game_not_surrend')],
            btn_commands=[yes,no],
            text = Get_text('game_agree?'),
            title = Get_text('game_press_surrend'),
            size = [Sizes.board_size[0], .5 * Sizes.board_size[1] ],
            title_color = [.1,0,1,1]
        ).open()

def create_interface(main_widget,app_size,Game):
    global interfase
    def set_draw(press):
        if Game.made_moves > 3 or (Game.color_do_hod_now == 'white' and Game.made_moves == 3):
            draw_message()
        else:
            create_message(Get_text('game_cant_draw'))
    
    interfase = interface.Graphical_interfase(Game,app_size, [back,pause,surrend,set_draw] )

    wid = Game_rect(size=app_size.board_size)
    rect = Rectangle(
            source=Settings.get_board_picture(Game.type_of_chess),
            pos=[app_size.x_top_board,app_size.y_top_board],
            size=app_size.board_size)
    wid.canvas.add(rect)
    main_widget.add_widget(wid)
    main_widget.wid = wid

def init_game():
    global choose_figure, gr_line, Figure
    global Game, Sizes, Main_Window
    Game = global_constants.game
    Sizes = global_constants.Sizes
    Main_Window = global_constants.Main_Window

    if Game.type_of_chess == 'kuej':
        Figure = kuej_figure.Figure
    else:
        Figure = glin_figure.Figure

    choose_figure = Figure('white',0,0,'empty')
    create_interface(Main_Window,Sizes,Game)
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
            text = str(text),
            title = Get_text('game_error'),
            size = [Sizes.board_size[0], .5 * Sizes.board_size[1] ],
            title_color = [.1,0,1,1]
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
            gr_line.show_field(-1,0)

    def no():
        Game.voyaje_message = False

    Game.voyaje_message = True
    Window(
        btn_texts=[Get_text(f'game_{i}') for i in ['no','yes'] ],
        btn_commands=[no,yes],
        text = Get_text('game_offer_draw?'),
        size = [Sizes.board_size[0], .5 * Sizes.board_size[1] ],
        title_color = [.1,0,1,1],
        title = Get_text('game_draw?')
    ).open()

def draw_board():
    rect = Rectangle(source=Settings.get_board_picture(Game.type_of_chess),
            pos=[Sizes.x_top_board,Sizes.y_top_board],
            size=Sizes.board_size)
    Main_Window.wid.canvas.add(rect)
    Game.tips_drawed = False
    for line in Game.board:
        for field in line:
            if field.figure.type != 'empty':
                Main_Window.wid.canvas.add(field.figure.rect)
    if choose_figure.type != 'empty':
        x,y = choose_figure.x,choose_figure.y
        gr_line.show_field(x,y)



