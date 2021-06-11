from typing import Set
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle,Color
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.clock import Clock

import random
import os

from settings import Settings
import tutorial
from translater import Get_text
from my_spinner import Spinner
from switch import Switch_ as Switch
from round_button import RoundButton
import global_constants


"""
This module was created for realisation of interface of choosing type of chess
"""


def create_settings_interface(tap):
    global_constants.game.window = 'settings'
    main_widget = global_constants.Main_Window
    size = global_constants.Sizes
    main_widget.clear_widgets()
    main_widget.canvas.clear()
    main_widget.canvas.add(Rectangle(
        source=Settings.get_bace_picture() ,
        size = size.window_size
    ))

    main_widget.add_widget(Label(
        text = find_name(),
        color = (0.8,0.5,0,1),
        pos = [size.window_size[0]*.35,size.window_size[1]*.8],
        font_size = 70     ))

    main_widget.add_widget(Settings_widget(
        size = [.5 * size.window_size[0],.5 * size.window_size[1] ],
        pos = [.5 * size.window_size[0], .2 * size.window_size[1] ]   ))

    names = [Get_text('all_back'),Get_text('change_study') ,Get_text('all_start')]
    commands = [main_widget.set_change, tutorial.tutorial, create_game_process]
    colors = [   (0.5,0.01,0.2,0.7) ,
                 (1,1,0,0.5) , 
                 (0,1,0,0.5) ]
    colors2 = [  (1,1,0,1),
                 (0.1,0,5,1), 
                 (0,0,1,0.8) ]
    
    grid = GridLayout(
        size = [size.window_size[0]*0.6,size.window_size[1]*0.065],
        pos=[size.window_size[0]*0.3,size.window_size[1]*0.05] ,
        cols = 3 )

    for a in range(3):
        grid.add_widget(Button(
            text=names[a],
            font_size=25,
            background_color=colors[a],
            background_normal='',
            color= colors2[a],
            on_press = commands[a]
        ))
    main_widget.add_widget(grid)

def create_game_process(click):
    game = global_constants.game
    if game.state_game == 'one':
        game.create_game(click)
    elif game.state_game == 'host':
        game.create_game(click)
    else:
        create_worning()

def find_name():
    for chess in all_chess:
        if chess.type == global_constants.game.type_of_chess:
            return chess.text
    return 'not found'

def create_worning():
    window = Popup()
    window.auto_dismiss = False
    window.title = Get_text('change_warning')
    wid = GridLayout(cols = 1)
    wid.add_widget(Label(
        color = [1,0,0,1],
        font_size = 31,
        text = Get_text('change_error_who')
    ))
    wid.add_widget(Button(
        text = Get_text('all_ok'),
        on_press = lambda par:window.dismiss(),
        size_hint_y = None
    ))
    window.add_widget(wid)
    window.open()

def sort_games(games):
    if not Settings.must_sort_games:
        return games
    rule = Settings.get_sorting(all_chess)
    def sol(game1):
        return rule[game1.type]
    return sorted(games,key=sol,reverse=True)


############################################################
# useful classes
#############################################################

class Chess_type():
    def __init__(self,tip):
        self.type = tip
    
    def set_chess(self,click):
        global_constants.Main_Window.clear_widgets()
        global_constants.game.type_of_chess = self.type
        tutorial.get_params(create_settings_interface)
        create_settings_interface(1)

    @property
    def picture(self):
        if self.type == 'horse_battle':
            return 'presentation_horse.png'
        elif self.type == 'bad_chess':
            return 'presentation_bad.png'
        else:
            return f'presentation_{self.type}.png'
    
    @property
    def text(self):
        if self.type == 'horse_battle':
            return Get_text('bace_horse')
        if self.type == 'magik':
            return Get_text('bace_magic')
        if self.type == 'los_alamos':
            return Get_text('bace_alamos')
        if self.type == 'circle_chess':
            return Get_text('bace_circle')
        if self.type == 'bad_chess':
            return Get_text('bace_bad')
        return Get_text(f'bace_{self.type}')


