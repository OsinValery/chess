from kivy.uix.label import Label
from kivy.graphics import Rectangle

from translater import Get_text
from settings import Settings
import global_constants
from tutorial_widget import Tutorial_Widget
from picture_tutorial import Static_picture
from film_widget import VideoChess
from tutorial_button import Button_ as Button

import random
import os


normal_font_size = 24


def get_text(text,width,leng):
    sim = width // leng - 1
    pos = 0
    end_text = ''
    words = text.split()
    while len(words) != 0:
        if len(words[0]) <= sim - pos:
            end_text += words[0] + ' '
            pos += len(words[0]) + 1
            words = words[1::]
        else:
            end_text += '\n'
            pos = 0
    return end_text

def get_params(command):
    global back_command
    back_command = command


def help_tutorial():
    global_constants.Main_Window.clear_widgets()
    global_constants.Main_Window.canvas.clear()
    global_constants.Main_Window.canvas.add(Rectangle(
        size = global_constants.Main_Window.size,
        source= os.path.join(Settings.folder,'pictures','tutorial.png'),
        pos = (0,0)
    )) 
    size = global_constants.Main_Window.size

    def leave(click):
        for wid in global_constants.Main_Window.children:
            if type(wid) == VideoChess:
                wid.must = False
                wid.__del__()
        back_command(click)

    global_constants.Main_Window.add_widget(Button(
        text = Get_text('tutorial_to_game'),
        background_color = (0,1,0,0.3),
        color =  (1,1,0,1),
        size = (size[0]*0.15 , size[1]*0.05),
        pos = (size[0] * 0.75 , size[1] * 0.9),
        on_press = leave
    ))


def lost_tutorial():
    help_tutorial()
    global_constants.Main_Window.add_widget(Label(
        text = 'Я бы мог вас обучить, \nно не знаю как!',
        color = [1,0,0,1],
        font_size = 40,
        center = global_constants.Main_Window.center
    ))

def interactive_interface(size,figure,btn_command,label_text='',fig_pos = [4,4]):
    """
    create standart interface of tutorial
    with onetype parameters of objects\n
    size - window.size\n
    figure = 'bishop'\n
    label_text <- Get_text(...)
    """
    global_constants.Main_Window.add_widget(Label(
        text = get_text(label_text,size[0]*0.9,normal_font_size/2),
        shorten=True,
        font_size = normal_font_size,
        color = (0,0,0,1),
        pos = (size[0]*0.05,size[1]*0.55),
        size = (size[0]*0.9,size[1]*0.4),
        halign="center",
        valign = "middle",
    ))

    global_constants.Main_Window.add_widget(Tutorial_Widget(
        size = [0.7*size[0]]*2,
        pos = (size[0]*0.05,size[1]*0.2),
        game =global_constants.game,
        figures = [[figure,random.choice(['black','white']),*fig_pos]]
    ))

    global_constants.Main_Window.add_widget(Button(
        text = Get_text('tutorial_next'),
        pos = (size[0] * 0.65 , size[1] * 0.05),
        background_normal = '',
        background_color = (1,1,0,0.3),
        color = (0,1,0,1),
        on_press = btn_command
    ))

def static_interface(size,label_text,btn_command,repeat=False):
    global_constants.Main_Window.add_widget(Label(
        text = get_text(label_text,size[0]*0.9,normal_font_size/2),
        shorten=True,
        font_size = normal_font_size,
        color = (0,0,0,1),
        pos = (size[0]*0.05,size[1]*0.55),
        size = (size[0]*0.9,size[1]*0.4),
        halign="center",
        valign = "middle",
    ))
    global_constants.Main_Window.add_widget(Static_picture(
        size=[0.7*size[0]]*2,
        game = global_constants.game,
        options=['start']
    ))

    button_text = Get_text('tutorial_next') if not repeat else Get_text('tutorial_repeat')
    global_constants.Main_Window.add_widget(Button(
        text = button_text,
        pos = (size[0] * 0.65 , size[1] * 0.05),
        background_normal = '',
        background_color = (1,1,0,0.3),
        color = (0,1,0,1),
        on_press = btn_command
    ))

def video_interface(board,actions=[],speed=1,command=print,text=''):
    help_tutorial()
    size = global_constants.Main_Window.size
    global_constants.Main_Window.add_widget(Label(
        text = text,
        shorten=True,
        font_size = normal_font_size,
        color = (0,0,0,1),
        pos = (size[0]*0.05,size[1]*0.5),
        size = (size[0]*0.9,size[1]*0.4),
        halign="center",
        valign = "middle",
    ))

    video = VideoChess(
        board = board,
        speed = speed,
        actions=actions
    )
    global_constants.Main_Window.add_widget(video)

    def later(cllick):
        video.timer.cancel()
        video.__del__()
        video.must = False
        command(cllick)

    global_constants.Main_Window.add_widget(Button(
        text = Get_text('tutorial_next'),
        pos = (size[0] * 0.65 , size[1] * 0.05),
        background_color = (1,1,0,0.3),
        color = (0,1,0,1),
        on_press = later
    ))


def tutorial(press):
    game = global_constants.game
    if game.type_of_chess == 'classic':
        do_classic_tutorial(0)
    elif game.type_of_chess == 'fisher':
        do_fisher_tutorial()
    elif game.type_of_chess == 'horse_battle':
        do_horse_tutorial(1)
    elif game.type_of_chess == 'magik':
        do_magik_tutorial(1)
    elif game.type_of_chess == 'los_alamos':
        do_los_alamos_tutorial(1)
    elif game.type_of_chess == 'permutation':
        do_permut_tutorial(1)
    elif game.type_of_chess == 'glinskiy':
        do_glinskiy_tutorial()
    elif game.type_of_chess == 'circle_chess':
        do_round_tutorial()
    elif game.type_of_chess == 'bizantion':
        do_bizantion_tutorial()
    elif game.type_of_chess == 'kuej':
        do_kuej_tutorial()
    elif game.type_of_chess == 'garner':
        do_garner_tutorial()
    elif game.type_of_chess == 'horde':
        do_horde_tutorial()
    elif game.type_of_chess == 'week':
        do_weak_tutorial()
    elif game.type_of_chess == 'kamikadze':
        do_kamikadze_tutorial()
    elif game.type_of_chess == 'bad_chess':
        do_bad_tutorial()
    elif game.type_of_chess == 'rasing':
        do_racing_tutorial()
    elif game.type_of_chess == 'haotic':
        do_haos_tutorial()
    elif game.type_of_chess == 'schatranj':
        do_schatranj_tutorial()
    elif game.type_of_chess == 'dark_chess':
        do_dark_tutorial()
    else:
        lost_tutorial()

# for classic chess
def do_classic_tutorial(click):
    help_tutorial()
    static_interface(
        global_constants.Main_Window.size,
        Get_text('tutorial_classic_description'),
        classic_1
    )

def classic_1(press):
    help_tutorial()
    size = global_constants.Main_Window.size
    command = classic_2
    if global_constants.game.type_of_chess == 'los_alamos':
        command = classic_3
    interactive_interface(
        size = size,
        figure = 'horse',
        btn_command=command,
        label_text=Get_text('tutorial_classic_horse')
    )

