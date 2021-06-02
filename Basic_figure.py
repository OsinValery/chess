from kivy.graphics import Rectangle
import settings 
import os

folder = ''
main_widget = None
size = None
d = os.path.sep

def get_widget(widget,size_app):
    global main_widget,size,folder
    size = size_app 
    main_widget = widget
    path = settings.Settings.get_folder()
    f_set = settings.Settings.get_fig_set()
    folder =  path + f'pictures{d}{f_set}{d}'


class Figure():
    board_size = [8,8]

    def __init__(self,color,x,y,fig_type):
        self.color = color
        self.type = fig_type
        self.x = 0
        self.y = 0
        if fig_type == 'pawn':
            self.do_hod_now = False
        self.do_hod_before = False
        # some time i create empty figure named chose_figure
        if self.type != 'empty' and fig_type != '':
            name = fig_type[0] + color[0] + '.png'
            self.rect = Rectangle(source=folder+name,size=[size.field_size]*2)
            main_widget.canvas.add(self.rect)
            self.set_coords_on_board(x,y)

    def set_coords_on_board(self,x,y):
        self.x = x
        self.y = y
        pos_x = x * size.field_size + size.x_top + size.x_top_board
        pos_y = y * size.field_size + size.y_top + size.y_top_board
        self.rect.pos = (pos_x, pos_y)

    def first_list(self,board):
        my_hod = []
        x , y = self.x , self.y
        max_x, max_y = self.board_size
        if self.type == 'horse':
            if x - 2 >= 0 :
                if y + 1 < max_y and self.color != board[x-2][y+1].figure.color :
                    my_hod.append([x-2,y+1])
                if y - 1 >= 0 and self.color != board[x-2][y-1].figure.color :
                    my_hod.append([x-2,y-1])
            if x + 2 < max_x :
                if y + 1 < max_y and self.color != board[x+2][y+1].figure.color :
                    my_hod.append([x+2,y+1])
                if y - 1 >=0 and self.color != board[x+2][y-1].figure.color :
                    my_hod.append([x+2,y-1])
            if y + 2 < max_y:
                if x + 1 < max_x and self.color != board[x+1][y+2].figure.color :
                    my_hod.append([x+1,y+2])
                if x - 1 >=0 and self.color != board[x-1][y+2].figure.color :
                    my_hod.append([x-1,y+2])
            if y - 2 >=0 :
                if x + 1 < max_x and self.color != board[x+1][y-2].figure.color :
                    my_hod.append([x+1,y-2])
                if x - 1 >= 0 and self.color != board[x-1][y-2].figure.color :
                    my_hod.append([x-1,y-2])
        elif self.type == 'rook' :
            a = 1
            while x + a < max_x and board[x+a][y].figure.type == 'empty':
                my_hod.append([x+a,y])
                a += 1
            if x + a < max_x and board[x+a][y].figure.color != self.color :
                my_hod.append([x+a,y])
            a = -1
            while x + a > -1 and board[x+a][y].figure.type == 'empty':
                my_hod.append([x+a,y])
                a -= 1
            if x + a > -1 and board[x+a][y].figure.color != self.color :
                my_hod.append([x+a,y])

            a = 1
            while y + a < max_y and board[x][y+a].figure.type == 'empty' :
                my_hod.append([x,y+a])
                a += 1
            if y + a < max_y and board[x][y+a].figure.color != self.color:
                my_hod.append([x,y+a])
            a = -1
            while y + a > -1 and board[x][y+a].figure.type == 'empty' :
                my_hod.append([x,y+a])
                a -= 1
            if y + a > -1 and board[x][y+a].figure.color != self.color:
                my_hod.append([x,y+a])
        elif self.type == 'pawn':
            if self.color == 'white':
                if board[x][y+1].figure.type == 'empty':
                    my_hod.append([x,y+1])
                    if y == 1 and board[x][y+2].figure.type == 'empty':
                        my_hod.append([x,y+2])
                if x != 0 and board[x-1][y+1].figure.color =='black':
                    my_hod.append([x-1,y+1])
                if x != 0 and board[x-1][y].figure.type == 'pawn' :
                    if board[x-1][y].figure.do_hod_now and board[x-1][y].figure.color != self.color:
                        my_hod.append([x-1,y+1])
                if x != max_x - 1 and board[x+1][y+1].figure.color == 'black':
                    my_hod.append([x+1,y+1])
                if x != max_x - 1 and board[x+1][y].figure.type == 'pawn' :
                    if board[x+1][y].figure.do_hod_now and board[x+1][y].figure.color != self.color:
                        my_hod.append([x+1,y+1])
            else:
                if board[x][y-1].figure.type == 'empty':
                    my_hod.append([x,y-1])
                    if y == max_y - 2 and board[x][y-2].figure.type == 'empty':
                        my_hod.append([x,y-2])
                if x!=0 and board[x-1][y-1].figure.color =='white':
                    my_hod.append([x-1,y-1])
                if x != 0 and board[x-1][y].figure.type == 'pawn' :
                    if board[x-1][y].figure.do_hod_now and board[x-1][y].figure.color != self.color:
                        my_hod.append([x-1,y-1])
                if x != max_x - 1 and board[x+1][y-1].figure.color == 'white':
                    my_hod.append([x+1,y-1])
                if x != max_x - 1 and board[x+1][y].figure.type == 'pawn' :
                    if board[x+1][y].figure.do_hod_now and board[x+1][y].figure.color != self.color:
                        my_hod.append([x+1,y-1])
        elif self.type == 'king':
            if y + 1 != max_y :
                if x + 1 < max_x and board[x+1][y+1].figure.color != self.color:
                    my_hod.append([x+1,y+1])
                if board[x][y+1].figure.color != self.color :
                    my_hod.append([x,y+1])
                if x - 1 >=0 and board[x-1][y+1].figure.color != self.color:
                    my_hod.append([x-1,y+1])
            if y  != 0 :
                if x + 1 < max_x and board[x+1][y-1].figure.color != self.color:
                    my_hod.append([x+1,y-1])
                if board[x][y-1].figure.color != self.color :
                    my_hod.append([x,y-1])
                if x - 1 >=0 and board[x-1][y-1].figure.color != self.color:
                    my_hod.append([x-1,y-1])
            if x + 1 < max_x and board[x+1][y].figure.color != self.color :
                my_hod.append([x+1,y])
            if x  > 0 and board[x-1][y].figure.color != self.color :
                my_hod.append([x-1,y])
        elif self.type == 'bishop':
            # xxv
            # xvx
            # xxx
            a = 1
            while x + a < max_x and y + a < max_y and board[x+a][y+a].figure.type == 'empty':
                my_hod.append([x+a,y+a])
                a+=1
            if x + a < max_x and y + a < max_y and board[a+x][y+a].figure.color != self.color:
                my_hod.append([x+a,y+a])
            # xxx
            # xvx
            # xxv
            a = 1
            while x + a < max_x and y - a > -1 and board[x+a][y-a].figure.type == 'empty':
                my_hod.append([x+a,y-a])
                a+=1
            if x + a < max_x and y - a > -1 and board[a+x][y-a].figure.color != self.color:
                my_hod.append([x+a,y-a])
            # xxx
            # xvx
            # vxx
            a = 1
            while x - a > -1 and y - a > -1 and board[x-a][y-a].figure.type == 'empty':
                my_hod.append([x-a,y-a])
                a +=1
            if x - a > -1 and y - a > -1 and board[x-a][y-a].figure.color != self.color:
                my_hod.append([x-a,y-a])
            # vxx
            # xvx
            # xxx
            a = 1
            while x - a > -1 and y + a < max_y and board[x-a][y+a].figure.type == 'empty':
                my_hod.append([x-a,y+a])
                a += 1
            if x - a > -1 and y + a < max_y and board[x-a][y+a].figure.color != self.color:
                my_hod.append([x-a,y+a])
        elif self.type == 'queen':
            a = 1
            while x + a < max_x and board[x+a][y].figure.type == 'empty':
                my_hod.append([x+a,y])
                a += 1
            if x + a < max_x and board[x+a][y].figure.color != self.color :
                my_hod.append([x+a,y])
            a = -1
            while x + a > -1 and board[x+a][y].figure.type == 'empty':
                my_hod.append([x+a,y])
                a -= 1
            if x + a > -1 and board[x+a][y].figure.color != self.color :
                my_hod.append([x+a,y])
            a = 1
            while y + a < max_y and board[x][y+a].figure.type == 'empty' :
                my_hod.append([x,y+a])
                a += 1
            if y + a < max_y and board[x][y+a].figure.color != self.color:
                my_hod.append([x,y+a])
            a = -1
            while y + a > -1 and board[x][y+a].figure.type == 'empty' :
                my_hod.append([x,y+a])
                a -= 1
            if y + a > -1 and board[x][y+a].figure.color != self.color:
                my_hod.append([x,y+a])
            a = 1
            while x + a < max_x and y + a < max_y and board[x+a][y+a].figure.type == 'empty':
                my_hod.append([x+a,y+a])
                a+=1
            if x + a < max_x and y + a < max_y and board[a+x][y+a].figure.color != self.color:
                my_hod.append([x+a,y+a])
            a = 1
            while x + a < max_x and y - a > -1 and board[x+a][y-a].figure.type == 'empty':
                my_hod.append([x+a,y-a])
                a+=1
            if x + a < max_x and y - a > -1 and board[a+x][y-a].figure.color != self.color:
                my_hod.append([x+a,y-a])
            a = 1
            while x - a > -1 and y - a > -1 and board[x-a][y-a].figure.type == 'empty':
                my_hod.append([x-a,y-a])
                a +=1
            if x - a > -1 and y - a > -1 and board[a-x][y-a].figure.color != self.color:
                my_hod.append([x-a,y-a])
            a = 1
            while x - a > -1 and y + a < max_y and board[x-a][y+a].figure.type == 'empty':
                my_hod.append([x-a,y+a])
                a += 1
            if x - a > -1 and y + a < max_y and board[a-x][y+a].figure.color != self.color:
                my_hod.append([x-a,y+a])

        return my_hod

    def do_attack(self,board):
        x,y = self.x, self.y
        if self.type == 'pawn':
            if self.color == 'white':
                if x != self.board_size[0] - 1 and y != self.board_size[1] - 1:
                    board[x+1][y+1].attacked = True
                if x != 0 and y != self.board_size[1] - 1:
                    board[x-1][y+1].attacked = True
            else:
                if x != self.board_size[0] - 1 and y != 0:
                    board[x+1][y-1].attacked = True
                if x != 0 and y != 0:
                    board[x-1][y-1].attacked = True
        else:
            list_attack = self.first_list(board)
            for element in list_attack:
                x,y = element[0],element[1]
                board[x][y].attacked = True

        return board

    def __str__(self):
        return f'{self.color} {self.type} on [{self.x}, {self.y}]'

    def destroy(self):
        if self.type != 'empty':
            main_widget.canvas.remove(self.rect)
            del self.rect
        self.type = 'empty'
        self.color = ''
        self.color = ''

    def pawn_on_last_line(self):
        if self.color == 'white' and self.y + 1 == self.board_size[1]:
            return True
        elif self.color == 'black' and self.y == 0:
            return True
        else:
            return False

    def transform_to(self,fig_type):
        if self.type == 'pawn':
            del self.do_hod_now
        self.type = fig_type
        self.rect.source = folder + fig_type[0] + self.color[0] + '.png'
        if fig_type == 'pawn':
            self.do_hod_now = False

    @property
    def save_data(self):
        data = f'{self.x} {self.y} {self.type} {self.color} '
        if 'do_hod_before' in dir(self):
            res = 'y' if self.do_hod_before else 'n'
            data += f'{res} '
        else:
            data += 'e '
        if 'do_hod_now' in dir(self):
            res = 'y' if self.do_hod_now else 'n' 
            data += f'{res} '
        else:
            data += 'e '
        return data + '\n'

    def from_saves(self,data):
        info = data.split()
        x, y, self.type = info[:3]
        self.x, self.y = int(x), int(y)
        if self.type != 'empty':
            self.color = info[3]
            info = info[1:]
        info = info[3:]
        if info[0] == 'n':
            self.do_hod_before = False
        if info[0] == 'y':
            self.do_hod_before = False
        if info[1] == 'y':
            self.do_hod_now = True
        if info[1] == 'n':
            self.do_hod_now = False
        # third possible variant is "e"
        if self.type != 'empty' :
            fig_type = self.type
            name = fig_type[0] + self.color[0] + '.png'
            self.rect = Rectangle(source=folder+name,size=[size.field_size]*2)
            main_widget.canvas.add(self.rect)
            self.set_coords_on_board(self.x,self.y)



