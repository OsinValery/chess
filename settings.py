from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.graphics import Color,Rectangle
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from my_spinner import Spinner
from switch import Switch_ as Switch

import os
import random
from translater import Get_text
import global_constants


def back(click):
    global settings_widget
    if 'figs'  in dir(settings_widget.widgets[1].board):
        del settings_widget.widgets[1].board.figs
    settings_widget.widgets[1].board.canvas.clear()
    settings_widget.widgets[1].board.clear_widgets()
    del settings_widget.widgets[1].board
    for wid in settings_widget.widgets:
        wid.canvas.clear()
        wid.clear_widgets()   
    settings_widget.clear_widgets()
    settings_widget.canvas.clear()    
    del settings_widget.widgets
    del settings_widget
    # при завершении работы приложения это педотвращает ошибки
    settings_widget = True
    global_constants.Main_Window.create_start_game(1)

music_files = [f'sound{i}.ogg' for i in range(1,9)]
move_files = [f'move{i}.ogg' for i in range(1,7)]
max_fig_set = 12
game_fon_files = ['fon{0}'.format(i) for i in range(1,13)]
boards_files = [str(i) for i in range(11)]
languages = ['Русский','English','Español','Deutsch','Français'] 


text_color = [1,.9,0,1]
settings_widget = True

class __Settings():
    def __init__(self):
        self.lang = 'ru'
        self.with_sound = True
        self.with_effects = True
        self.volume = .5
        self.fon_music = 'sound1.ogg'
        self.move_music = 'move1.ogg'
        self.bace_fon = 'pic4.png'
        self.game_fon = 'fon1.png'
        self.fig_set = 'fig_set1'
        self.boards = '0'
        self.folder = ''
        self.user_folder = ''
        self.default_nick = 'Super Hero'
        global_constants.Settings = self
    
    def read_settings(self):
        #this function dont run in __init__ because it need in \n
        #user folder, that will be found in App.build
        if 'settings.txt' in os.listdir(self.user_folder):
            try:
                file_settings = open(os.path.join(self.user_folder,'settings.txt'))
                sets = str(file_settings.read()).split('\n')
                file_settings.close()
                self.lang = sets[0]
                self.with_sound = True if sets[1]=='True' else False
                self.with_effects = sets[2] == 'True' 
                self.volume = float(sets[3])
                self.fon_music = sets[4]
                self.move_music = sets[5]
                self.bace_fon = sets[6]
                self.game_fon = sets[7]
                self.fig_set = sets[8]
                self.boards = sets[9]
                self.default_nick = sets[10]
            except:
                self.write_settings()
        else:
            self.write_settings()

    def write_settings(self):
        file_settings = open(os.path.join(self.user_folder,'settings.txt'),'w')
        file_settings.write(self.lang+'\n')
        file_settings.write('True\n' if self.with_sound else 'False\n')
        file_settings.write('True'+'\n' if self.with_effects else 'False'+'\n') 
        file_settings.write(str(self.volume)+'\n')
        file_settings.write(self.fon_music+'\n')
        file_settings.write(self.move_music+'\n')
        file_settings.write(self.bace_fon+'\n')
        file_settings.write(self.game_fon+'\n')
        file_settings.write(self.fig_set+'\n')
        file_settings.write(self.boards+'\n')
        file_settings.write(self.default_nick+'\n')

        file_settings.close()

    def get_lang(self):
        if self.lang == 'ru':
            return 'Русский'
        if self.lang == 'en':
            return 'English'
        if self.lang == 'es':
            return 'Español'
        if self.lang == 'de':
            return 'Deutsch'
        elif self.lang == 'fr':
            return 'Français'
        return 'Err'

    def get_folder(self):
        """return bace folder with main.py"""
        return self.folder + os.sep

    def get_board_picture(self,tipe):
        file = 'вы забыли поставить доску в settings.py'
        standart = [
            'classic','magik','fisher','horse_battle',
            'permutation','horde','week','kamikadze',
            'bad_chess','rasing', 'haotic', 'schatranj',
            'dark_chess','frozen'
        ]
        if tipe in standart:
            file =  'board.png'
        elif tipe == 'los_alamos':
            file =  'board6x6.png'
        elif tipe in ['circle_chess','bizantion']:
            file = 'board360.png'
        elif tipe in ['glinskiy','kuej']:
            file = 'gekso_board.png'
        elif tipe == 'garner':
            file = 'board5x5.png'
        return os.path.join(self.get_folder(),'pictures','boards',self.boards,file)

    def get_music(self):
        for file in music_files:
            if file == self.fon_music:
                return file[:-4]

    def get_move(self):
        return self.move_music[:-4]

    def get_bace_picture(self):
        return os.path.join(self.get_folder(),'pictures','bace_fons',self.bace_fon)

    def get_game_fon(self):
        return os.path.join(self.get_folder(),'pictures','game_fons',self.game_fon)
    
    def get_fig_set(self):
        return self.fig_set

    def set_folder(self,fold):
        self.folder = fold

    def set_sound(self,inst,value):
        self.with_sound = value
        if self.with_sound:
            global_constants.Music.start()
        else:
            global_constants.Music.stop()
        self.write_settings()
    
    def set_effects(self,inst,value):
        self.with_effects = value
        self.write_settings()
    
    def set_volume(self,value):
        self.volume = value
        self.write_settings()

    def set_nick(self,wid,nick):
        self.default_nick = nick
        self.write_settings()

    def change_music(self,spin,value):
        if self.fon_music != value + '.ogg':
            self.fon_music = value+'.ogg'
            self.write_settings()
            global_constants.Music.change_music(self.fon_music)

    def change_effect(self,spin,value):
        if self.fon_music != value + '.ogg':
            self.move_music = value + '.ogg'
            global_constants.Music.change_move(self.move_music)
            self.write_settings()
    
    def change_bace_picture(self,wid,value):
        value += '.png'
        self.bace_fon = value
        widget = global_constants.Main_Window
        widget.canvas.clear()
        widget.remove_widget(settings_widget)
        widget.canvas.add(Rectangle(size=widget.size,source=self.get_bace_picture()))
        widget.add_widget(settings_widget)
        but = widget.children[0]
        if type(but) != Button:
            but = widget.children[1]
        widget.remove_widget(but)
        widget.add_widget(but)
        self.write_settings()

    def change_game_fon(self,wid,value):
        self.game_fon = value + '.png'
        settings_widget.widgets[1].board.renew()
        self.write_settings()

    def change_boards(self,wid,value):
        self.boards = value
        settings_widget.widgets[1].board.renew()
        self.write_settings()

    def change_fig_set(self,wid,value):
        self.fig_set = value
        settings_widget.widgets[1].board.renew()
        self.write_settings()

    def change_language(self,wid,value):
        global settings_widget
        if value == 'Русский':
            self.lang = 'ru'
        elif value == 'English' :
            self.lang = 'en'
        elif value == 'Español':
            self.lang = 'es'
        elif value =='Deutsch':
            self.lang = 'de'
        elif value == 'Français':
            self.lang = 'fr'
        else:
            print( 'not defined language')
        self.write_settings()
        widget = global_constants.Main_Window
        widget.parent.title = Get_text('bace_title_app')
        widget.remove_widget(settings_widget)
        settings_widget.clear_widgets()
        settings_widget.canvas.clear()
        del settings_widget.widgets
        del settings_widget
        settings_widget = Settings_Widget(2)
        widget.add_widget(settings_widget)
        for wid in widget.children:
            if type(wid) == Button:
                wid.text = Get_text('all_back')