def classic_2(press):
    help_tutorial()
    interactive_interface(
        size = global_constants.Main_Window.size,
        figure = 'bishop',
        btn_command = classic_3,
        label_text = Get_text('tutorial_classic_bishop')
    )

def classic_3(press):
    help_tutorial()
    interactive_interface(
        size = global_constants.Main_Window.size,
        figure = 'rook',
        btn_command = classic_4,
        label_text=Get_text('tutorial_classic_rook')
    )
    
def classic_4(press):
    help_tutorial()
    command = classic_5
    if global_constants.game.type_of_chess in ['horde', 'rasing','los_alamos']:
        command = classic_7
    interactive_interface(
        size = global_constants.Main_Window.size,
        btn_command = command,
        label_text = Get_text('tutorial_classic_queen'),
        figure = 'queen'
    )

def classic_5(press):
    command = classic_6
    size = global_constants.Main_Window.size
    text = get_text(Get_text('tutorial_classic_pawn'),size[0]*0.9,normal_font_size/2)
    board = [
        ['white',2,1,'pawn'],['black',3,3,'pawn'],['white',1,5,'pawn'],
        ['white',6,3,'pawn'],['black',5,5,'pawn'],['black',2,6,'pawn']
    ]
    action = [
        ['show',6,3,[[6,4]]],       ['move',6,3,6,4],
        ['show',5,5,[[5,4]]],       ['move',5,5,5,4],
        ['show',6,4,[[6,5]]],       ['move',6,4,6,5],       
        ['show',5,4,[[5,3]]],       ['move',5,4,5,3],
        ['move',6,5,6,6],           ['move',5,3,5,2],
        ['move',6,6,6,7],           ['change',6,7,'queen'],
        ['move',5,2,5,1],           ['move',6,7,7,7],       
        ['show_attack',2,6,1,5],    ['pause'],
        ['take',2,6,1,5],           ['show',2,1,[[2,2],[2,3]]],
        ['move',2,1,2,3],           ["show_attack",3,3,2,2],
        ['pause'],                  ['take',3,3,2,2]
    ]
    video_interface(board,action,1,command,text)

def classic_6(press):
    size = global_constants.Main_Window.size    
    text = get_text(Get_text('tutorial_classic_pawn2'),size[0]*0.9,normal_font_size/2)
    board = [['white',7,1,'pawn'],['black',6,3,'pawn'],['white',6,1,'pawn'],
                ['black',1,6,'pawn'],['white',2,4,'pawn']]
    actions = [
        ['show',7,1,[[7,2],[7,3]]],     ['move',7,1,7,3],
        ['show_attack',6,3,7,2],        ['take',6,3,7,2],
        ['show_attack',6,1,7,2],        ['take',6,1,7,2],
        ['show',1,6,[[1,5],[1,4]]],     ['move',1,6,1,4],
        ['show_attack',2,4,1,5],        ['take',2,4,1,5]
    ]
    video_interface(board,actions,1,classic_7,text)

def classic_7(press):
    help_tutorial()
    game = global_constants.game
    if game.type_of_chess in [ 'classic','magik','permutation','horde','kamikadze','haotic']:
       command = classic_8
    elif game.type_of_chess in  ['los_alamos']:
        command = classic_9
    elif game.type_of_chess == 'week':
        command = do_weak_tutorial
    elif game.type_of_chess == 'bad_chess':
        command = bad_2
    elif game.type_of_chess == 'rasing':
        command = do_racing_tutorial
    elif game.type_of_chess in ['dark_chess']:
        command = classic_8
    else:
        command = fisher1

    interactive_interface(
        size = global_constants.Main_Window.size,
        figure = 'king',
        btn_command = command,
        label_text = Get_text('tutorial_classic_king')
    )

def classic_8(press):
    size = global_constants.Main_Window.size    
    text = get_text(Get_text('tutorial_classic_rocking'),size[0]*0.8,normal_font_size/2)
    board = [
        ['white',4,0,'king'],['white',7,0,'rook'],['white',0,0,'rook'],
        ['black',0,7,'rook'],['black',4,7,'king'],['black',7,7,'rook']
    ]
    actions = [
        ['show',4,0,[[6,0]]],     
        ['o-o',0],
        ['show_attack',5,0,5,7],
        ['show',4,7,[[2,7]]],
        ['o-o-o',7]
    ]
    video_interface(board,actions,1,classic_9,text)

def classic_9(press):
    help_tutorial()   
    size = global_constants.Main_Window.size
    game = global_constants.game
    global_constants.Main_Window.add_widget(Label(
        text = get_text(Get_text('tutorial_classic_end'),size[0]*0.8,normal_font_size/2),
        shorten=True,
        font_size = normal_font_size,
        color = (0,0,0,1),
        pos = (size[0]*0.05,size[1]*0.3),
        size = (size[0]*0.9,size[1]*0.4),
        halign="center",
        valign = "middle",
    ))

    but = Button(
        text = Get_text('tutorial_repeat'),
        pos = (size[0] * 0.65 , size[1] * 0.05),
        background_color = (1,1,0,0.3),
        color = (0,1,0,1),
    )
    if game.type_of_chess == 'magik':
        but.bind(on_press=do_magik_tutorial)
    elif game.type_of_chess == 'los_alamos':
        but.bind(on_press=do_los_alamos_tutorial)
    elif game.type_of_chess == 'permutation':
        but.bind(on_press = do_permut_tutorial)
    elif game.type_of_chess == 'horde':
        but.bind(on_press = do_horde_tutorial)
    elif game.type_of_chess == 'kamikadze':
        but.bind(on_press = kami_2)
    elif game.type_of_chess == 'haotic':
        but.bind(on_press=do_haos_tutorial)
    elif game.type_of_chess == 'dark_chess':
        but.bind(on_press = dark2)
    else:
        but.bind(on_press=do_classic_tutorial)
    global_constants.Main_Window.add_widget(but)

# end of classic chess

def do_fisher_tutorial(click = None):
    help_tutorial()
    static_interface(
        size = global_constants.Main_Window.size,
        btn_command = fisher1,
        label_text = Get_text('tutorial_fisher_start')
    )

def fisher1(press):
    help_tutorial()
    size = global_constants.Main_Window.size
    static_interface(
        size = size,
        label_text = Get_text('tutorial_fisher_second'),
        btn_command = fisher2
    )

    global_constants.Main_Window.add_widget(Button(
        text = Get_text('tutorial_see'),
        pos = (size[0] * 0.3 , size[1] * 0.05),
        background_color = (1,1,0,0.3),
        color = (1,0,1,1),
        on_press = classic_1
    ))

def fisher2(press):
    size = global_constants.Main_Window.size    
    text = get_text(Get_text('tutorial_fisher_rocking'),size[0]*0.8,normal_font_size/2)
    board = [
        ['white',4,0,'king'],['white',7,0,'rook'],['white',0,0,'rook'],
        ['black',0,7,'rook'],['black',4,7,'king'],['black',7,7,'rook']
    ]
    actions = [
        ['show',4,0,[[6,0]]],     
        ['o-o',0],
        ['show_attack',5,0,5,7],
        ['show',4,7,[[2,7]]],
        ['o-o-o',7]
    ]
    video_interface(board,actions,1,fisher3,text)