class Card(Widget):
    def  __init__(self,picture,command,pos):
        super(Card,self).__init__()
        size = global_constants.Sizes
        self.size = (size.window_size[0]*0.8,size.window_size[0]*.6)
        self.size_hint = [None,None]
        self.pos = pos
        path = os.path.join(Settings.get_folder(),'pictures','presentations',picture)
        self.canvas.add(Rectangle(
            size=[self.width,self.height],
            source = path,
            pos=pos
        ))
        size1 = (size.window_size[0]*0.95,size.window_size[0]*.6)        
        self.add_widget(Button(
            text=Get_text('change_play'),
            font_size = 25,
            background_color = (0,1,0,0.65),
            size=(size1[0]//3.7,size1[1]//5),
            pos = (self.pos[0] + self.size[0]*.6,self.pos[1]),
            color=(1,1,0,0.9),
            on_press = command
            ))


class Chess_menu(Widget):
    """
    this class shows list of buttons 
    when user choose class of chess
    """
    def __init__(self):
        super(Chess_menu,self).__init__()
        Clock.schedule_once(self.create_interface)
    
    def to_type(self,btn):
        self.clear_widgets()
        size = self.parent.size
        self.add_widget(Button(
            text=Get_text('all_back'),
            pos = [size[0]*0.8,size[1]*0.9],
            size = [size[0]*0.2,size[1]*0.07],
            background_color = (1,0.2,1,0.5),
            font_size = 20,
            color=(0,1,0.1,1),
            on_press = self.create_interface ))
        group = btn.group
        global_constants.game.window = 'chess_chooser'
        if group == 0:
            random.choice(all_chess).set_chess(1)
        elif group == 1:
            self.add_widget(Chess_view(sort_games(all_chess)))
        elif group == 2:
            self.add_widget(Chess_view(sort_games(classic_type)))
        elif group == 3:
            self.add_widget(Chess_view(sort_games(positions)))
        elif group == 4:
            self.add_widget(Chess_view(sort_games(with_effects)))
        elif group == 5:
            self.add_widget(Chess_view(sort_games(honestless)))
        elif group == 6:
            self.add_widget(Chess_view(sort_games(boards)))
        elif group == 7:
            self.add_widget(Chess_view(sort_games(other_rules)))
 
    def create_interface(self,arg=None):
        self.clear_widgets()
        self.size = global_constants.Sizes.window_size
        self.add_widget(Button(
            text=Get_text('all_back'),
            pos = [self.size[0]*0.8,self.size[1]*0.9],
            size = [self.size[0]*0.2,self.size[1]*0.07],
            background_color = (1,0.2,1,0.5),
            font_size = 20,
            color=(0,1,0.1,1),
            on_press = global_constants.Main_Window.create_start_game ))

        texts = ['random','all','classic', 'positions', 'effects', 'honestlessly','boards','others']
        # size of button's shape
        width = .6 * self.size[0]
        height = .6 * self.size[1]
        pos =  [.2 * self.size[0], .2 * self.size[0]]
        h = height / len(texts)
        spacing = 20
        for i in range(len(texts)):
            but = RoundButton(
                text = Get_text('change_' + texts[i]),
                color = [.5,1,0,1],
                on_press = self.to_type,
                background_color = [.3,.6,1,.7],
                size = [width,h-spacing],
                pos = [pos[0],pos[0]+height-h*(i+1)]
            )
            but.group = i
            self.add_widget(but)


class Chess_view(ScrollView):
    def __init__(self,chess_list):
        super(Chess_view,self).__init__()
        self.size_hint = (None,None)
        size = global_constants.Sizes
        self.size = (size.window_size[0]*0.95,size.window_size[0]*.6)
        self.pos = (size.window_size[0]*0.025,size.window_size[1]*.3)

        width = size.window_size[0]*.8 + 10
        big_wid = Widget(
            size_hint=[None,None],
            size = (width*len(chess_list)+10,size.window_size[0]*.6)
        )
        # add cards with presentations of types of game
        for i in range(len(chess_list)):
            pos = [self.pos[0] + width  * i,0]
            big_wid.add_widget(Card(chess_list[i].picture,chess_list[i].set_chess,pos))
        self.add_widget(big_wid)


class Input(TextInput):
    def __init__(self,size,pos,text):
        super(Input,self).__init__()
        self.size = size
        self.pos = pos
        self.text = text
        self.multiline = False
    
    def input_filter(self,text:str,ind):
        if ind:
            return text
        if (text.isalnum() or text in [' ','_','-']) and len(self.text) < 14 :
            return text
        else:
            return ''


class Frozen_Input(TextInput):
    def __init__(self,size,pos,text):
        super(Frozen_Input,self).__init__()
        self.size = size
        self.pos = pos
        self.text = text
        self.multiline = False
        def change_frozen(wid,value):
            if value == '':
                global_constants.game.frozen_moves = 20
            elif int(value) > 0:
                global_constants.game.frozen_moves = int(value)            
            else:
                global_constants.game.frozen_moves = 20
                wid.text = '20'

        self.bind(text = change_frozen)

    def input_filter(self,text:str,ind):
        if ind:
            return text
        if text.isdigit() and (self.text == '' or int(self.text) < 100):
            return text
        else:
            return ''


class Settings_widget(Widget):
    def __init__(self, size,pos):
        super(Settings_widget,self).__init__()
        self.size = size
        self.pos = pos
        with self.canvas:
            Color(0.1,0.2,0.7,0.5)
            Rectangle(
                size=size,
                pos=pos   
            )
        self.create_text()
        self.create_active()

    def create_text(self):
        texts = [Get_text('change_time'),Get_text('change_tips'),Get_text('change_add')]
        poses = [
            [self.pos[0] + self.size[0] * .1, self.pos[1] + self.size[1] * .5],
            [self.pos[0] + self.size[0] * .1, self.pos[1] + self.size[1] * .2],
            [self.pos[0] + self.size[0] * .1, self.pos[1] + self.size[1] * .37]
        ]
        if global_constants.game.type_of_chess == 'magik':
            texts.append(Get_text('change_magia'))
            poses.append([self.pos[0]+self.size[0]*.17, self.pos[1]+self.size[1]*.09])
        if global_constants.game.type_of_chess == 'frozen':
            texts.append(Get_text('change_frozen'))
            poses.append([self.pos[0]+self.size[0]*.1, self.pos[1]+self.size[1]*.07])
        if global_constants.game.state_game == 'one':
            texts.append(Get_text('change_nik'))
            poses.append([self.pos[0]+.01*self.size[0], self.pos[1]+.8*self.size[1]])
        else:
            texts.append(Get_text('change_your_color'))
            poses.append([self.pos[0]+.08*self.size[0], self.pos[1]+.78 *self.size[1]])

        for i in range(len(texts)):
            self.add_widget(Label(
                text = texts[i],
                color = (1,1,0,1),
                pos = poses[i]
            ))

    def create_active(self):
        pos = self.pos
        size = self.size
        game = global_constants.game
       # niks
        if game.state_game == 'one':
            texts = [game.name1, game.name2]
            for i in 0,1:
                self.add_widget(Input(   
                    size = [.62 * self.size[0], 50],
                    pos = [ pos[0] + size[0] * .35  , pos[1] + size[1] * (9-i) / 10],
                    text= texts[i]
                ))
        else:
            def set_color(wid,value):
                if value in ['Белый','White','Blanc','Blanco','weiß']:
                    global_constants.game.play_by = 'white'
                else:
                    global_constants.game.play_by = 'black'

            self.add_widget(Spinner(
                on_change=set_color,
                text = Get_text(f'change_{game.play_by}'),
                values = [ Get_text('change_'+i) for i in ['white','black']],
                size=[.4 * size[0] , 50 ],
                pos=[ pos[0] + .5 * size[0] , pos[1] + .8 * size[1]]   
            ))


        #  Подсказки хода 
        def tip(wid,value):
            global_constants.game.make_tips=value

        self.add_widget(Switch(
            active=game.make_tips,
            pos=[ pos[0] + size[0] * .55, pos[1] + size[1] * .23],
            size = [110,40],
            on_change = tip
        ))

        #time
        mins = Get_text('change_min')
        self.add_widget(Spinner(
            on_change=self.change_time,
            pos = [pos[0] + .5 * size[0] , pos[1] + size[1] * .53 ] ,
            size = [.4 * self.size[0] , 50],
            value = f'{game.time_mode//60} ' + mins ,
            values = [f'{i} ' + mins for i in [0,5,15,30,60,90]] ,
            background_color = [.9 , 0.196, .266, .5],
            background_normal = ''

        ))

        # add time
        sec = Get_text('change_sec')
        self.add_widget(Spinner(
            on_change = self.change_add,
            text = f'{game.add_time} ' + sec,
            values=[f'{i} ' + sec for i in [0,1,5,10,15,30,90,300]],
            size = [.4 * size[0] , 50 ],
            pos = [ pos[0] + .5 * size[0] , pos[1] + .4 * size[1]],
            background_color = [.9 , 0.196, .266, .5],
            background_normal = ''
        ))
    
        if game.type_of_chess == 'magik':
            def magia(wid,value):
                game.magia_moves = int(value)
            self.add_widget(Spinner(
                on_change=magia,
                text = '10',
                values = [str(i) for i in [1,2,3,5,10,15,20]],
                size=[.4 * size[0] , 50 ],
                pos=[ pos[0] + .5 * size[0] , pos[1] + .06 * size[1]],
                background_normal = '',
                background_color = [1, 0.8 ,.0 ,.5],
                drop_color = [1, 1, 1, 1],
                drop_spacing = 8,
                drop_background_color = [.259, .66, 1, .8]
           ))
        
        if game.type_of_chess == 'frozen':
            self.add_widget(Frozen_Input(
                pos=[ pos[0] + .5 * size[0] , pos[1] + .1 * size[1]],
                text=str(game.frozen_moves),
                size=[.2 * self.size[0], 50]
            ))

    def change_add(self,wid,value):
        value = int( value.split()[0] )
        current = value
        game = global_constants.game
        if value == 300 and game.time_mode < 5400 :
            value = 90
        if value == 90 and game.time_mode < 3600 :
            value = 30
        if value == 30 and game.time_mode < 1800 :
            value = 15
        if value == 15 and game.time_mode < 15 * 60 :
            value = 10
        if not game.with_time :
            value = 0
        sec = Get_text('change_sec')
        game.set_add(value)
        if current != value :
            wid.text = f'{value} {sec}'

    def change_time(self,wid,value):
        value = int(value.split()[0])
        game = global_constants.game
        game.with_time = value != 0 
        game.set_time(value*60)
        a = 0
        # another spinner
        if value == 0 :
            self.children[a].text = self.children[a].values[0]  # 0
            game.set_add(0)
        else:
            if value == 5 and game.add_time > 10 :
                self.children[a].text = self.children[a].values[3]  # 0,1,5,10
                game.add_time = 10
            elif value == 15 and game.add_time > 15:
                game.add_time = 15
                self.children[a].text = self.children[a].values[4]  #  0,1,5,10,15
            elif value == 30 and game.add_time > 30:
                game.add_time = 30
                self.children[a].text = self.children[a].values[5]  # 0,1,5,10,15,30
            elif value == 60 and game.add_time > 90 :
                game.add_time = 90
                self.children[a].text = self.children[a].values[6]  # 0,1,5,10,15,30,90

    def on_touch_down(self,touch):
        a = super(Settings_widget,self).on_touch_down(touch)
        if a:
            for wid in self.children:
                if type(wid) == Spinner and not wid.collide_point(*touch.pos) :
                    wid.close()
        return a



###############################################################
# create lists with all types of chess
###############################################################


classic_type = [Chess_type(el)for el in['classic', 'los_alamos', 'garner','schatranj']]
positions =    [Chess_type(el)for el in['fisher','horse_battle']]
with_effects = [Chess_type(el)for el in['magik', 'permutation', 'kamikadze', 
                            'haotic','dark_chess','frozen'
                ]]
honestless =   [Chess_type(el)for el in['horde', 'week', 'bad_chess']]
boards =       [Chess_type(el)for el in['circle_chess', 'bizantion', 'glinskiy', 'kuej']]
other_rules =  [Chess_type(el)for el in['rasing']]

all_chess = classic_type + positions + with_effects + honestless + boards + other_rules

