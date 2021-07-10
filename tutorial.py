from kivy.uix.label import Label
from kivy.graphics import Rectangle

from translater import Get_text
from settings import Settings
import global_constants
from tutorial_widget import Tutorial_Widget
from picture_tutorial import Static_picture
from film_widget import VideoChess
import sovereign_interactive_tutorial
from tutorial_button import Button_ as Button

import random
import os


normal_font_size = 20


def get_text(text, width, leng):
    sim = width // leng - 10
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
        size=global_constants.Main_Window.size,
        source=os.path.join(Settings.folder, 'pictures', 'tutorial.png'),
        pos=(0, 0)
    ))
    size = global_constants.Main_Window.size

    def leave(click):
        for wid in global_constants.Main_Window.children:
            if type(wid) == VideoChess:
                wid.must = False
                wid.__del__()
            elif type(wid) == sovereign_interactive_tutorial.VideoChess:
                wid.must = False
                wid.__del__()
        back_command(click)

    global_constants.Main_Window.add_widget(Button(
        text=Get_text('tutorial_to_game'),
        font_name=global_constants.Settings.get_font(),
        background_color=(0, 1, 0, 0.3),
        color=(1, 1, 0, 1),
        size=(size[0]*0.15, size[1]*0.05),
        pos=(size[0] * 0.75, size[1] * 0.9),
        on_press=leave
    ))


def lost_tutorial():
    help_tutorial()
    global_constants.Main_Window.add_widget(Label(
        text='Я бы мог вас обучить, \nно не знаю как!',
        font_name=global_constants.Settings.get_font(),
        color=[1, 0, 0, 1],
        font_size=40,
        center=global_constants.Main_Window.center
    ))


def interactive_interface(size, figure, btn_command, label_text='', fig_pos=[4, 4]):
    """
    create standart interface of tutorial
    with onetype parameters of objects\n
    size - window.size\n
    figure = 'bishop'\n
    label_text <- Get_text(...)
    """
    global_constants.Main_Window.add_widget(Label(
        text=get_text(label_text, size[0]*0.9, normal_font_size/2),
        shorten=True,
        font_size=normal_font_size,
        color=(0, 0, 0, 1),
        pos=(size[0]*0.05, size[1]*0.55),
        size=(size[0]*0.9, size[1]*0.4),
        halign="center",
        valign="middle",
        font_name=Settings.get_font()
    ))

    global_constants.Main_Window.add_widget(Tutorial_Widget(
        size=[0.7*size[0]]*2,
        pos=(size[0]*0.05, size[1]*0.2),
        game=global_constants.game,
        figures=[[figure, random.choice(['black', 'white']), *fig_pos]]
    ))

    global_constants.Main_Window.add_widget(Button(
        text=Get_text('tutorial_next'),
        font_name=Settings.get_font(),
        pos=(size[0] * 0.65, size[1] * 0.05),
        background_normal='',
        background_color=(1, 1, 0, 0.3),
        color=(0, 1, 0, 1),
        on_press=btn_command
    ))


def static_interface(size, label_text, btn_command, repeat=False):
    global_constants.Main_Window.add_widget(Label(
        text=get_text(label_text, size[0]*0.9, normal_font_size/2),
        shorten=True,
        font_size=normal_font_size,
        color=(0, 0, 0, 1),
        pos=(size[0]*0.05, size[1]*0.55),
        size=(size[0]*0.9, size[1]*0.4),
        halign="center",
        valign="middle",
        font_name=Settings.get_font()
    ))

    global_constants.Main_Window.add_widget(Static_picture(
        size=[0.7*size[0]]*2,
        game=global_constants.game,
        options=['start']
    ))

    button_text = Get_text(
        'tutorial_next') if not repeat else Get_text('tutorial_repeat')
    global_constants.Main_Window.add_widget(Button(
        text=button_text,
        pos=(size[0] * 0.65, size[1] * 0.05),
        background_normal='',
        background_color=(1, 1, 0, 0.3),
        color=(0, 1, 0, 1),
        on_press=btn_command
    ))