def fisher3(press):
    help_tutorial()
    size = global_constants.Main_Window.size
    global_constants.Main_Window.add_widget(Label(
        text = get_text(Get_text('tutorial_fisher_end'),size[0]*0.8,normal_font_size/2),
        shorten=True,
        font_size = normal_font_size,
        color = (0,0,0,1),
        pos = (size[0]*0.05,size[1]*0.55),
        size = (size[0]*0.9,size[1]*0.4),
        halign="center",
        valign = "middle",
    ))
    global_constants.Main_Window.add_widget(Button(
        text = Get_text('tutorial_repeat'),
        pos = (size[0] * 0.65 , size[1] * 0.05),
        background_color = (1,1,0,0.3),
        color = (0,1,0,1),
        on_press=do_fisher_tutorial
    ))

# end fisher tutorial
def do_horse_tutorial(p):
    help_tutorial()
    size = global_constants.Main_Window.size
    static_interface(size = size,
    label_text = Get_text('tutorial_horse_start'),
    btn_command = horse1
    )

def horse1(press):
    help_tutorial()
    interactive_interface(
        size = global_constants.Main_Window.size,
        label_text = Get_text('tutorial_horse_horse'),
        btn_command = horse2,
        figure = 'horse'
    )

def horse2(press):
    size = global_constants.Main_Window.size
    comand = horse3
    text = get_text(Get_text('tutorial_horse_pawn'),size[0]*0.9,normal_font_size/2)
    board = [
        ['white',2,1,'pawn'],['black',3,3,'pawn'],['white',1,5,'pawn'],
        ['white',6,3,'pawn'],['black',5,5,'pawn'],['black',2,6,'pawn']
    ]
    action = [
        ['show',6,3,[[6,4]]],       ['move',6,3,6,4],
        ['show',5,5,[[5,4]]],       ['move',5,5,5,4],
        ['show',6,4,[[6,5]]],       ['move',6,4,6,5],       
        ['show',5,4,[[5,3]]],       ['move',5,4,5,3],
        ['move',6,5,6,6],           ['move',5,3,5,2],
        ['move',6,6,6,7],           ['change',6,7,'queen'],
        ['move',5,2,5,1],           ['move',6,7,7,7],       
        ['show_attack',2,6,1,5],    ['pause'],
        ['take',2,6,1,5],           ['show',2,1,[[2,2],[2,3]]],
        ['move',2,1,2,3],           ["show_attack",3,3,2,2],
        ['pause'],                  ['take',3,3,2,2]
    ]
    video_interface(board,action,1,comand,text)

def horse3(click):
    size = global_constants.Main_Window.size    
    text = get_text(Get_text('tutorial_horse_pawn2'),size[0]*0.9,normal_font_size/2)
    board = [['white',7,1,'pawn'],['black',6,3,'pawn'],['white',6,1,'pawn'],
                ['black',1,6,'pawn'],['white',2,4,'pawn']]
    actions = [
        ['show',7,1,[[7,2],[7,3]]],     ['move',7,1,7,3],
        ['show_attack',6,3,7,2],        ['take',6,3,7,2],
        ['show_attack',6,1,7,2],        ['take',6,1,7,2],
        ['show',1,6,[[1,5],[1,4]]],     ['move',1,6,1,4],
        ['show_attack',2,4,1,5],        ['take',2,4,1,5]
    ]
    video_interface(board,actions,1,horse4,text)

def horse4(press):
    help_tutorial()
    interactive_interface(
        size = global_constants.Main_Window.size,
        btn_command = horse5,
        label_text = Get_text( 'tutorial_horse_king'),
        figure = 'king'
    )

def horse5(press):
    help_tutorial()
    size = global_constants.Main_Window.size
    global_constants.Main_Window.add_widget(Label(
        text = get_text(Get_text('tutorial_horse_end'),size[0]*0.8,normal_font_size/2),
        shorten=True,
        font_size = normal_font_size,
        color = (0,0,0,1),
        pos = (size[0]*0.05,size[1]*0.3),
        size = (size[0]*0.9,size[1]*0.4),
        halign="center",
        valign = "middle",
    ))

    global_constants.Main_Window.add_widget(Button(
        text = Get_text('tutorial_repeat'),
        pos = (size[0] * 0.65 , size[1] * 0.05),
        background_color = (1,1,0,0.3),
        color = (0,1,0,1),
        on_press=do_horse_tutorial
    ))

# end of horse battle tutorial

def do_magik_tutorial(u):
    help_tutorial()
    static_interface(
        size = global_constants.Main_Window.size,
        label_text = Get_text('tutorial_magik_start'),
        btn_command = classic_2
    )

# end magik tutorial

def do_los_alamos_tutorial(press):
    help_tutorial()
    static_interface(
        size = global_constants.Main_Window.size,
        label_text = Get_text('tutorial_alamos_start'),
        btn_command = los_2
    )

def los_2(preess = 1):
    help_tutorial()
    static_interface(
        size = global_constants.Main_Window.size,
        label_text = Get_text('tutorial_alamos_end'),
        btn_command = classic_1
    )

# end los_alamos tutorial


def do_permut_tutorial(click = None):
    help_tutorial()
    static_interface(
        size = global_constants.Main_Window.size,
        label_text = Get_text('tutorial_permut_start'),
        btn_command = permut_2
    )

def permut_2(click = None):
    help_tutorial()
    size = global_constants.Main_Window.size
    global_constants.Main_Window.add_widget(Label(
            text = Get_text('tutorial_permut_cycle'),
            shorten=True,
            font_size = normal_font_size,
            color = (0,0,0,1),
            pos = (size[0]*0.05,size[1]*0.55),
            size = (size[0]*0.9,size[1]*0.4),
            halign="center",
            valign = "middle"    
    ))

    global_constants.Main_Window.add_widget(Tutorial_Widget(
        size = [0.7*size[0]]*2,
        pos = (size[0]*0.05,size[1]*0.2),
        game = global_constants.game,
        figures = [['bishop','white',4,4],['king','white',3,3] ],
        options = ['rotate']
    ))

    global_constants.Main_Window.add_widget(Button(
        text = Get_text('tutorial_repeat'),
        pos = (size[0] * 0.65 , size[1] * 0.05),
        background_color = (1,1,0,0.3),
        color = (0,1,0,1),
        on_press = do_permut_tutorial   
    ))    
    
    global_constants.Main_Window.add_widget(Button(
        text = Get_text('tutorial_see'),
        pos = (size[0] * 0.3 , size[1] * 0.05),
        background_color = (1,1,0,0.3),
        color = (0,1,0,1),
        on_press = do_classic_tutorial   ))

# end of permutation tutorial

def do_glinskiy_tutorial(click=None):
    help_tutorial()
    static_interface(
        size = global_constants.Main_Window.size,
        label_text = Get_text('tutorial_glinskiy_start'),
        btn_command = glinskiy2
    )

