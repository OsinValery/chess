import global_constants
from kivy.clock import Clock
from kivy.utils import platform
import connection
import settings
from translater import Get_text
import Window_info

from all_chess_types import find_chess_module

import sovereign_chess
import chess
import bad_chess 



class Game():
    def __init__(self, version):
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
        self.test = not (platform in ['android', 'ios'])
        self.name1 = 'Player1'
        self.name2 = 'Player2'
        self.magia_moves = 10
        self.frozen_moves = 20
        self.version = version
        global_constants.game = self
        connection.Game = self

    def renew(self):
        self.with_time = False
        self.ind = False
        self.type_of_chess = ''
        self.time_mode = 0
        self.make_tips = False
        self.add_time = 0
        self.window = 'main'

    def start_play(self, settings):
        print(settings)
        """for game by network\n 
        it parse message and create game"""
        # it will run in addition thread in connection module
        data = settings.split('\n')
        self.type_of_chess = data[0].split(':')[1]
        self.play_by = data[1].split(':')[1]
        self.time_mode = int(data[2].split(':')[1])
        self.add_time = int(data[3].split(':')[1])
        self.make_tips = data[4].split(':')[1] == 't'
        if self.type_of_chess == 'magik':
            self.magia_moves = int(data[5].split(':')[1])
        if self.type_of_chess == 'fisher':
            self.position = data[5].split(':')[1]
        if self.type_of_chess == 'bad_chess':
            self.position = data[5].split(':')[1]

        if self.play_by == 'white':
            self.name1 = global_constants.Connection_manager.my_nick
            self.name2 = global_constants.Connection_manager.friend_nick
        else:
            self.name2 = global_constants.Connection_manager.my_nick
            self.name1 = global_constants.Connection_manager.friend_nick
        self.ind = True
        self.window = 'game'
        global_constants.Settings.change_sorting(self.type_of_chess)
        if self.time_mode != 0:
            self.with_time = True

        def start(time):
            """ error of thresds makes me create this function"""
            self.Game_logik = find_chess_module(self.type_of_chess).Game_logik()
            self.Game_logik.players_time = {'white': self.time_mode, 'black': self.time_mode}            
            global_constants.Main_Window.clear_widgets()
            global_constants.Main_Window.canvas.clear()
            self.Game_logik.init_game()

        Clock.schedule_once(start)

    def create_game(self, touch):
        main_widget = global_constants.Main_Window
        if self.type_of_chess == 'magik':
            player1 = main_widget.children[1].children[5].text
            player2 = main_widget.children[1].children[4].text
        elif self.type_of_chess == 'frozen':
            player1 = main_widget.children[1].children[5].text
            player2 = main_widget.children[1].children[4].text
        else:
            player1 = main_widget.children[1].children[4].text
            player2 = main_widget.children[1].children[3].text

        if player1 == '':
            self.name1 = 'Player1'
        else:
            self.name1 = player1
        if player2 == '':
            self.name2 = 'Player2'
        else:
            self.name2 = player2
        if self.name1 == self.name2:
            self.name2 += '2'
            self.name1 += '1'

        self.Game_logik = find_chess_module(self.type_of_chess).Game_logik()
        self.Game_logik.players_time = {'white': self.time_mode, 'black': self.time_mode}
        # send info about game to partner
        # if game in pair on different devices
        if self.state_game == 'host':
            text = self.Game_logik.get_game_config_message(self)
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
            global_constants.Connection_manager.send(text)

        self.ind = True
        main_widget.clear_widgets()
        main_widget.canvas.clear()
        self.window = 'game'
        settings.Settings.change_sorting(self.type_of_chess)
        self.Game_logik.init_game()

    def work_message(self, message):
        """ this function create game by message from partner \n
        also this work all messages at time of game"""
        # эта функция выполняется в потоке сетки
        if message[:4] == 'move':
            if self.type_of_chess == 'sovereign':
                def action(timeout):
                    sovereign_chess.work_network_message(message[5:])
                Clock.schedule_once(action)
                return
            data = message[5:].split()
            x0 = int(data[0])
            y0 = int(data[1])
            x1 = int(data[2])
            y1 = int(data[3])
            if not self.ind:
                return

            self.Game_logik.choose_figure = self.Game_logik.board[x0][y0].figure

            def movement(time_sec):
                options = data[4:]
                self.Game_logik.move_figure(self.Game_logik.board, x1, y1, options)

            Clock.schedule_once(movement)
        elif 'pause' in message:
            data = message[5:].split()

            def pause(time):
                if data[0] == 'on':
                    self.Game_logik.pause_command(1, True)
                elif self.ind:
                    self.Game_logik.return_board(1)
                try:
                    self.Game_logik.players_time['white'] = int(data[1])
                    self.Game_logik.players_time['black'] = int(data[2])
                except:
                    pass
            Clock.schedule_once(pause)
        elif 'surrend' in message:
            def surr_action():
                self.ind = False
                if self.with_time:
                    self.Game_logik.time.cancel()
                self.Game_logik.interfase.do_info(Get_text('game_friend_surrend'))
            Clock.schedule_once(surr_action)

        elif 'draw' in message:
            def draw_action():
                data = message[4:].split()
                if 'offer' in data:
                    if self.with_time:
                        self.Game_logik.time.cancel()

                    def no():
                        global_constants.Connection_manager.send('draw no')
                        if self.with_time:
                            self.Game_logik.time = Clock.schedule_interval(
                                self.Game_logik.tick, 1)
                        self.Game_logik.voyaje_message = False

                    def yes():
                        global_constants.Connection_manager.send('draw yes')
                        self.Game_logik.voyaje_message = False
                        self.ind = False
                        self.Game_logik.interfase.do_info(Get_text('game_draw_ok'))

                    self.Game_logik.voyaje_message = True
                    app_size = global_constants.Sizes
                    Window_info.Window(
                        btn_texts=[Get_text('game_'+i) for i in ['no', 'yes']],
                        btn_commands=[no, yes],
                        text=Get_text('game_want_draw'),
                        title=Get_text('game_draw_title'),
                        size=[app_size.board_size[0], .5 * app_size.board_size[1]],
                        title_color=[.1, 0, 1, 1],
                        background_color=[.1, 1, .1, .15]
                    ).open()

                elif 'yes' in data:
                    self.Game_logik.voyaje_message = False
                    self.ind = False
                    self.Game_logik.interfase.do_info(Get_text('game_draw_ok'))
                    self.Game_logik.draw_board()

                elif 'no' in data:
                    self.Game_logik.voyaje_message = False
                    if self.with_time:
                        self.Game_logik.time = Clock.schedule_interval(
                            self.Game_logik.tick, 1)
                    self.Game_logik.draw_board()
            
            Clock.schedule_once(draw_action)

        elif 'leave' in message and self.ind:
            self.ind = False
            app_size = global_constants.Sizes

            def draw(time):
                self.Game_logik.interfase.do_info(Get_text('game_leave'))
                def ok(arg=None):
                    pass
                Window_info.Window(
                    btn_texts=['ok'],
                    btn_commands=[ok],
                    text=Get_text('connection_leave'),
                    size=[app_size.board_size[0], .5 * app_size.board_size[1]],
                    title_color=[.1, 0, 1, 1],
                    title=''
                ).open()
            Clock.schedule_once(draw)

    def set_time(self, sec):
        self.time_mode = sec

    def set_add(self, par):
        self.add_time = par

    @property
    def save_data(self):
        data = self.type_of_chess + '\n'
        must = 'y' if self.with_time else 'n'
        data += f"{must} {self.Game_logik.players_time['white']} {self.Game_logik.players_time['black']}"
        must = 'y' if self.Game_logik.need_change_figure else 'n'
        data += f' {self.add_time}\n' + must + '\n'
        data += f'{self.Game_logik.made_moves} {self.magia_moves} {self.Game_logik.color_do_hod_now}\n'
        data += f'{self.name1}\n{self.name2}\n'
        x = len(self.Game_logik.board)
        y = len(self.Game_logik.board[0])
        must = 'y' if self.make_tips else 'n'
        data += f'{must} {x} {y} \n'
        for line in self.Game_logik.board:
            for field in line:
                data += field.figure.save_data
        if self.type_of_chess == 'sovereign':
            data += self.Game_logik.game_state.save_data
        return data

    def from_saves(self, data):
        self.type_of_chess = data[0]
        self.Game_logik = find_chess_module(self.type_of_chess).Game_logik()
        times = data[1].split()
        self.with_time = times[0] == 'y'
        self.Game_logik.players_time['white'] = int(times[1])
        self.Game_logik.players_time['black'] = int(times[2])
        self.add_time = int(times[-1])
        self.Game_logik.need_change_figure = data[2] == 'y'
        self.Game_logik.made_moves = int(data[3].split()[0])
        self.magia_moves = int(data[3].split()[1])
        self.name1 = data[4]
        self.name2 = data[5]
        self.make_tips = data[6].split()[0] == 'y'
        x, y = data[6].split()[1:]
        # width and height of board
        x, y = int(x), int(y)

        self.ind = True
        global_constants.Main_Window.clear_widgets()
        global_constants.Main_Window.canvas.clear()
        self.window = 'game'
        self.Game_logik.init_game()
        self.Game_logik.color_do_hod_now = data[3].split()[2]
        info = Get_text(f'game_{self.Game_logik.color_do_hod_now}_move')
        self.Game_logik.interfase.do_info(info)
        for line in self.Game_logik.board:
            for field in line:
                field.figure.destroy()
        n = 7
        for x1 in range(x):
            for y1 in range(y):
                self.Game_logik.board[x1][y1].figure.from_saves(data[n])
                n += 1
        if self.type_of_chess == 'sovereign':
            self.Game_logik.game_state.from_save_data(data[n:])
        if self.Game_logik.need_change_figure:
            fig = None
            for y1 in 0, y-1:
                for x1 in range(x):
                    if self.Game_logik.board[x1][y1].figure.type == 'pawn':
                        fig = self.Game_logik.board[x1][y1].figure
            if not fig is None:
                self.Game_logik.choose_figure = fig
                self.Game_logik.do_transformation(fig.color, fig.x, fig.y)
            else:
                self.Game_logik.need_change_figure = False

    def renew_game(self):
        self.ind = True
        global_constants.Main_Window.clear_widgets()
        global_constants.Main_Window.canvas.clear()
        self.window = 'game'
        settings.Settings.change_sorting(self.type_of_chess)
        self.Game_logik = find_chess_module(self.type_of_chess).Game_logik()
        self.Game_logik.players_time = {'white': self.time_mode, 'black': self.time_mode}
        self.Game_logik.init_game()




