import socket
from threading import Thread

from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Rectangle, Color, RoundedRectangle, Line
from kivy.metrics import dp

from translater import Get_text
from settings import Settings

Game = None


def end_connection_activity(who=0):
    """
    0 - exit message
    else - broken
    """
    Game.state_game = 'one'
    if Game.window == 'connection':
        Connection.redraw()
    if Game.window == 'game':
        Game.ind = False
    if Game.window != 'connection':
        window = Popup()
        window.auto_dismiss = False
        grid = GridLayout(cols=1)
        window.add_widget(grid)
        text = Get_text('connection_exit')
        if who != 0:
            text = Get_text('connection_broken')
        grid.add_widget(Label(
            text = text,
            color = [1,0,0,1]
        ))

        grid.add_widget(Button(
            text = Get_text('all_ok'),
            size_hint_y = None,
            on_press = lambda click: window.dismiss()
        ))
        window.open()

def check_my_ip():
    """try to know my ip address"""
    my_ip = socket.gethostbyname(socket.gethostname())
    if my_ip == '127.0.0.1':
        # higly likely it will true for android and linux
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("gmail.com",80))
        Connection.my_ip = s.getsockname()[0]
        s.close()
        del s
        """
        # more universal solution
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.connect(('255.255.255.255',2000))
        my_ip = s.getsockname()[0]
        s.close()
    return my_ip


class connection():
    my_nick = ''
    my_ip = ''
    friend_ip = ''
    friend_nick = ''
    friend_version = ''
    password = ''
    #  1 if connection accept
    # 0 if connection down
    state = 0
    connected = False
    who = ''
    # server or client
    sock = socket.socket()
    conn = socket.socket()
    # i will create it in connect or in start
    messages = []

    def kill(self):   
        self.messages += ['exit']
        self.who = ''
        self.password = ''
        Game.state_game = 'one'
    
    def close_connection(self):
        # function for server
        self.messages = []
        self.connected = False
        self.state = 0
        if not self.conn._closed:
            self.conn.close()
    
    def start(self):
        # function for server
        def server(par=None):
            self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.sock.settimeout(1)
            self.sock.bind(('',2020))
            self.sock.listen(1)
            self.state = 1
            # server run
            try:
                while self.state :
                    # connect with sth
                    try:
                        self.conn, addr = self.sock.accept()
                        self.friend_ip = addr
                        self.conn.send(b'pass')
                        task = self.conn.recv(1024).decode('utf-8')

                        valid_password = 'empty'
                        if self.password != '':
                            valid_password = self.password
                        
                        if task == valid_password:
                            self.conn.send(b'valid')
                            self.connected = True 
                        else:
                            self.conn.send(b'invalid')
                            self.connected = False
                            self.conn.close()

                        if self.connected:
                            self.friend_nick = self.conn.recv(1024).decode('utf-8')
                            self.conn.send(self.my_nick.encode('utf-8'))

                            if self.my_nick == self.friend_nick:
                                self.connected = False
                                try:
                                    if not self.conn._closed:
                                        self.conn.close()
                                except:
                                    pass
                    except socket.timeout:
                        pass

                    # valid connection
                    # it is exectly friend now
                    self.messages = []
                    if self.connected:
                        self.redraw()
                        self.conn.settimeout(0.5)
                        Game.state_game = 'host'
                        self.friend_version = self.conn.recv(1024).decode('utf-8')
                        
                    while self.connected:
                        # server must be manager
                        if self.conn._closed == True:
                            self.connected = False
                        elif self.messages != []:
                            mes = self.messages.pop(0) + ' '
                            self.conn.send(mes.encode('utf-8'))
                            if 'exit' in mes:
                                self.close_connection()
                                end_connection_activity()
                        else:
                            # else i try take message from opponent
                            data = '#'
                            try:
                                data = self.conn.recv(1024).decode('utf-8').strip()
                                if 'exit' in data:
                                    self.close_connection()
                                    end_connection_activity()
                                    Game.state_game = 'one'
                                elif data == '':
                                    self.close_connection()
                                    end_connection_activity(2)
                                    print('empty data')          
                                else:
                                    Game.work_message(data)
                            except socket.timeout:
                                pass

                # if self.state == 0 it will
                print('stop')
                self.conn.close()
                Game.state_game = 'one'
            except:
                print('error')
                self.state = 0
                Game.state_game = 'one'
        
        self.server = Thread(target=server,daemon=True)
        self.server.start()

    def create_user(self):
        def moroz():
            self.sock.settimeout(0.5)
            Game.state_game = 'user'
            self.messages = []
            while self.state == 1:
                if self.sock._closed:
                    self.state = 0
                    Game.state_game = 'one'
                    print('_closed')
                elif self.messages != []:
                    data = self.messages.pop(0) + ' '
                    self.sock.send(data.encode('utf-8'))
                    if 'exit' in data:
                        self.state = 0
                        end_connection_activity()
                        Game.state_game = 'one'
                else:
                    try:
                        data = '#'
                        data = self.sock.recv(1024).decode('utf-8').strip()
                        if 'exit' in data:
                            self.state = 0
                            if self.sock._closed == False:
                                self.sock.close()
                            end_connection_activity()
                        elif data == '':
                            print('empty data')
                            self.state = 0
                            end_connection_activity(2)
                        elif data[:5] == 'start':
                            Game.start_play(data[6:])
                        else:
                            Game.work_message(data)

                    except socket.timeout:
                        pass
            Game.state_game = 'one'
            if self.sock._closed == False:
                self.sock.close()

        self.server = Thread(target=moroz,daemon=True)
        self.server.start()

    def connect(self):
        """return 
        0 - success
        1 - not connection
        2 - invalid code
        3 - nicks is equal
        """
        sock = socket.socket()
        try:
            sock.connect((Connection.friend_ip,2020))   
            n = sock.recv(1024)
            if self.password == '':
                sock.send('empty'.encode('utf-8'))
            else:
                sock.send(self.password.encode('utf-8'))
            task = sock.recv(1024).decode('utf-8')
            if task == 'valid':
                sock.send(self.my_nick.encode('utf-8'))
                self.friend_nick = sock.recv(1024).decode('utf-8')
                if self.my_nick == self.friend_nick:
                    sock.close()
                    return 3
                self.state = 1
                self.sock = sock
                sock.send(Game.version.encode('utf-8'))
                self.create_user()
                Game.state_game = 'user'
                # there run server of user
                return 0
            else:
                return 2
        except Exception as e:
            print(e)
            return 1





Connection = connection()


class server_widget(Widget):
    def __init__(self,size,parent):
        self.size = size
        super(server_widget,self).__init__()
        self.create_interface(parent)
        Connection.redraw = self.redraw

    def redraw(self):
        self.canvas.clear()
        self.clear_widgets()
        self.create_interface(self.parent)

    def create_interface(self,parent):
        text = Get_text('all_back')
        self.canvas.add(Rectangle(source=Settings.get_bace_picture(),size = self.size))
        self.add_widget(Button(
            text = text,
            color = [1,1,0,1],
            pos = [.7 * self.size[0],.05 * self.size[1]],
            size = [.2 * self.size[0], .05 * self.size[1]],
            background_normal = '',
            background_color = [.7,.1,.1,.6],
            on_press = parent.create_start_game
        ))

        if Connection.state == 1:
            # connected with friend
            with self.canvas:
                Color(.3,.5,.5,.7)
                Rectangle(
                    pos = [.1 * self.size[0], .35 * self.size[1]],
                    size = [.8 * self.size[0], .2 * self.size[1]]
                )
                Color(.3,.5,.5,0)
            self.add_widget(Label(
                text = Get_text(description='connection_has',params=[Connection]),
                color = [1,1,1,1],
                pos = [.1 * self.size[0],.4 * self.size[1]],
                size = [.8 * self.size[0], .1 * self.size[1]],
                font_size=35
            ))
            def kill(btn):
                Connection.kill()
                Connection.state = 0
                self.redraw()
                Game.state_game = 'one'
            
            self.add_widget(Button(
                text = Get_text('connection_kill'),
                color = [1,1,0,1],
                background_normal = '',
                background_color = [.7,0,0,.7],
                pos = [.2 * self.size[0], .05 * self.size[1]],
                size = [.2 * self.size[0], .05 * self.size[1]],
                on_press = kill
            ))
            def go_to_games(click):
                parent.set_change(click)
            if Game.state_game == 'host':
                self.add_widget(Button(
                    text = Get_text('connection_to_game'),
                    pos = [.1 * self.size[0], .3 * self.size[1]],
                    size = [.8 * self.size[0], .05 * self.size[1]],
                    on_press = go_to_games,
                    background_normal='',
                    color=[0,1,0,1],
                    background_color=[1,0,1,1]
                ))
        else:
            # there is not connection
            self.add_widget(Button(
                text = Get_text('connection_create'),
                color = [1,1,0,1],
                background_color = [0.1, 1, .1 , 1],
                background_normal = '',
                pos = [.3 * self.size[0], .7 * self.size[1]],
                size = [.4 * self.size[0], .05 * self.size[1]],
                on_press = self.create
            ))
            self.add_widget(Button(
                text = Get_text('connection_connect'),
                color = [1,1,0,1],
                background_color = [0.1, 1, .1 , 1],
                background_normal = '',
                pos = [.3 * self.size[0], .55 * self.size[1]],
                size = [.4 * self.size[0], .05 * self.size[1]],
                on_press = self.connect
            ))

    def create(self,click=None):
        """ create server """
        self.clear_widgets()
        self.add_widget(Button(
            text = Get_text('all_back'),
            color = [1,1,0,1],
            pos = [.7 * self.size[0],.05 * self.size[1]],
            size = [.2 * self.size[0], .05 * self.size[1]],
            background_normal = '',
            background_color = [.7,.1,.1,.6],
            on_press = lambda par:self.redraw()
        ))
        try:
            # try to know my ip
            Connection.my_ip = check_my_ip()
            if Connection.my_ip == '127.0.0.1':
                raise Exception('network connection error')

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

            def change_nick(text):
                if Connection.state == 0:
                    Connection.my_nick = text
        
            def change_pass(text):
                if Connection.state == 0:
                    Connection.password = text
            
            comandes = change_nick, change_pass
            descriptions = ['connection_nick','connection_pass']
            if Settings.default_nick != '' and Connection.my_nick == '':
                Connection.my_nick = Settings.default_nick
            texts = [Connection.my_nick, Connection.password]
            
            grid.add_widget(Label(
                text = Get_text('connection_ip') + '\n' + Connection.my_ip,
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
            
            def create(click):
                # this function create server and wait of connection
                # second press on button ( if wait - it is cancel), thos function stop waiting and server
                if Connection.state == 0:
                    if Connection.my_nick == '':
                        create_error(Get_text('connection_empty_nick'))
                    else:
                        try:
                            Connection.who = 'host'
                            Game.state_game = 'host'
                            Game.play_by = 'white'
                            Connection.start()
                            for ch in self.children:
                                if type(ch) == Button:
                                    ch.disabled = True
                            click.disabled = False
                            click.text = Get_text('connection_cancel')
                            click.background_color = [1,0,0,.4]
                        except :
                            create_error(Get_text('connection_cant'))
                else:
                    Connection.state = 0
                    if Connection.connected:
                        if not Connection.conn.__closed:
                            Connection.conn.close()
                            Connection.connected =  False
                    click.text = Get_text('connection_create')
                    click.background_color = [0.1, 1, .1 , 1]
                    for ch in self.children:
                        if type(ch) == Button:
                            ch.disabled = False

            self.add_widget(Button(
                    text = Get_text('connection_create'),
                    color = [1,1,0,1],
                    background_color = [0.1, 1, .1 , 1],
                    background_normal = '',
                    pos = [.3 * self.size[0], .25 * self.size[1]],
                    size = [.4 * self.size[0], .05 * self.size[1]],
                    on_press = create
            ))

        except:
            # have not wifi
            self.add_widget(NotConnection_Widget(
                size=self.size,
                pos = (.04 * self.size[0], .2 * self.size[1])
            ))

    def connect(self,click=None):
        # connect to server interface 
        # it is for host
        self.clear_widgets()
        self.add_widget(Button(
            text = Get_text('all_back'),
            color = [1,1,0,1],
            pos = [.7 * self.size[0],.05 * self.size[1]],
            size = [.2 * self.size[0], .05 * self.size[1]],
            background_normal = '',
            background_color = [.7,.1,.1,.6],
            on_press = lambda par:self.redraw()
        ))
        with self.canvas:
            Color(.7,.3,1,.5)
            self.canvas.add(Rectangle(
                pos = [.2 * self.size[0], .3 * self.size[1]],
                size = [.6 * self.size[0], .5 * self.size[1]]
            ))
            Color(1,1,1,0)

        def change_nick(text):
            Connection.my_nick = text

        def change_ip(text):
            Connection.friend_ip = text
        
        def change_pass(text):
            Connection.password = text


        grid = GridLayout(
            cols = 1,
            pos = [.2 * self.size[0], .3 * self.size[1]],
            spacing = [0,30],
            size = [.6 * self.size[0], .5 * self.size[1]]
        )
        self.add_widget(grid)
        comandes = change_nick,change_ip,change_pass
        descriptions = ['connection_nick','connection_ip','connection_pass']
        Connection.my_nick = Settings.default_nick
        for i in 0,1,2:
            grid.add_widget(Label(
                text = Get_text(descriptions[i]),
                color = [1,1,0,1]
            ))
            text = ''
            if i == 0:
                text = Connection.my_nick
            grid.add_widget(Text_line(
                comandes[i],text = text,
                size = [.4 * self.size[0], .05 * self.size[1]],
                pos = [.3 * self.size[0], .7 * self.size[1]],
                size_hint = [1,None]
            ))
        
        def create(click=None):
            # this function tryes to connect with server
            if Connection.my_nick.isspace() or Connection.my_nick == '':
                create_error(Get_text('connection_empty_nick'))
            elif not correct_ip(Connection.friend_ip):
                create_error(Get_text('connection_incorrect_ip'))
            else:
                try:
                    Connection.who = 'user'
                    n = Connection.connect()
                    if n == 0:
                        click.disabled = True
                        self.redraw()
                    elif n == 1:
                        create_error(Get_text('connection_cant'))
                    elif n == 2:
                        create_error(Get_text('connection_invalid_pass'))
                    elif n == 3:
                        create_error(Get_text('connection_equal_nicks'))
                except:
                    create_error(Get_text('connection_cant'))

        self.add_widget(Button(
                text = Get_text('connection_connect'),
                color = [1,1,0,1],
                background_color = [0.1, 1, .1 , 1],
                background_normal = '',
                pos = [.3 * self.size[0], .25 * self.size[1]],
                size = [.4 * self.size[0], .05 * self.size[1]],
                on_press = create
        ))


class Text_line(TextInput):
    def __init__(self,changed,**kwargs):
        self.changed = changed
        self.multiline = False
        super(Text_line,self).__init__(**kwargs)
        self.bind(text=self.text_redact)

    def text_redact(self,wid,text):
        self.changed(text)


def correct_ip(ip:str):
    try:
        digs = ip.split('.')
    except:
        return False
    if len(digs) != 4:
        return False
    for el in digs:
        if not el.isdigit():
            return False
        n = int(el)
        if n < 0 or n > 255:
            return False

    return True


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
        





if __name__ == '__main__':
    from kivy.app import App
    from kivy.core.window import Window
    import os

    Settings.lang = 'ru'

    class My_Test(App):
        def build(self):
            
            s = [800,1400]
            s = Window.size
            path = os.path.join(self.directory,'pictures','bace_fons','pic4.png')

            wid = Widget(size=s)
            wid.canvas.add(Rectangle(
                size = s,
                source = path
            ))
            #Window.size = [s[0]//2,s[1]//2]
            wid.add_widget(NotConnection_Widget(
                size=s,
                pos=(.04 * s[0], .2 * s[1])
            ))
            return wid
    
    My_Test().run()