def glinskiy2(click=None):
    help_tutorial()
    interactive_interface(
        size = global_constants.Main_Window.size,
        btn_command = glinskiy3,
        figure = 'rook',
        fig_pos = [5,5],
        label_text = Get_text('tutorial_glinskiy_rook')
    )

def glinskiy3(click=None):
    help_tutorial()
    interactive_interface(
        label_text = Get_text('tutorial_glinskiy_bishop'),
        size = global_constants.Main_Window.size,
        btn_command = glinskiy4,
        figure = 'bishop',
        fig_pos = [2,5]
    )

def glinskiy4(click=None):
    help_tutorial()
    interactive_interface(
        size = global_constants.Main_Window.size,
        label_text = Get_text('tutorial_glinskiy_queen'),
        figure = 'queen',
        fig_pos = [10,4],
        btn_command = glinskiy5
    )

def glinskiy5(click=None):
    help_tutorial()
    interactive_interface(
        size = global_constants.Main_Window.size,
        btn_command = glinskiy6,
        figure = 'horse',
        fig_pos = [3,6],
        label_text = Get_text('tutorial_glinskiy_horse')
    )

def glinskiy6(click=None):
    size = global_constants.Main_Window.size
    text = get_text(Get_text('tutorial_glinskiy_pawn'),size[0]*0.9,normal_font_size/2)
    board = [['white',7,2,'pawn'],['white',3,1,'pawn'],
        ['black',4,3,'pawn'],['black',8,3,'pawn']]
    actions = [
        ['show',3,1,[[3,2],[3,3]]],
        ['move',3,1,3,3],
        ['show_attack',4,3,3,2],
        ['take',4,3,3,2],
        ['show',7,2,[[7,3],[7,4]]],
        ['move',7,2,7,3],
        ['show_attack',8,3,7,3],
        ['take',8,3,7,3]
    ]
    video_interface(board,actions,1,glinskiy7,text)

def glinskiy7(click=None):
    help_tutorial()
    interactive_interface(
        label_text = Get_text('tutorial_glinskiy_king'),
        figure = 'king',
        fig_pos = [4,5],
        size = global_constants.Main_Window.size,
        btn_command = glinskiy8
    )

def glinskiy8(click=None):
    help_tutorial()
    size = global_constants.Main_Window.size
    game = global_constants.game
    global_constants.Main_Window.add_widget(Label(
        text = get_text(Get_text('tutorial_glinskiy_end'),size[0]*0.9,normal_font_size/2),
        shorten=True,
        font_size = normal_font_size,
        color = (0,0,0,1),
        pos = (size[0]*0.05,size[1]*0.5),
        size = (size[0]*0.9,size[1]*0.4),
        halign="center",
        valign = "middle",
    ))

    command = do_glinskiy_tutorial if game.type_of_chess != 'kuej' else do_kuej_tutorial
    global_constants.Main_Window.add_widget(Button(
        text = Get_text('tutorial_repeat'),
        pos = (size[0] * 0.65 , size[1] * 0.05),
        background_color = (1,1,0,0.3),
        color = (0,1,0,1),
        on_press=command
    ))

# end of glinskiy tutorial

def do_round_tutorial(clivk=[]):
    help_tutorial()
    static_interface(
        size = global_constants.Main_Window.size,
        label_text = Get_text('tutorial_round_start'),
        btn_command = round1
    )

def round1(click=None):
    help_tutorial()
    interactive_interface(
        size = global_constants.Main_Window.size,
        figure = 'bishop',
        fig_pos = [2,14],
        label_text = Get_text('tutorial_round_bishop'),
        btn_command = round2
    )

def round2(click=None):
    help_tutorial()
    interactive_interface(
        size = global_constants.Main_Window.size,
        figure = 'rook',
        fig_pos = [2,14],
        label_text = Get_text('tutorial_round_rook'),
        btn_command = round3
    )

def round3(parr=1):
    help_tutorial()
    interactive_interface(
        size = global_constants.Main_Window.size,
        figure = 'queen',
        fig_pos = [0,7],
        label_text = Get_text('tutorial_round_queen'),
        btn_command = round4
    )

def round4(click=None):
    help_tutorial()
    interactive_interface(
        size = global_constants.Main_Window.size,
        figure = 'horse',
        fig_pos = [2,14],
        label_text = Get_text('tutorial_round_horse'),
        btn_command = round5
    )

def round5(par=1):
    help_tutorial()
    interactive_interface(
        size = global_constants.Main_Window.size,
        figure = 'king',
        fig_pos = [1,3],
        label_text = Get_text('tutorial_round_king'),
        btn_command = round6
    )

def round6(par=0):
    help_tutorial()
    size = global_constants.Main_Window.size
    global_constants.Main_Window.add_widget(Label(
        text = get_text(Get_text('tutorial_round_pawn'),size[0]*0.9,normal_font_size/2),
        shorten=True,
        font_size = normal_font_size,
        color = (0,0,0,1),
        pos = (size[0]*0.05,size[1]*0.5),
        size = (size[0]*0.9,size[1]*0.4),
        halign="center",
        valign = "middle",
    ))
    global_constants.Main_Window.add_widget(Tutorial_Widget(
        size = [0.7*size[0]]*2,
        pos = (size[0]*0.05,size[1]*0.2),
        game = global_constants.game,
        figures = [['pawn','black',3,2,'down'], ['pawn','black',1,5,'up']]
    ))

    global_constants.Main_Window.add_widget(Button(
        text = Get_text('tutorial_repeat'),
        pos = (size[0] * 0.65 , size[1] * 0.05),
        background_color = (1,1,0,0.3),
        color = (0,1,0,1),
        on_press=do_round_tutorial
    ))

# end of circle tutorial

def do_bizantion_tutorial(click=None):
    help_tutorial()
    static_interface(
        size = global_constants.Main_Window.size,
        label_text = Get_text('tutorial_bizantion_start'),
        btn_command = biz1
    )

def biz1(click=None):
    help_tutorial()
    size = global_constants.Main_Window.size
    global_constants.Main_Window.add_widget(Label(
        text = get_text(Get_text('tutorial_bizantion_pawn'),size[0]*0.9,normal_font_size/2),
        shorten=True,
        font_size = normal_font_size,
        color = (0,0,0,1),
        pos = (size[0]*0.05,size[1]*0.5),
        size = (size[0]*0.9,size[1]*0.4),
        halign="center",
        valign = "middle",
    ))
    global_constants.Main_Window.add_widget(Tutorial_Widget(
        size = [0.7*size[0]]*2,
        pos = (size[0]*0.05,size[1]*0.2),
        game = global_constants.game,
        figures = [['pawn','black',3,2,'down'], ['pawn','black',1,5,'up']]
    ))
    global_constants.Main_Window.add_widget(Button(
        text = Get_text('tutorial_next'),
        pos = (size[0] * 0.65 , size[1] * 0.05),
        background_color = (1,1,0,0.3),
        color = (0,1,0,1),
        on_press=biz2
    ))

