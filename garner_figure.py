import os
import Basic_figure
import settings
from kivy.graphics import Rectangle
import global_constants


def get_folder():
    path = settings.Settings.get_folder()
    f_set = settings.Settings.get_fig_set()
    d = os.sep
    return  path + f'pictures{d}{f_set}{d}'

    

class Figure(Basic_figure.Figure):
    board_size = [5,5]
    def __init__(self,col,x,y,fig_type):
        super(Figure,self).__init__(col,x,y,fig_type)
        del self.do_hod_before
        if self.type == 'pawn':
            del self.do_hod_now
    
    def first_list(self,board):
        if self.type == 'empty':
            return []
        if self.type != 'pawn':
            return super(Figure,self).first_list(board)
        x, y = self.x, self.y
        my_hod = []
        if self.color == 'white':
            if board[x][y+1].figure.type == 'empty':
                my_hod.append([x,y+1])
            if x != 0 and board[x-1][y+1].figure.color =='black':
                my_hod.append([x-1,y+1])
            if x != 4 and board[x+1][y+1].figure.color == 'black':
                my_hod.append([x+1,y+1])
        else:
            if board[x][y-1].figure.type == 'empty':
                my_hod.append([x,y-1])
            if x!=0 and board[x-1][y-1].figure.color =='white':
                my_hod.append([x-1,y-1])
            if x != 4 and board[x+1][y-1].figure.color == 'white':
                my_hod.append([x+1,y-1])
        return my_hod

    @property
    def save_data(self):
        return f'{self.x} {self.y} {self.type} {self.color}\n'

    def from_saves(self,data):
        info = data.split()
        x, y, self.type = info[:3]
        self.x, self.y = int(x), int(y)
        if self.type != 'empty':
            self.color = info[3]
            name = self.type[0] + self.color[0] + '.png'
            folder = get_folder()
            size = global_constants.Sizes
            self.rect = Rectangle(source=folder+name,size=[size.field_size]*2)
            global_constants.current_figure_canvas.add(self.rect)
            self.set_coords_on_board(self.x,self.y)


