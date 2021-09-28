__version__ = '0.0.51'

import os
import time

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Rectangle
from kivy.uix.button import Button
from kivy.uix.widget import Widget

import sizes
import global_constants
import game as game_class
import saved_games
import settings
import connection
import change_widget
from round_button import RoundButton
from sounds import Music
from translater import Get_text

class GameWidget(Widget):
    def __init__(self, **kwargs):
        super(GameWidget, self).__init__(**kwargs)
        game.main_widget = self
        global_constants.Main_Window = self

        def back_button(window, key, *arg):
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

    def create_start_game(self, touch=None):
        self.clear_widgets()
        self.canvas.clear()
        game.window = 'main'
        size = app_size.window_size
        # background texture
        self.canvas.add(
            Rectangle(source=settings.Settings.get_bace_picture(), size=size))
        # button's params
        colors = [(0.7, 0, 0.7, 0.5), (.5, .3, .7, .4), (.5, .3, .7, .4),
                  (.5, .3, .7, .4), (.5, .3, .7, .4)]
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
        [width, height] = [.57 * size[0], .45 * size[1]]
        pos = [.25 * size[0], .25 * size[1]]
        spacing = 30
        h = height / 5

        for i in range(5):
            self.add_widget(RoundButton(
                text=texts[i],
                size=[width, h-spacing],
                pos=[pos[0], pos[1]+height-(i+1)*h],
                on_press=commands[i],
                font_size=35,
                color=(0, 3, 0, 10),
                background_color=colors[i]
            ))

    def set_change(self, touch):
        self.clear_widgets()
        self.canvas.clear()
        game.window = 'menu'
        size = app_size.window_size
        self.canvas.add(
            Rectangle(source=settings.Settings.get_bace_picture(), size=size))
        self.add_widget(Button(
            text=Get_text('all_back'),
            pos=[size[0]*0.8, size[1]*0.9],
            size=[size[0]*0.2, size[1]*0.07],
            background_color=(1, 0.2, 1, 0.5),
            font_size=20,
            font_name = settings.Settings.get_font(),
            color=(0, 1, 0.1, 1),
            on_press=self.create_start_game
        ))
        self.add_widget(change_widget.Chess_menu())

    def to_connection(self, click):
        self.canvas.clear()
        game.window = 'connection'
        self.clear_widgets()
        self.add_widget(connection.server_widget(self.size, self))

    def to_saves(self, click):
        if game.state_game != 'one':
            return
        self.clear_widgets()
        self.canvas.clear()
        size = app_size.window_size
        self.canvas.add(Rectangle(
            source=settings.Settings.get_bace_picture(),
            size=size
        ))
        self.add_widget(Button(
            text=Get_text('all_back'),
            pos=[size[0]*0.8, size[1]*0.9],
            size=[size[0]*0.2, size[1]*0.07],
            background_color=(1, 0.2, 1, 0.5),
            font_name = settings.Settings.get_font(),
            font_size=20,
            color=(0, 1, 0.1, 1),
            on_press=self.create_start_game
        ))
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

    def after_start(self, par=None):
        def test(time=1):
            Music.create()
        Clock.schedule_once(test, 2)
        if not 'Saves' in os.listdir(self.user_data_dir):
            os.mkdir(os.path.join(self.user_data_dir, 'Saves'))

    def stop(self):
        if connection.Connection.state == 1:
            connection.Connection.messages += ['exit']
            time.sleep(2)
        if settings.settings_widget in game.main_widget.children:
            settings.back(1)
        if 'wid' in dir(game.main_widget):
            global_constants.Main_Window.wid.clear_widgets()
            global_constants.Main_Window.wid.canvas.clear()
            del global_constants.Main_Window.wid
        global_constants.Main_Window.clear_widgets()
        global_constants.Main_Window.canvas.clear()
        super(GameApp, self).stop()


def close(click):
    if connection.Connection.state == 1:
        connection.Connection.messages = ['exit']
        time.sleep(2)
    Music.stop()
    myapp.stop()


game = game_class.Game(__version__)
app_size = sizes.Size()
myapp = GameApp()
myapp.run()