def biz2(click=None):
    help_tutorial()
    interactive_interface(
        size = global_constants.Main_Window.size,
        figure = 'rook',
        fig_pos = [0,10],
        label_text = Get_text('tutorial_bizantion_rook'),
        btn_command = biz3
    )

def biz3(click=[]):
    help_tutorial()
    size = global_constants.Main_Window.size
    interactive_interface(
        size = global_constants.Main_Window.size,
        figure = 'bishop',
        fig_pos = [2,14],
        label_text = Get_text('tutorial_bizantion_bishop'),
        btn_command = biz4
    )

def biz4(click):
    help_tutorial()
    interactive_interface(
        size = global_constants.Main_Window.size,
        figure = 'horse',
        fig_pos = [3,5],
        label_text = Get_text('tutorial_bizantion_horse'),
        btn_command = biz5
    )

def biz5(clicl):
    help_tutorial()
    interactive_interface(
        size = global_constants.Main_Window.size,
        figure = 'king',
        fig_pos = [2,9],
        label_text = Get_text('tutorial_bizantion_king'),
        btn_command = biz6
    )

def biz6(click):
    help_tutorial()
    interactive_interface(
        size = global_constants.Main_Window.size,
        figure = 'queen',
        fig_pos = [0,11],
        label_text = Get_text('tutorial_bizantion_queen'),
        btn_command = biz7
    )

def biz7(clicl):
    help_tutorial()
    size = global_constants.Main_Window.size
    global_constants.Main_Window.add_widget(Label(
        text = get_text(Get_text('tutorial_bizantion_end'),size[0]*0.9,normal_font_size),
        shorten=True,
        font_size = normal_font_size,
        color = (0,0,0,1),
        pos = (size[0]*0.05,size[1]*0.5),
        size = (size[0]*0.9,size[1]*0.4),
        halign="center",
        valign = "middle",
    ))
    global_constants.Main_Window.add_widget(Button(
        text = Get_text('tutorial_repeat'),
        pos = (size[0] * 0.65 , size[1] * 0.05),
        background_color = (1,1,0,0.3),
        color = (0,1,0,1),
        on_press=do_bizantion_tutorial
    ))

# end of bizantion tutorial

def do_kuej_tutorial(click=None):
    help_tutorial()
    static_interface(
        size = global_constants.Main_Window.size,
        btn_command = pawn_kuej_tutorial,
        label_text = Get_text( 'tutorial_kuej_start')
    )

def pawn_kuej_tutorial(click):
    help_tutorial()
    size = global_constants.Main_Window.size
    global_constants.Main_Window.add_widget(Label(
        text = get_text(Get_text( 'tutorial_kuej_end'),size[0]*0.9,normal_font_size/2),
        shorten=True,
        font_size = normal_font_size,
        color = (0,0,0,1),
        pos = (size[0]*0.05,size[1]*0.5),
        size = (size[0]*0.9,size[1]*0.4),
        halign="center",
        valign = "middle",
    ))
    global_constants.Main_Window.add_widget(Static_picture(
        size=[0.7*size[0]]*2,
        game = global_constants.game,
        options=['start']
    ))
    global_constants.Main_Window.add_widget(Button(
        text = Get_text('tutorial_see'),
        pos = (size[0] * 0.3 , size[1] * 0.05),
        background_color = (1,1,0,0.3),
        color = (0,1,0,1),
        on_press=glinskiy2
    ))
    global_constants.Main_Window.add_widget(Button(
        text = Get_text('tutorial_repeat'),
        pos = (size[0] * 0.65 , size[1] * 0.05),
        background_color = (1,1,0,0.3),
        color = (0,1,0,1),
        on_press=do_kuej_tutorial
    )    )

# end of mak - Quej tutorial

def do_garner_tutorial(click=None):
    help_tutorial()
    static_interface(
        size = global_constants.Main_Window.size,
        label_text = Get_text('tutorial_garner_start'),
        btn_command = garner2
    )

def garner2(click=None):
    help_tutorial()
    size = global_constants.Main_Window.size
    global_constants.Main_Window.add_widget(Label(
        text = get_text(Get_text('tutorial_garner_second'),size[0]*0.9,normal_font_size/2),
        shorten=True,
        font_size = normal_font_size,
        color = (0,0,0,1),
        pos = (size[0]*0.05,size[1]*0.5),
        size = (size[0]*0.9,size[1]*0.4),
        halign="center",
        valign = "middle",
    ))
    #[ figure, x, y, color ]
    pos = [
        ['queen',0,1,'white'], ['king',0,0,'white'], ['pawn',1,2,'white'],['pawn',3,1,'white'], 
        ['pawn',4,1,'white'], ['bishop',2,0,'white'], ['horse',3,0,'white'], ['rook',4,0,'white'],
        ['queen',1,4,'black'], ['king',0,4,'black'], ['pawn',1,3,'black'],['pawn',3,2,'black'], 
        ['pawn',4,3,'black'], ['bishop',2,4,'black'], ['horse',3,4,'black'], ['rook',4,4,'black']
    ]
    global_constants.Main_Window.add_widget(Static_picture(
        size=[0.7*size[0]]*2,
        game = global_constants.game,
        options=[],
        position = pos
    ))

    global_constants.Main_Window.add_widget(Button(
        text = Get_text('tutorial_next'),
        pos = (size[0] * 0.65 , size[1] * 0.05),
        background_color = (1,1,0,0.3),
        color = (0,1,0,1),
        on_press=garner3
    ))

def garner3(click=None):
    help_tutorial()
    size = global_constants.Main_Window.size
    global_constants.Main_Window.add_widget(Label(
        text = get_text(Get_text( 'tutorial_garner_pawn'),size[0]*0.9,normal_font_size/2),
        shorten=True,
        font_size = normal_font_size,
        color = (0,0,0,1),
        pos = (size[0]*0.05,size[1]*0.5),
        size = (size[0]*0.9,size[1]*0.4),
        halign="center",
        valign = "middle"
    ))

    global_constants.Main_Window.add_widget(Button(
        text = Get_text('tutorial_next'),
        pos = (size[0] * 0.65 , size[1] * 0.05),
        background_color = (1,1,0,0.3),
        color = (0,1,0,1),
        on_press=garner4
    ))

def garner4(click=None):
    help_tutorial()
    interactive_interface(
        size = global_constants.Main_Window.size,
        figure = 'bishop',
        fig_pos = [2,2],
        label_text = Get_text('tutorial_garner_bishop'),
        btn_command = garner5
    )

def garner5(click=None):
    help_tutorial()
    interactive_interface(
        size = global_constants.Main_Window.size,
        figure = 'horse',
        fig_pos = [2,2],
        label_text = Get_text('tutorial_garner_horse'),
        btn_command = garner6
    )

def garner6(click=None):
    help_tutorial()
    interactive_interface(
        size = global_constants.Main_Window.size,
        figure = 'rook',
        fig_pos = [2,2],
        label_text = Get_text('tutorial_garner_rook'),
        btn_command = garner7
    )

def garner7(click=None):
    help_tutorial()
    interactive_interface(
        size = global_constants.Main_Window.size,
        figure = 'queen',
        fig_pos = [3,2],
        label_text = Get_text('tutorial_garner_queen'),
        btn_command = garner8
    )

