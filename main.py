__version__ = '0.0.46'

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics import Rectangle
from kivy.uix.button import Button
from kivy.utils import platform
from round_button import RoundButton

import sizes
import global_constants
import settings
from translater import Get_text
from sounds import Music
import change_widget
import connection
import saved_games

import chess
import chess_los_alamos
import circle_chess
import gekso_chess
import garner
import week_chess
import magic_play
import kamikaze
import bad_chess
import rasing
import haotic
import schatranj

import time
import os


def find_chess_module(tip):
    if tip in [ 'classic','fisher','horse_battle','permutation','horde']:
        return chess
    elif tip == 'los_alamos':
        return chess_los_alamos
    elif tip in ['circle_chess','bizantion']:
        return circle_chess
    elif tip in ['glinskiy','kuej']:
        return gekso_chess
    elif tip == 'garner':
        return garner
    elif tip == 'week':
        return week_chess
    elif tip == 'magik':
        return magic_play
    elif tip == 'kamikadze':
        return kamikaze
    elif tip == 'bad_chess':
        return bad_chess
    elif tip == 'rasing':
        return rasing
    elif tip == 'haotic':
        return haotic
    elif tip == 'schatranj':
        return schatranj
    if game.test:
        print()
        print('you tryes to run undefined chess type!!!!!!')
        print('file main.py def find_chess_module')
        print()
    quit()