def video_interface(board, actions=[], speed=1, command=print, text=''):
    help_tutorial()
    size = global_constants.Main_Window.size
    global_constants.Main_Window.add_widget(Label(
        text=text,
        shorten=True,
        font_size=normal_font_size,
        color=(0, 0, 0, 1),
        pos=(size[0]*0.05, size[1]*0.5),
        size=(size[0]*0.9, size[1]*0.4),
        halign="center",
        valign="middle",
        font_name=Settings.get_font()
    ))

    video = VideoChess(
        board=board,
        speed=speed,
        actions=actions
    )
    global_constants.Main_Window.add_widget(video)

    def later(cllick):
        video.timer.cancel()
        video.__del__()
        video.must = False
        command(cllick)

    global_constants.Main_Window.add_widget(Button(
        text=Get_text('tutorial_next'),
        pos=(size[0] * 0.65, size[1] * 0.05),
        background_color=(1, 1, 0, 0.3),
        color=(0, 1, 0, 1),
        on_press=later
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
    elif game.type_of_chess == 'frozen':
        do_freeze_tutorial()
    elif game.type_of_chess == 'nuclear':
        do_nuclear_tutorial()
    elif game.type_of_chess == 'legan':
        do_legan_tutorial()
    elif game.type_of_chess == 'sovereign':
        do_sovereign_tutorial()
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
        size=size,
        figure='horse',
        btn_command=command,
        label_text=Get_text('tutorial_classic_horse')
    )


def classic_2(press):
    help_tutorial()
    interactive_interface(
        size=global_constants.Main_Window.size,
        figure='bishop',
        btn_command=classic_3,
        label_text=Get_text('tutorial_classic_bishop')
    )


def classic_3(press):
    help_tutorial()
    interactive_interface(
        size=global_constants.Main_Window.size,
        figure='rook',
        btn_command=classic_4,
        label_text=Get_text('tutorial_classic_rook')
    )


def classic_4(press):
    help_tutorial()
    command = classic_5
    if global_constants.game.type_of_chess in ['horde', 'rasing', 'los_alamos', 'legan']:
        command = classic_7
    interactive_interface(
        size=global_constants.Main_Window.size,
        btn_command=command,
        label_text=Get_text('tutorial_classic_queen'),
        figure='queen'
    )


def classic_5(press):
    command = classic_6
    size = global_constants.Main_Window.size
    text = get_text(Get_text('tutorial_classic_pawn'),
                    size[0]*0.9, normal_font_size/2)
    board = [
        ['white', 2, 1, 'pawn'], ['black', 3, 3, 'pawn'], ['white', 1, 5, 'pawn'],
        ['white', 6, 3, 'pawn'], ['black', 5, 5, 'pawn'], ['black', 2, 6, 'pawn']
    ]
    action = [
        ['show', 6, 3, [[6, 4]]],       ['move', 6, 3, 6, 4],
        ['show', 5, 5, [[5, 4]]],       ['move', 5, 5, 5, 4],
        ['show', 6, 4, [[6, 5]]],       ['move', 6, 4, 6, 5],
        ['show', 5, 4, [[5, 3]]],       ['move', 5, 4, 5, 3],
        ['move', 6, 5, 6, 6],           ['move', 5, 3, 5, 2],
        ['move', 6, 6, 6, 7],           ['change', 6, 7, 'queen'],
        ['move', 5, 2, 5, 1],           ['move', 6, 7, 7, 7],
        ['show_attack', 2, 6, 1, 5],    ['pause'],
        ['take', 2, 6, 1, 5],           ['show', 2, 1, [[2, 2], [2, 3]]],
        ['move', 2, 1, 2, 3],           ["show_attack", 3, 3, 2, 2],
        ['pause'],                  ['take', 3, 3, 2, 2]
    ]
    video_interface(board, action, 1, command, text)


def classic_6(press):
    size = global_constants.Main_Window.size
    text = get_text(Get_text('tutorial_classic_pawn2'),
                    size[0]*0.9, normal_font_size/2)
    board = [['white', 7, 1, 'pawn'], ['black', 6, 3, 'pawn'], ['white', 6, 1, 'pawn'],
             ['black', 1, 6, 'pawn'], ['white', 2, 4, 'pawn']]
    actions = [
        ['show', 7, 1, [[7, 2], [7, 3]]],     ['move', 7, 1, 7, 3],
        ['show_attack', 6, 3, 7, 2],        ['take', 6, 3, 7, 2],
        ['show_attack', 6, 1, 7, 2],        ['take', 6, 1, 7, 2],
        ['show', 1, 6, [[1, 5], [1, 4]]],     ['move', 1, 6, 1, 4],
        ['show_attack', 2, 4, 1, 5],        ['take', 2, 4, 1, 5]
    ]
    video_interface(board, actions, 1, classic_7, text)


def classic_7(press):
    help_tutorial()
    game = global_constants.game
    if game.type_of_chess in ['classic', 'magik', 'permutation', 'horde', 'kamikadze', 'haotic']:
        command = classic_8
    elif game.type_of_chess in ['los_alamos', 'legan']:
        command = classic_9
    elif game.type_of_chess == 'week':
        command = do_weak_tutorial
    elif game.type_of_chess == 'bad_chess':
        command = bad_2
    elif game.type_of_chess == 'rasing':
        command = do_racing_tutorial
    elif game.type_of_chess in ['dark_chess', 'frozen', 'nuclear']:
        command = classic_8
    else:
        command = fisher1

    interactive_interface(
        size=global_constants.Main_Window.size,
        figure='king',
        btn_command=command,
        label_text=Get_text('tutorial_classic_king')
    )


def classic_8(press):
    size = global_constants.Main_Window.size
    text = get_text(Get_text('tutorial_classic_rocking'),
                    size[0]*0.8, normal_font_size/2)
    board = [
        ['white', 4, 0, 'king'], ['white', 7, 0, 'rook'], ['white', 0, 0, 'rook'],
        ['black', 0, 7, 'rook'], ['black', 4, 7, 'king'], ['black', 7, 7, 'rook']
    ]
    actions = [
        ['show', 4, 0, [[6, 0]]],
        ['o-o', 0],
        ['show_attack', 5, 0, 5, 7],
        ['show', 4, 7, [[2, 7]]],
        ['o-o-o', 7]
    ]
    video_interface(board, actions, 1, classic_9, text)


def classic_9(press):
    help_tutorial()
    size = global_constants.Main_Window.size
    game = global_constants.game
    global_constants.Main_Window.add_widget(Label(
        text=get_text(Get_text('tutorial_classic_end'),
                      size[0]*0.8, normal_font_size/2),
        shorten=True,
        font_size=normal_font_size,
        font_name=Settings.get_font(),
        color=(0, 0, 0, 1),
        pos=(size[0]*0.05, size[1]*0.3),
        size=(size[0]*0.9, size[1]*0.4),
        halign="center",
        valign="middle",
    ))

    but = Button(
        text=Get_text('tutorial_repeat'),
        pos=(size[0] * 0.65, size[1] * 0.05),
        background_color=(1, 1, 0, 0.3),
        color=(0, 1, 0, 1),
    )
    if game.type_of_chess == 'magik':
        but.bind(on_press=do_magik_tutorial)
    elif game.type_of_chess == 'los_alamos':
        but.bind(on_press=do_los_alamos_tutorial)
    elif game.type_of_chess == 'permutation':
        but.bind(on_press=do_permut_tutorial)
    elif game.type_of_chess == 'horde':
        but.bind(on_press=do_horde_tutorial)
    elif game.type_of_chess == 'kamikadze':
        but.bind(on_press=kami_2)
    elif game.type_of_chess == 'haotic':
        but.bind(on_press=do_haos_tutorial)
    elif game.type_of_chess == 'dark_chess':
        but.bind(on_press=dark2)
    elif game.type_of_chess == 'frozen':
        but.bind(on_press=freeze4)
    elif game.type_of_chess == 'nuclear':
        but.bind(on_press=do_nuclear_tutorial)
    elif game.type_of_chess == 'legan':
        but.bind(on_press=do_legan_tutorial)
    else:
        but.bind(on_press=do_classic_tutorial)
    global_constants.Main_Window.add_widget(but)

# end of classic chess


def do_fisher_tutorial(click=None):
    help_tutorial()
    static_interface(
        size=global_constants.Main_Window.size,
        btn_command=fisher1,
        label_text=Get_text('tutorial_fisher_start')
    )


def fisher1(press):
    help_tutorial()
    size = global_constants.Main_Window.size
    static_interface(
        size=size,
        label_text=Get_text('tutorial_fisher_second'),
        btn_command=fisher2
    )

    global_constants.Main_Window.add_widget(Button(
        text=Get_text('tutorial_see'),
        pos=(size[0] * 0.3, size[1] * 0.05),
        background_color=(1, 1, 0, 0.3),
        color=(1, 0, 1, 1),
        on_press=classic_1
    ))


def fisher2(press):
    size = global_constants.Main_Window.size
    text = get_text(Get_text('tutorial_fisher_rocking'),
                    size[0]*0.8, normal_font_size/2)
    board = [
        ['white', 4, 0, 'king'], ['white', 7, 0, 'rook'], ['white', 0, 0, 'rook'],
        ['black', 0, 7, 'rook'], ['black', 4, 7, 'king'], ['black', 7, 7, 'rook']
    ]
    actions = [
        ['show', 4, 0, [[6, 0]]],
        ['o-o', 0],
        ['show_attack', 5, 0, 5, 7],
        ['show', 4, 7, [[2, 7]]],
        ['o-o-o', 7]
    ]
    video_interface(board, actions, 1, fisher3, text)


def fisher3(press):
    help_tutorial()
    size = global_constants.Main_Window.size
    global_constants.Main_Window.add_widget(Label(
        text=get_text(Get_text('tutorial_fisher_end'),
                      size[0]*0.8, normal_font_size/2),
        shorten=True,
        font_size=normal_font_size,
        color=(0, 0, 0, 1),
        pos=(size[0]*0.05, size[1]*0.55),
        size=(size[0]*0.9, size[1]*0.4),
        halign="center",
        valign="middle",
        font_name=Settings.get_font(),
    ))
    global_constants.Main_Window.add_widget(Button(
        text=Get_text('tutorial_repeat'),
        pos=(size[0] * 0.65, size[1] * 0.05),
        background_color=(1, 1, 0, 0.3),
        color=(0, 1, 0, 1),
        on_press=do_fisher_tutorial
    ))

# end fisher tutorial


def do_horse_tutorial(p):
    help_tutorial()
    size = global_constants.Main_Window.size
    static_interface(size=size,
                     label_text=Get_text('tutorial_horse_start'),
                     btn_command=horse1
                     )


def horse1(press):
    help_tutorial()
    interactive_interface(
        size=global_constants.Main_Window.size,
        label_text=Get_text('tutorial_horse_horse'),
        btn_command=horse2,
        figure='horse'
    )


def horse2(press):
    size = global_constants.Main_Window.size
    comand = horse3
    text = get_text(Get_text('tutorial_horse_pawn'),
                    size[0]*0.9, normal_font_size/2)
    board = [
        ['white', 2, 1, 'pawn'], ['black', 3, 3, 'pawn'], ['white', 1, 5, 'pawn'],
        ['white', 6, 3, 'pawn'], ['black', 5, 5, 'pawn'], ['black', 2, 6, 'pawn']
    ]
    action = [
        ['show', 6, 3, [[6, 4]]],       ['move', 6, 3, 6, 4],
        ['show', 5, 5, [[5, 4]]],       ['move', 5, 5, 5, 4],
        ['show', 6, 4, [[6, 5]]],       ['move', 6, 4, 6, 5],
        ['show', 5, 4, [[5, 3]]],       ['move', 5, 4, 5, 3],
        ['move', 6, 5, 6, 6],           ['move', 5, 3, 5, 2],
        ['move', 6, 6, 6, 7],           ['change', 6, 7, 'queen'],
        ['move', 5, 2, 5, 1],           ['move', 6, 7, 7, 7],
        ['show_attack', 2, 6, 1, 5],    ['pause'],
        ['take', 2, 6, 1, 5],           ['show', 2, 1, [[2, 2], [2, 3]]],
        ['move', 2, 1, 2, 3],           ["show_attack", 3, 3, 2, 2],
        ['pause'],                  ['take', 3, 3, 2, 2]
    ]
    video_interface(board, action, 1, comand, text)


def horse3(click):
    size = global_constants.Main_Window.size
    text = get_text(Get_text('tutorial_horse_pawn2'),
                    size[0]*0.9, normal_font_size/2)
    board = [['white', 7, 1, 'pawn'], ['black', 6, 3, 'pawn'], ['white', 6, 1, 'pawn'],
             ['black', 1, 6, 'pawn'], ['white', 2, 4, 'pawn']]
    actions = [
        ['show', 7, 1, [[7, 2], [7, 3]]],     ['move', 7, 1, 7, 3],
        ['show_attack', 6, 3, 7, 2],        ['take', 6, 3, 7, 2],
        ['show_attack', 6, 1, 7, 2],        ['take', 6, 1, 7, 2],
        ['show', 1, 6, [[1, 5], [1, 4]]],     ['move', 1, 6, 1, 4],
        ['show_attack', 2, 4, 1, 5],        ['take', 2, 4, 1, 5]
    ]
    video_interface(board, actions, 1, horse4, text)


def horse4(press):
    help_tutorial()
    interactive_interface(
        size=global_constants.Main_Window.size,
        btn_command=horse5,
        label_text=Get_text('tutorial_horse_king'),
        figure='king'
    )


def horse5(press):
    help_tutorial()
    size = global_constants.Main_Window.size
    global_constants.Main_Window.add_widget(Label(
        text=get_text(Get_text('tutorial_horse_end'),
                      size[0]*0.8, normal_font_size/2),
        shorten=True,
        font_size=normal_font_size,
        font_name=Settings.get_font(),
        color=(0, 0, 0, 1),
        pos=(size[0]*0.05, size[1]*0.3),
        size=(size[0]*0.9, size[1]*0.4),
        halign="center",
        valign="middle",
    ))

    global_constants.Main_Window.add_widget(Button(
        text=Get_text('tutorial_repeat'),
        pos=(size[0] * 0.65, size[1] * 0.05),
        background_color=(1, 1, 0, 0.3),
        color=(0, 1, 0, 1),
        on_press=do_horse_tutorial
    ))

# end of horse battle tutorial


def do_magik_tutorial(u):
    help_tutorial()
    static_interface(
        size=global_constants.Main_Window.size,
        label_text=Get_text('tutorial_magik_start'),
        btn_command=classic_2
    )

# end magik tutorial


def do_los_alamos_tutorial(press):
    help_tutorial()
    static_interface(
        size=global_constants.Main_Window.size,
        label_text=Get_text('tutorial_alamos_start'),
        btn_command=los_2
    )


def los_2(preess=1):
    help_tutorial()
    static_interface(
        size=global_constants.Main_Window.size,
        label_text=Get_text('tutorial_alamos_end'),
        btn_command=classic_1
    )

# end los_alamos tutorial


def do_permut_tutorial(click=None):
    help_tutorial()
    static_interface(
        size=global_constants.Main_Window.size,
        label_text=Get_text('tutorial_permut_start'),
        btn_command=permut_2
    )


def permut_2(click=None):
    help_tutorial()
    size = global_constants.Main_Window.size
    global_constants.Main_Window.add_widget(Label(
        text=Get_text('tutorial_permut_cycle'),
        shorten=True,
        font_size=normal_font_size,
        color=(0, 0, 0, 1),
        pos=(size[0]*0.05, size[1]*0.55),
        size=(size[0]*0.9, size[1]*0.4),
        halign="center",
        valign="middle",
        font_name=Settings.get_font(),
    ))

    global_constants.Main_Window.add_widget(Tutorial_Widget(
        size=[0.7*size[0]]*2,
        pos=(size[0]*0.05, size[1]*0.2),
        game=global_constants.game,
        figures=[['bishop', 'white', 4, 4], ['king', 'white', 3, 3]],
        options=['rotate']
    ))

    global_constants.Main_Window.add_widget(Button(
        text=Get_text('tutorial_repeat'),
        pos=(size[0] * 0.65, size[1] * 0.05),
        background_color=(1, 1, 0, 0.3),
        color=(0, 1, 0, 1),
        on_press=do_permut_tutorial
    ))

    global_constants.Main_Window.add_widget(Button(
        text=Get_text('tutorial_see'),
        pos=(size[0] * 0.3, size[1] * 0.05),
        background_color=(1, 1, 0, 0.3),
        color=(0, 1, 0, 1),
        on_press=do_classic_tutorial))

# end of permutation tutorial


def do_glinskiy_tutorial(click=None):
    help_tutorial()
    static_interface(
        size=global_constants.Main_Window.size,
        label_text=Get_text('tutorial_glinskiy_start'),
        btn_command=glinskiy2
    )


def glinskiy2(click=None):
    help_tutorial()
    interactive_interface(
        size=global_constants.Main_Window.size,
        btn_command=glinskiy3,
        figure='rook',
        fig_pos=[5, 5],
        label_text=Get_text('tutorial_glinskiy_rook')
    )


def glinskiy3(click=None):
    help_tutorial()
    interactive_interface(
        label_text=Get_text('tutorial_glinskiy_bishop'),
        size=global_constants.Main_Window.size,
        btn_command=glinskiy4,
        figure='bishop',
        fig_pos=[2, 5]
    )


def glinskiy4(click=None):
    help_tutorial()
    interactive_interface(
        size=global_constants.Main_Window.size,
        label_text=Get_text('tutorial_glinskiy_queen'),
        figure='queen',
        fig_pos=[10, 4],
        btn_command=glinskiy5
    )


def glinskiy5(click=None):
    help_tutorial()
    interactive_interface(
        size=global_constants.Main_Window.size,
        btn_command=glinskiy6,
        figure='horse',
        fig_pos=[3, 6],
        label_text=Get_text('tutorial_glinskiy_horse')
    )


def glinskiy6(click=None):
    size = global_constants.Main_Window.size
    text = get_text(Get_text('tutorial_glinskiy_pawn'),
                    size[0]*0.9, normal_font_size/2)
    board = [['white', 7, 2, 'pawn'], ['white', 3, 1, 'pawn'],
             ['black', 4, 3, 'pawn'], ['black', 8, 3, 'pawn']]
    actions = [
        ['show', 3, 1, [[3, 2], [3, 3]]],
        ['move', 3, 1, 3, 3],
        ['show_attack', 4, 3, 3, 2],
        ['take', 4, 3, 3, 2],
        ['show', 7, 2, [[7, 3], [7, 4]]],
        ['move', 7, 2, 7, 3],
        ['show_attack', 8, 3, 7, 3],
        ['take', 8, 3, 7, 3]
    ]
    video_interface(board, actions, 1, glinskiy7, text)


def glinskiy7(click=None):
    help_tutorial()
    interactive_interface(
        label_text=Get_text('tutorial_glinskiy_king'),
        figure='king',
        fig_pos=[4, 5],
        size=global_constants.Main_Window.size,
        btn_command=glinskiy8
    )


def glinskiy8(click=None):
    help_tutorial()
    size = global_constants.Main_Window.size
    game = global_constants.game
    global_constants.Main_Window.add_widget(Label(
        text=get_text(Get_text('tutorial_glinskiy_end'),
                      size[0]*0.9, normal_font_size/2),
        shorten=True,
        font_size=normal_font_size,
        color=(0, 0, 0, 1),
        pos=(size[0]*0.05, size[1]*0.5),
        size=(size[0]*0.9, size[1]*0.4),
        font_name=Settings.get_font(),
        halign="center",
        valign="middle",
    ))

    command = do_glinskiy_tutorial if game.type_of_chess != 'kuej' else do_kuej_tutorial
    global_constants.Main_Window.add_widget(Button(
        text=Get_text('tutorial_repeat'),
        pos=(size[0] * 0.65, size[1] * 0.05),
        background_color=(1, 1, 0, 0.3),
        color=(0, 1, 0, 1),
        on_press=command
    ))

# end of glinskiy tutorial


def do_round_tutorial(clivk=[]):
    help_tutorial()
    static_interface(
        size=global_constants.Main_Window.size,
        label_text=Get_text('tutorial_round_start'),
        btn_command=round1
    )


def round1(click=None):
    help_tutorial()
    interactive_interface(
        size=global_constants.Main_Window.size,
        figure='bishop',
        fig_pos=[2, 14],
        label_text=Get_text('tutorial_round_bishop'),
        btn_command=round2
    )


def round2(click=None):
    help_tutorial()
    interactive_interface(
        size=global_constants.Main_Window.size,
        figure='rook',
        fig_pos=[2, 14],
        label_text=Get_text('tutorial_round_rook'),
        btn_command=round3
    )


def round3(parr=1):
    help_tutorial()
    interactive_interface(
        size=global_constants.Main_Window.size,
        figure='queen',
        fig_pos=[0, 7],
        label_text=Get_text('tutorial_round_queen'),
        btn_command=round4
    )


def round4(click=None):
    help_tutorial()
    interactive_interface(
        size=global_constants.Main_Window.size,
        figure='horse',
        fig_pos=[2, 14],
        label_text=Get_text('tutorial_round_horse'),
        btn_command=round5
    )


def round5(par=1):
    help_tutorial()
    interactive_interface(
        size=global_constants.Main_Window.size,
        figure='king',
        fig_pos=[1, 3],
        label_text=Get_text('tutorial_round_king'),
        btn_command=round6
    )


def round6(par=0):
    help_tutorial()
    size = global_constants.Main_Window.size
    global_constants.Main_Window.add_widget(Label(
        text=get_text(Get_text('tutorial_round_pawn'),
                      size[0]*0.9, normal_font_size/2),
        shorten=True,
        font_size=normal_font_size,
        color=(0, 0, 0, 1),
        pos=(size[0]*0.05, size[1]*0.5),
        size=(size[0]*0.9, size[1]*0.4),
        halign="center",
        valign="middle",
        font_name=Settings.get_font(),
    ))
    global_constants.Main_Window.add_widget(Tutorial_Widget(
        size=[0.7*size[0]]*2,
        pos=(size[0]*0.05, size[1]*0.2),
        game=global_constants.game,
        figures=[['pawn', 'black', 3, 2, 'down'],
                 ['pawn', 'black', 1, 5, 'up']]
    ))

    global_constants.Main_Window.add_widget(Button(
        text=Get_text('tutorial_repeat'),
        pos=(size[0] * 0.65, size[1] * 0.05),
        background_color=(1, 1, 0, 0.3),
        color=(0, 1, 0, 1),
        on_press=do_round_tutorial
    ))

# end of circle tutorial


def do_bizantion_tutorial(click=None):
    help_tutorial()
    static_interface(
        size=global_constants.Main_Window.size,
        label_text=Get_text('tutorial_bizantion_start'),
        btn_command=biz1
    )


def biz1(click=None):
    help_tutorial()
    size = global_constants.Main_Window.size
    global_constants.Main_Window.add_widget(Label(
        text=get_text(Get_text('tutorial_bizantion_pawn'),
                      size[0]*0.9, normal_font_size/2),
        shorten=True,
        font_size=normal_font_size,
        color=(0, 0, 0, 1),
        pos=(size[0]*0.05, size[1]*0.5),
        size=(size[0]*0.9, size[1]*0.4),
        halign="center",
        valign="middle",
        font_name=Settings.get_font(),
    ))
    global_constants.Main_Window.add_widget(Tutorial_Widget(
        size=[0.7*size[0]]*2,
        pos=(size[0]*0.05, size[1]*0.2),
        game=global_constants.game,
        figures=[['pawn', 'black', 3, 2, 'down'],
                 ['pawn', 'black', 1, 5, 'up']]
    ))
    global_constants.Main_Window.add_widget(Button(
        text=Get_text('tutorial_next'),
        pos=(size[0] * 0.65, size[1] * 0.05),
        background_color=(1, 1, 0, 0.3),
        color=(0, 1, 0, 1),
        on_press=biz2
    ))


def biz2(click=None):
    help_tutorial()
    interactive_interface(
        size=global_constants.Main_Window.size,
        figure='rook',
        fig_pos=[0, 10],
        label_text=Get_text('tutorial_bizantion_rook'),
        btn_command=biz3
    )


def biz3(click=[]):
    help_tutorial()
    size = global_constants.Main_Window.size
    interactive_interface(
        size=global_constants.Main_Window.size,
        figure='bishop',
        fig_pos=[2, 14],
        label_text=Get_text('tutorial_bizantion_bishop'),
        btn_command=biz4
    )


def biz4(click):
    help_tutorial()
    interactive_interface(
        size=global_constants.Main_Window.size,
        figure='horse',
        fig_pos=[3, 5],
        label_text=Get_text('tutorial_bizantion_horse'),
        btn_command=biz5
    )


def biz5(clicl):
    help_tutorial()
    interactive_interface(
        size=global_constants.Main_Window.size,
        figure='king',
        fig_pos=[2, 9],
        label_text=Get_text('tutorial_bizantion_king'),
        btn_command=biz6
    )


def biz6(click):
    help_tutorial()
    interactive_interface(
        size=global_constants.Main_Window.size,
        figure='queen',
        fig_pos=[0, 11],
        label_text=Get_text('tutorial_bizantion_queen'),
        btn_command=biz7
    )


def biz7(clicl):
    help_tutorial()
    size = global_constants.Main_Window.size
    global_constants.Main_Window.add_widget(Label(
        text=get_text(Get_text('tutorial_bizantion_end'),
                      size[0]*0.9, normal_font_size),
        shorten=True,
        font_size=normal_font_size,
        color=(0, 0, 0, 1),
        pos=(size[0]*0.05, size[1]*0.5),
        size=(size[0]*0.9, size[1]*0.4),
        font_name=Settings.get_font(),
        halign="center",
        valign="middle",
    ))
    global_constants.Main_Window.add_widget(Button(
        text=Get_text('tutorial_repeat'),
        pos=(size[0] * 0.65, size[1] * 0.05),
        background_color=(1, 1, 0, 0.3),
        color=(0, 1, 0, 1),
        on_press=do_bizantion_tutorial
    ))

# end of bizantion tutorial


def do_kuej_tutorial(click=None):
    help_tutorial()
    static_interface(
        size=global_constants.Main_Window.size,
        btn_command=pawn_kuej_tutorial,
        label_text=Get_text('tutorial_kuej_start')
    )


def pawn_kuej_tutorial(click):
    help_tutorial()
    size = global_constants.Main_Window.size
    global_constants.Main_Window.add_widget(Label(
        text=get_text(Get_text('tutorial_kuej_end'),
                      size[0]*0.9, normal_font_size/2),
        shorten=True,
        font_size=normal_font_size,
        color=(0, 0, 0, 1),
        pos=(size[0]*0.05, size[1]*0.5),
        size=(size[0]*0.9, size[1]*0.4),
        font_name=Settings.get_font(),
        halign="center",
        valign="middle",
    ))
    global_constants.Main_Window.add_widget(Static_picture(
        size=[0.7*size[0]]*2,
        game=global_constants.game,
        options=['start']
    ))
    global_constants.Main_Window.add_widget(Button(
        text=Get_text('tutorial_see'),
        pos=(size[0] * 0.3, size[1] * 0.05),
        background_color=(1, 1, 0, 0.3),
        color=(0, 1, 0, 1),
        on_press=glinskiy2
    ))
    global_constants.Main_Window.add_widget(Button(
        text=Get_text('tutorial_repeat'),
        pos=(size[0] * 0.65, size[1] * 0.05),
        background_color=(1, 1, 0, 0.3),
        color=(0, 1, 0, 1),
        on_press=do_kuej_tutorial
    ))

# end of mak - Quej tutorial


def do_garner_tutorial(click=None):
    help_tutorial()
    static_interface(
        size=global_constants.Main_Window.size,
        label_text=Get_text('tutorial_garner_start'),
        btn_command=garner2
    )


def garner2(click=None):
    help_tutorial()
    size = global_constants.Main_Window.size
    global_constants.Main_Window.add_widget(Label(
        text=get_text(Get_text('tutorial_garner_second'),
                      size[0]*0.9, normal_font_size/2),
        shorten=True,
        font_size=normal_font_size,
        color=(0, 0, 0, 1),
        pos=(size[0]*0.05, size[1]*0.5),
        size=(size[0]*0.9, size[1]*0.4),
        font_name=Settings.get_font(),
        halign="center",
        valign="middle",
    ))
    #[ figure, x, y, color ]
    pos = [
        ['queen', 0, 1, 'white'], ['king', 0, 0, 'white'], [
            'pawn', 1, 2, 'white'], ['pawn', 3, 1, 'white'],
        ['pawn', 4, 1, 'white'], ['bishop', 2, 0, 'white'], [
            'horse', 3, 0, 'white'], ['rook', 4, 0, 'white'],
        ['queen', 1, 4, 'black'], ['king', 0, 4, 'black'], [
            'pawn', 1, 3, 'black'], ['pawn', 3, 2, 'black'],
        ['pawn', 4, 3, 'black'], ['bishop', 2, 4, 'black'], [
            'horse', 3, 4, 'black'], ['rook', 4, 4, 'black']
    ]
    global_constants.Main_Window.add_widget(Static_picture(
        size=[0.7*size[0]]*2,
        game=global_constants.game,
        options=[],
        position=pos
    ))

    global_constants.Main_Window.add_widget(Button(
        text=Get_text('tutorial_next'),
        pos=(size[0] * 0.65, size[1] * 0.05),
        background_color=(1, 1, 0, 0.3),
        color=(0, 1, 0, 1),
        on_press=garner3
    ))


def garner3(click=None):
    help_tutorial()
    size = global_constants.Main_Window.size
    global_constants.Main_Window.add_widget(Label(
        text=get_text(Get_text('tutorial_garner_pawn'),
                      size[0]*0.9, normal_font_size/2),
        shorten=True,
        font_size=normal_font_size,
        color=(0, 0, 0, 1),
        pos=(size[0]*0.05, size[1]*0.5),
        size=(size[0]*0.9, size[1]*0.4),
        font_name=Settings.get_font(),
        halign="center",
        valign="middle"
    ))

    global_constants.Main_Window.add_widget(Button(
        text=Get_text('tutorial_next'),
        pos=(size[0] * 0.65, size[1] * 0.05),
        background_color=(1, 1, 0, 0.3),
        color=(0, 1, 0, 1),
        on_press=garner4
    ))


def garner4(click=None):
    help_tutorial()
    interactive_interface(
        size=global_constants.Main_Window.size,
        figure='bishop',
        fig_pos=[2, 2],
        label_text=Get_text('tutorial_garner_bishop'),
        btn_command=garner5
    )


def garner5(click=None):
    help_tutorial()
    interactive_interface(
        size=global_constants.Main_Window.size,
        figure='horse',
        fig_pos=[2, 2],
        label_text=Get_text('tutorial_garner_horse'),
        btn_command=garner6
    )


def garner6(click=None):
    help_tutorial()
    interactive_interface(
        size=global_constants.Main_Window.size,
        figure='rook',
        fig_pos=[2, 2],
        label_text=Get_text('tutorial_garner_rook'),
        btn_command=garner7
    )


def garner7(click=None):
    help_tutorial()
    interactive_interface(
        size=global_constants.Main_Window.size,
        figure='queen',
        fig_pos=[3, 2],
        label_text=Get_text('tutorial_garner_queen'),
        btn_command=garner8
    )


def garner8(click=None):
    help_tutorial()
    interactive_interface(
        size=global_constants.Main_Window.size,
        figure='king',
        fig_pos=[2, 2],
        label_text=Get_text('tutorial_garner_king'),
        btn_command=garner9
    )


def garner9(click=None):
    help_tutorial()
    size = global_constants.Main_Window.size
    global_constants.Main_Window.add_widget(Label(
        text=get_text(Get_text('tutorial_garner_end'),
                      size[0]*0.9, normal_font_size/2),
        shorten=True,
        font_size=normal_font_size,
        color=(0, 0, 0, 1),
        pos=(size[0]*0.05, size[1]*0.5),
        size=(size[0]*0.9, size[1]*0.4),
        font_name=Settings.get_font(),
        halign="center",
        valign="middle",
    ))

    global_constants.Main_Window.add_widget(Button(
        text=Get_text('tutorial_repeat'),
        pos=(size[0] * 0.65, size[1] * 0.05),
        background_color=(1, 1, 0, 0.3),
        color=(0, 1, 0, 1),
        on_press=do_garner_tutorial
    ))

# end of garner tutorial


def do_horde_tutorial(click=None):
    help_tutorial()
    static_interface(
        size=global_constants.Main_Window.size,
        btn_command=horde2,
        label_text=Get_text('tutorial_horde_start')
    )


def horde2(click=None):
    help_tutorial()
    static_interface(
        size=global_constants.Main_Window.size,
        label_text=Get_text('tutorial_horde_second'),
        btn_command=horde3
    )


def horde3(click=None):
    help_tutorial()
    size = global_constants.Main_Window.size
    global_constants.Main_Window.add_widget(Label(
        text=get_text(Get_text('tutorial_horde_pawn'),
                      size[0]*0.9, normal_font_size/2),
        shorten=True,
        font_size=normal_font_size,
        color=(0, 0, 0, 1),
        pos=(size[0]*0.05, size[1]*0.5),
        size=(size[0]*0.9, size[1]*0.4),
        font_name=Settings.get_font(),
        halign="center",
        valign="middle",
    ))

    global_constants.Main_Window.add_widget(Button(
        text=Get_text('tutorial_next'),
        pos=(size[0] * 0.65, size[1] * 0.05),
        background_color=(1, 1, 0, 0.3),
        color=(0, 1, 0, 1),
        on_press=horde4
    ))


def horde4(click=None):
    help_tutorial()
    size = global_constants.Main_Window.size
    global_constants.Main_Window.add_widget(Label(
        text=get_text(Get_text('tutorial_horde_also'),
                      size[0]*0.9, normal_font_size/2),
        shorten=True,
        font_size=normal_font_size,
        color=(0, 0, 0, 1),
        pos=(size[0]*0.05, size[1]*0.5),
        size=(size[0]*0.9, size[1]*0.4),
        font_name=Settings.get_font(),
        halign="center",
        valign="middle",
    ))
    global_constants.Main_Window.add_widget(Static_picture(
        size=[0.7*size[0]]*2,
        game=global_constants.game,
        options=['start']
    ))

    global_constants.Main_Window.add_widget(Button(
        text=Get_text('tutorial_next'),
        pos=(size[0] * 0.65, size[1] * 0.05),
        background_color=(1, 1, 0, 0.3),
        color=(0, 1, 0, 1),
        on_press=classic_1
    ))
    global_constants.Main_Window.add_widget(Button(
        text=Get_text('tutorial_repeat'),
        pos=(size[0] * 0.3, size[1] * 0.05),
        background_normal='',
        background_color=(1, 1, 0, 0.3),
        color=(0, 1, 0, 1),
        on_press=do_horde_tutorial
    ))

# end of horde tutorial


def do_weak_tutorial(click=None):
    help_tutorial()
    static_interface(
        size=global_constants.Main_Window.size,
        label_text=Get_text('tutorial_weak_start'),
        btn_command=week2
    )


def week2(click):
    help_tutorial()
    static_interface(
        size=global_constants.Main_Window.size,
        label_text=Get_text('tutorial_weak_2'),
        btn_command=week3
    )


def week3(click):
    help_tutorial()
    size = global_constants.Main_Window.size
    global_constants.Main_Window.add_widget(Label(
        text=get_text(Get_text('tutorial_weak_3'),
                      size[0]*0.9, normal_font_size/2),
        shorten=True,
        font_size=normal_font_size,
        color=(0, 0, 0, 1),
        pos=(size[0]*0.05, size[1]*0.5),
        font_name=Settings.get_font(),
        size=(size[0]*0.9, size[1]*0.4),
        halign="center",
        valign="middle",
    ))
    global_constants.Main_Window.add_widget(Static_picture(
        size=[0.7*size[0]]*2,
        game=global_constants.game,
        options=['start']
    ))

    global_constants.Main_Window.add_widget(Button(
        text=Get_text('tutorial_see'),
        pos=(size[0] * 0.3, size[1] * 0.05),
        background_color=(1, 1, 0, 0.3),
        color=(0, 1, 0, 1),
        on_press=classic_1
    ))

    global_constants.Main_Window.add_widget(Button(
        text=Get_text('tutorial_repeat'),
        pos=(size[0] * 0.65, size[1] * 0.05),
        background_color=(1, 1, 0, 0.3),
        color=(0, 1, 0, 1),
        on_press=do_weak_tutorial
    ))

# end of weak tutorial


def do_kamikadze_tutorial(click=None):
    help_tutorial()
    static_interface(
        size=global_constants.Main_Window.size,
        label_text=Get_text('tutorial_kamikadze_start'),
        btn_command=kami_2
    )


def kami_2(click=None):
    help_tutorial()
    size = global_constants.Main_Window.size
    global_constants.Main_Window.add_widget(Label(
        text=get_text(Get_text('tutorial_kamikadze_2'),
                      size[0]*0.9, normal_font_size/2),
        shorten=True,
        font_size=normal_font_size,
        color=(0, 0, 0, 1),
        pos=(size[0]*0.05, size[1]*0.5),
        size=(size[0]*0.9, size[1]*0.4),
        font_name=Settings.get_font(),
        halign="center",
        valign="middle",
    ))
    global_constants.Main_Window.add_widget(Static_picture(
        size=[0.7*size[0]]*2,
        game=global_constants.game,
        options=['start']
    ))

    global_constants.Main_Window.add_widget(Button(
        text=Get_text('tutorial_see'),
        pos=(size[0] * 0.3, size[1] * 0.05),
        background_color=(1, 1, 0, 0.3),
        color=(0, 1, 0, 1),
        on_press=classic_1
    ))

    global_constants.Main_Window.add_widget(Button(
        text=Get_text('tutorial_next'),
        pos=(size[0] * 0.65, size[1] * 0.05),
        background_color=(1, 1, 0, 0.3),
        color=(0, 1, 0, 1),
        on_press=kami_3
    ))


def kami_3(click=None):
    help_tutorial()
    static_interface(
        size=global_constants.Main_Window.size,
        label_text=Get_text('tutorial_kamikadze_3'),
        btn_command=kami_4
    )


def kami_4(click=None):
    help_tutorial()
    label_text = Get_text('tutorial_kamikadze_4')
    size = global_constants.Main_Window.size
    global_constants.Main_Window.add_widget(Label(
        text=get_text(label_text, size[0]*0.9, normal_font_size/2),
        shorten=True,
        font_size=normal_font_size,
        color=(0, 0, 0, 1),
        pos=(size[0]*0.05, size[1]*0.5),
        size=(size[0]*0.9, size[1]*0.4),
        halign="center",
        font_name=Settings.get_font(),
        valign="middle",
    ))
    global_constants.Main_Window.add_widget(Static_picture(
        size=[0.7*size[0]]*2,
        game=global_constants.game,
        position=[['king', 7, 4, 'black'], [
            'king', 2, 5, 'white'], ['queen', 6, 4, 'white']]
    ))

    global_constants.Main_Window.add_widget(Button(
        text=Get_text('tutorial_next'),
        pos=(size[0] * 0.65, size[1] * 0.05),
        background_color=(1, 1, 0, 0.3),
        color=(0, 1, 0, 1),
        on_press=kami_5
    ))


def kami_5(click=None):
    help_tutorial()
    label_text = Get_text('tutorial_kamikadze_5')
    size = global_constants.Main_Window.size
    global_constants.Main_Window.add_widget(Label(
        text=get_text(label_text, size[0]*0.9, normal_font_size/2),
        shorten=True,
        font_size=normal_font_size,
        color=(0, 0, 0, 1),
        pos=(size[0]*0.05, size[1]*0.5),
        size=(size[0]*0.9, size[1]*0.4),
        halign="center",
        valign="middle",
        font_name=Settings.get_font(),
    ))
    pos = [
        ['king', 5, 4, 'white'], ['king', 5, 7, 'black'],
        ['bishop', 3, 4, 'black'], ['queen', 1, 4, 'black'],
        ['horse', 4, 2, 'white'], ['queen', 2, 0, 'white']
    ]
    global_constants.Main_Window.add_widget(Static_picture(
        size=[0.7*size[0]]*2,
        game=global_constants.game,
        position=pos
    ))

    global_constants.Main_Window.add_widget(Button(
        text=Get_text('tutorial_next'),
        pos=(size[0] * 0.65, size[1] * 0.05),
        background_color=(1, 1, 0, 0.3),
        color=(0, 1, 0, 1),
        on_press=kami_6
    ))


def kami_6(click=None):
    help_tutorial()
    size = global_constants.Main_Window.size
    global_constants.Main_Window.add_widget(Label(
        text=get_text(Get_text('tutorial_kamikadze_6'),
                      size[0]*0.9, normal_font_size/2),
        shorten=True,
        font_size=normal_font_size,
        color=(0, 0, 0, 1),
        pos=(size[0]*0.05, size[1]*0.5),
        size=(size[0]*0.9, size[1]*0.4),
        halign="center",
        valign="middle",
        font_name=Settings.get_font(),
    ))
    global_constants.Main_Window.add_widget(Static_picture(
        size=[0.7*size[0]]*2,
        game=global_constants.game,
        options=['start']
    ))

    global_constants.Main_Window.add_widget(Button(
        text=Get_text('tutorial_repeat'),
        size=(size[0]*0.1, size[1]*0.05),
        pos=(size[0] * 0.8, size[1] * 0.05),
        background_normal='',
        background_color=(1, 1, 0, 0.3),
        color=(0, 1, 0, 1),
        on_press=do_kamikadze_tutorial
    ))

# end of kamikadze_tutorial


def do_bad_tutorial(click=None):
    help_tutorial()
    static_interface(
        size=global_constants.Main_Window.size,
        label_text=Get_text('tutorial_bad_start'),
        btn_command=bad_2
    )


def bad_2(clicl):
    help_tutorial()
    static_interface(
        size=global_constants.Main_Window.size,
        label_text=Get_text('tutorial_bad_2'),
        btn_command=bad_3
    )
    size = global_constants.Main_Window.size
    global_constants.Main_Window.add_widget(Button(
        text=Get_text('tutorial_see'),
        pos=(size[0] * 0.3, size[1] * 0.05),
        background_color=(1, 1, 0, 0.3),
        color=(0, 1, 0, 1),
        on_press=classic_1
    ))


def bad_3(clic=None):
    help_tutorial()
    size = global_constants.Main_Window.size
    global_constants.Main_Window.add_widget(Label(
        text=Get_text('tutorial_bad_3'),
        shorten=True,
        font_size=normal_font_size,
        color=(0, 0, 0, 1),
        pos=(size[0]*0.05, size[1]*0.5),
        size=(size[0]*0.9, size[1]*0.4),
        halign="left",
        font_name=Settings.get_font(),
        valign="middle",
    ))
    global_constants.Main_Window.add_widget(Static_picture(
        size=[0.7*size[0]]*2,
        game=global_constants.game,
        options=['start']
    ))

    global_constants.Main_Window.add_widget(Button(
        text=Get_text('tutorial_next'),
        pos=(size[0] * 0.65, size[1] * 0.05),
        background_color=(1, 1, 0, 0.3),
        color=(0, 1, 0, 1),
        on_press=bad_4
    ))


def bad_4(click=None):
    help_tutorial()
    help_tutorial()
    size = global_constants.Main_Window.size
    global_constants.Main_Window.add_widget(Label(
        text=get_text(Get_text('tutorial_bad_4'),
                      size[0]*0.9, normal_font_size/2),
        shorten=True,
        font_size=normal_font_size,
        color=(0, 0, 0, 1),
        pos=(size[0]*0.05, size[1]*0.5),
        size=(size[0]*0.9, size[1]*0.4),
        font_name=Settings.get_font(),
        halign="center",
        valign="middle",
    ))
    global_constants.Main_Window.add_widget(Static_picture(
        size=[0.7*size[0]]*2,
        game=global_constants.game,
        options=['start']
    ))

    global_constants.Main_Window.add_widget(Button(
        text=Get_text('tutorial_repeat'),
        pos=(size[0] * 0.65, size[1] * 0.05),
        background_color=(1, 1, 0, 0.3),
        color=(0, 1, 0, 1),
        on_press=do_bad_tutorial
    ))

# end of bad_chess tutorial


def do_racing_tutorial(par=None):
    help_tutorial()
    size = global_constants.Main_Window.size
    static_interface(
        size=global_constants.Main_Window.size,
        label_text=Get_text('tutorial_rase_start'),
        btn_command=rase2
    )
    global_constants.Main_Window.add_widget(Button(
        text=Get_text('tutorial_see'),
        pos=(size[0] * 0.3, size[1] * 0.05),
        background_color=(1, 1, 0, 0.3),
        color=(0, 1, 0, 1),
        on_press=classic_1
    ))


def rase2(par=None):
    help_tutorial()
    size = global_constants.Main_Window.size
    label_text = Get_text('tutorial_rase_2')
    position = [
        ['king', 6, 7, 'white'], ['king', 3, 6,
                                  'black'], ['bishop', 2, 2, 'black'],
        ['rook', 5, 3, 'white'], ['rook', 1, 2, 'black'], ['bishop', 2, 4, 'white']
    ]

    global_constants.Main_Window.add_widget(Label(
        text=get_text(label_text, size[0]*0.9, normal_font_size/2),
        shorten=True,
        font_size=normal_font_size,
        color=(0, 0, 0, 1),
        pos=(size[0]*0.05, size[1]*0.55),
        size=(size[0]*0.9, size[1]*0.4),
        halign="center",
        valign="middle",
        font_name=Settings.get_font(),
    ))
    global_constants.Main_Window.add_widget(Static_picture(
        size=[0.7*size[0]]*2,
        game=global_constants.game,
        position=position
    ))

    global_constants.Main_Window.add_widget(Button(
        text=Get_text('tutorial_next'),
        pos=(size[0] * 0.65, size[1] * 0.05),
        background_normal='',
        background_color=(1, 1, 0, 0.3),
        color=(0, 1, 0, 1),
        on_press=rase3
    ))


def rase3(par=None):
    help_tutorial()
    size = global_constants.Main_Window.size
    label_text = Get_text('tutorial_rase_3')
    position = [['king', 'white', 4, 4], [
        'king', 'black', 2, 0], ['queen', 'black', 2, 5]]

    global_constants.Main_Window.add_widget(Label(
        text=get_text(label_text, size[0]*0.9, normal_font_size/2),
        font_size=normal_font_size,
        color=(0, 0, 0, 1),
        pos=(size[0]*0.05, size[1]*0.55),
        size=(size[0]*0.9, size[1]*0.4),
        halign="center",
        valign="middle",
        font_name=Settings.get_font(),
    ))
    global_constants.Main_Window.add_widget(Tutorial_Widget(
        size=[0.7*size[0]]*2,
        game=global_constants.game,
        pos=(size[0]*0.05, size[1]*0.2),
        figures=position,
        options=['check']
    ))

    global_constants.Main_Window.add_widget(Button(
        text=Get_text('tutorial_next'),
        pos=(size[0] * 0.65, size[1] * 0.05),
        background_normal='',
        background_color=(1, 1, 0, 0.3),
        color=(0, 1, 0, 1),
        on_press=rase4
    ))


def rase4(par=None):
    help_tutorial()
    size = global_constants.Main_Window.size
    global_constants.Main_Window.add_widget(Label(
        text=get_text(Get_text('tutorial_rase_4'),
                      size[0]*0.9, normal_font_size/2),
        font_size=normal_font_size,
        color=(0, 0, 0, 1),
        pos=(size[0]*0.05, size[1]*0.5),
        size=(size[0]*0.9, size[1]*0.4),
        halign="center",
        valign="middle",
        font_name=Settings.get_font(),
    ))
    global_constants.Main_Window.add_widget(Static_picture(
        size=[0.7*size[0]]*2,
        game=global_constants.game,
        options=['start']
    ))

    global_constants.Main_Window.add_widget(Button(
        text=Get_text('tutorial_repeat'),
        pos=(size[0] * 0.65, size[1] * 0.05),
        background_color=(1, 1, 0, 0.3),
        color=(0, 1, 0, 1),
        on_press=do_racing_tutorial
    ))

# end of rasing tutorial


def do_haos_tutorial(par=None):
    help_tutorial()
    size = global_constants.Main_Window.size
    static_interface(
        size=global_constants.Main_Window.size,
        label_text=Get_text('tutorial_haos_start'),
        btn_command=haos2
    )
    global_constants.Main_Window.add_widget(Button(
        text=Get_text('tutorial_see'),
        pos=(size[0] * 0.3, size[1] * 0.05),
        background_color=(1, 1, 0, 0.3),
        color=(0, 1, 0, 1),
        on_press=classic_1
    ))


def haos2(par=None):
    help_tutorial()
    static_interface(
        size=global_constants.Main_Window.size,
        label_text=Get_text('tutorial_haos_2'),
        btn_command=do_haos_tutorial,
        repeat=True
    )

# add haotic tutorial


def do_schatranj_tutorial(par=None):
    help_tutorial()
    static_interface(
        size=global_constants.Main_Window.size,
        label_text=Get_text('tutorial_shcatranj_start'),
        btn_command=schat2
    )


def schat2(par=...):
    help_tutorial()
    static_interface(
        size=global_constants.Main_Window.size,
        label_text=Get_text('tutorial_shcatranj_changes'),
        btn_command=schat3
    )


def schat3(par=None):
    help_tutorial()
    board = [
        ['white', 5, 5, 'pawn'], ['white', 1, 1, 'pawn'], ['black', 2, 3, 'pawn'],
        ['white', 4, 2, 'pawn'], ['black', 5, 3, 'pawn']
    ]
    actions = [
        ['show', 1, 1, [[1, 2]]],         ['move', 1, 1, 1, 2],
        ['show_attack', 2, 3, 1, 2],       ['take', 2, 3, 1, 2],
        ['show_attack', 4, 2, 5, 3],       ['take', 4, 2, 5, 3],
        ['move', 1, 2, 1, 1],              ['move', 5, 5, 5, 6],
        ['move', 1, 1, 1, 0],              ['change', 1, 0, 'queen'],
        ['move', 5, 6, 5, 7],              ['change', 5, 7, 'queen']
    ]
    size = global_constants.Main_Window.size
    text = get_text(Get_text('tutorial_shcatranj_pawn'),
                    size[0]*0.9, normal_font_size/2)
    video_interface(board, actions, 1.2, schat4, text)


def schat4(par=None):
    help_tutorial()
    interactive_interface(
        size=global_constants.Main_Window.size,
        figure='bishop',
        btn_command=schat5,
        label_text=Get_text('tutorial_shcatranj_bishop')
    )


def schat5(par=...):
    help_tutorial()
    interactive_interface(
        size=global_constants.Main_Window.size,
        figure='rook',
        btn_command=schat6,
        label_text=Get_text('tutorial_shcatranj_rook')
    )


def schat6(par=...):
    help_tutorial()
    interactive_interface(
        size=global_constants.Main_Window.size,
        figure='king',
        btn_command=schat7,
        label_text=Get_text('tutorial_shcatranj_king')
    )


def schat7(par=...):
    help_tutorial()
    interactive_interface(
        size=global_constants.Main_Window.size,
        figure='horse',
        btn_command=schat8,
        label_text=Get_text('tutorial_shcatranj_horse')
    )


def schat8(par=...):
    help_tutorial()
    interactive_interface(
        size=global_constants.Main_Window.size,
        figure='queen',
        btn_command=schat9,
        label_text=Get_text('tutorial_shcatranj_queen')
    )


def schat9(par=...):
    help_tutorial()
    static_interface(
        repeat=True,
        size=global_constants.Main_Window.size,
        label_text=Get_text('tutorial_shcatranj_end'),
        btn_command=do_schatranj_tutorial
    )

# end of schatranj tutorial


def do_dark_tutorial(par=...):
    help_tutorial()
    static_interface(
        repeat=False,
        size=global_constants.Main_Window.size,
        label_text=Get_text('tutorial_dark_start'),
        btn_command=dark2
    )


def dark2(par=None):
    size = global_constants.Main_Window.size
    help_tutorial()
    static_interface(
        size=size,
        label_text=Get_text('tutorial_dark_second'),
        btn_command=dark3
    )
    global_constants.Main_Window.add_widget(Button(
        text=Get_text('tutorial_see'),
        pos=(size[0] * 0.32, size[1] * 0.05),
        background_normal='',
        background_color=(1, 1, 0, 0.3),
        color=(0, 1, 0, 1),
        on_press=classic_1
    ))


def dark3(par=None):
    help_tutorial()
    static_interface(
        size=global_constants.Main_Window.size,
        label_text=Get_text('tutorial_dark_purpose'),
        btn_command=dark4
    )


def dark4(par=...):
    help_tutorial()
    static_interface(
        label_text=Get_text('tutorial_dark_last'),
        repeat=True,
        btn_command=do_dark_tutorial,
        size=global_constants.Main_Window.size
    )

# end of dark tutorial


def do_freeze_tutorial(par=...):
    help_tutorial()
    static_interface(
        size=global_constants.Main_Window.size,
        label_text=Get_text('tutorial_freeze_start'),
        repeat=False,
        btn_command=freeze2
    )


def freeze2(par=None):
    help_tutorial()
    figures = ['rook', 'horse', 'bishop', 'queen',
               'king', 'bishop', 'horse', 'rook']
    board = []
    for x in range(8):
        board.append(['white', x, 0, figures[x]])
        board.append(['black', x, 7, figures[x]])
        board.append(['white', x, 1, 'pawn'])
        board.append(['black', x, 6, 'pawn'])
        for y in 2, 3, 4, 5:
            board.append(['', x, y, 'frozen'])
    size = global_constants.Main_Window.size
    text = get_text(Get_text('tutorial_freeze_2'),
                    size[0]*0.9, normal_font_size/2)
    actions = [
        ['show', 5, 1, [[6, 2], [4, 2]]],    ['take', 5, 1, 6, 2],
        ['show', 3, 6, [[2, 5], [4, 5]]],    ['take', 3, 6, 2, 5],
        ['take', 6, 2, 5, 3],              ['take', 6, 7, 5, 5],
        ['take', 5, 3, 4, 4],              ['take', 2, 7, 4, 5],
        ['pause']
    ]
    video_interface(board, actions, 1.1, freeze3, text)


def freeze3(par=None):
    help_tutorial()
    static_interface(
        size=global_constants.Main_Window.size,
        label_text=Get_text('tutorial_freeze_3'),
        repeat=False,
        btn_command=freeze4
    )


def freeze4(par=None):
    help_tutorial()
    size = global_constants.Main_Window.size
    static_interface(
        size=global_constants.Main_Window.size,
        label_text=Get_text('tutorial_freeze_4'),
        repeat=True,
        btn_command=do_freeze_tutorial
    )
    global_constants.Main_Window.add_widget(Button(
        text=Get_text('tutorial_see'),
        pos=(size[0] * 0.32, size[1] * 0.05),
        background_normal='',
        background_color=(1, 1, 0, 0.3),
        color=(0, 1, 0, 1),
        on_press=classic_1
    ))

# end of freeze tutorial


def do_nuclear_tutorial(par=None):
    help_tutorial()
    size = global_constants.Main_Window.size
    static_interface(
        size=global_constants.Main_Window.size,
        label_text=Get_text('tutorial_nuclear_start'),
        repeat=False,
        btn_command=nuc2
    )
    global_constants.Main_Window.add_widget(Button(
        text=Get_text('tutorial_see'),
        pos=(size[0] * 0.32, size[1] * 0.05),
        background_normal='',
        background_color=(1, 1, 0, 0.3),
        color=(0, 1, 0, 1),
        on_press=classic_1
    ))


def nuc2(par=...):
    help_tutorial()
    size = global_constants.Main_Window.size
    text = get_text(Get_text('tutorial_nuclear_2'),
                    size[0]*0.9, normal_font_size/2)
    board = []
    figures = ['rook', 'horse', 'bishop', 'queen',
               'king', 'bishop', 'horse', 'rook']
    for x in range(8):
        board.append(['white', x, 1, 'pawn'])
        board.append(['black', x, 6, 'pawn'])
        board.append(['white', x, 0, figures[x]])
        board.append(['black', x, 7, figures[x]])
    action = [
        ['move', 1, 0, 2, 2],         ['move', 1, 7, 2, 5],
        ['move', 2, 2, 1, 4],         ['move', 6, 7, 5, 5],
        ['take', 1, 4, 2, 6],         ['boom', 2, 6],
        ['move', 5, 5, 4, 3],         ['move', 1, 1, 1, 2],
        ['take', 4, 3, 5, 1],         ['boom', 5, 1],
        ['pause'],                ['pause']
    ]
    video_interface(board, action, 1.1, nuc3, text)


def nuc3(par=...):
    help_tutorial()
    size = global_constants.Main_Window.size
    text = get_text(Get_text('tutorial_nuclear_3'),
                    size[0]*0.9, normal_font_size/2)
    board = [
        ['black', 7, 6, 'pawn'], ['black', 6, 6, 'pawn'], ['black', 5, 6, 'pawn'],
        ['black', 6, 7, 'king'], ['white', 7, 1, 'pawn'], ['white', 6, 1, 'pawn'],
        ['white', 6, 0, 'king'], ['white', 3, 0,
                                  'rook'], ['black', 1, 6, 'bishop'],
        ['black', 0, 6, 'pawn'], ['black', 1, 5, 'pawn'], ['black', 2, 6, 'pawn'],
        ['white', 0, 1, 'pawn'], ['white', 1, 1, 'pawn'], ['white', 2, 1, 'pawn']
    ]
    rook_line = []
    for y in range(1, 8):
        rook_line.append([3, y])
    action = [
        ['show', 3, 0, rook_line], ['move', 3, 0, 3, 7], [
            'show_attack', 3, 7, 6, 7],
        ['show_attack', 1, 6, 6, 1], ['take', 1, 6, 6, 1], ['boom', 6, 1]
    ]
    video_interface(board, action, 1.7, nuc4, text)


def nuc4(par=...):
    help_tutorial()
    size = global_constants.Main_Window.size
    text = get_text(Get_text('tutorial_nuclear_4'),
                    size[0]*0.9, normal_font_size/2)
    board = [
        ['black', 7, 6, 'pawn'], ['black', 6, 5, 'pawn'], ['black', 5, 6, 'pawn'],
        ['black', 6, 7, 'king'], ['white', 7, 1, 'pawn'], ['white', 6, 1, 'pawn'],
        ['white', 6, 0, 'king'], ['white', 3, 0,
                                  'rook'], ['black', 1, 6, 'bishop'],
        ['black', 0, 6, 'pawn'], ['black', 1, 5, 'pawn'], ['black', 2, 6, 'pawn'],
        ['white', 0, 1, 'pawn'], ['white', 1, 1, 'pawn'], ['white', 2, 1, 'pawn']
    ]
    rook_line = []
    for y in range(1, 8):
        rook_line.append([3, y])
    action = [
        ['show', 3, 0, rook_line], ['move', 3, 0, 3, 7], [
            'show_attack', 3, 7, 6, 7],
        ['show_attack', 1, 6, 6, 1], ['take', 1, 6, 6, 1], ['boom', 6, 1]
    ]
    video_interface(board, action, 1.7, nuc5, text)


def nuc5(par=...):
    help_tutorial()
    pos = [['king', 4, 4, 'white'], [
        'king', 3, 4, 'black'], ['queen', 2, 2, 'white']]
    size = global_constants.Main_Window.size

    global_constants.Main_Window.add_widget(Label(
        text=get_text(Get_text('tutorial_nuclear_5'),
                      size[0]*0.9, normal_font_size/2),
        shorten=True,
        font_size=normal_font_size,
        color=(0, 0, 0, 1),
        pos=(size[0]*0.05, size[1]*0.55),
        size=(size[0]*0.9, size[1]*0.4),
        halign="center",
        valign="middle",
        font_name=Settings.get_font(),
    ))

    global_constants.Main_Window.add_widget(Static_picture(
        size=[0.7*size[0]]*2,
        game=global_constants.game,
        position=pos,
        options=[]
    ))

    button_text = Get_text('tutorial_next')
    global_constants.Main_Window.add_widget(Button(
        text=button_text,
        pos=(size[0] * 0.65, size[1] * 0.05),
        background_normal='',
        background_color=(1, 1, 0, 0.3),
        color=(0, 1, 0, 1),
        on_press=nuc6
    ))


def nuc6(par=...):
    help_tutorial()
    size = global_constants.Main_Window.size
    text = get_text(Get_text('tutorial_nuclear_5'),
                    size[0]*0.9, normal_font_size/2)
    board = [
        ['white', 3, 3, 'king'], ['black', 2, 3, 'bishop'],
        ['white', 2, 6, 'rook'], ['black', 7, 7, 'king']
    ]
    fields = [[2, 7], [2, 4], [2, 5]]
    for x in 0, 1, 3, 4, 5, 6, 7:
        fields.append([x, 6])

    action = [
        ['show_attack', 2, 6, 2, 3], ['show', 2, 6, fields], ['move', 2, 6, 0, 6]
    ]
    video_interface(board, action, 1.5, nuc7, text)


def nuc7(par=...):
    help_tutorial()
    size = global_constants.Main_Window.size
    board = [['king', 1, 1, 'white'], [
        'king', 7, 7, 'black'], ['rook', 6, 6, 'white']]

    global_constants.Main_Window.add_widget(Label(
        text=get_text(Get_text('tutorial_nuclear_5'),
                      size[0]*0.9, normal_font_size/2),
        shorten=True,
        font_size=normal_font_size,
        color=(0, 0, 0, 1),
        pos=(size[0]*0.05, size[1]*0.55),
        size=(size[0]*0.9, size[1]*0.4),
        halign="center",
        valign="middle",
        font_name=Settings.get_font(),
    ))

    global_constants.Main_Window.add_widget(Static_picture(
        size=[0.7*size[0]]*2,
        game=global_constants.game,
        position=board,
        options=[]
    ))

    button_text = Get_text('tutorial_next')
    global_constants.Main_Window.add_widget(Button(
        text=button_text,
        pos=(size[0] * 0.65, size[1] * 0.05),
        background_normal='',
        background_color=(1, 1, 0, 0.3),
        color=(0, 1, 0, 1),
        on_press=nuc8
    ))


def nuc8(par=...):
    help_tutorial()
    static_interface(
        size=global_constants.Main_Window.size,
        label_text=Get_text('tutorial_nuclear_end'),
        btn_command=do_nuclear_tutorial,
        repeat=True
    )

# end of nuclear tutorial


def do_legan_tutorial(par=...):
    help_tutorial()
    static_interface(
        size=global_constants.Main_Window.size,
        label_text=Get_text('tutorial_legan_start'),
        btn_command=legan2,
        repeat=False
    )


def legan2(par=...):
    help_tutorial()
    static_interface(
        size=global_constants.Main_Window.size,
        label_text=Get_text('tutorial_legan_2'),
        btn_command=legan3,
        repeat=False
    )
    size = global_constants.Main_Window.size
    global_constants.Main_Window.add_widget(Button(
        text=Get_text('tutorial_see'),
        pos=(size[0] * 0.32, size[1] * 0.05),
        background_normal='',
        background_color=(1, 1, 0, 0.3),
        color=(0, 1, 0, 1),
        on_press=classic_1
    ))


def legan3(par=None):
    help_tutorial()
    board = [
        ['white', 5, 1, 'pawn'], ['black', 4, 3, 'horse'],
        ['black', 2, 5, 'pawn'], ['white', 3, 6, 'pawn'],
        ['black', 0, 3, 'pawn']
    ]
    actions = [
        ['show', 5, 1, [[4, 2]]], ['move', 5, 1, 4, 2], ['show', 2, 5, [[3, 4]]],
        ['move', 2, 5, 3, 4], ['show_attack', 4, 2, 4, 3], ['take', 4, 2, 4, 3],
        ['move', 0, 3, 1, 2], ['move', 3, 6, 2, 7], ['change', 2, 7, 'queen'],
        ['pause']
    ]
    size = global_constants.Main_Window.size
    text = get_text(Get_text('tutorial_legan_3'),
                    size[0]*0.9, normal_font_size/2)
    video_interface(
        board=board,
        actions=actions,
        speed=1.3,
        command=legan4,
        text=text
    )


def legan4(par=None):
    help_tutorial()
    size = global_constants.Main_Window.size
    label_text = Get_text('tutorial_legan_4')
    global_constants.Main_Window.add_widget(Label(
        text=get_text(label_text, size[0]*0.9, normal_font_size/2),
        shorten=True,
        font_size=normal_font_size,
        color=(0, 0, 0, 1),
        pos=(size[0]*0.05, size[1]*0.55),
        size=(size[0]*0.9, size[1]*0.4),
        halign="center",
        valign="middle",
        font_name=Settings.get_font(),
    ))
    pos = []
    for x in 4, 5, 6, 7:
        pos.append(['pawn', x, 0, 'white'])
        pos.append(['pawn', 0, x, 'black'])
    for i in 1, 2, 3:
        pos.append(['pawn', 7, i, 'white'])
        pos.append(['pawn', i, 7, 'black'])
    global_constants.Main_Window.add_widget(Static_picture(
        size=[0.7*size[0]]*2,
        game=global_constants.game,
        options=[],
        position=pos
    ))

    button_text = Get_text('tutorial_next')
    global_constants.Main_Window.add_widget(Button(
        text=button_text,
        pos=(size[0] * 0.65, size[1] * 0.05),
        background_normal='',
        background_color=(1, 1, 0, 0.3),
        color=(0, 1, 0, 1),
        on_press=legan5
    ))


def legan5(par=None):
    help_tutorial()
    static_interface(
        size=global_constants.Main_Window.size,
        label_text=Get_text('tutorial_legan_end'),
        btn_command=do_legan_tutorial,
        repeat=1
    )

# end of legan tutorial


def do_sovereign_tutorial(par=...):
    help_tutorial()
    text = Get_text('tutorial_sovereign_start')
    size = global_constants.Main_Window.size
    static_interface(size, text, sov2)


def sov2(par=None):
    help_tutorial()
    text = Get_text('tutorial_sovereign_2')
    size = global_constants.Main_Window.size
    static_interface(size, text, sov3)


def sov3(par=...):
    help_tutorial()
    text = Get_text('tutorial_sovereign_3')
    size = global_constants.Main_Window.size
    static_interface(size, text, sov4)


def get_sovereign_start_board():
    board = []
    colors = [
        'gray', 'gray', 'pink', 'pink', 'white', 'white',
        'white', 'white', 'white', 'white', 'white', 'white',
        'green', 'green', 'light', 'light']
    figures = [
        'queen', 'bishop', 'rook', 'horse', 'rook', 'horse',
        'bishop', 'queen', 'king', 'bishop', 'horse', 'rook',
        'horse', 'rook', 'bishop', 'queen'
    ]
    for i in range(16):
        board.append([colors[i], i, 0, figures[i]])
        if i not in [0, 1, 15, 14]:
            board.append([colors[i], i, 1, 'pawn'])

    colors = [
        'light', 'light', 'purple', 'purple', 'black', 'black', 'black',
        'black', 'black', 'black', 'black', 'black', 'yellow', 'yellow',
        'gray', 'gray'
    ]
    for i in range(16):
        board.append([colors[i], i, 15, figures[i]])
        if i not in [0, 1, 15, 14]:
            board.append([colors[i], i, 14, 'pawn'])
    board.append(['gray', 0, 1, 'rook'])
    board.append(['gray', 1, 1, 'horse'])
    board.append(['light', 14, 1, 'horse'])
    board.append(['light', 15, 1, 'rook'])
    board.append(['light', 0, 14, 'rook'])
    board.append(['light', 1, 14, 'horse'])
    board.append(['gray', 14, 14, 'horse'])
    board.append(['gray', 15, 14, 'rook'])
    colors = [
        'red', 'red', 'orange', 'orange', 'yellow', 'yellow', 'green',
        'green', 'cyan', 'cyan', 'blue', 'blue'
    ]
    figures = [
        'bishop', 'queen', 'rook', 'horse', 'bishop', 'queen',
        'queen', 'bishop', 'horse', 'rook', 'queen', 'bishop'
    ]
    for i in range(0, 12):
        board.append((colors[i], 0, i+2, figures[i]))
        board.append([colors[i], 1, i+2, 'pawn'])
    colors = [
        'cyan', 'cyan', 'blue', 'blue', 'purple', 'purple',
        'pink', 'pink', 'red', 'red', 'orange', 'orange'
    ]
    for i in range(0, 12):
        board.append([colors[i], 15, i+2, figures[i]])
        board.append([colors[i], 14, i+2, 'pawn'])
    return board


def sovereign_video_interface(board, actions=[], speed=1, text='test_text', command=print):
    size = global_constants.Main_Window.size
    global_constants.Main_Window.add_widget(Label(
        text=get_text(text, size[0]*0.9, normal_font_size/2),
        shorten=True,
        font_size=normal_font_size,
        color=(0, 0, 0, 1),
        pos=(size[0]*0.05, size[1]*0.5),
        size=(size[0]*0.9, size[1]*0.4),
        halign="center",
        valign="middle",
        font_name=Settings.get_font()
    ))

    video = sovereign_interactive_tutorial.VideoChess(
        board=board,
        speed=speed,
        actions=actions,
    )
    global_constants.Main_Window.add_widget(video)

    def later(cllick):
        video.timer.cancel()
        video.__del__()
        video.must = False
        command(cllick)

    global_constants.Main_Window.add_widget(Button(
        text=Get_text('tutorial_next'),
        pos=(size[0] * 0.65, size[1] * 0.05),
        background_color=(1, 1, 0, 0.3),
        color=(0, 1, 0, 1),
        on_press=later
    ))


def sov4(arg=None):
    help_tutorial()
    board = get_sovereign_start_board()
    activity = [
        ['show', 4, 1, [[4, 2], [4, 3]]], ['move', 4, 1, 4, 3],
        ['show', 4, 14, [[4, 13], [4, 12]]], ['move', 4, 14, 4, 12],
        ['move', 4, 3, 4, 4], ['move', 4, 12, 4, 11],
        ['show', 4, 4, [[4, 5], [5, 4]]], ['pause'], [
            'show', 1, 12, [[2, 12], [3, 12]]],
        ['pause'], ['pause'], ['move', 1, 12, 3, 12],
        ['move', 1, 3, 3, 3], ['show', 4, 4, [[4, 5], [5, 4]]],
        ['move', 4, 4, 5, 4], ['move', 10, 14, 10, 12],
        ['move', 5, 4, 5, 5], ['move', 10, 12, 10, 11], ['move', 11, 1, 11, 3],
        ['show', 10, 11, [[9, 11]]], ['pause'], ['move', 7, 14, 7, 13],
        ['show', 11, 3, [[10, 3]]]
    ]
    text = Get_text('tutorial_sovereign_4')

    size = global_constants.Main_Window.size
    global_constants.Main_Window.add_widget(Label(
        text=get_text(text, size[0]*0.9, normal_font_size/2),
        shorten=True,
        font_size=normal_font_size,
        color=(0, 0, 0, 1),
        pos=(size[0]*0.05, size[1]*0.5),
        size=(size[0]*0.9, size[1]*0.4),
        halign="center",
        valign="middle",
        font_name=Settings.get_font()
    ))

    video = sovereign_interactive_tutorial.VideoChess(
        board=board,
        speed=1.7,
        actions=activity,
    )
    global_constants.Main_Window.add_widget(video)

    def later(cllick):
        video.timer.cancel()
        video.__del__()
        video.must = False
        sov5(cllick)

    global_constants.Main_Window.add_widget(Button(
        text=Get_text('tutorial_next'),
        pos=(size[0] * 0.65, size[1] * 0.05),
        background_color=(1, 1, 0, 0.3),
        color=(0, 1, 0, 1),
        on_press=later
    ))


def sov5(arg=...):
    help_tutorial()
    activity = [
        ['move', 4, 1, 4, 3], ['move', 4, 14, 4, 12], ['move', 4, 3, 4, 4],
        ['move', 4, 12, 4, 11], ['change_color', 8, 0, 'blue'], ['pause'],
        ['change_color', 8, 15, 'red'], ['pause'], [
            'show', 14, 5, [[13, 5], [12, 5]]],
        ['move', 14, 5, 12, 5]
    ]
    sovereign_video_interface(
        board=get_sovereign_start_board(),
        actions=activity,
        speed=1.5,
        text=Get_text('tutorial_sovereign_5'),
        command=sov6
    )


def sov6(arg=None):
    help_tutorial()
    activity = [
        ['move', 4, 1, 4, 3], ['move', 4, 14, 4, 12], ['move', 4, 3, 4, 4],
        ['move', 4, 12, 4, 11], ['change_color', 8, 0, 'blue'], ['pause'],
        ['move', 6, 14, 6, 13], ['move', 15, 5, 13, 6], ['move', 7, 15, 3, 11],
        ['move', 13, 6, 11, 7], ['move', 3, 11, 6, 8], ['move', 11, 7, 10, 9],
        ['move', 6, 8, 7, 8], ['show_attack', 7, 0, 8, 0], ['take', 8, 0, 9, 1],
        ['move', 10, 0, 11, 2], ['show_attack', 11, 2, 9, 1], ['pause'], ['pause']
    ]
    sovereign_video_interface(
        board=get_sovereign_start_board(),
        actions=activity,
        speed=1.5,
        text=Get_text('tutorial_sovereign_6'),
        command=sov7
    )


def sov7(arg=...):
    help_tutorial()
    board = [
        ['black', 3, 11, 'king'], ['black', 0, 15, 'rook'],
        ['white', 6, 5, 'queen'], ['white', 7, 9, 'bishop'],
        ['white', 15, 0, 'king'], ['white', 11, 0, 'rook']
    ]
    activity = [
        ['show', 6, 5, [[5, 5], [4, 5], [3, 5], [2, 5], [1, 5], [0, 5], [5, 4], [4, 3], [3, 2], [2, 1], [1, 0],
                        [5, 6], [4, 7], [3, 8], [2, 9], [1, 10], [0, 11], [
                            6, 4], [6, 3], [6, 2], [6, 1], [6, 0], [7, 4], [8, 3],
                        [9, 2], [10, 1], [7, 5], [8, 5], [9, 5], [10, 5], [
            11, 5], [12, 5], [13, 5], [14, 5], [7, 6],
            [8, 7], [9, 8], [10, 9], [11, 10], [12, 11], [13, 12], [
                14, 13], [6, 6], [6, 7], [6, 8], [6, 9], [6, 10],
            [6, 11], [6, 12], [6, 13]]],
        ['pause'], ['pause'], ['pause'],
        ['move', 6, 5, 6, 0],
        ['show', 0, 15, [[0, 14], [0, 13], [0, 12], [0, 11], [0, 10], [0, 9], [0, 8], [0, 7], [1, 15], [2, 15], [3, 15],
                         [4, 15], [5, 15], [6, 15], [7, 15], [8, 15]]],
        ['pause'], ['pause'],
        ['move', 0, 15, 0, 10], ['pause'],
        ['show', 7, 9, [[6, 8], [5, 7], [4, 6], [3, 5], [2, 4], [1, 3], [0, 2], [6, 10], [5, 11], [4, 12], [3, 13], [2, 14],
                        [1, 15], [8, 10], [9, 11], [10, 12], [11, 13], [12, 14], [
                            13, 15], [8, 8], [9, 7], [10, 6], [11, 5], [12, 4],
                        [13, 3], [14, 2], [15, 1]]],
        ['pause'], ['pause'], ['pause'],
        ['move', 7, 9, 0, 2], ['pause'],
        ['show', 3, 11, [[2, 10], [2, 11], [2, 12], [
            3, 10], [3, 12], [4, 10], [4, 11], [4, 12]]],
        ['pause'], ['pause'],
        ['move', 3, 11, 4, 11],
        ['pause'],
        ['show', 11, 0, [[12, 0], [13, 0], [14, 0], [10, 0], [
            9, 0], [8, 0], [7, 0], [11, 1], [11, 2], [11, 3]]],
        ['pause'], ['pause'],
        ['move', 11, 0, 11, 3],
        ['pause']
    ]
    sovereign_video_interface(
        board=board,
        actions=activity,
        text=Get_text('tutorial_sovereign_7'),
        command=sov8
    )


def sov8(arg=...):
    help_tutorial()
    size = global_constants.Main_Window.size
    text = Get_text('tutorial_sovereign_8')
    global_constants.Main_Window.add_widget(Label(
        text=get_text(text, size[0]*0.9, normal_font_size/2),
        shorten=True,
        font_size=normal_font_size,
        color=(0, 0, 0, 1),
        pos=(size[0]*0.05, size[1]*0.5),
        size=(size[0]*0.9, size[1]*0.4),
        halign="center",
        valign="middle",
        font_name=Settings.get_font()
    ))

    global_constants.Main_Window.add_widget(Button(
        text=Get_text('tutorial_next'),
        pos=(size[0] * 0.65, size[1] * 0.05),
        background_color=(1, 1, 0, 0.3),
        color=(0, 1, 0, 1),
        on_press=sov9
    ))


def sov9(arg=...):
    help_tutorial()
    board = [
        ['white', 8, 0, 'pawn'], ['black', 11,14, 'pawn'], ['white', 1, 3, 'pawn'],
        ['white', 15, 0, 'king'], ['black', 0, 15, 'king'], ['black', 7, 4, 'pawn']
    ]
    activity = [
        ['show', 11, 14, [[10, 14], [11, 13], [11, 12]]], ['pause'],
        ['move', 11, 14, 10, 14],
        ['show',8,0,[[8,1],[8,2]]], ['pause'],
        ['move',8,0,8,2],
        ['show',10,14,[[10,13], [9,14]]], ['pause'],
        ['move',10,14,9,14],
        ['move',8,2,8,3],['pause'],
        ['move',9,14,9,13],
        ['show_attack',8,3,7,4], ['pause'],
        ['take',8,3,7,4], ['move',9,13,9,12],['move',7,4,7,5],
        ['move',9,12,9,11], ['move', 7, 5, 7, 6],['change',7,6,'queen'],
        ['pause'], ['move',9,11,9,10], ['show',1,3,[[1,4],[2,3],[3,3]]],
        ['pause'], ['move',1,3,3,3],['pause'],
        ['move',9,10,9,9], ['change',9,9,'rook'], ['pause']
    ]
    sovereign_video_interface(
        board=board,
        text=Get_text('tutorial_sovereign_9'),
        speed=1.5,
        actions=activity,
        command=sov10
    )

def sov10(arg=...):
    help_tutorial()
    board = [
        ['white',2,2,'pawn'], ['white',13,2,'pawn'],
        ['black',2,13,'pawn'], ['black',13,13,'pawn']
        ]
    action = [
        ['show',2,2,[[3,3],[3,1], [1,3] ]], ['pause'],
        ['show',13,2,[[12,3],[12,1], [14,3]]], ['pause'],
        ['show',2,13,[[3,12],[3,14], [1,12]]], ['pause'],
        ['show',13,13,[[12,12],[14,12],[12,14]]],['pause']
    ]
    sovereign_video_interface(
        board=board,
        text=Get_text('tutorial_sovereign_10'),
        speed=1.5,
        actions=action,
        command=sov11
    )

def sov11(arg=...):
    help_tutorial()
    board = [
        ['white',8,0,'king'], ['white',11,0,'rook'],
        ['black',8,15,'king'],['purple',2,15,'rook'],['black',8,10,'pawn']
    ]
    action = [
        ['show',8,0,[[10,0]]],['pause'],
        ['o-o',0],
        ['show',8,10,[]],['pause'],
        ['show',8,15,[[3,15]]],['pause'],
        ['o-o-o',15], ['pause']
    ]
    sovereign_video_interface(board,action,1.5,Get_text('tutorial_sovereign_11'),sov12)

def sov12(arg=...):
    help_tutorial()
    text = Get_text('tutorial_sovereign_12')
    board = [
        ['white',8,0,'king'], ['black',8,15,'king'],
        ['white',7,5,'pawn'], ['black',4,11,'pawn'],
        ['red',10,9,'pawn']
    ]
    action = [
        ['pause'],
        ['move',7,5,7,6],['change',7,6,'king'],['change',8,0,'empty'],
        ['pause'],['pause'],['pause'],['pause'],
        ['move',10,9,9,9],['change',9,9,'king'],['change',8,15,'empty'],
        ['pause'],['pause'],['pause'],['pause']
    ]
    sovereign_video_interface(board,action,0.5,text,sov13)

def sov13(arg=...):
    help_tutorial()
    text = Get_text('tutorial_sovereign_13')
    size = global_constants.Main_Window.size
    static_interface(size,text,do_sovereign_tutorial,1)

# end of sovereign tutorial