def garner8(click=None):
    help_tutorial()
    interactive_interface(
        size = global_constants.Main_Window.size,
        figure = 'king',
        fig_pos = [2,2],
        label_text = Get_text('tutorial_garner_king'),
        btn_command = garner9
    )

def garner9(click=None):
    help_tutorial()
    size = global_constants.Main_Window.size
    global_constants.Main_Window.add_widget(Label(
        text = get_text(Get_text('tutorial_garner_end'),size[0]*0.9,normal_font_size/2),
        shorten=True,
        font_size = normal_font_size,
        color = (0,0,0,1),
        pos = (size[0]*0.05,size[1]*0.5),
        size = (size[0]*0.9,size[1]*0.4),
        halign="center",
        valign = "middle",
    ))

    global_constants.Main_Window.add_widget(Button(
        text = Get_text('tutorial_repeat'),
        pos = (size[0] * 0.65 , size[1] * 0.05),
        background_color = (1,1,0,0.3),
        color = (0,1,0,1),
        on_press=do_garner_tutorial
    ))

# end of garner tutorial

def do_horde_tutorial(click=None):
    help_tutorial()
    static_interface(
        size = global_constants.Main_Window.size,
        btn_command = horde2,
        label_text = Get_text('tutorial_horde_start')
    )

def horde2(click=None):
    help_tutorial()
    static_interface(
        size = global_constants.Main_Window.size,
        label_text = Get_text('tutorial_horde_second'),
        btn_command = horde3
    )

def horde3(click=None):
    help_tutorial()
    size = global_constants.Main_Window.size
    global_constants.Main_Window.add_widget(Label(
        text = get_text(Get_text('tutorial_horde_pawn'),size[0]*0.9,normal_font_size/2),
        shorten=True,
        font_size = normal_font_size,
        color = (0,0,0,1),
        pos = (size[0]*0.05,size[1]*0.5),
        size = (size[0]*0.9,size[1]*0.4),
        halign="center",
        valign = "middle",
    ))

    global_constants.Main_Window.add_widget(Button(
        text = Get_text('tutorial_next'),
        pos = (size[0] * 0.65 , size[1] * 0.05),
        background_color = (1,1,0,0.3),
        color = (0,1,0,1),
        on_press=horde4
    ))

def horde4(click=None):
    help_tutorial()
    size = global_constants.Main_Window.size
    global_constants.Main_Window.add_widget(Label(
        text = get_text(Get_text('tutorial_horde_also'),size[0]*0.9,normal_font_size/2),
        shorten=True,
        font_size = normal_font_size,
        color = (0,0,0,1),
        pos = (size[0]*0.05,size[1]*0.5),
        size = (size[0]*0.9,size[1]*0.4),
        halign="center",
        valign = "middle",
    ))
    global_constants.Main_Window.add_widget(Static_picture(
        size=[0.7*size[0]]*2,
        game = global_constants.game,
        options=['start']
    ))

    global_constants.Main_Window.add_widget(Button(
        text = Get_text('tutorial_next'),
        pos = (size[0] * 0.65 , size[1] * 0.05),
        background_color = (1,1,0,0.3),
        color = (0,1,0,1),
        on_press=classic_1
    ))
    global_constants.Main_Window.add_widget(Button(
        text = Get_text('tutorial_repeat'),
        pos = (size[0] * 0.3 , size[1] * 0.05),
        background_normal = '',
        background_color = (1,1,0,0.3),
        color = (0,1,0,1),
        on_press=do_horde_tutorial
    ))

# end of horde tutorial

def do_weak_tutorial(click=None):
    help_tutorial()
    static_interface(
        size = global_constants.Main_Window.size,
        label_text = Get_text('tutorial_weak_start'),
        btn_command = week2
    )

def week2(click):
    help_tutorial()
    static_interface(
        size = global_constants.Main_Window.size,
        label_text = Get_text('tutorial_weak_2'),
        btn_command = week3
    )

def week3(click):
    help_tutorial()
    size = global_constants.Main_Window.size
    global_constants.Main_Window.add_widget(Label(
        text = get_text(Get_text('tutorial_weak_3'),size[0]*0.9,normal_font_size/2),
        shorten=True,
        font_size = normal_font_size,
        color = (0,0,0,1),
        pos = (size[0]*0.05,size[1]*0.5),
        size = (size[0]*0.9,size[1]*0.4),
        halign="center",
        valign = "middle",
    ))
    global_constants.Main_Window.add_widget(Static_picture(
        size=[0.7*size[0]]*2,
        game = global_constants.game,
        options=['start']
    ))

    global_constants.Main_Window.add_widget(Button(
        text = Get_text('tutorial_see'),
        pos = (size[0] * 0.3 , size[1] * 0.05),
        background_color = (1,1,0,0.3),
        color = (0,1,0,1),
        on_press=classic_1
    ))

    global_constants.Main_Window.add_widget(Button(
        text = Get_text('tutorial_repeat'),
        pos = (size[0] * 0.65 , size[1] * 0.05),
        background_color = (1,1,0,0.3),
        color = (0,1,0,1),
        on_press=do_weak_tutorial
    ))

#end of weak tutorial

def do_kamikadze_tutorial(click=None):
    help_tutorial()
    static_interface(
        size = global_constants.Main_Window.size,
        label_text = Get_text('tutorial_kamikadze_start'),
        btn_command = kami_2
    )

def kami_2(click=None):
    help_tutorial()
    size = global_constants.Main_Window.size
    global_constants.Main_Window.add_widget(Label(
        text = get_text(Get_text('tutorial_kamikadze_2'),size[0]*0.9,normal_font_size/2),
        shorten=True,
        font_size = normal_font_size,
        color = (0,0,0,1),
        pos = (size[0]*0.05,size[1]*0.5),
        size = (size[0]*0.9,size[1]*0.4),
        halign="center",
        valign = "middle",
    ))
    global_constants.Main_Window.add_widget(Static_picture(
        size=[0.7*size[0]]*2,
        game = global_constants.game,
        options=['start']
    ))

    global_constants.Main_Window.add_widget(Button(
        text = Get_text('tutorial_see'),
        pos = (size[0] * 0.3 , size[1] * 0.05),
        background_color = (1,1,0,0.3),
        color = (0,1,0,1),
        on_press=classic_1
    ))

    global_constants.Main_Window.add_widget(Button(
        text = Get_text('tutorial_next'),
        pos = (size[0] * 0.65 , size[1] * 0.05),
        background_color = (1,1,0,0.3),
        color = (0,1,0,1),
        on_press=kami_3
    ))

def kami_3(click=None):
    help_tutorial()
    static_interface(
        size = global_constants.Main_Window.size,
        label_text = Get_text('tutorial_kamikadze_3'),
        btn_command = kami_4
    )