Settings = __Settings()
# next code is graphics

def create_interface(click):
    global settings_widget
    widget = global_constants.Main_Window
    settings_widget = Settings_Widget()
    widget.clear_widgets()
    size = widget.size
    widget.add_widget(Button(
        text=Get_text('all_back'),
        pos = [size[0]*0.8,size[1]*0.9],
        size = [size[0]*0.2,size[1]*0.07],
        background_color = (1,0.2,1,0.5),
        font_size = 30,
        color=(0,1,0.1,1),
        on_press = back   ))
    widget.add_widget(settings_widget)


class Settings_Widget(Widget):
    def __init__(self,active=0):
        super(Settings_Widget,self).__init__()
        widget = global_constants.Main_Window

        self.size = [.8*widget.size[0],.8*widget.size[1]]
        self.pos = [.1*widget.size[0],.1*widget.size[1]]
        self.widgets = []

        with self.canvas:
            Color(0,1,1,.3)
            Rectangle(
                size = self.size,
                pos = self.pos
            )


        self.names = [  Get_text('settings_music'),
                        Get_text('settings_see'),
                        Get_text('settings_all')  ]
        def press(touch):
            self.set_block(self.names.index(touch.text))
            for wid in self.children:
                if type(wid) == Button :
                    if wid.text == touch.text:
                        wid.background_color = [0,1,0,.5]
                    else:
                        wid.background_color = [1,.5,0,.5]
            

        size = self.size[0] // len(self.names)
        for i in range(len(self.names)):
            self.add_widget(Button(
                text = self.names[i],
                size = [size,50],
                pos = [self.pos[0] + i * size,self.pos[1] + self.size[1]-50],
                on_press = press,
                background_color = [0,1,0,.5] if i == active else [1,.5,0,.5]
            ))
            self.widgets.append(Widget(
                pos = self.pos,
                size =  [self.size[0],self.size[1]-50]
            ))
        
        self.fill_widgets()
        self.current = self.widgets[active]
        self.add_widget(self.current)

    def fill_widgets(self):
        fill_0(self.widgets[0])
        fill_1(self.widgets[1])
        fill_2(self.widgets[2])  

    def set_block(self,nomber):
        if nomber < 0 or nomber >= len(self.widgets):
            raise 'Nomber has bad value'    
        self.remove_widget(self.current)
        self.current = self.widgets[nomber]
        self.add_widget(self.current)

    def on_touch_down(self,touch):
        a = super(Settings_Widget,self).on_touch_down(touch)
        if a:
            for wid in self.current.children:
                if type(wid) == Spinner and not wid.collide_point(*touch.pos):
                    wid.close()
        return a


