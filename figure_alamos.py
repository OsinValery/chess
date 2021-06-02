import os
from kivy.graphics import Rectangle
from settings import Settings
import Basic_figure


def get_widget(widget,size_app):
    global main_widget,size,folder
    Basic_figure.get_widget(widget,size_app)
    size = size_app 
    main_widget = widget
    path = Settings.get_folder()
    d = os.sep
    f_set = Settings.get_fig_set()
    folder =  path + f'pictures{d}{f_set}{d}'


class Figure(Basic_figure.Figure):
    board_size = [6,6]
    def __init__(self,col,x,y,fig_type):
        super(Figure,self).__init__(col,x,y,fig_type)
        del self.do_hod_before
        if 'do_hod_now' in dir(self):
            del self.do_hod_now
        
    def first_list(self,board):
        if self.type in ['horse','king','rook','queen']:
            return super(Figure,self).first_list(board)
        my_hod = []
        x , y = self.x , self.y
        max_x = self.board_size[0] - 1
        max_x = self.board_size[1] - 1     
        # logic of pawn   
        if self.color == 'white':
            if board[x][y+1].figure.type == 'empty':
                my_hod.append([x,y+1])
            if x != 0 and board[x-1][y+1].figure.color =='black':
                my_hod.append([x-1,y+1])
            if x != max_x and board[x+1][y+1].figure.color == 'black':
                my_hod.append([x+1,y+1])
        else:
            if board[x][y-1].figure.type == 'empty':
                my_hod.append([x,y-1])
            if x!=0 and board[x-1][y-1].figure.color =='white':
                my_hod.append([x-1,y-1])
            if x != max_x and board[x+1][y-1].figure.color == 'white':
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
            self.rect = Rectangle(source=folder+name,size=[size.field_size]*2)
            main_widget.canvas.add(self.rect)
            self.set_coords_on_board(self.x,self.y)


