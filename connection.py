import socket

from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.graphics import Rectangle, Color, RoundedRectangle, Line
from kivy.metrics import dp
from kivy.factory import Factory

from translater import Get_text
from settings import Settings
import global_constants
import network


class Text_line(TextInput):
    def __init__(self,changed,**kwargs):
        self.changed = changed
        self.multiline = False
        super(Text_line,self).__init__(**kwargs)
        self.bind(text=self.text_redact)

    def text_redact(self,wid,text):
        self.changed(text)


def create_error(message):
    pop = Popup()
    pop.title = 'Error '
    pop.auto_dismiss = False
    grid = GridLayout(cols = 1)
    grid.add_widget(Label(
        text = message,
        color = [1,0,0,1]
    ))
    grid.add_widget(Button(
        text = 'OK',
        color = [0,1,0,1],
        background_color = [1,1,0,1],
        size_hint = [1,None],
        on_press = lambda click:pop.dismiss()
    ))
    pop.add_widget(grid)
    pop.open()


class NotConnection_Widget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.padding = (dp(15), dp(10))
        size = (.92 * self.size[0], .55 * self.size[1])

        lab = Label(
            size=size,
            pos = self.pos,     
            text = Get_text('connection_wire_error'),             
            markup=True,
            text_size = [size[0] , None],
            halign = 'left',
            valign = 'center',
            padding = self.padding,
            color = [1,0,0,1]
        )
        lab._label.refresh()
        lab.size = lab._label.texture.size
        self.add_widget(lab)
        with self.canvas.before:
            Color(1,1,0,0.8)
            RoundedRectangle(
                pos=self.pos,
                size=lab._label.texture.size,
                radius=[(50, 50), (200, 200), (100, 100), (70, 70)]
            )
            Color(0.5, 0, 1, .5)
            Line(
                rounded_rectangle=(*self.pos, *lab._label.texture.size, *[70,100,200,50], 100),
                width=5
            )
            Color(1, 1, 1, 1)
        

class EmptyConnectionWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = global_constants.Sizes.window_size
        parent = global_constants.Main_Window
        texts = ['all_back', 'connection_create', 'connection_connect']
        poses = [
            [.7 * self.size[0],.05 * self.size[1]],
            [.3 * self.size[0], .7 * self.size[1]],
            [.3 * self.size[0], .55 * self.size[1]],
        ]
        sizes = [
            [.2 * self.size[0], .05 * self.size[1]],
            [.4 * self.size[0], .06 * self.size[1]],
            [.4 * self.size[0], .06 * self.size[1]],
        ]
        back_colors = [[.7,.1,.1,.6], [0.1, 1, .1 , 1], [0.1, 1, .1 , 1]]
        commands = (parent.create_start_game, self.create, self.connect)
        for i in range(len(commands)):
            self.add_widget(Button(
                text = Get_text(texts[i]),
                color = [1,1,0,1],
                pos = poses[i],
                size = sizes[i],
                background_normal = '',
                background_color = back_colors[i],
                on_press = commands[i]
            ))

    
    def create(self, press):
        """This function creates WIFI server Settings"""
        parent = global_constants.Main_Window
        parent.clear_widgets()
        try:
            global_constants.Connection_manager.server_ip = network.check_my_ip()
            if '127.0.0' in global_constants.Connection_manager.server_ip:
                raise Exception('Have not internet connection')
            parent.add_widget(WiFi_Server_Settings_Widget())
            global_constants.Connection_manager.type = 'host'
        except Exception as e:
            print(e)
            parent.add_widget(NotConnection_Widget(
                size=self.size,
                pos = (.04 * self.size[0], .2 * self.size[1])
            ))

            def add_me(click):
                parent.clear_widgets()
                parent.add_widget(EmptyConnectionWidget())

            parent.add_widget(Button(
                text = Get_text('all_back'),
                color = [1,1,0,1],
                pos = [.7 * self.size[0],.05 * self.size[1]],
                size = [.2 * self.size[0], .05 * self.size[1]],
                background_normal = '',
                background_color = [.7,.1,.1,.6],
                on_press = add_me
            ))

    def connect(self, press):
        """This function create interfase for USER Settings for WIFI"""
        global_constants.Main_Window.clear_widgets()
        global_constants.Main_Window.add_widget(User_Settings_Widget())