def kami_4(click=None):
    help_tutorial()
    label_text = Get_text('tutorial_kamikadze_4')
    size = global_constants.Main_Window.size
    global_constants.Main_Window.add_widget(Label(
        text = get_text(label_text,size[0]*0.9,normal_font_size/2),
        shorten=True,
        font_size = normal_font_size,
        color = (0,0,0,1),
        pos = (size[0]*0.05,size[1]*0.5),
        size = (size[0]*0.9,size[1]*0.4),
        halign="center",
        valign = "middle",
    ))
    global_constants.Main_Window.add_widget(Static_picture(
        size=[0.7*size[0]]*2,
        game = global_constants.game,
        position=[['king',7,4,'black'], ['king',2,5,'white'], ['queen',6,4,'white']]
    ))

    global_constants.Main_Window.add_widget(Button(
        text = Get_text('tutorial_next'),
        pos = (size[0] * 0.65 , size[1] * 0.05),
        background_color = (1,1,0,0.3),
        color = (0,1,0,1),
        on_press = kami_5
    ))

def kami_5(click=None):
    help_tutorial()
    label_text = Get_text('tutorial_kamikadze_5')
    size = global_constants.Main_Window.size
    global_constants.Main_Window.add_widget(Label(
        text = get_text(label_text,size[0]*0.9,normal_font_size/2),
        shorten=True,
        font_size = normal_font_size,
        color = (0,0,0,1),
        pos = (size[0]*0.05,size[1]*0.5),
        size = (size[0]*0.9,size[1]*0.4),
        halign="center",
        valign = "middle",
    ))
    pos = [
        ['king',5,4,'white'], ['king',5,7,'black'],
        ['bishop',3,4,'black'], ['queen',1,4,'black'],
        ['horse',4,2,'white'], ['queen',2,0,'white']
    ]
    global_constants.Main_Window.add_widget(Static_picture(
        size=[0.7*size[0]]*2,
        game = global_constants.game,
        position=pos
    ))

    global_constants.Main_Window.add_widget(Button(
        text = Get_text('tutorial_next'),
        pos = (size[0] * 0.65 , size[1] * 0.05),
        background_color = (1,1,0,0.3),
        color = (0,1,0,1),
        on_press = kami_6
    ))

def kami_6(click=None):
    help_tutorial()
    size = global_constants.Main_Window.size
    global_constants.Main_Window.add_widget(Label(
        text = get_text(Get_text('tutorial_kamikadze_6'),size[0]*0.9,normal_font_size/2),
        shorten=True,
        font_size = normal_font_size,
        color = (0,0,0,1),
        pos = (size[0]*0.05,size[1]*0.5),
        size = (size[0]*0.9,size[1]*0.4),
        halign="center",
        valign = "middle",
    ))
    global_constants.Main_Window.add_widget(Static_picture(
        size=[0.7*size[0]]*2,
        game = global_constants.game,
        options=['start']
    ))

    global_constants.Main_Window.add_widget(Button(
        text = Get_text('tutorial_repeat'),
        size= (size[0]*0.1 , size[1]*0.05) ,
        pos = (size[0] * 0.8 , size[1] * 0.05),
        background_normal = '',
        background_color = (1,1,0,0.3),
        color = (0,1,0,1),
        on_press = do_kamikadze_tutorial
    ))

# end of kamikadze_tutorial

def do_bad_tutorial(click=None):
    help_tutorial()
    static_interface(
        size = global_constants.Main_Window.size,
        label_text = Get_text('tutorial_bad_start'),
        btn_command = bad_2
    )

def bad_2(clicl):
    help_tutorial()
    static_interface(
        size = global_constants.Main_Window.size,
        label_text = Get_text('tutorial_bad_2'),
        btn_command = bad_3
    )
    size = global_constants.Main_Window.size
    global_constants.Main_Window.add_widget(Button(
        text = Get_text('tutorial_see'),
        pos = (size[0] * 0.3 , size[1] * 0.05),
        background_color = (1,1,0,0.3),
        color = (0,1,0,1),
        on_press = classic_1
    ))

def bad_3(clic=None):
    help_tutorial()
    size = global_constants.Main_Window.size
    global_constants.Main_Window.add_widget(Label(
        text = Get_text('tutorial_bad_3'),
        shorten=True,
        font_size = normal_font_size,
        color = (0,0,0,1),
        pos = (size[0]*0.05,size[1]*0.5),
        size = (size[0]*0.9,size[1]*0.4),
        halign="left",
        valign = "middle",
    ))
    global_constants.Main_Window.add_widget(Static_picture(
        size=[0.7*size[0]]*2,
        game =global_constants.game,
        options=['start']
    ))

    global_constants.Main_Window.add_widget(Button(
        text = Get_text('tutorial_next'),
        pos = (size[0] * 0.65 , size[1] * 0.05),
        background_color = (1,1,0,0.3),
        color = (0,1,0,1),
        on_press = bad_4
    ))

def bad_4(click=None):
    help_tutorial()
    help_tutorial()
    size = global_constants.Main_Window.size
    global_constants.Main_Window.add_widget(Label(
        text = get_text(Get_text('tutorial_bad_4'),size[0]*0.9,normal_font_size/2),
        shorten=True,
        font_size = normal_font_size,
        color = (0,0,0,1),
        pos = (size[0]*0.05,size[1]*0.5),
        size = (size[0]*0.9,size[1]*0.4),
        halign="center",
        valign = "middle",
    ))
    global_constants.Main_Window.add_widget(Static_picture(
        size=[0.7*size[0]]*2,
        game =global_constants.game,
        options=['start']
    ))

    global_constants.Main_Window.add_widget(Button(
        text = Get_text('tutorial_repeat'),
        pos = (size[0] * 0.65 , size[1] * 0.05),
        background_color = (1,1,0,0.3),
        color = (0,1,0,1),
        on_press = do_bad_tutorial
    ))

# end of bad_chess tutorial

def do_racing_tutorial(par=None):
    help_tutorial()
    size = global_constants.Main_Window.size
    static_interface(
        size = global_constants.Main_Window.size,
        label_text = Get_text('tutorial_rase_start'),
        btn_command = rase2
    )
    global_constants.Main_Window.add_widget(Button(
        text = Get_text('tutorial_see'),
        pos = (size[0] * 0.3 , size[1] * 0.05),
        background_color = (1,1,0,0.3),
        color = (0,1,0,1),
        on_press=classic_1
    ))

def rase2(par=None):
    help_tutorial()
    size = global_constants.Main_Window.size
    label_text = Get_text('tutorial_rase_2')
    position = [
        ['king',6,7,'white'],['king',3,6,'black'],['bishop',2,2,'black'],
        ['rook',5,3,'white'],['rook',1,2,'black'],['bishop',2,4,'white']
    ]

    global_constants.Main_Window.add_widget(Label(
        text = get_text(label_text,size[0]*0.9,normal_font_size/2),
        shorten=True,
        font_size = normal_font_size,
        color = (0,0,0,1),
        pos = (size[0]*0.05,size[1]*0.55),
        size = (size[0]*0.9,size[1]*0.4),
        halign="center",
        valign = "middle",
    ))
    global_constants.Main_Window.add_widget(Static_picture(
        size=[0.7*size[0]]*2,
        game =global_constants.game,
        position=position
    ))

    global_constants.Main_Window.add_widget(Button(
        text = Get_text('tutorial_next'),
        pos = (size[0] * 0.65 , size[1] * 0.05),
        background_normal = '',
        background_color = (1,1,0,0.3),
        color = (0,1,0,1),
        on_press = rase3
    ))

