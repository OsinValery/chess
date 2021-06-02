import os
import Basic_figure
import settings

def get_widget(widget,size_app):
    global folder
    path = settings.Settings.get_folder()
    d = os.path.sep
    fig = settings.Settings.get_fig_set()
    folder = path + f'pictures{d}{fig}{d}'
    Basic_figure.get_widget(widget,size_app)
    

class Figure(Basic_figure.Figure):
    board_size = [8,8]
    def swap(self):
        if self.type in [ 'pawn', 'king' , 'empty'] :
            return
        if self.type == 'horse':
            tip = 'bishop'
        elif self.type == 'bishop':
            tip = 'rook'
        elif self.type == 'rook':
            tip = 'queen'
        else:
            tip = 'horse'
        self.type = tip
        name = tip[0] + self.color[0] + '.png'
        self.rect.source = folder + name


