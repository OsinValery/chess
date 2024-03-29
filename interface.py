import os

from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Rectangle,Color,Line
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout

import settings
from translater import Get_text
import global_constants

def time(sec):
    # convert seconds to min : sec
    mins = sec//60
    sec = sec - 60 * mins
    a = str(mins)
    b = str(sec)
    if len(a) == 1:
        a = '0' + a
    if len(b) == 1:
        b = '0' + b
    return f'{a}:{b}'

def empty(click=None):
    pass

def exit_command(command):
    if not global_constants.game.ind and global_constants.game.state_game == 'one':
        # одиночная игра закончилась
        Repeat_message(command).open()
    elif global_constants.game.state_game != 'one':
        if not global_constants.game.ind:
            # network game is completed
            command(1)
        else:
            Network_Exit(command).open()
    else:
        # game is not completed
        Message_exit(command=command).open()

class Repeat_message(Popup):
    def __init__(self, command, **kwargs):
        self.background_color = [1, 1, 0, 0.25]
        self.background = 'window_fon.png'        
        super(Repeat_message,self).__init__(**kwargs)
        self.auto_dismiss = False
        self.pos = (0, 0)
        self.title = Get_text('bace_exit') + '?'

        size = global_constants.Main_Window.size
        self.size = (.7 * size[0], .5 * size[1])
        self.size_hint = (None, None)

        def repeat(par=...):
            self.dismiss()
            global_constants.game.renew_game()

        
        def _exit(par=...):
            self.dismiss()
            command(1)
        
        commands = (self.dismiss, repeat, _exit)
        texts = (Get_text('all_back'),Get_text('tutorial_repeat'), Get_text('bace_exit'))

        grid = GridLayout(cols = 1,spacing=(0,15))
        self.add_widget(grid)
        grid.add_widget(Label(
            text = Get_text('bace_repeat_text'),
            color = [0,1,1,1]
        ))
        for i in 0,1,2:
            grid.add_widget(Button(
                text = texts[i],
                size_hint_y = None,
                on_press = commands[i],
                background_color = [1,.1,1,.7]
            ))


class Message_exit(Popup):
    def __init__(self,command,**kwargs):
        self.background_color = [1,1,0,0.25]
        self.background = 'window_fon.png'

        super(Message_exit,self).__init__(**kwargs)
        self.auto_dismiss = False
        self.pos = (0,0)
        self.title = Get_text('bace_exit?')
        
        size = global_constants.Main_Window.size
        self.size = (.7 * size[0], .5 * size[1])
        self.size_hint = (None,None)
        
        def exit_(par=None):
            self.dismiss()
            command(1)

        def save(par=None):
            self.dismiss()
            data = global_constants.game.save_data
            folder = os.path.join(settings.Settings.user_folder,'Saves')
            cont = sorted(os.listdir(folder))
            if cont == []:
                name = 'save1'
            else:
                file_name = cont[-1]
                name = f'save{int(file_name[4:]) + 1}'
            with open(os.path.join(folder,name),mode='w') as file:
                file.write(data)
            command(1)

        commands = (self.dismiss, exit_, save)
        texts = (Get_text('all_back'), Get_text('bace_exit'),Get_text('bace_save?'))

        grid = GridLayout(cols = 1,spacing=[0,15])
        self.add_widget(grid)
        grid.add_widget(Label(
            text = Get_text('bace_exit_message'),
            color = [0,1,1,1]
        ))

        for i in 0,1,2:
            grid.add_widget(Button(
                text = texts[i],
                size_hint_y = None,
                on_press = commands[i],
                background_color = [1,.1,1,.7]
            ))


class Network_Exit(Popup):
    def __init__(self, command, **kwargs):
        self.background_color = [1,1,0,1/4]
        self.background = 'window_fon.png'
        super(Network_Exit,self).__init__(**kwargs)
        self.auto_dismiss = False
        self.pos = [0,0]
        self.title = Get_text('bace_exit') + '?'

        size = global_constants.Main_Window.size
        self.size = [.7 * size[0], .5 * size[1]]
        self.size_hint = [None,None]

        def _exit(par=...):
            self.dismiss()
            command(1)
        
        commands = [self.dismiss,_exit]
        texts = [Get_text('all_back'), Get_text('bace_exit')]

        grid = GridLayout(cols = 1,spacing=[0,15])
        self.add_widget(grid)
        grid.add_widget(Label(
            text = Get_text('bace_repeat_text'),
            color = [0,1,1,1]
        ))

        for i in 0,1:
            grid.add_widget(Button(
                text = texts[i],
                size_hint_y = None,
                on_press = commands[i],
                background_color = [1,.1,1,.7]
            ))