def rase3(par=None):
    help_tutorial()
    size = global_constants.Main_Window.size
    label_text = Get_text('tutorial_rase_3')
    position = [['king','white',4,4], ['king','black',2,0], ['queen','black',2,5]]

    global_constants.Main_Window.add_widget(Label(
        text = get_text(label_text,size[0]*0.9,normal_font_size/2),
        font_size = normal_font_size,
        color = (0,0,0,1),
        pos = (size[0]*0.05,size[1]*0.55),
        size = (size[0]*0.9,size[1]*0.4),
        halign="center",
        valign = "middle",
    ))
    global_constants.Main_Window.add_widget(Tutorial_Widget(
        size=[0.7*size[0]]*2,
        game =global_constants.game,
        pos = (size[0]*0.05,size[1]*0.2),
        figures=position,
        options = ['check']
    ))

    global_constants.Main_Window.add_widget(Button(
        text = Get_text('tutorial_next'),
        pos = (size[0] * 0.65 , size[1] * 0.05),
        background_normal = '',
        background_color = (1,1,0,0.3),
        color = (0,1,0,1),
        on_press = rase4
    ))

def rase4(par=None):
    help_tutorial()
    size = global_constants.Main_Window.size
    global_constants.Main_Window.add_widget(Label(
        text = get_text(Get_text('tutorial_rase_4'),size[0]*0.9,normal_font_size/2),
        font_size = normal_font_size,
        color = (0,0,0,1),
        pos = (size[0]*0.05,size[1]*0.5),
        size = (size[0]*0.9,size[1]*0.4),
        halign="center",
        valign = "middle",
    ))
    global_constants.Main_Window.add_widget(Static_picture(
        size=[0.7*size[0]]*2,
        game =global_constants.game,
        options=['start']
    ))

    global_constants.Main_Window.add_widget(Button(
        text = Get_text('tutorial_repeat'),
        pos = (size[0] * 0.65 , size[1] * 0.05),
        background_color = (1,1,0,0.3),
        color = (0,1,0,1),
        on_press = do_racing_tutorial
    ))

# end of rasing tutorial


def do_haos_tutorial(par=None):
    help_tutorial()
    size = global_constants.Main_Window.size
    static_interface(
        size = global_constants.Main_Window.size,
        label_text = Get_text('tutorial_haos_start'),
        btn_command = haos2
    )
    global_constants.Main_Window.add_widget(Button(
        text = Get_text('tutorial_see'),
        pos = (size[0] * 0.3 , size[1] * 0.05),
        background_color = (1,1,0,0.3),
        color = (0,1,0,1),
        on_press=classic_1
    ))

def haos2(par=None):
    help_tutorial()
    static_interface(
        size = global_constants.Main_Window.size,
        label_text = Get_text('tutorial_haos_2'),
        btn_command = do_haos_tutorial,
        repeat=True
    )

# add haotic tutorial

def do_schatranj_tutorial(par=None):
    help_tutorial()
    static_interface(
        size = global_constants.Main_Window.size,
        label_text = Get_text('tutorial_shcatranj_start'),
        btn_command = schat2
    )

def schat2(par=...):
    help_tutorial()
    static_interface(
        size = global_constants.Main_Window.size,
        label_text = Get_text('tutorial_shcatranj_changes'),
        btn_command = schat3
    )

def schat3(par=None):
    help_tutorial()
    board = [
        ['white',5,5,'pawn'], ['white',1,1,'pawn'], ['black',2,3,'pawn'],
        ['white',4,2,'pawn'], ['black',5,3,'pawn']
    ]
    actions = [
        ['show',1,1,[[1,2]] ],         ['move',1,1,1,2],
        ['show_attack',2,3,1,2],       ['take',2,3,1,2],
        ['show_attack',4,2,5,3],       ['take',4,2,5,3],
        ['move',1,2,1,1],              ['move',5,5,5,6],
        ['move',1,1,1,0],              ['change',1,0,'queen'],
        ['move',5,6,5,7],              ['change',5,7,'queen']
    ]
    size = global_constants.Main_Window.size    
    text = get_text(Get_text('tutorial_shcatranj_pawn'),size[0]*0.9,normal_font_size/2)
    video_interface(board,actions,1.2,schat4,text)

def schat4(par=None):
    help_tutorial()
    interactive_interface(
        size=global_constants.Main_Window.size,
        figure = 'bishop',
        btn_command=schat5,
        label_text=Get_text('tutorial_shcatranj_bishop')
    )

def schat5(par=...):
    help_tutorial()
    interactive_interface(
        size=global_constants.Main_Window.size,
        figure = 'rook',
        btn_command=schat6,
        label_text=Get_text('tutorial_shcatranj_rook')
    )

def schat6(par=...):
    help_tutorial()
    interactive_interface(
        size=global_constants.Main_Window.size,
        figure = 'king',
        btn_command=schat7,
        label_text=Get_text('tutorial_shcatranj_king')
    )

def schat7(par=...):
    help_tutorial()
    interactive_interface(
        size=global_constants.Main_Window.size,
        figure = 'horse',
        btn_command=schat8,
        label_text=Get_text('tutorial_shcatranj_horse')
    )

def schat8(par=...):
    help_tutorial()
    interactive_interface(
        size=global_constants.Main_Window.size,
        figure = 'queen',
        btn_command=schat9,
        label_text=Get_text('tutorial_shcatranj_queen')
    )

def schat9(par=...):
    help_tutorial()
    static_interface(
        repeat=True,
        size=global_constants.Main_Window.size,
        label_text= Get_text('tutorial_shcatranj_end'),
        btn_command=do_schatranj_tutorial
        )

# end of schatranj tutorial

def do_dark_tutorial(par=...):
    help_tutorial()
    static_interface(
        repeat=False,
        size = global_constants.Main_Window.size,
        label_text=Get_text('tutorial_dark_start'),
        btn_command=dark2
    )

def dark2(par=None):
    size = global_constants.Main_Window.size
    help_tutorial()
    static_interface(
        size = size,
        label_text=Get_text('tutorial_dark_second'),
        btn_command=dark3
    )
    global_constants.Main_Window.add_widget(Button(
        text = Get_text('tutorial_see'),
        pos = (size[0] * 0.32 , size[1] * 0.05),
        background_normal = '',
        background_color = (1,1,0,0.3),
        color = (0,1,0,1),
        on_press = classic_1
    ))

def dark3(par=None):
    help_tutorial()
    static_interface(
        size = global_constants.Main_Window.size,
        label_text=Get_text('tutorial_dark_purpose'),
        btn_command=dark4
    )

def dark4(par=...):
    help_tutorial()
    static_interface(
        label_text = Get_text('tutorial_dark_last'),
        repeat=True,
        btn_command=do_dark_tutorial,
        size = global_constants.Main_Window.size
    )

# end of dark tutorial

