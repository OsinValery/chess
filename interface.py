import os

from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Rectangle,Color,Line
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout

import settings
from translater import Get_text
import global_constants
import change_widget

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


def exit_command(command):
    if not global_constants.game.ind :
        Repeat_message(command).open()
    elif global_constants.game.state_game != 'one':
        command(1)
    else:
        Message_exit(command=command).open()

class Repeat_message(Popup):
    def __init__(self, command, **kwargs):
        self.background_color = [1,1,0,1/4]
        self.background = 'window_fon.png'        
        super(Repeat_message,self).__init__(**kwargs)
        self.auto_dismiss = False
        self.pos = [0,0]
        self.title = Get_text('bace_exit') + '?'

        size = global_constants.Main_Window.size
        self.size = [.7 * size[0], .5 * size[1]]
        self.size_hint = [None,None]

        def repeat(par=...):
            self.dismiss()
            game = global_constants.game
            tip = game.type_of_chess
            with_tips = game.make_tips
            name1, name2 = game.name1, game.name2
            add, mode = game.add_time, game.time_mode
            with_time = game.with_time
            command(1)
            game.make_tips = with_tips
            game.name1 = name1; game.name2= name2
            game.with_time = with_time
            game.time_mode = mode
            game.add_time = add
            global_constants.Main_Window.set_change(1)
            change_widget.Chess_type(tip).set_chess(1)
        
        def _exit(par=...):
            self.dismiss()
            command(1)
        
        commands = [self.dismiss,repeat,_exit]
        texts = [Get_text('all_back'),Get_text('tutorial_repeat'), Get_text('bace_exit')]

        grid = GridLayout(cols = 1,spacing=[0,15])
        self.add_widget(grid)
        grid.add_widget(Label(
            text = Get_text('bace_repeat_text'),
            color = [0,1,1,1]
        ))

        for i in 0,1,2:
            but = Button(
                text = texts[i],
                size_hint_y = None,
                on_press = commands[i],
                background_color = [1,.1,1,.7]
            )
            grid.add_widget(but)


class Message_exit(Popup):
    def __init__(self,command,**kwargs):
        self.background_color = [1,1,0,0.25]
        self.background = 'window_fon.png'

        super(Message_exit,self).__init__(**kwargs)
        self.auto_dismiss = False
        self.pos = [0,0]
        self.title = Get_text('bace_exit?')
        
        size = global_constants.Main_Window.size
        self.size = [.7 * size[0], .5 * size[1]]
        self.size_hint = [None,None]
        
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
                name = 'save' + str(int(file_name[4:]) + 1)
            file = open(os.path.join(folder,name),mode='w')
            file.write(data)
            file.close()
            command(1)

        commands = [self.dismiss, exit_, save]
        texts = [Get_text('all_back'), Get_text('bace_exit'),Get_text('bace_save?')]

        grid = GridLayout(cols = 1,spacing=[0,15])
        self.add_widget(grid)
        grid.add_widget(Label(
            text = Get_text('bace_exit_message'),
            color = [0,1,1,1]
        ))

        for i in 0,1,2:
            but = Button(
                text = texts[i],
                size_hint_y = None,
                on_press = commands[i],
                background_color = [1,.1,1,.7]
            )
            grid.add_widget(but)

