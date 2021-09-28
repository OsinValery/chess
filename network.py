import socket
import global_constants
import threading




class Connection_info():
    def __init__(self) -> None:
        self.connected = False
        self.connection_type = 'wifi'
        self.type = ''
        # user or server
        self.mode = 'p2p'
    


class Server():
    def __init__(self) -> None:
        self.state = 0
        # disabled
        self.my_ip = ''
        self.password = ''
        self.enable_users = 1
        print('set connection typi for the socket in Server class')
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

    def activity(self):
        self.socket.settimeout(1)
        self.socket.listen(self.enable_users)
        self.socket.bind(('',2020))
        print('check the quontity of enabled users')
        while self.state == 1:
            try:
                user_socket, address = self.socket.accept()
                user_socket.send(b'pass')
                trile_password = user_socket.recv(1024).decode('utf-8')
                correct_password = self.password if self.password else 'empty'
                if trile_password != correct_password:
                    user_socket.send(b'invalid')
                    user_socket.close()
                    continue
                user_socket.send(b'valid')
                user_nickname = user_socket.recv(1024).decode('utf-8')
                user_socket.send()
            except socket.timeout:
                pass
            except:
                pass

    def register_user(self, user):
        pass




class User():
    def __init__(self) -> None:
        self.password = ''
        self.server_ip = ''
        self.friend_username = ''
        self.messages = []
        self.socket = socket.socket()
    
    def connect(self):
        try:
            self.socket.connect((self.server_ip,2020))
            self.socket.recv(1024).decode('utf-8')
            print('check eccess in User Class!!!!')
        except:
            pass


    def send(self, message):
        pass

    def close(self):
        pass