class WiFi_server_Widget(Widget):
    # this widget manage result connection
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = global_constants.Sizes.window_size
        self.clock = Clock.schedule_interval(self.renew, 0.5)
        global_constants.Connection_manager.set_options('wifi','p2p')
        if  global_constants.Connection_manager.server is None:
            global_constants.Connection_manager.server = network.Server()
        global_constants.Connection_manager.server.start()
        global_constants.Connection_manager.active = True
        global_constants.Connection_manager.users = []
        self.add_widget(Factory.Connection_Manager(size=self.size))

    def renew(self, time):
        if global_constants.Connection_manager.users != []:
            self.clock.cancel()
            global_constants.Main_Window.clear_widgets()
            global_constants.Main_Window.add_widget(Connection_info_Widget())

    def back(self, click):
        global_constants.Connection_manager.active = False
        global_constants.Connection_manager.server.stop()
        global_constants.Connection_manager.server = None
        global_constants.Main_Window.clear_widgets()
        global_constants.Main_Window.add_widget(WiFi_Server_Settings_Widget())


class WiFi_Server_Settings_Widget(Widget):
    # this class creates settings for server
    def __init__(self, **kwargs):
        self.size = global_constants.Sizes.window_size
        super().__init__(**kwargs)
        global_constants.game.state_game = 'one'

        self.add_widget(Button(
            text = Get_text('all_back'),
            color = [1,1,0,1],
            pos = [.7 * self.size[0],.05 * self.size[1]],
            size = [.2 * self.size[0], .05 * self.size[1]],
            background_normal = '',
            background_color = [.7,.1,.1,.6],
            on_press = self.back
        ))
        self.add_widget(Button(
            text = Get_text('connection_create'),
            color = [1,1,0,1],
            background_color = [0.1, 1, .1 , 1],
            background_normal = '',
            pos = [.3 * self.size[0], .25 * self.size[1]],
            size = [.4 * self.size[0], .05 * self.size[1]],
            on_press = self.create
        ))
        with self.canvas:
            Color(.7,.3,1,.5)
            self.canvas.add(Rectangle(
                pos = [.2 * self.size[0], .3 * self.size[1]],
                size = [.6 * self.size[0], .5 * self.size[1]]
            ))
            Color(1,1,1,0)
            
        grid = GridLayout(cols = 1,
            size = [.6 * self.size[0], .5 * self.size[1] ],
            pos = [.2 * self.size[0], .3 * self.size[1]]  )
        self.add_widget(grid)

        comandes = self.change_nickname, self.change_pass
        descriptions = ['connection_nick','connection_pass']
        nick = global_constants.Connection_manager.own_user.username
        if Settings.default_nick != '' and nick == '':
            nick = Settings.default_nick
            global_constants.Connection_manager.own_user.username = nick
        texts = [nick, global_constants.Connection_manager.password]
        
        grid.add_widget(Label(
            text = Get_text('connection_ip') + '\n' + \
                    global_constants.Connection_manager.server_ip,
            color = [1,1,0,1]
        ))
        for i in 0,1:
            grid.add_widget(Label(
                text = Get_text(descriptions[i]),
                color = [1,1,0,1]
            ))
            grid.add_widget(Text_line(
                comandes[i],text = texts[i],
                size = [.4 * self.size[0], .05 * self.size[1]],
                pos = [.3 * self.size[0], .7 * self.size[1]],
                size_hint = [1,None]
            ))
    
    def back(self, click):
        global_constants.Main_Window.clear_widgets()
        global_constants.Main_Window.add_widget(EmptyConnectionWidget())
        global_constants.Connection_manager.type = ''
    
    def change_pass(self, text):
        global_constants.Connection_manager.password = text

    def change_nickname(self, text):
        global_constants.Connection_manager.own_user.username = text

    def create(self, touch):
        if global_constants.Connection_manager.own_user.username == '':
            create_error('connection_empty_nick')
            return
        global_constants.Main_Window.clear_widgets()
        global_constants.Main_Window.add_widget(WiFi_server_Widget())
        global_constants.game.state_game = 'host'