class Game():
    def __init__(self):
        self.do_hod = None
        self.fit_field = None
        self.window = 'main'
        # init default values
        self.renew()
        self.state_game = 'one'
        # one - game at one phone
        # host or user - at two devises as host or as client
        self.play_by = 'white'
        # color of that sample of app
        self.test = not (platform in ['android','ios'] )
        self.name1 = 'Player1'
        self.name2 = 'Player2'
        global_constants.game = self
        connection.Game = self

    def do_sf(self,touch):
        def draw():
            if self.color_do_hod_now == 'white' and self.want_draw['black']:
                return True
            if self.color_do_hod_now == 'black' and self.want_draw['white']:
                return True
            return False
        
        if self.ind and not self.need_change_figure and not self.pause and not \
            self.want_surrend and not draw() and not self.voyaje_message :
            x,y = self.fit_field(touch)
            if x != -1 and y != -1 :
                self.board = self.do_hod(x,y,self.board)   

    def renew(self):
        self.with_time = False
        self.ind = False
        self.type_of_chess = ''
        self.time_mode = 0
        self.players_time = {'white':-1,'black':-1}
        self.want_draw = {'white':False,'black':False}
        self.make_tips = False
        self.need_change_figure = False
        self.tips = []
        self.pause = False
        self.want_surrend = False
        self.voyaje_message = False
        self.add_time = 0
        self.made_moves = 0
        self.magia_moves = 10
        self.board = []
        self.window = 'main'

    def start_play(self,settings):
        """for game by network\n 
        it parse message and create game"""
        # it will run in addition thread in connection module
        data = settings.split('\n')
        self.type_of_chess = data[0].split(':')[1]
        self.play_by = data[1].split(':')[1]
        self.time_mode = int(data[2].split(':')[1] )
        self.add_time = int(data[3].split(':')[1] )
        self.make_tips = data[4].split(':')[1] == 't'
        if self.type_of_chess == 'magik':
            self.magia_moves = int(data[5].split(':')[1] )
        if self.type_of_chess == 'fisher':
            self.position = data[5].split(':')[1]
        if self.type_of_chess == 'bad_chess':
            self.position = data[5].split(':')[1]

        if self.play_by == 'white':
            self.name1 = connection.Connection.my_nick
            self.name2 = connection.Connection.friend_nick
        else:
            self.name2 = connection.Connection.my_nick
            self.name1 = connection.Connection.friend_nick  
        self.ind = True
        self.window = 'game' 
        self.players_time = {'white':self.time_mode,'black':self.time_mode}   
        if self.time_mode != 0:
            self.with_time = True
        def start(time):
            """ error of thresds makes me create this function"""  
            self.main_widget.clear_widgets()
            self.main_widget.canvas.clear()
            find_chess_module(self.type_of_chess).init_game()
        Clock.schedule_once(start)

    def create_game(self,touch):
        main_widget = global_constants.Main_Window
        if self.type_of_chess == 'magik':
            player1 = main_widget.children[1].children[5].text
            player2 = main_widget.children[1].children[4].text
        else:
            player1 = main_widget.children[1].children[4].text
            player2 = main_widget.children[1].children[3].text

        if player1 == '':   self.name1 = 'Player1'
        else:               self.name1 = player1
        if player2 == '':   self.name2 = 'Player2'
        else:               self.name2 = player2
        if self.name1 == self.name2:
            self.name2 += '2'
            self.name1 += '1'

        # send info about game to partner
        # if game in pair on different devices
        if self.state_game == 'host':
            text = f'start\ntype:{game.type_of_chess}\ncolor:'
            if self.play_by == 'white':
                text += 'black'
                self.name1 = connection.Connection.my_nick
                self.name2 = connection.Connection.friend_nick
            else:
                text += 'white'
                self.name2 = connection.Connection.my_nick
                self.name1 = connection.Connection.friend_nick
            text += f'\ntime:{self.time_mode}\nadd:{self.add_time}\ntips:'
            if self.make_tips: text += 't'
            else: text += 'f'
            if self.type_of_chess == 'magik':
                text += f'\nmagic:{self.magia_moves}'
            if self.type_of_chess == 'fisher':
                text += '\nposition:'
                pos = chess.fisher.gen_random_position()
                self.position = ''
                for figure in pos:
                    self.position += figure[0]
                text += self.position
            elif self.type_of_chess == 'bad_chess':
                text += '\nposition:'
                pos = bad_chess.bad_help.gen_random_position()
                self.position = ''
                for figure in pos:
                    self.position += figure[0]
                text += self.position
            connection.Connection.messages += [text]
        self.ind = True
        main_widget.clear_widgets()
        main_widget.canvas.clear()
        self.window = 'game'
        find_chess_module(self.type_of_chess).init_game()

    def work_message(self,message):
        """ this function create game by message from partner \n
        also this work all messages at time of game"""
        if message[:4] == 'move':
            data = message[5:].split()
            x0 = int(data[0])
            y0 = int(data[1])
            x1 = int(data[2])
            y1 = int(data[3])
            print(data)
            if not game.ind :
                return
            find_chess_module(self.type_of_chess).choose_figure = self.board[x0][y0].figure
            def movement(time_sec):
                options = data[4:]
                self.board = find_chess_module(self.type_of_chess).move_figure(self.board,x1,y1,options)
            Clock.schedule_once(movement)
        elif 'pause' in message:
            data = message[5:].split()
            def pause(time):
                if data[0] == 'on':
                    find_chess_module(self.type_of_chess).pause(1)
                else:
                    find_chess_module(self.type_of_chess).return_board(1)
                self.players_time['white'] = int(data[1])
                self.players_time['black'] = int(data[2])
            Clock.schedule_once(pause)
        elif 'surrend' in message:
            self.ind = False
            if self.with_time:
                self.time.cancel()
            text = Get_text('game_friend_surrend')
            find_chess_module(self.type_of_chess).interfase.do_info(text)
        elif 'draw' in message:
            data = message[4:].split()
            if 'offer' in data:
                if self.with_time:
                    self.time.cancel()
                def no():
                    connection.Connection.messages += ['draw no']
                    if self.with_time:
                        self.time = Clock.schedule_interval(find_chess_module(self.type_of_chess).tick,1)
                    self.voyaje_message = False

                def yes():
                    connection.Connection.messages += ['draw yes']
                    self.voyaje_message = False
                    self.ind = False
                    find_chess_module(self.type_of_chess).interfase.do_info(Get_text('game_draw_ok'))

                self.voyaje_message = True
                find_chess_module(self.type_of_chess).Window(
                    btn_texts=[Get_text('game_'+i) for i in ['no', 'yes']],
                    btn_commands=[no,yes],
                    text = Get_text('game_want_draw'),
                    title=Get_text('game_draw_title'),
                    size = [app_size.board_size[0], .5 * app_size.board_size[1] ],
                    title_color = [.1,0,1,1],
                    background_color = [.1,1,.1,.15]
                ).open()
            
            elif 'yes' in data:
                self.voyaje_message = False
                self.ind = False
                find_chess_module(self.type_of_chess).interfase.do_info(Get_text('game_draw_ok'))
                find_chess_module(self.type_of_chess).draw_board()
            
            elif 'no' in data:
                self.voyaje_message = False
                if self.with_time:
                    self.time =  Clock.schedule_interval(find_chess_module(self.type_of_chess).tick,1)
                find_chess_module(self.type_of_chess).draw_board()

        elif 'leave' in message and self.ind:
            self.ind = False
            def draw(time):
                find_chess_module(self.type_of_chess).interfase.do_info(Get_text('game_leave'))
                def ok(arg=None):
                    pass
                find_chess_module(self.type_of_chess).Window(
                    btn_texts=['ok' ],
                    btn_commands=[ok],
                    text = Get_text('connection_leave'),
                    size = [app_size.board_size[0], .5 * app_size.board_size[1] ],
                    title_color = [.1,0,1,1],
                    title = ''
                ).open()
            Clock.schedule_once(draw)

    def set_time(self,sec):
        self.players_time = {'white':sec,'black':sec}
        self.time_mode = sec

    def set_add(self,par):
        self.add_time = par
    @property
    def save_data(self):
        data = self.type_of_chess + '\n'
        must = 'y' if self.with_time else 'n'
        data += f"{must} {self.players_time['white']} {self.players_time['black']}"
        must = 'y' if self.need_change_figure else 'n'
        data += f' {self.add_time}\n' + must + '\n'
        data += f'{self.made_moves} {self.magia_moves} {self.color_do_hod_now}\n'
        data += f'{self.name1}\n{self.name2}\n'
        x = len(self.board)
        y = len(self.board[0])
        must = 'y' if self.make_tips else 'n'
        data += f'{must} {x} {y} \n'
        for line in self.board:
            for field in line:
                data += field.figure.save_data

        return data

    def from_saves(self,data):
        self.type_of_chess = data[0]
        times = data[1].split()
        self.with_time = times[0] == 'y'
        self.players_time['white'] = int(times[1])
        self.players_time['black'] = int(times[2])
        self.add_time = int(times[-1])
        self.need_change_figure = data[2] == 'y'
        self.made_moves = int(data[3].split()[0])
        self.magia_moves = int(data[3].split()[1])
        self.name1 = data[4]
        self.name2 = data[5]
        self.make_tips = data[6].split()[0] == 'y'
        x,y = data[6].split()[1:]
        # width and height of board
        x, y = int(x), int(y)

        self.ind = True
        self.main_widget.clear_widgets()
        self.main_widget.canvas.clear()
        self.window = 'game'
        find_chess_module(self.type_of_chess).init_game()
        self.color_do_hod_now = data[3].split()[2]
        info = Get_text(f'game_{self.color_do_hod_now}_move')
        find_chess_module(self.type_of_chess).interfase.do_info(info)
        for line in self.board:
            for field in line:
                field.figure.destroy()
        n = 7
        for x1 in range(x):
            for y1 in range(y):
                self.board[x1][y1].figure.from_saves(data[n])
                n += 1
        if self.need_change_figure:
            fig = None
            for y1 in 0, y-1:
                for x1 in range(x):
                    if self.board[x1][y1].figure.type == 'pawn':
                        fig = self.board[x1][y1].figure
            find_chess_module(self.type_of_chess).choose_figure = fig
            find_chess_module(self.type_of_chess).do_transformation(
                fig.color, fig.x, fig.y
            )


