from kivy.uix.widget import Widget
from kivy.graphics import Rectangle

from settings import Settings
import global_constants

# Figures
import help_chess
import figure_alamos
import garner_figure
import glin_figure
import kuej_figure
import circle_figure
import garner_figure
import horde_figure
import bad_figure
import rasing_figure
import frozen_figure
import legan_figure

Figure = None

# Start position
import classic
import fisher
import horse_battle
import los_alamos
import gen_glinskiy
import gen_kuej
import gen_horde
import week
import bad_help
import schatranj
import frozen
import legan_chess

#Chess types
import circle_chess
import garner
import rasing


class Field():
    def __init__(self,x,y,tip,color):
        global Figure
        self.attacked = False
        self.figure = Figure(color,x,y,tip)


class Static_picture(Widget):
    def __init__(self,size,game,position=[],options=[]):
        """ 
        position - list of [ figure, x, y, color ]\n
        options is [ 'start' ]
        """
        self.size = size
        self.type_of_chess = game.type_of_chess
        super(Static_picture,self).__init__()
        self.app_size = global_constants.Sizes
        self.options = options
        self.position = position
        self.create_interface()

    def create_interface(self):
        global Figure
        self.canvas.add(Rectangle(
            size = self.app_size.board_size,
            pos = [self.app_size.x_top_board,self.app_size.y_top_board],
            source = Settings.get_board_picture(self.type_of_chess)
        ))

        standart = [
            'classic','fisher','horse_battle','magik',
            'permutation','week','kamikadze','haotic',
            'schatranj','dark_chess','nuclear'
            ]
        if self.type_of_chess in standart:
            help_chess.get_widget(self,self.app_size)
            Figure = help_chess.Figure   
            if 'start' in self.options:
                if self.type_of_chess in [
                    'classic', 'magik', 'permutation', 
                    'kamikadze','haotic','dark_chess',
                    'nuclear',
                        ]:
                    classic.create_start_game_board()
                elif self.type_of_chess == 'fisher':
                    fisher.create_start_game_board()
                elif self.type_of_chess == 'week':
                    week.create_start_game_board()
                elif self.type_of_chess == 'schatranj':
                    schatranj.create_start_game_board()
                else:
                    horse_battle.create_start_game_board()

        elif self.type_of_chess == 'los_alamos':
            figure_alamos.get_widget(self,self.app_size)
            Figure = figure_alamos.Figure
            if 'start' in self.options:
                los_alamos.create_start_game_board()

        elif self.type_of_chess == 'glinskiy':
            glin_figure.get_widget(self,self.app_size)
            Figure = glin_figure.Figure
            if 'start' in self.options:
                gen_glinskiy.create_start_game_board()

        elif self.type_of_chess == 'kuej':
            kuej_figure.get_widget(self,self.app_size)
            Figure = glin_figure.Figure
            if 'start' in self.options:
                gen_kuej.create_start_game_board()

        elif self.type_of_chess in ['circle_chess','bizantion']:
            circle_figure.get_widget(self,self.app_size)
            Figure = circle_figure.Figure
            if 'start' in self.options:
                circle_chess.create_round_board()

        elif self.type_of_chess == 'garner':
            garner_figure.get_widget(self,self.app_size)
            Figure = garner_figure.Figure
            if 'start' in self.options:
                garner.create_start_game_board()
            
        elif self.type_of_chess == 'horde':
            horde_figure.get_widget(self,self.app_size)
            Figure = horde_figure.Figure
            if 'start' in self.options:
                gen_horde.create_start_game_board()
        elif self.type_of_chess == 'bad_chess':
            bad_figure.get_widget(self,self.app_size)
            Figure = bad_figure.Figure
            if 'start' in self.options:
                bad_help.create_start_game_board()
        elif self.type_of_chess == 'rasing':
            rasing_figure.get_widget(self,self.app_size)
            Figure = rasing_figure.Figure
            if 'start' in self.options:
                rasing.get_start_position()
        elif self.type_of_chess == 'frozen':
            frozen_figure.get_widget(self,self.app_size)
            Figure = frozen_figure.Figure
            if 'start' in self.options:
                frozen.create_start_game_board()
        elif self.type_of_chess == 'legan':
            legan_figure.get_widget(self,self.app_size)
            Figure = legan_figure.Figure
            if 'start' in self.options:
                legan_chess.create_start_game_board()

            
        


        for el in self.position:
            # format is [ figure's type, x, y, color ]
            x = el[1]
            y = el[2]
            color = el[3]
            tip = el[0]
            fig = Figure(color,x,y,tip)

    def __del__(self):
        self.canvas.clear()
        self.clear_widgets()




