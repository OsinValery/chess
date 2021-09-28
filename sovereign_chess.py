
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Ellipse, Color, Line
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
import core_game_logik
import sovereign

import sovereign_figure
Figure = sovereign_figure.Figure


class Game_logik(core_game_logik.CoreGameLogik):
    def __init__(self) -> None:
        super().__init__()
        self.game_state = None

    def init_game(self):
        Main_Window = global_constants.Main_Window
        self.create_interface(Main_Window, global_constants.Sizes)
        global_constants.current_figure_canvas = Main_Window.wid.canvas
        self.build_game()
        self.choose_figure = self.Figure('white', 0, 0, 'empty')        
        self.green_line = Green_line()
        self.green_line.get_canv(Main_Window.wid.canvas)

    def create_interface(self, main_widget, app_size):
        def set_draw(press):
            if not global_constants.game.ind:
                return
            if self.made_moves > 3 or (self.color_do_hod_now == 'white' and self.made_moves == 3):
                draw_message()
            else:
                create_message(Get_text('game_cant_draw'))

        self.interfase = interface.Graphical_interfase(
            global_constants.game, app_size, [back, self.pause_command, self.surrend, set_draw])

        wid = Game_rect(size=app_size.virtual_board_size)
        wid.canvas.add(Rectangle(
            source=Settings.get_board_picture(global_constants.game.type_of_chess),
            size=app_size.virtual_board_size))
        scroll = ScrollView(
            size = global_constants.Sizes.board_size,
            pos = [global_constants.Sizes.x_top_board, 
                    global_constants.Sizes.y_top_board],
        )
        scroll.add_widget(wid)
        wid.size_hint = [None] * 2
        main_widget.add_widget(scroll)
        main_widget.wid = wid
        Sizes = global_constants.Sizes
        main_widget.add_widget(sovereign.Color_dropDown(
            pos =  [Sizes.window_size[0]*0.4,Sizes.window_size[1]*.93],
            size=(Sizes.window_size[0]*0.16,Sizes.window_size[1]*0.07)
        ))

    def build_game(self):
        super().build_game()
        self.Figure = sovereign_figure.Figure
        self.board = sovereign.create_start_game_board()
        self.game_state = sovereign.Game_State()

    def is_chax(self, board, player):
        res = False
        for a in range(16):
            for b in range(16):
                if (board[a][b].figure.type == 'king') and (board[a][b].attacked):
                    if self.game_state.get_owner(board[a][b].figure.color) == player:
                        res = True
                        break
        return res

    def tick(self, cd):
        self.players_time[self.color_do_hod_now] -= 1
        self.interfase.set_time(self.players_time)
        if self.players_time[self.color_do_hod_now] == 0:
            global_constants.game.ind = False
            Music.time_passed()
            text = Get_text('game_end_time') + '!\n'
            if self.color_do_hod_now == 'white':
                text += Get_text('game_lose_of',[1])
            else:
                text += Get_text('game_lose_of',[2])
            self.interfase.do_info(text)
            self.time.cancel()

    def change_color(self, time=None):
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
                self.interfase.do_info(Get_text('game_move_of',[2]))
            self.color_do_hod_now = 'black'
        elif self.color_do_hod_now == 'black':
            if global_constants.game.ind:
                self.interfase.do_info(Get_text('game_move_of',[1]))
            self.color_do_hod_now = 'white'
        if global_constants.game.with_time:
            self.interfase.set_time(self.players_time)

    def return_board(self, press):
        super().return_board(press)
        with global_constants.Main_Window.wid.canvas:
            Color(0,1,0,1)
            global_constants.Main_Window.wid.canvas.add(self.green_line)
            Color(1,1,1,1)

    def create_tips(self, a, b, board):
        list1 = self.find_fields(board, board[a][b].figure)
        Sizes = global_constants.Sizes
        field = Sizes.field_size
        color = [0, 1, 0, .8]
        if self.color_do_hod_now != self.game_state.get_owner(board[a][b].figure.color):
            color = [1, 0, 0, .8]
        if global_constants.game.state_game != 'one' and self.color_do_hod_now != global_constants.game.play_by:
            color = [1, 0, 0, .8]
        r = Sizes.field_size // 6
        with global_constants.Main_Window.wid.canvas:
            Color(*color, mode='rgba')
        for el in list1:
            self.tips_drawed = True
            x, y = el[0], el[1]
            global_constants.Main_Window.wid.canvas.add(Ellipse(
                pos=[Sizes.x_top - r/2 + (x+0.5)*field, Sizes.y_top - r/2 + (y+0.5)*field],
                size=[r, r]))
        with global_constants.Main_Window.wid.canvas:
            Color(1, 1, 1, 1, mode='rgba')

    def delete_tips(self):
        if self.tips_drawed:
            global_constants.Main_Window.wid.canvas.clear()
            Sizes = global_constants.Sizes
            with global_constants.Main_Window.wid.canvas:
                Rectangle(
                    source=Settings.get_board_picture(global_constants.game.type_of_chess),
                    size=Sizes.virtual_board_size)
            self.tips_drawed = False
            for x in range(16):
                for y in range(16):
                    if self.board[x][y].figure.type != 'empty':
                        global_constants.Main_Window.wid.canvas.add(self.board[x][y].figure.rect)
            with global_constants.Main_Window.wid.canvas:
                Color(0,1,0,1)
                global_constants.Main_Window.wid.canvas.add(self.green_line)
                Color(1,1,1,1)

    def surrend(self, click):
        if not global_constants.game.ind:
            return

        def yes():
            global_constants.game.ind = False
            if global_constants.game.state_game == 'one':
                if self.color_do_hod_now == 'white':
                    f = Get_text('game_surrend_of',[1])
                else:
                    f = Get_text('game_surrend_of',[2])
            else:
                f = Get_text('game_you_surrend')
            self.interfase.do_info(f)
            if global_constants.game.with_time:
                self.time.cancel()
            if global_constants.game.state_game != 'one':
                Connection.messages += ['surrend']

        def no():
            self.want_surrend = False

        if self.made_moves < 4 or (self.made_moves == 3 and self.color_do_hod_now == 'black'):
            create_message(Get_text('game_cant_surrend'))
        elif not self.pause and not self.need_change_figure and not self.want_surrend:
            self.want_surrend = True
            Sizes = global_constants.Sizes
            Window(
                btn_texts=[Get_text('game_want_surrend'),
                        Get_text('game_not_surrend')],
                btn_commands=[yes, no],
                text=Get_text('game_agree?'),
                title=Get_text('game_press_surrend'),
                size=[Sizes.board_size[0], .5 * Sizes.board_size[1]],
                title_color=[.1, 0, 1, 1]
            ).open()

    def able_to_do_hod(self, board, player):
        for a in board:
            for field in a:
                if field.figure.type != 'empty' and self.game_state.get_owner(field.figure.color) == player:
                    if self.find_fields(board, field.figure) != []:
                        return True   
        return False

    def find_fields(self, board, figure:Figure):
        time_list = figure.first_list(board,self.game_state)
        if figure.type == 'king':
            time_list += sovereign.find_rocking(figure,board,self.game_state.copy())
        list2 = []
        for element in time_list:
            board2 = sovereign.copy_board(board)
            new_state = self.game_state.copy()
            new_state.check_control([figure.x,figure.y,*element],figure.color)

            # как будто был сделан туда ход, и нет ли шаха королю ходящего цвета
            board2[figure.x][figure.y].figure.type = 'empty'
            board2[figure.x][figure.y].figure.color = ''
            board2[element[0]][element[1]].figure.type = copy.copy(figure.type)
            board2[element[0]][element[1]].figure.color = copy.copy(figure.color)

            for a in range(16):
                for b in range(16):
                    if board2[a][b].figure.type != 'empty':
                        if new_state.get_owner(board2[a][b].figure.color) != self.color_do_hod_now:
                            if board2[a][b].figure.type == board[a][b].figure.type:
                                board2 = board[a][b].figure.do_attack(board2,new_state)

            if not self.is_chax(board2, self.color_do_hod_now):
                list2.append(element)
        # if check and figure == pawn on the prelast line, figure may be changed to king
        if figure.type == 'pawn' and figure.pawn_on_penultimate_line:
            board2 = sovereign.copy_board(board)
            for a in range(16):
                for b in range(16):
                    if board2[a][b].figure.type != 'empty':
                        if self.game_state.get_owner(board2[a][b].figure.color) != self.color_do_hod_now:
                            board2 = board[a][b].figure.do_attack(board2,self.game_state)
            if self.is_chax(board2, self.color_do_hod_now):
                # at that time important movement may be lost
                movements = figure.first_list(board,self.game_state)
                fig2 = self.Figure(figure.color,figure.x,figure.y,'empty')
                fig2.type = figure.type
                for el in movements:
                    fig2.x, fig2.y = el
                    if fig2.pawn_on_last_line():
                        board2 = sovereign.copy_board(board)
                        new_state = self.game_state.copy()
                        new_state.check_control([figure.x,figure.y,el[0],el[1]],figure.color)
                        board2[figure.x][figure.y].type = 'empty'
                        board2[figure.x][figure.y].color = ''
                        
                        # check color of king and correct it in new_state
                        if self.game_state.get_owner(figure.color) == 'white':
                            old_color = self.game_state.white_player
                        else:
                            old_color = self.game_state.black_player
                        for a in range(16):
                            for b in range(16):
                                if board2[a][b].figure.type == 'king':
                                    if board2[a][b].figure.color == old_color:
                                        board2[a][b].figure.type = 'empty'
                                        board2[a][b].figure.color = ''     
                        board2[el[0]][el[1]].figure.type = 'king'  
                        board2[el[0]][el[1]].figure.color = figure.color
                        new_state.update_player_color(old_color,figure.color,board2)
                        # check board
                        for a in range(16):
                            for b in range(16):
                                if board2[a][b].figure.type != 'empty':
                                    if new_state.get_owner(board2[a][b].figure.color) != self.color_do_hod_now:
                                        if board2[a][b].figure.type == board[a][b].figure.type:
                                            board2 = board[a][b].figure.do_attack(board2,new_state)

                        if not self.is_chax(board2, self.color_do_hod_now):
                            list2.append(element)
        return list2

    def is_end_of_game(self, board):
        is_mate = False
        board2 = sovereign.copy_board(board)
        for x in range(16):
            for y in range(16):
                if self.game_state.get_owner(board2[x][y].figure.color) != self.color_do_hod_now:
                    board2 = board[x][y].figure.do_attack(board2,self.game_state)
        if self.color_do_hod_now == 'white':
            if self.is_chax(board2, 'white'):
                if not self.able_to_do_hod(board, 'white'):
                    is_mate = True
                    self.interfase.do_info(Get_text('game_mate_to',[1]))
                else:
                    self.interfase.do_info(Get_text('game_chax_to',[1]))
        else:
            if self.is_chax(board2, 'black'):
                if not self.able_to_do_hod(board, 'black'):
                    self.interfase.do_info(Get_text('game_mate_to',[2]))
                    is_mate = True
                else:
                    self.interfase.do_info(Get_text('game_chax_to',[2]))

        if not is_mate:
            if not self.able_to_do_hod(board, self.color_do_hod_now):
                print('try to change interface info')
                self.interfase.do_info(Get_text('game_pat', params=None))
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

    def do_hod(self, x, y, board):
        if (self.choose_figure.type != 'empty') and (self.choose_figure is board[x][y].figure):
            # кликнули на выбранную фигуру
            if self.choose_figure.type == 'king':
                desertion(x,y,board)
            else:
                self.choose_figure = self.Figure('', 0, 0, 'empty')
                self.green_line.show_field(-1, y)
                self.list_of_hod_field = []
                if global_constants.game.make_tips:
                    self.delete_tips()
        elif (board[x][y].figure.type != 'empty') and (self.game_state.get_owner(board[x][y].figure.color) != self.color_do_hod_now) and not([x, y] in self.list_of_hod_field):
            # попросить подсказку хода для врага
            if global_constants.game.make_tips:
                self.delete_tips()
                self.create_tips(x, y, board)
        elif self.game_state.get_owner(board[x][y].figure.color) == self.color_do_hod_now:
            # выбрать фигуру
            self.choose_figure = board[x][y].figure
            self.list_of_hod_field = self.find_fields(board, self.choose_figure)
            self.green_line.show_field(x, y)
            if global_constants.game.make_tips:
                self.delete_tips()
                self.create_tips(x, y, board)
        elif self.choose_figure.type != 'empty':
            # move figure
            if [x, y] in self.list_of_hod_field:
                if global_constants.game.state_game != 'one' and self.color_do_hod_now != global_constants.game.play_by:
                    return board
                board = self.move_figure(board, x, y)
        return board

    def move_figure(self, board, x, y, options=None):
        self.message = f'move {self.choose_figure.x} {self.choose_figure.y} {x} {y}'
        Music.move()
        if self.choose_figure.color == 'white':
            self.made_moves += 1

        a, b = self.choose_figure.x, self.choose_figure.y
        self.game_state.check_control([a,b,x,y],self.choose_figure.color)
        board[a][b].figure = self.Figure('', 0, 0, 'empty')
        board[x][y].figure.destroy()
        board[x][y].figure = self.choose_figure
        board[x][y].figure.set_coords_on_board(x, y)
        if board[x][y].figure.type == 'king':
            sovereign.do_rocking(a,b,x,y,board)
        board[x][y].figure.do_hod_before = True

        if self.choose_figure.type == 'pawn' and board[x][y].figure.pawn_on_last_line():
            if global_constants.game.state_game != 'one' and self.color_do_hod_now != global_constants.game.play_by:
                n, m = self.choose_figure.x, self.choose_figure.y
                self.board[n][m].figure.transform_to(options[1])
                if options[1] == 'king':
                    transform_to_king(n,m,board)
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
            self.choose_figure = Figure('', 0, 0, 'empty')
            self.change_color(options)
            self.is_end_of_game(board)

        self.delete_tips()
        self.green_line.show_field(x=-1, y=-1)
        self.list_of_hod_field = []
        return board

    def do_transformation(self, color, x, y, options=None):
        def complete(ftype):
            x, y = self.choose_figure.x, self.choose_figure.y
            self.board[x][y].figure.transform_to(ftype)
            if ftype == 'king':
                transform_to_king(x,y,self.board)
            self.choose_figure = self.Figure('', 0, 0, 'empty')
            global_constants.Main_Window.remove_widget(self.bub)
            del self.bub
            self.need_change_figure = False
            if global_constants.game.state_game != 'one':
                self.message += ' = ' + ftype
                self.message += f" {self.players_time['white']} {self.players_time['black']}"
                Connection.messages += [self.message]
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
        
        def change_k(click):
            complete('king')

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
            padding=[Sizes.field_size*0.05]*4
        )
        d = os.path.sep
        folder = Settings.get_folder() + f'pictures{d}fig_set1{d}'
        commands = []
        names = []

        # if check, pawn must be transformed to king
        new_board = sovereign.copy_board(self.board)
        for a in range(16):
            for b in range(16):
                if self.game_state.get_owner(new_board[a][b].figure.color) != color:
                    new_board = self.board[a][b].figure.do_attack(new_board,self.game_state)
        if not self.is_chax(new_board,self.color_do_hod_now):
            if color == 'white':
                names = ['qw.png', 'bw.png', 'hw.png', 'rw.png']
            else:
                names = ['qb.png', 'bb.png', 'hb.png', 'rb.png']
            commands = [change_q, change_b, change_h, change_r]
        
        # add king
        new_board = sovereign.copy_board(self.board)
        for a in range(16):
            for b in range(16):
                if new_board[a][b].figure.type == 'king':
                    if self.game_state.get_owner(new_board[a][b].figure.color) == color:
                        new_board[a][b].figure.color = ''
                        new_board[a][b].figure.type = 'empty'
        new_board[x][y].figure.type = 'king'
        for a in range(16):
            for b in range(16):
                if self.game_state.get_owner(new_board[a][b].figure.color) != color:
                    new_board = self.board[a][b].figure.do_attack(new_board,self.game_state)
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

        self.bub.add_widget(box)
        global_constants.Main_Window.add_widget(self.bub)


    def fit_field(self, event):
        x, y = 0, 0
        e_x, e_y = event.x, event.y
        s = global_constants.Sizes
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

