import help_chess
import settings
import kivy.utils

if kivy.utils.platform == 'win':
    d = '\\'
else:
    d = '/'
folder = settings.Settings.get_folder() + \
    'pictures{0}{1}{0}'.format(d,settings.Settings.get_fig_set())

def get_widget(widget,size_app):
    global main_widget,size,folder
    size = size_app 
    main_widget = widget
    folder = settings.Settings.get_folder() +     \
                            'pictures{0}{1}{0}'.format(d,settings.Settings.get_fig_set())
    help_chess.get_widget(widget,size_app)


class Figure(help_chess.Figure):
    def first_list(self,board):
        if self.color == 'black' or self.type != 'pawn':
            return super(Figure,self).first_list(board)
        my_hod = []
        x , y = self.x , self.y
        # move of white pawn different with classic version
        # pawn may make double move from 1 and 2 lines (in logic 0 and 1)
        if self.color == 'white':
                if board[x][y+1].figure.type == 'empty':
                    my_hod.append([x,y+1])
                    if y < 2 and board[x][y+2].figure.type == 'empty':
                        my_hod.append([x,y+2])
                if x != 0 and board[x-1][y+1].figure.color =='black':
                    my_hod.append([x-1,y+1])
                if x != 0 and board[x-1][y].figure.type == 'pawn' :
                    if board[x-1][y].figure.do_hod_now and board[x-1][y].figure.color != self.color:
                        my_hod.append([x-1,y+1])
                if x != 7 and board[x+1][y+1].figure.color == 'black':
                    my_hod.append([x+1,y+1])
                if x != 7 and board[x+1][y].figure.type == 'pawn' :
                    if board[x+1][y].figure.do_hod_now and board[x+1][y].figure.color != self.color:
                        my_hod.append([x+1,y+1])
        return my_hod