# all graphical interface without board and figures 
class Graphical_interfase():
    def __init__(self,game,sizes,commands):
        self.create(game,sizes,commands)
        
        if game.with_time:
            line = time(game.Game_logik.players_time['white'])
        else:
            line = '--:--'

        poses = (
            [   sizes.x_top_board + sizes.board_size[0] * 0.9 - sizes.field_size,
                sizes.y_top_board - sizes.board_size[1] / 10
            ],
            [   sizes.x_top_board + sizes.board_size[0] * 0.9 - sizes.field_size, 
                sizes.y_top_board + sizes.board_size[1]
            ]
        )
        self.white_time = Label(pos=poses[0])
        self.black_time = Label(pos=poses[1])

        for label in [self.white_time,self.black_time]:
            label.text = line
            label.size = [sizes.board_size[0],sizes.board_size[1] / 10]
            label.color = (1, 0, 0, 1)
            label.font_name = global_constants.Settings.get_font()
            label.valign = 'middle'
            label.text_size = [sizes.board_size[0], sizes.board_size[1]/10]
            global_constants.Main_Window.add_widget(label)

        self.info = Label(
            size=[sizes.board_size[0], 2 * sizes.board_size[1] / 10],
            pos = [sizes.x_top_board,sizes.y_top_board-3*sizes.board_size[0]/10],
            text = Get_text('game_white_move'),
            font_size = 40,
            color = [0.1,0.8,1,2],
            font_name = global_constants.Settings.get_font()
        )
        global_constants.Main_Window.add_widget(self.info)
    
    def set_time(self,play_time:dict):
        self.white_time.text = time(play_time['white'])
        self.black_time.text = time(play_time['black'])

    def do_info(self,info):
        self.info.text = info
    
    def create(self,game,sizes,commands):
        main_widget = global_constants.Main_Window
        main_widget.canvas.add(Rectangle(
            size=sizes.window_size,
            pos=(0,0),
            background_color=(0,0,0,0),
            source=settings.Settings.get_game_fon() 
        ))

        main_widget.add_widget(Button(
            text=Get_text('all_exit'),
            font_size = 30,
            background_normal='',
            font_name = global_constants.Settings.get_font(),
            background_color=(1,0,0,0.5),
            color=(1,1,0,1),
            pos =  [sizes.window_size[0]*0.85,sizes.window_size[1]*.93],
            size=(sizes.window_size[0]*0.15,sizes.window_size[1]*0.07),
            on_press = lambda par:exit_command(commands[0])
        ))

        # add clock - nick rectangle
        names = [game.name2,game.name1]
        mas = [  [sizes.x_top_board , sizes.y_top_board + sizes.board_size[1]  ],
                 [sizes.x_top_board , sizes.y_top_board - sizes.board_size[1] / 10  ]
        ]
        for x in 0,1:
            with main_widget.canvas:
                Color(.1,.1,.1,.3)
                Rectangle(
                    size= [sizes.board_size[0] , sizes.board_size[1] / 10],
                    pos=mas[x]
                )

            main_widget.add_widget(Label(
                pos=mas[x],
                size=[ sizes.board_size[0] , sizes.board_size[1] / 10 ],
                color=(1,0,0,1),
                text_size = [ sizes.board_size[0] , sizes.board_size[1] / 10 ],
                font_name = global_constants.Settings.get_font(),
                valign='middle',
                text=f' {names[x]}'
            ))

        # add purple rectangle
        with main_widget.canvas:
            Color(1,0,0.8,0.3,mode = 'rgba')
            Rectangle(
                size=[sizes.board_size[0],2*sizes.board_size[1] / 10],
                pos = [sizes.x_top_board,sizes.y_top_board-3*sizes.board_size[1] / 10]
            )
            Color(1,1,1,1)

        # pause button
        pause_but = Button(
            text = '',
            background_normal='',
            background_color=(0,0,0,0.5),
            pos =  [sizes.window_size[0]*0.75,sizes.window_size[1]*.93],
            size=(sizes.window_size[0]*0.09,sizes.window_size[1]*0.07),
            on_press = commands[1]
        )
        s = (sizes.window_size[0]*0.09,sizes.window_size[1]*0.07)
        with pause_but.canvas:
            Color(1,0,0,1)
            for x in 1,2:
                Line(
                    width = 3,
                    points=(
                        x / 3 * s[0] + sizes.window_size[0] * 0.75 ,
                        0.2 * s[1] + sizes.window_size[1]*.93 ,
                        x / 3 * s[0] + sizes.window_size[0]*0.75 ,
                        0.8 * s[1] + sizes.window_size[1]*.93
                    )
                )
        main_widget.add_widget(pause_but)

        directory = global_constants.Settings.folder
        # surrend button(0) + draw  button(1)
        pictures = ['surrend.png', 'draw.png']
        for i in 0,1:
            d =  i * 0.1
            but = Button(
                text='',
                size=(sizes.window_size[0]*0.09,sizes.window_size[1]*0.07),
                pos=[sizes.window_size[0]*d, sizes.window_size[1]*.93],
                background_normal = os.path.join(directory,'pictures','empty.png'),
                background_down = os.path.join(directory,'pictures','empty.png'),
                on_press=commands[2+i]
            )
            with but.canvas:
                Rectangle(
                    source = os.path.join(directory,'pictures',pictures[i]),
                    size = (sizes.window_size[0]*0.09,sizes.window_size[1]*0.07),
                    pos = [sizes.window_size[0]*d,sizes.window_size[1]*.93]
                )
            main_widget.add_widget(but)


    def __delattr__(self):
        del self.black_time
        del self.white_time
        del self.info




      