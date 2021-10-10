import socket

import global_constants
import threading
from translater import Get_text

from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup



def end_connection_activity(who=0):
    """
    0 - exit message
    else - broken
    """
    Game = global_constants.game
    if Game.state_game == 'host':
        for user in global_constants.Connection_manager.users:
                if not user.state :
                    global_constants.Connection_manager.users.remove(user)
        if global_constants.Connection_manager.mode == 'p2p':
            global_constants.Connection_manager.server.stop()
            global_constants.Connection_manager.server = None
        else:
            print(global_constants.Connection_manager.mode)
        print('after removing')
        print(global_constants.Connection_manager.users)
        print(global_constants.Connection_manager.mode)
    else:
        global_constants.Connection_manager.active = False
    if Game.window == 'connection':
        global_constants.Main_Window.clear_widgets()
        if global_constants.game.state_game == 'user':
            global_constants.Main_Window.create_start_game(1)
        elif global_constants.Connection_manager.mode == 'p2p':
            global_constants.Main_Window.create_start_game(1)
            
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
    Game.state_game = 'one'

def check_my_ip():
    """try to know my ip address"""
    my_ip = '127.0.0.1'
    try:
        my_ip = socket.gethostbyname(socket.gethostname())
    except:
        pass
    if my_ip == '127.0.0.1':
        # higly likely it will true for android and linux
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.connect(('255.255.255.255',2000))
        my_ip = s.getsockname()[0]
        s.close()
    return my_ip

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


class Connection_manager():
    def __init__(self) -> None:
        self.connection_type = 'wifi'
        self.type = ''
        # user or host
        self.mode = 'p2p'
        self.password = ''
        self.server_ip = ''
        self.server_nick = ''
        self.users = []
        self.active = False
        # this user for current devise
        # it will not be incuded in massive users
        self.own_user = User()
        self.server = None
    
    def set_options(self, connectopn_type, mode ='p2p'):
        self.mode = mode
        self.connection_type = connectopn_type
    
    def send(self, message):
        if global_constants.game.state_game == 'user':
            self.own_user.send(message)
        elif global_constants.game.state_game == 'host':
            if self.users == []:
                return
            self.users[0].send(message)
        else:
            print('from network.Connection_info.send:')
            print('do not know what to do')
            print('message = ', message)
    
    @property
    def friend_version(self):
        """returns minimal version"""
        version = self.users[0].version
        for user in self.users:
            if user.version < version:
                version = user.version
        return version
    
    @property
    def my_nick(self):
        state = global_constants.game.state_game
        if state == 'user':
            return global_constants.Connection_manager.own_user.username
        elif state == 'host':
            return global_constants.Connection_manager.own_user.username
        return 'error'
    
    @property
    def friend_nick(self):
        state = global_constants.game.state_game
        if state == 'user':
            return global_constants.Connection_manager.server_nick
        elif  state == 'host':
            return global_constants.Connection_manager.users[0].username
        return 'error'