# all graphical interface without board and figures 
class Graphical_interfase():
    def __init__(self,game,sizes,commands):
        self.create(game,sizes,commands)
        
        if game.with_time:
            line = time(game.players_time['white'])
        else:
            line = '--:--'

        self.white_time = Label(
            text=line,
            pos=[ sizes.x_top_board + sizes.board_size[0] * 0.9 - sizes.field_size,
                        sizes.y_top_board - sizes.y_top * 2 ],
            size=[sizes.board_size[0],2*sizes.y_top],
            color=(1,0,0,1),
            text_size = [sizes.board_size[0],2*sizes.y_top],
            valign='middle'
        )
        self.black_time = Label(
            text=line,
            size= [sizes.board_size[0],2*sizes.y_top],
            pos=[sizes.x_top_board + sizes.board_size[0] * 0.9 - sizes.field_size, 
                        sizes.y_top_board + sizes.board_size[1] ],
            color=(1,0,0,1),
            text_size=[sizes.board_size[0],2*sizes.y_top],
            valign='middle'
            ) 
        self.info = Label(
            size=[sizes.board_size[0],2*sizes.field_size],
            pos = [sizes.x_top_board,sizes.y_top_board-3*sizes.field_size],
            text = Get_text('game_white_move'),
            font_size = 40,
            color = [0.1,0.8,1,2]
        )

        global_constants.Main_Window.add_widget(self.white_time)
        global_constants.Main_Window.add_widget(self.black_time)
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
            background_color=(1,0,0,0.5),
            color=(1,1,0,1),
            pos =  [sizes.window_size[0]*0.85,sizes.window_size[1]*.93],
            size=(sizes.window_size[0]*0.15,sizes.window_size[1]*0.07),
            on_press = lambda par:exit_command(commands[0])
        ))
        names = [game.name2,game.name1]
        mas = [  [sizes.x_top_board , sizes.y_top_board + sizes.board_size[1]  ],
                 [sizes.x_top_board , sizes.y_top_board - 2 * sizes.y_top  ]
        ]
        for x in 0,1:
            with main_widget.canvas:
                Color(.1,.1,.1,.3)
                Rectangle(
                    size= [sizes.board_size[0] , 2 * sizes.y_top],
                    pos=mas[x]
                )

            main_widget.add_widget(Label(
                pos=mas[x],
                size=[ sizes.board_size[0] , 2 * sizes.y_top ],
                color=(1,0,0,1),
                text_size = [ sizes.board_size[0] , 2 * sizes.y_top ],
                valign='middle',
                text=names[x]
            ))

        with main_widget.canvas:
            Color(1,0,0.8,0.2,mode = 'rgba')
            Rectangle(
                size=[sizes.board_size[0],2*sizes.field_size],
                pos = [sizes.x_top_board,sizes.y_top_board-3*sizes.field_size]
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
            pause_but.canvas.add(Line(
                points=(
                    x*0.33*s[0] + sizes.window_size[0]*0.75 ,
                    0.2*s[1] + sizes.window_size[1]*.93 ,
                    x*0.33*s[0] + sizes.window_size[0]*0.75 ,
                    0.8*s[1] + sizes.window_size[1]*.93
                    ),
                width = 3,  
            ))
        main_widget.add_widget(pause_but)

        directory = global_constants.Settings.folder
        # surrend button
        but = Button(
            background_normal = os.path.join(directory,'pictures','empty.png'),
            background_down = os.path.join(directory,'pictures','empty.png'),
            size=(sizes.window_size[0]*0.09,sizes.window_size[1]*0.07),
            text = '',
            pos = [sizes.window_size[0]*0.65,sizes.window_size[1]*.93],
            on_press = commands[2]
        )
        with but.canvas:
            Rectangle(
                source = os.path.join(directory,'pictures','surrend.png'),
                size = (sizes.window_size[0]*0.09,sizes.window_size[1]*0.07),
                pos = [sizes.window_size[0]*0.65,sizes.window_size[1]*.93]
            )
        main_widget.add_widget(but)

        # draw button
        but = Button(
            text = '',
            background_normal = os.path.join(directory,'pictures','empty.png'),
            background_down = os.path.join(directory,'pictures','empty.png'),
            on_press = commands[3],
            size = (sizes.window_size[0]*0.09,sizes.window_size[1]*0.07),
            pos = [sizes.window_size[0]*0.55,sizes.window_size[1]*.93]
        )
        with but.canvas:
            Rectangle(
                source = os.path.join(directory,'pictures','draw.png'),
                size = (sizes.window_size[0]*0.09,sizes.window_size[1]*0.07),
                pos = [sizes.window_size[0]*0.55,sizes.window_size[1]*.93]
            )
        main_widget.add_widget(but)

    def __delattr__(self):
        del self.black_time
        del self.white_time
        del self.info




      