class Game_rect(Widget):
    def on_touch_down(self, touch):
        global_constants.game.Game_logik.do_sf(touch)

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
            Sizes = global_constants.Sizes
            pad_x = Sizes.x_top
            pad_y = Sizes.y_top
            pad = Sizes.field_size
            self.points = (
                pad_x + pad * x, pad_y + pad * y,
                pad_x + pad * (x+1), pad_y + pad * y,
                pad_x + pad * (x+1), pad_y + pad * (y+1),
                pad_x + pad * x, pad_y + pad * (y + 1)
            )



def desertion(x,y,board):
    game = global_constants.game
    colors = game.Game_logik.game_state.friend_colors(board[x][y].figure.color)
    result_colors = []
    if game.Game_logik.game_state.is_control_point(x,y):
        color = game.Game_logik.game_state.get_control_point_color([x,y])
        if color in colors:
            colors.remove(color)
    # check all colors on check
    # it is important!!!
    for color in colors:
        if color == board[x][y].figure.color:
            result_colors.append(color)
        else:
            new_board = sovereign.copy_board(board)
            new_state = game.Game_logik.game_state.copy()
            new_board[x][y].figure.color = color
            new_state.update_player_color(board[x][y].figure.color,color,new_board)
            for a in range(16):
                for b in range(16):
                    if new_state.get_owner(new_board[a][b].figure.color)!=game.Game_logik.color_do_hod_now:
                        new_board = board[a][b].figure.do_attack(new_board,new_state)
            if not game.Game_logik.is_chax(new_board,game.Game_logik.color_do_hod_now):
                result_colors.append(color)

    if len(result_colors) < 2:
        # skip green square and return
        game.Game_logik.choose_figure = game.Game_logik.Figure('', 0, 0, 'empty')
        game.Game_logik.green_line.show_field(-1, y)
        game.Game_logik.list_of_hod_field = []
        if game.make_tips:
            game.Game_logik.delete_tips()
        return

    # create interfase for changing, it is possible to do

    def change_color_player(color):
        color = color.text
        game.Game_logik.need_change_figure = False
        global_constants.Main_Window.remove_widget(bub)
        if color == board[x][y].figure.color:
            return
        game.Game_logik.game_state.update_player_color(board[x][y].figure.color,color,board)
        board[x][y].figure.change_color(color)
        for wid in global_constants.Main_Window.children:
            if type(wid) == sovereign.Color_dropDown:
                wid.update_state()

        if game.state_game != 'one':
            message = f'move {x} {y} {x} {y} = {color}'
            message += f" {game.Game_logik.players_time['white']} {game.Game_logik.players_time['black']}"
            Connection.messages += [message]
        game.Game_logik.choose_figure = game.Game_logik.Figure('', 0, 0, 'empty')
        game.Game_logik.change_color()
        game.Game_logik.delete_tips()
        game.Game_logik.green_line.show_field(x=-1, y=-1)
        game.Game_logik.list_of_hod_field = []

    sizes = global_constants.Sizes
    pos_x = sizes.x_top_board
    pos_y = sizes.y_top_board + .2 * sizes.board_size[1]
    grid = GridLayout(cols=4)
    bub = Bubble(
        pos = [pos_x, pos_y],
        size = [sizes.board_size[0], .6 * sizes.board_size[1]]
    )
    bub.add_widget(grid)
    global_constants.Main_Window.add_widget(bub)
    for color in result_colors:
        grid.add_widget(BubbleButton(
            text = color,
            color = (1,0,0,0),
            on_press = change_color_player,
            background_normal=sovereign.get_image_path(color),
            size_hint=[None,None],
            width=global_constants.Sizes.board_size[0] / grid.cols,
            height=bub.size[1] / (12 / grid.cols)
        ))
    game.Game_logik.need_change_figure = True