def fill_0(content):
    cont_size = content.size
    pos = content.pos

    label_texts = [
        Get_text('settings_music'),
        Get_text('settings_effects'),
        Get_text('settings_volume'),
        Get_text('settings_check_music'),
        Get_text('settings_change_effect'),
    ]
    label_poses = [
        [pos[0],pos[1]+.8*cont_size[1]],
        [pos[0],pos[1]+.6*cont_size[1]],
        [pos[0],pos[1]+.4*cont_size[1]],
        [pos[0]+cont_size[0]*.05,pos[1]+cont_size[1]/4],
        [pos[0]+cont_size[0]*.05,pos[1]+cont_size[1]/10],
    ]

    for i in range(len(label_poses)):
        content.add_widget(Label(
            size = [.3*cont_size[0],.1*cont_size[1]],
            pos = label_poses[i],
            text = label_texts[i],
            color = text_color
        ))

    #add all of the active widgets
    content.add_widget(Switch(
        active = Settings.with_sound,
        pos = [pos[0]+.5*cont_size[0],pos[1]+.83*cont_size[1]],
        on_change = Settings.set_sound
    ))

    content.add_widget(Switch(
        active = Settings.with_effects,
        pos = [pos[0]+.5*cont_size[0],pos[1]+.63*cont_size[1]],
        on_change = Settings.set_effects
    ))

    def renew(self,touch):
        Settings.set_volume(slide.value_normalized)
        global_constants.Music.change_volume(slide.value_normalized)

    slide = Slider(
        min = 0,
        max = 100,
        step = 1,
        pos = [pos[0]+.45*cont_size[0],pos[1]+.43*cont_size[1]],
        size = [.4*cont_size[0],20],
        value = Settings.volume * 100,
        on_touch_move = renew
    )
    content.add_widget(slide)

    changes = [Settings.change_music,Settings.change_effect]
    poses = [
        [pos[0] + cont_size[0]*.5,pos[1] + cont_size[1] * .28],
        [pos[0] + cont_size[0]*.5,pos[1] + cont_size[0] * .22],
    ]
    texts = [Settings.get_music(),Settings.get_move()]
    values = [
        [file[:-4] for file in music_files],
        [file[:-4] for file in move_files],
    ]

    for i in 0,1:
        content.add_widget(Spinner(
            on_change=changes[i],
            text=texts[i],
            values = values[i],
            pos = poses[i],
            size = [.22*cont_size[0],55],
            drop_color = text_color,
            drop_background_normal = '',
            background_color = [.9 , 0.196, .266, .5],
            drop_spacing = 5,
            drop_height = 80
        ))


def fill_1(content:Widget):
    cont_size = content.size
    pos = content.pos

    content.board = Demonstrate_interface(
        size = [.8* content.size[0] ,.5* content.size[1]],
        pos = [.1 * content.size[0] + pos[0],.1 * content.size[0] + pos[1]]
    )
    content.add_widget(content.board)

    texts = [Settings.fig_set,       Settings.boards,
            Settings.game_fon[:-4],  Settings.bace_fon[:-4]
    ]
    values = [
        [f'fig_set{i}' for i in range(1,max_fig_set+1)],
        boards_files,  game_fon_files,
        [f'pic{i}' for i in range(1,9)],
    ]
    poses = [
        [pos[0] + cont_size[0]*.5,pos[1]+cont_size[1]*.63],
        [pos[0] + cont_size[0]*.5,pos[1]+cont_size[1]*.73],
        [pos[0] + cont_size[0]*.5,pos[1]+cont_size[1]*.83],
        [pos[0] + cont_size[0]*.5,pos[1]+cont_size[1]*.93],
    ]
    changes = [
        Settings.change_fig_set,
        Settings.change_boards,
        Settings.change_game_fon,
        Settings.change_bace_picture,
    ]

    for i in 0,1,2,3:
        content.add_widget(Spinner(
            text = texts[i],
            values = values[i],
            size = [cont_size[0]*.4,55],
            pos = poses[i],
            on_change=changes[i],
            drop_color = text_color,
            drop_height = 50,
            drop_background_color = [.259, .66, 1, 2],
            drop_spacing = 10
            )) 

    texts = [
        Get_text('settings_change_fon'),
        Get_text('settings_change_game_fon'),
        Get_text('settings_change_board'),
        Get_text('settings_change_figure'),
    ]

    for i in 0,1,2,3:
        content.add_widget(Label(
            color = text_color,
            text = texts[i],
            pos = [pos[0]+cont_size[0]/10, pos[1]+cont_size[1]*(9-i)/10],
            font_size = 36     
        ))

    