class User_Settings_Widget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = global_constants.Sizes.window_size
        self.add_widget(Button(
            text = Get_text('all_back'),
            color = [1,1,0,1],
            pos = [.7 * self.size[0],.05 * self.size[1]],
            size = [.2 * self.size[0], .05 * self.size[1]],
            background_normal = '',
            background_color = [.7,.1,.1,.6],
            on_press = self.back
        ))

        with self.canvas:
            Color(.7,.3,1,.5)
            self.canvas.add(Rectangle(
                pos = [.2 * self.size[0], .3 * self.size[1]],
                size = [.6 * self.size[0], .5 * self.size[1]]
            ))
            Color(1,1,1,0)
        
        grid = GridLayout(
            cols = 1,
            pos = [.2 * self.size[0], .3 * self.size[1]],
            spacing = [0,30],
            size = [.6 * self.size[0], .5 * self.size[1]]
        )
        self.add_widget(grid)
        comandes = self.change_nick, self.change_ip, self.change_pass
        descriptions = ['connection_nick','connection_ip','connection_pass']
        global_constants.Connection_manager.own_user.username = Settings.default_nick
        user = global_constants.Connection_manager.own_user
        texts = [user.username, user.server_ip, user.password]

        for i in 0,1,2:
            grid.add_widget(Label(
                text = Get_text(descriptions[i]),
                color = [1,1,0,1]
            ))
            grid.add_widget(Text_line(
                comandes[i],text = texts[i],
                size = [.4 * self.size[0], .05 * self.size[1]],
                pos = [.3 * self.size[0], .7 * self.size[1]],
                size_hint = [1,None]
            ))
        
        self.add_widget(Button(
                text = Get_text('connection_connect'),
                color = [1,1,0,1],
                background_color = [0.1, 1, .1 , 1],
                background_normal = '',
                pos = [.3 * self.size[0], .25 * self.size[1]],
                size = [.4 * self.size[0], .05 * self.size[1]],
                on_press = self.connect
        ))
        
    def connect(self, click):
        user = global_constants.Connection_manager.own_user
        if user.username.isspace() or user.username == '':
            create_error(Get_text('connection_empty_nick'))
        elif not network.correct_ip(user.server_ip):
            create_error(Get_text('connection_incorrect_ip'))
        else:
            try:
                n = user.connect()
                if n == 0:
                    # connected
                    global_constants.Main_Window.clear_widgets()
                    global_constants.Main_Window.add_widget(Connection_info_Widget())
                    user.start()
                elif n == 1:
                    create_error(Get_text('connection_cant'))
                elif n == 2:
                    create_error(Get_text('connection_invalid_pass'))
                elif n == 3:
                    create_error(Get_text('connection_equal_nicks'))
                else:
                    print(n)
            except:
                create_error(Get_text('connection_cant'))

    def back(self, touch):
        global_constants.Main_Window.clear_widgets()
        global_constants.Main_Window.add_widget(EmptyConnectionWidget())

    def change_nick(self, text):
        global_constants.Connection_manager.own_user.username =  text

    def change_ip(self, text):
        global_constants.Connection_manager.own_user.server_ip = text
    
    def change_pass(self, text):
        global_constants.Connection_manager.own_user.password = text


class Connection_info_Widget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = global_constants.Sizes.window_size
        with self.canvas:
            Color(.3,.5,.5,.7)
            Rectangle(
                pos = [.1 * self.size[0], .35 * self.size[1]],
                size = [.8 * self.size[0], .2 * self.size[1]]
            )
            Color(.3,.5,.5,0)
        def kill(btn):
            global_constants.Connection_manager.send('exit')
            global_constants.game.state_game = 'one'        

        texts = ['all_back', 'connection_kill']
        poses = [
            [.7 * self.size[0],.05 * self.size[1]],
            [.2 * self.size[0], .05 * self.size[1]],
        ]
        commands = global_constants.Main_Window.create_start_game, kill
        for i in range(len(commands)):
            self.add_widget(Button(
                text = Get_text(texts[i]),
                color = [1,1,0,1],
                pos = poses[i],
                size = [.2 * self.size[0], .05 * self.size[1]],
                background_normal = '',
                background_color = [.7,.1,.1,.6],
                on_press = commands[i]
            ))
        self.add_widget(Label(
            text = Get_text('connection_has'),
            color = [1,1,1,1],
            pos = [.1 * self.size[0],.4 * self.size[1]],
            size = [.8 * self.size[0], .1 * self.size[1]],
            font_size=35
        ))

        if global_constants.game.state_game == 'host':
            self.add_widget(Button(
                text = Get_text('connection_to_game'),
                pos = [.1 * self.size[0], .3 * self.size[1]],
                size = [.8 * self.size[0], .05 * self.size[1]],
                on_press = global_constants.Main_Window.set_change,
                background_normal='',
                color=[0,1,0,1],
                background_color=[1,0,1,1]
            ))


