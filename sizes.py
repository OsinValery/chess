from kivy.utils import platform
from kivy.core.window import Window
import global_constants


class Size():
    def __init__(self):
        s = [800,1400]
        if global_constants.game.test:
            if platform == 'macosx':
                Window.size = [s[0]//2,s[1]//2]
                self.window_size = s
            else:
                Window.size = s
                self.window_size = s
        else:
            self.window_size = Window.size
        global_constants.Sizes = self
    
    @property
    def board_size(self):
        if global_constants.game.window == 'game':
            return [self.window_size[0]*0.9]*2
        else:
            return [self.window_size[0]*.75]*2
    
    @property
    def virtual_board_size(self):
        return self.board_size
        if global_constants.game.type_of_chess == 'sovereign':
                return [900, 900]
        return [900, 900]



    @property
    def x_top(self):
        game = global_constants.game
        if game.type_of_chess == 'los_alamos':
            return self.board_size[0]//16
        if game.type_of_chess == 'sovereign':
            return self.virtual_board_size[0] / 65
        if game.type_of_chess == 'garner':
            return self.board_size[0]//12
        return self.board_size[0]//20
    
    @property
    def y_top(self):
        game = global_constants.game
        if game.type_of_chess == 'los_alamos':
            return self.board_size[0]//16
        if game.type_of_chess == 'sovereign':
            return self.virtual_board_size[0] / 63
        if game.type_of_chess == 'garner':
            return self.board_size[1]//12
        return self.board_size[1]//20
    
    @property
    def field_size(self):
        game = global_constants.game
        if game.type_of_chess == 'los_alamos':
            return (self.board_size[0]-2*self.x_top)//6
        if game.type_of_chess == 'sovereign':
            if global_constants.game.window != 'game':
                return (self.board_size[0]-2/65*self.board_size[0]) / 16
            return (self.virtual_board_size[0] -2 * self.x_top) / 16
        if game.type_of_chess == 'garner':
            return (self.board_size[0]-2*self.x_top)//5
        return (self.board_size[0]-2*self.x_top)//8
    
    @property
    def x_top_board(self):
        if global_constants.game.window == 'game':
            return 0.05 * self.window_size[0]
        else:
            return .1 * self.window_size[0]
    
    @property
    def y_top_board(self):
        if global_constants.game.window == 'game':
            return .3 * self.window_size[1]
        else:
            return .2 * self.window_size[1]
    
    @property
    def r_min(self):
        return .19 * self.board_size[0]
    
    @property
    def r(self):
        return .0780 * self.board_size[0]
    
    @property
    def r_max(self):
        return self.r * 4 + self.r_min

    @property
    def center(self):
        return [
            self.x_top_board + .5 * self.board_size[0],
            self.y_top_board + .5 * self.board_size[0]
        ]
    
    @property
    def field_len(self):
        return self.board_size[0] / 17

    @property
    def field_h(self):
        return self.board_size[1] / 11