class Server():
    def __init__(self) -> None:
        self.state = 0
        # disabled
        self.my_ip = ''
        self.enable_users = 1
        print('set connection typi for the socket in Server class')
        if global_constants.Connection_manager.connection_type == 'wifi':
            self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        else:
            self.socket = socket.socket()
        self.thread = threading.Thread(daemon=True)

    def start(self):
        if not self.state:
            self.thread = threading.Thread(daemon=True)
            self.thread.run = self.activity
            self.thread.start()
            self.state = 1
    
    def stop(self):
        self.state = False
        for user in global_constants.Connection_manager.users:
            if user.state:
                user.close()
        global_constants.Connection_manager.users = []
        self.socket.close()
        global_constants.Connection_manager.active = False
        global_constants.Connection_manager.server = None

    def activity(self):
        self.socket.settimeout(1)
        self.socket.bind(('',2020))        
        self.socket.listen(self.enable_users)

        print('check the quontity of enabled users')
        while self.state == 1:
            try:
                user_socket, address = self.socket.accept()
                players = len(global_constants.Connection_manager.users)
                if players >= self.enable_users:
                    user_socket.send(b'access denied')
                    user_socket.close()
                    continue
                user_socket.send(b'pass')
                trile_password = user_socket.recv(1024).decode('utf-8')
                pas = global_constants.Connection_manager.password
                correct_password = pas if pas else 'empty'
                if trile_password != correct_password:
                    user_socket.send(b'invalid')
                    continue
                user_socket.send(b'valid')
                user_nickname = user_socket.recv(1024).decode('utf-8')
                user_socket.send(global_constants.Connection_manager.own_user.username.encode('utf-8'))
                if user_nickname == global_constants.Connection_manager.own_user.username:
                    user_socket.close()
                    continue
                version = user_socket.recv(1024).decode('utf-8')
                user = User()
                user.set_options(user_nickname, user_socket)
                self.register_user(user)
                user.version = version
            except socket.timeout:
                pass
            except Exception as e:
                print(e)
        self.socket.close()

    def register_user(self, user):
        global_constants.Connection_manager.users.append(user)
        user.start()


class User():
    def __init__(self) -> None:
        self.password = ''
        self.server_ip = ''
        self.messages = []
        self.socket = socket.socket()
        self.thread = threading.Thread()
        self.username = ''
        self.state = True
        self.version = ''
    
    def connect(self):
        """returns 
         0 - success
        1 - not connection
         2 - invalid code
        3 - nicks is equal
        """
        try:
            self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.socket.settimeout(10)            
            self.socket.connect((self.server_ip,2020))

            res = self.socket.recv(1024).decode('utf-8')
            print('check eccess in User Class!!!!')
            if res != 'pass':
                self.socket.close()
                return 1
            password = self.password if self.password else 'empty'
            self.socket.send(password.encode('utf-8'))
            res = self.socket.recv(1024).decode('utf-8')
            if res == 'invalid':
                self.socket.close()
                return 2
            self.socket.send(self.username.encode('utf-8'))
            second_nick = self.socket.recv(1024).decode('utf-8')
            if self.username == second_nick:
                self.socket.close()
                return 3
            global_constants.Connection_manager.server_nick = second_nick
            version = global_constants.game.version
            self.socket.send(version.encode('utf-8'))
            global_constants.game.state_game = 'user'
            return 0
        except Exception as e:
            print(e)
            self.socket.close()
            return 1

    def send(self, message):
        self.messages.append(message)

    def close(self):
        self.messages = ['exit']

    def set_options(self, nick, sock):
        self.socket = sock
        self.username = nick

    def start(self):
        self.thread = threading.Thread(daemon=True,target=self.activity)
        self.state = True
        self.thread.start()

    def activity(self):
        self.socket.settimeout(0.5)
        self.messages = []
        while self.state:
            try:
                if self.socket._closed:
                    self.state = False
                    print('connection broken')
                if self.messages == []:
                    mes = '#'
                    mes = self.socket.recv(1024).decode('utf-8')
                    print('i found')
                    print(mes)
                    if mes == 'exit':
                        self.socket.close()
                        self.state = False
                        end_connection_activity()
                    elif mes == '':
                        print('empty message')
                        self.socket.close()
                        self.state = False
                        end_connection_activity()
                    elif 'start' in mes:
                        global_constants.game.start_play(mes[6:])
                    else:
                        global_constants.game.work_message(mes)
                else:
                    mes = self.messages.pop(0)
                    self.socket.send(mes.encode('utf-8'))
                    if mes == 'exit':
                        self.socket.close()
                        self.state = False
                        end_connection_activity()
                        if self in global_constants.Connection_manager.users:
                            global_constants.Connection_manager.users.remove(self)
            except socket.timeout:
                pass
            except Exception as e:
                print(e)
        print('end activity in User')
        self.messages = []
        global_constants.game.state_game = 'one'

