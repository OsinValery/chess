from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Line, Color, Ellipse
from copy import deepcopy as copy

import global_constants
from sovereign_figure import Figure


class VideoChess(Widget):
    def __init__(self, board, speed=1, actions=[], **kwargs):
        super().__init__(**kwargs)
        self.timer = Clock.schedule_interval(self.next, speed)
        self.actions = actions
        self.actions.append(['start'])
        self.start_pos = [[['', 0, 0, 'empty']
                           for y in range(16)] for x in range(16)]
        """ color, x, y, type """
        for figure in board:
            x, y = figure[1:3]
            self.start_pos[x][y] = figure
        self.cur_pos = copy(self.start_pos)
        global_constants.current_figure_canvas = self.canvas
        self.move = 0
        self.effects = []
        self.must = True
        self.draw()

    def __del__(self):
        self.timer.cancel()
        self.canvas.clear()

    def remove(self):
        try:
            self.timer.cancel()
        except:
            pass
        del self

    def next(self, time):
        if not self.must:
            self.timer.cancel()
            return
        if self.actions[self.move][0] == 'start':
            self.move = -1
            self.cur_pos = copy(self.start_pos)
        elif self.actions[self.move][0] == 'move':
            x, y, a, b = self.actions[self.move][1:5]
            self.cur_pos[x][y][1:3] = [a, b]
            self.cur_pos[a][b][1:3] = [x, y]
            self.cur_pos[x][y], self.cur_pos[a][b] = self.cur_pos[a][b], self.cur_pos[x][y]
        elif self.actions[self.move][0] == 'change':
            x, y, fig = self.actions[self.move][1:]
            self.cur_pos[x][y][3] = fig
        elif self.actions[self.move][0] == 'take':
            x, y, a, b = self.actions[self.move][1:5]
            if self.cur_pos[a][b][3] == 'empty':
                if self.cur_pos[x][y][3] == 'pawn':
                    self.cur_pos[a][y] = ['', 0, 0, 'empty']
                    self.cur_pos[a][b], self.cur_pos[x][y] = self.cur_pos[x][y], self.cur_pos[a][b]
                    self.cur_pos[a][b][1:3] = [a, b]
            else:
                self.cur_pos[a][b] = copy(self.cur_pos[x][y])
                self.cur_pos[a][b][1:3] = [a, b]
                self.cur_pos[x][y] = ['', 0, 0, 'empty']

        elif self.actions[self.move][0] == 'show':
            # all moves
            x, y, fields = self.actions[self.move][1:]
            self.effects = []
            s = global_constants.Sizes
            pos = [s.x_top_board + s.x_top, s.y_top_board + s.y_top]
            points = [
                [pos[0] + x*s.field_size, pos[1] + y*s.field_size],
                [pos[0] + (x+1)*s.field_size, pos[1] + y*s.field_size],
                [pos[0] + (x+1)*s.field_size, pos[1] + (y+1)*s.field_size],
                [pos[0] + x*s.field_size, pos[1] + (y+1)*s.field_size],
            ]
            self.effects.append([0.1, 1, 0.1, 1])
            self.effects += [Line(points=points, width=3, close=True)]
            r = 10
            for x, y in fields:
                self.effects.append(Ellipse(
                    pos=[pos[0] - r/2 + (x+0.5)*s.field_size,
                         pos[1] - r/2 + (y+0.5)*s.field_size],
                    size=[r, r]
                ))

        elif self.actions[self.move][0] == 'show_attack':
            x, y, a, b = self.actions[self.move][1:5]
            self.effects.append([1, 0, 0, 1])
            s = global_constants.Sizes
            pos = [s.x_top_board + s.x_top, s.y_top_board + s.y_top]
            points = [
                [pos[0]+(x+0.5)*s.field_size, pos[1]+s.field_size*(y+0.5)],
                [pos[0]+(a+0.5)*s.field_size, pos[1]+(b+0.5)*s.field_size]
            ]
            self.effects.append(Line(
                points=points,
                cap='round',
                width=3
            ))
        elif self.actions[self.move][0] == 'o-o':
            y = self.actions[self.move][1]
            self.cur_pos[8][y][1] = 10
            self.cur_pos[8][y], self.cur_pos[10][y] = self.cur_pos[10][y], self.cur_pos[8][y]
            self.cur_pos[11][y][1] = 9
            self.cur_pos[11][y], self.cur_pos[9][y] = self.cur_pos[9][y], self.cur_pos[11][y]
        elif self.actions[self.move][0] == 'o-o-o':
            y = self.actions[self.move][1]
            self.cur_pos[8][y], self.cur_pos[3][y] = self.cur_pos[3][y], self.cur_pos[8][y]
            self.cur_pos[2][y], self.cur_pos[4][y] = self.cur_pos[4][y], self.cur_pos[2][y]
            self.cur_pos[4][y][1] = 4
            self.cur_pos[3][y][1] = 3
        elif self.actions[self.move][0] == 'change_color':
            x, y, color = self.actions[self.move][1:]
            self.cur_pos[x][y][0] = color

        if self.actions[self.move][0] != 'pause':
            self.draw()
        self.move += 1

    def draw(self):
        if not self.must:
            return
        self.canvas.clear()
        sizes = global_constants.Sizes
        with self.canvas:
            Rectangle(
                source=global_constants.Settings.get_board_picture(
                    'sovereign'),
                pos=[sizes.x_top_board, sizes.y_top_board],
                size=sizes.board_size
            )

        for line in self.cur_pos:
            for fig in line:
                if fig[-1] != 'empty':
                    figure = Figure(*fig)
        figure = None

        if len(self.effects) != 0:
            with self.canvas:
                Color(*self.effects[0])
            for el in self.effects[1:]:
                self.canvas.add(el)
            self.effects = []
            with self.canvas:
                Color(1, 1, 1, 1)
