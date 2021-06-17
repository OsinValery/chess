import os
import datetime

from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.graphics import Rectangle, RoundedRectangle, Color, Line

from settings import Settings
from translater import Get_text
from change_widget import Chess_type
import global_constants

"""
in this module collected all the logik of game saves
this module opens it or  removes
"""


def sorted(object):
    def nomber(file):
        return int(file[4:])

    for i in range(len(object)):
        for x in range(len(object)-1-i):
            if nomber(object[x]) < nomber(object[x+1]):
                object[x], object[x+1] = object[x+1], object[x]
    return object


class Saved_games(ScrollView):
    def __init__(self, size, pos):
        super(Saved_games, self).__init__()
        self.size = size
        self.pos = pos
        self.do_scroll = [False, True]
        global_constants.game.window = 'saved'

        folder = Settings.user_folder
        files = sorted(os.listdir(os.path.join(folder, 'Saves')))
        height = 105 * len(files) + 100
        grid = GridLayout(
            cols=1,
            size=[self.size[0], height],
            size_hint=[None, None],
            spacing=[0, 5]
        )
        self.add_widget(grid)

        def remove_save(click):
            file = click.parent.file
            create_remove(Window.size, os.path.join(folder, 'Saves', file))

        def create_game(click):
            file = click.parent.file
            create_start(Window.size, os.path.join(folder, 'Saves', file))

        for name in files:
            grid2 = GridLayout(
                cols=2,
                size_hint_y=None
            )
            grid.add_widget(grid2)
            grid2.file = name

            grid2.add_widget(Button(
                text=name,
                size_hint=[.9, None],
                background_color=[.5, .5, 0, .5],
                background_normal='',
                color=[1, 0, 0, 1],
                on_press=create_game
            ))
            grid2.add_widget(Button(
                text='x',
                size_hint=[.2, None],
                background_color=[.9, .1, 0, .5],
                background_normal='',
                on_press=remove_save
            ))


def create_remove(size, file_path):
    wid = global_constants.Main_Window
    wid.clear_widgets()
    wid.canvas.clear()
    path = os.path.join(Settings.get_folder(), 'pictures', 'delete_game.png')
    wid.canvas.add(Rectangle(size=size, source=path))
    grid = GridLayout(
        rows=1,
        pos=[.1 * size[0], .05*size[1]],
        size=[.8*size[0], .1 * size[1]]
    )

    def back(click=None):
        wid.to_saves(1)

    def remove(click=None):
        os.remove(file_path)
        wid.to_saves(1)

    grid.add_widget(Button(
        text=Get_text('all_back'),
        color=[1, 1, 0, 1],
        background_color=[0, 1, 0, .7],
        on_press=back
    ))
    grid.add_widget(Button(
        text=Get_text('bace_remove'),
        background_color=[1, 0, 0, .5],
        color=[0, 1, 0, 1],
        on_press=remove
    ))
    wid.add_widget(grid)
    wid.add_widget(Interface(
        path=file_path,
        size=[.55 * size[0], .4 * size[1]],
        pos=[.45*size[0], .15*size[1]]
    ))


def create_start(size, file_path):
    wid = global_constants.Main_Window
    wid.clear_widgets()
    wid.canvas.clear()
    wid.canvas.add(Rectangle(source=Settings.get_bace_picture(), size=size))

    grid = GridLayout(
        rows=1,
        pos=[.1 * size[0], .05*size[1]],
        size=[.8*size[0], .1 * size[1]]
    )

    def back(click=None):
        wid.to_saves(1)

    def start(click=None):
        file = open(file_path, mode='r')
        data = file.readlines()
        file.close()
        data2 = []
        for el in data:
            data2.append(el[:-1])
        global_constants.game.from_saves(data2)

    grid.add_widget(Button(
        text=Get_text('all_back'),
        color=[1, 1, 0, 1],
        background_color=[1, 0, 0, .7],
        on_press=back
    ))
    grid.add_widget(Button(
        text=Get_text('all_start'),
        background_color=[0, 1, 0, .5],
        color=[1, 1, 0, .7],
        on_press=start
    ))

    wid.add_widget(grid)
    wid.add_widget(Interface(
        path=file_path,
        size=[.65 * size[0], .4 * size[1]],
        pos=[.15*size[0], .15*size[1]]
    ))