class GameWidget(Widget):
    def __init__(self,**kwargs):
        super(GameWidget,self).__init__(**kwargs)
        game.main_widget = self
        global_constants.Main_Window = self
        def back_button(window,key,*arg):
            if key in [27, 1001]:
                if game.window == 'settings_app':
                    settings.back(1)
                    game.window = 'main'
                elif game.window == 'menu':
                    self.create_start_game(1)
                elif game.window == 'chess_chooser':
                    for el in self.children:
                        if type(el) == change_widget.Chess_menu:
                            el.create_interface(1)
                elif game.window == 'settings':
                    # it is settings before the game
                    self.set_change(1)

                return True
            else:
                pass

        Window.bind(on_keyboard=back_button)
        self.create_start_game()

    def create_start_game(self,touch=None):
        self.clear_widgets()
        self.canvas.clear()
        game.window = 'main'
        size = app_size.window_size
        # background texture
        self.canvas.add(Rectangle(source=settings.Settings.get_bace_picture(),size = size))
        # button's params
        colors = [ (0.7,0,0.7,0.5), (.5,.3,.7,.4), (.5,.3,.7,.4),
                    (.5,.3,.7,.4), (.5,.3,.7,.4)]
        texts = [
            Get_text('all_start'),    Get_text('bace_settings'),
            Get_text('bace_saved'),   Get_text('connection_friend'),
            Get_text('bace_exit')
        ]
        def to_settings(par=None):
            game.window = 'settings_app'
            settings.create_interface(par)

        commands = [
            self.set_change,
            to_settings,
            self.to_saves,
            self.to_connection,
            close
        ]

        # button's shape
        [width,height] = [.57 * size[0], .45 * size[1]]
        pos = [.25 * size[0],.25 * size[1]]
        spacing = 30
        h = height / 5

        for i in range(5):
            self.add_widget(RoundButton(
                text = texts[i],
                size = [width,h-spacing],
                pos = [pos[0],pos[1]+height-(i+1)*h],
                on_press =  commands[i],
                font_size = 35,
                color = (0,3,0,10),
                background_color = colors[i]
            ))

    def set_change(self,touch):
        self.clear_widgets()
        self.canvas.clear()
        game.window = 'menu'        
        size = app_size.window_size
        self.canvas.add(Rectangle(source=settings.Settings.get_bace_picture(),size = size))
        but = Button(
            text=Get_text('all_back'),
            pos = [size[0]*0.8,size[1]*0.9],
            size = [size[0]*0.2,size[1]*0.07],
            background_color = (1,0.2,1,0.5),
            font_size = 20,
            color=(0,1,0.1,1),
            on_press=self.create_start_game
        )
        self.add_widget(but)
        self.add_widget(change_widget.Chess_menu())

    def to_connection(self,click):
        self.canvas.clear()
        game.window = 'connection'
        self.clear_widgets()
        self.add_widget(connection.server_widget(self.size,self))

    def to_saves(self,click):
        if game.state_game != 'one':
            return
        self.clear_widgets()
        self.canvas.clear()
        size = app_size.window_size
        self.canvas.add(Rectangle(
            source=settings.Settings.get_bace_picture(),
            size = size
        ))
        but = Button(
            text=Get_text('all_back'),
            pos = [size[0]*0.8,size[1]*0.9],
            size = [size[0]*0.2,size[1]*0.07],
            background_color = (1,0.2,1,0.5),
            font_size = 20,
            color=(0,1,0.1,1),
            on_press=self.create_start_game
        )
        self.add_widget(but)
        self.add_widget(saved_games.Saved_games(
            size=[.8 * size[0], .6 * size[1]],
            pos=[.1 * size[0], .05 * size[1]]
        ))

    def __del__(self):
        if 'wid' in dir(self):
            del self.wid
        self.canvas.clear()
        self.clear_widgets()