def transform_to_king(x,y,board):
    game = global_constants.game
    if board[x][y].figure.color == game.Game_logik.game_state.white_player:
        for a in range(16):
            for b in range(16):
                if [a,b] != [x,y]:
                    if board[a][b].figure.type == 'king':
                        if board[a][b].figure.color == game.Game_logik.game_state.white_player:
                            board[a][b].figure.destroy()
    elif board[x][y].figure.color == game.Game_logik.game_state.black_player:
        for a in range(16):
            for b in range(16):
                if [a,b] != [x,y]:
                    if board[a][b].figure.type == 'king':
                        if board[a][b].figure.color == game.Game_logik.game_state.black_player:
                            board[a][b].figure.destroy()
    else:
        color = board[x][y].figure.color
        if game.Game_logik.game_state.get_owner(color) == 'white':
            old_color = game.Game_logik.game_state.white_player
        else:
            old_color = game.Game_logik.game_state.black_player
        for a in range(16):
            for b in range(16):
                if board[a][b].figure.color == old_color:
                    if board[a][b].figure.type == 'king':
                        board[a][b].figure.destroy()
        game.Game_logik.game_state.update_player_color(old_color,color,board)

def work_network_message(message:str):
    Game = global_constants.game
    data = message.split()
    x0 = int(data[0])
    y0 = int(data[1])
    x1 = int(data[2])
    y1 = int(data[3])
    options = data[4:]
    if [x0,y0] != [x1,y1]:
        Game.Game_logik.choose_figure = Game.Game_logik.board[x0][y0].figure
        Game.Game_logik.board = Game.Game_logik.move_figure(Game.Game_logik.board, x1, y1, options)
    else:
        color = options[1]
        board = Game.Game_logik.board
        Game.Game_logik.game_state.update_player_color(board[x0][y0].figure.color,color,board)
        board[x0][y0].figure.change_color(color)
        Game.Game_logik.change_color(options[2:])
        Game.Game_logik.delete_tips()
        Game.Game_logik.green_line.show_field(x=-1, y=-1)
        Game.Game_logik.list_of_hod_field = []

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
            Connection.messages += ['draw offer']
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
        Connection.messages += ['leave']
    Game.renew()
    global_constants.Main_Window.canvas.clear()
    global_constants.Main_Window.create_start_game(touch)