def fill_2(content):
    cont_size = content.size
    pos = content.pos
    content.add_widget(Label(
        text = Get_text('settings_language'),
        pos = [pos[0] + .2*cont_size[0],pos[1] + .8 * cont_size[1]],
        font_size = 36,
        color = text_color
    ))
    content.add_widget(Spinner(
        on_change=Settings.change_language,
        text = Settings.get_lang(),
        size = [cont_size[0]*.4, 55],
        values = languages,
        pos = [pos[0] + .5*cont_size[0],pos[1] + .82 * cont_size[1]],
        drop_height = 50,
        drop_color = text_color,
        drop_background_normal = '',
        drop_background_color = [.4, 0, 1, .5],
        background_color = [1, .6, 0, .7],
        background_normal = ''
    ))
    text = TextInput(
        text = Settings.default_nick,
        pos = [pos[0] + .5*cont_size[0],pos[1] + .7 * cont_size[1]],
        size = [.3 * content.size[0], 0.05 * content.size[1]],
        multiline = False
    )
    text.bind(text = Settings.set_nick)
    content.add_widget(text)
    content.add_widget(Label(
        text = Get_text('settings_nick'),
        pos = [pos[0] + .15 * cont_size[0],pos[1] + .7 * cont_size[1]],
        font_size = 36,
        color = text_color,
        size = [.3 * content.size[0], text.size[1]]
    ))


def get_fig_file(figure):
    name = figure[0][0] + figure[1][0] + '.png'
    return os.path.join(Settings.get_folder(),'pictures',Settings.get_fig_set(),name)


class Demonstrate_interface(Widget):
    def __init__(self,size,pos):
        super(Demonstrate_interface,self).__init__()
        self.size = size
        self.pos = pos
        self.board_size = [.7*self.size[0]] * 2
        self.board_pos = [  
            (self.size[0]-self.board_size[0])//2 + pos[0] ,
            (self.size[1]-self.board_size[1])//2 + pos[1]
        ]   

        self.canvas.add(Rectangle(
            size = self.size,
            pos = [self.pos[0],self.pos[1]],
            source = Settings.get_game_fon()
        ))
        self.canvas.add(Rectangle(
            size = self.board_size,
            pos = self.board_pos,
            source = Settings.get_board_picture('classic')
        ))

        n = random.randint(0,10)
        fill = []
        x,y = random.randint(0,7), random.randint(0,7)
        x2,y2 = x,y
        while abs(x-x2) < 2 or abs(y-y2) < 2:
            x2 = random.randint(0,7)
            y2 = random.randint(0,7)
        fill = [[x,y],[x2,y2]]
        del x,y, x2,y2

        self.figs = [ ['king','white',fill[0]]  ]
        self.figs.append( [ 'king','black',fill[1] ] )
        # create another figures
        for i in range(n):
            x,y = fill[0]
            while [x,y] in fill:
                x,y = random.randint(0,7),random.randint(0,7)
            set_ = ['queen','horse','bishop','rook']
            if y not in [0,7]:
                set_.append('pawn')
            fill.append([x,y])
            tip = random.choice(set_)
            self.figs.append( [tip,random.choice(['white','black']) , [x,y] ] )
        
        field = (9/80) * self.board_size[0]
        top = .05 * self.board_size[0]
        del fill
        for fig in self.figs:
            x,y = fig[2]
            rect = Rectangle(
                size = [field]*2,
                source = get_fig_file(fig),
                pos = [self.board_pos[0] + field * x + top, self.board_pos[1] + field * y + top]
                )
            self.canvas.add(rect)
            fig.append(rect)

    def renew(self):
        self.canvas.clear()
        self.canvas.add(Rectangle(
            size = self.size,
            pos = [self.pos[0],self.pos[1]],
            source = Settings.get_game_fon()
        ))
        self.canvas.add(Rectangle(
            size = self.board_size,
            pos = self.board_pos,
            source = Settings.get_board_picture('classic')
        ))
        for fig in self.figs:
            fig[3].source = get_fig_file(fig)
            self.canvas.add(fig[3])



    
