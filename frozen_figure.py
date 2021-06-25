from kivy.graphics import Rectangle
import os
import Basic_figure
import global_constants


def get_folder():
    path = global_constants.Settings.get_folder()
    f_set = global_constants.Settings.get_fig_set()
    return  os.path.join(path,'pictures',f_set) + os.sep


class Figure(Basic_figure.Figure):
    def __init__(self, color, x, y, fig_type):
        self.color = color
        self.type = fig_type
        self.x = x
        self.y = y
        if fig_type == 'pawn':
            self.do_hod_now = False
        self.do_hod_before = False
        # some time i create empty figure named chose_figure
        if self.type == 'frozen':
            path = global_constants.Settings.get_folder()
            file = os.path.join(path,'pictures','ice.png')
            self.rect = Rectangle(
                source = file,
                size=[global_constants.Sizes.field_size]*2
            )
            global_constants.current_figure_canvas.add(self.rect)
            self.set_coords_on_board(x,y)
        elif self.type != 'empty' and fig_type != '':
            name = fig_type[0] + color[0] + '.png'
            Sizes = global_constants.Sizes
            folder = get_folder()
            self.rect = Rectangle(source=folder+name,size=[Sizes.field_size]*2)
            global_constants.current_figure_canvas.add(self.rect)
            self.set_coords_on_board(x,y)

    def freeze(self):
        if self.type == 'pawn':
            del self.do_hod_now
        self.type = 'frozen'
        self.color = ''
        path = global_constants.Settings.get_folder()
        file = os.path.join(path,'pictures','ice.png')
        self.rect = Rectangle(
            source = file,
            size=[global_constants.Sizes.field_size]*2
        )
        global_constants.current_figure_canvas.add(self.rect)
        self.set_coords_on_board(self.x, self.y)
    
    def destroy(self):
        if self.type != 'empty':
            global_constants.current_figure_canvas.remove(self.rect)
            del self.rect
        self.type = 'empty'
        self.color = ''

    def first_list(self, board):
        if self.type == 'pawn':
            return get_pawn_moves(self,board)
        return super().first_list(board)
    


def get_pawn_moves(figure:Figure,board):
    x,y = figure.x, figure.y
    my_hod = []
    max_x, max_y = figure.board_size
    if figure.color == 'white':
        if board[x][y+1].figure.type == 'empty':
            my_hod.append([x,y+1])
            if y == 1 and board[x][y+2].figure.type == 'empty':
                my_hod.append([x,y+2])
        if x != 0 and (board[x-1][y+1].figure.color =='black' or board[x-1][y+1].figure.type == 'frozen'):
            my_hod.append([x-1,y+1])
        if x != 0 and board[x-1][y].figure.type == 'pawn' :
            if board[x-1][y].figure.do_hod_now and board[x-1][y].figure.color != figure.color:
                my_hod.append([x-1,y+1])
        if x != max_x - 1 and \
            (board[x+1][y+1].figure.color == 'black' or board[x+1][y+1].figure.type == 'frozen'):
                my_hod.append([x+1,y+1])
        if x != max_x - 1 and board[x+1][y].figure.type == 'pawn' :
            if board[x+1][y].figure.do_hod_now and board[x+1][y].figure.color != figure.color:
                my_hod.append([x+1,y+1])
    else:
        if board[x][y-1].figure.type == 'empty':
            my_hod.append([x,y-1])
            if y == max_y - 2 and board[x][y-2].figure.type == 'empty':
                my_hod.append([x,y-2])
        if x!=0 and (board[x-1][y-1].figure.color =='white' or board[x-1][y-1].figure.type == 'frozen'):
            my_hod.append([x-1,y-1])
        if x != 0 and board[x-1][y].figure.type == 'pawn' :
            if board[x-1][y].figure.do_hod_now and board[x-1][y].figure.color != figure.color:
                my_hod.append([x-1,y-1])
        if x != max_x - 1 and \
            (board[x+1][y-1].figure.color == 'white' or board[x+1][y-1].figure.type == 'frozen'):
                my_hod.append([x+1,y-1])
        if x != max_x - 1 and board[x+1][y].figure.type == 'pawn' :
            if board[x+1][y].figure.do_hod_now and board[x+1][y].figure.color != figure.color:
                my_hod.append([x+1,y-1])

    return my_hod