class GameApp(App):
    def build(self):
        settings.Settings.set_folder(self.directory)
        settings.Settings.user_folder = self.user_data_dir
        settings.Settings.read_settings()
        self.title = Get_text('bace_title_app')
        self.icon = 'icon.png'
        wid = GameWidget()
        self.bind(on_start=self.after_start)
        return wid  

    def after_start(self,par=None):
        def test(time=1):
            Music.create()
        Clock.schedule_once(test,1.5)
        if not 'Saves' in os.listdir(self.user_data_dir):
            os.mkdir(os.path.join(self.user_data_dir,'Saves'))

    def stop(self):
        if connection.Connection.state == 1:
            connection.Connection.messages += ['exit']
            time.sleep(2)
        if settings.settings_widget in game.main_widget.children:
            settings.back(1)
        if game.type_of_chess != '':
            if 'wid' in dir(game.main_widget):
                find_chess_module(game.type_of_chess).back(1)
        if 'wid' in dir(game.main_widget):
            game.main_widget.wid.clear_widgets()
            game.main_widget.wid.canvas.clear()
            del game.main_widget.wid
        game.main_widget.clear_widgets()
        game.main_widget.canvas.clear()
        super(GameApp,self).stop()

def close(click):
    if connection.Connection.state == 1:
        connection.Connection.messages = ['exit']
        time.sleep(2)
    Music.stop()
    myapp.stop()


game = Game()
app_size = sizes.Size()
myapp = GameApp()
myapp.run()