class Interface(Widget):
    def __init__(self, path, size, pos):
        self.size = size
        self.pos = pos
        super(Interface, self).__init__()
        with self.canvas:
            Color(.2, .8, 0, .4)
            RoundedRectangle(
                pos=pos,
                size=size,
                radius=[(30, 30), (30, 30), (30, 30), (30, 30)]
            )
            Color(1, 0, 0, .5)
            Line(
                rounded_rectangle=(*pos, *size, *[30]*4, 100),
                width=3
            )
        with open(path) as file:
            data = file.readlines()
            data = [line[:-1] for line in data]
        texts = [
            [Get_text('interface_file'),       os.path.split(path)[-1]],
            [Get_text('interface_mode'),       Chess_type(data[0]).text],
            [Get_text('interface_saved'),      creation_date(path)],
            [Get_text('interface_playtime'),   'time'],
            [Get_text('interface_cur_move'),   str(1+int(data[3].split()[0]))],
            [Get_text('interface_color_move'), 'moves']
        ]
        # time in game
        cur_time = data[1].split()[1:3]
        cur_str = f'{time_convert(int(cur_time[0]))} / {time_convert(int(cur_time[1]))}'
        texts[3][1] = cur_str
        # color of move
        color = data[3].split()[2]
        texts[5][1] = Get_text(f'change_{color}')

        n = len(texts)
        # color of text(1) and of line(2)
        colors = [[1, 1, 0, 1]]*n
        colors2 = [[1, 0, 1, 1], [0, 0, 1, 1], [0, 0, 1, 1],
                   [1, .5, 0, 1], [0, 0, 1, 1], [1, 0, 0, 1]]

        content_size = [x, y] = [.9, .8]
        texts = texts[::-1]
        for i in range(len(texts)):
            self.add_widget(TextLine(
                size=[size[0] * x, y * size[1] / n],
                pos=[pos[0] + (1-x)/2 * size[0], pos[1] + i *
                     y * size[1] / n + (1-y)/2 * size[1]],
                texts=texts[i],
                color=colors[i],
                line_color=colors2[i]
            ))


class TextLine(Widget):
    def __init__(self, size, pos, texts, color, line_color):
        super(TextLine, self).__init__()
        self.size = size
        self.pos = pos

        lengths = [0, 0]
        for i in 0, 1:
            cont = texts[i].split('\n')
            m = len(cont[0])
            for el in cont:
                if len(el) > m:
                    m = len(el)
            lengths[i] = m

        d = lengths[0] / sum(lengths)
        x = .05
        poses = [[pos[0]+x*size[0], pos[1]],
                 [pos[0]+size[0]*d-x*size[0], pos[1]]]
        sizes = [[size[0]*d, size[1]], [size[0]*(1-d), size[1]]]
        haligans = ['left', 'right']
        for i in 0, 1:
            self.add_widget(Label(
                text=texts[i],
                pos=poses[i],
                size=sizes[i],
                color=color,
                text_size=sizes[i],
                halign=haligans[i],
                valign='top'
            ))
        line_h = .1
        points = [
            pos[0] + x * size[0], pos[1] + line_h * size[1],
            pos[0] + (1-x) * size[0], pos[1] + line_h * size[1]
        ]
        with self.canvas:
            Color(*line_color)
            Line(
                width=2,
                points=points
            )


def time_convert(sec):
    if sec == -1:
        return '00:00'
    # returns time in format 'minutes:seconds'
    mins = sec//60
    sec = sec - 60 * mins
    a = str(mins)
    b = str(sec)
    if len(a) == 1:
        a = '0' + a
    if len(b) == 1:
        b = '0' + b
    return f'{a}:{b}'


def creation_date(path):
    sec = os.path.getmtime(path)
    time = datetime.datetime.fromtimestamp(sec)
    time = time.timetuple()
    return f'{time[2]}.{time[1]}.{time[0]%100} {time[3]}:{time[4]}'
