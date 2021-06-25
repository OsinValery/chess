from kivy.graphics import Rectangle
import settings
import os
import global_constants
import Basic_figure


def get_folder():
    path = settings.Settings.get_folder()
    fig = settings.Settings.get_fig_set()
    d = os.path.sep
    return  path + f'pictures{d}{fig}{d}'


class Figure(Basic_figure.Figure):
    def __init__(self,col,x,y,fig_type):
        self.color = col
        self.type = fig_type
        self.x = 0
        self.y = 0
        if fig_type == 'pawn':
            self.do_hod_now = False
        # some time i create empty figure named chose_figure
        if self.type != 'empty' and fig_type != '':
            name = fig_type[0] + col[0] + '.png'
            size = global_constants.Sizes
            folder = get_folder()
            self.rect = Rectangle(source=folder+name,size=[size.field_len]*2)
            global_constants.current_figure_canvas.add(self.rect)
            self.set_coords_on_board(x,y)
    
    def set_coords_on_board(self,x,y):
        self.x = x
        self.y = y
        size = global_constants.Sizes
        dy = (size.field_h - size.field_len) / 2
        self.rect.pos = ((.5 + 1.5 * x) * size.field_len +size.x_top_board,
            y * size.field_h + size.y_top_board + abs(5-x) * .5 * size.field_h + dy)
        
    def first_list(self,board):
        my_hod = []
        x , y = self.x , self.y
        if self.type == 'horse':
            my_hod = horse_move(board,x,y,self.color)
        elif self.type == 'rook' :
            my_hod = rook_move(board,x,y,self.color)
        elif self.type == 'pawn':
            my_hod = pawn_move(board,x,y,self.color)
        elif self.type == 'king':
            my_hod = king_move(board,x,y,self.color)
        elif self.type == 'bishop':
            my_hod = bishop_move(board,x,y,self.color)
        elif self.type == 'queen':
            my_hod = bishop_move(board,x,y,self.color) + rook_move(board,x,y,self.color)

        return my_hod
    
    def do_attack(self,board):
        x,y = self.x, self.y
        if self.type == 'pawn':
            if self.color == 'white':
                if x > 0:
                    if x <= 5:
                        board[x-1][y+1].attacked = True
                    else:
                        board[x-1][y+2].attacked = True
                if x < 10:
                    if x < 5:
                        board[x+1][y+2].attacked = True
                    else:
                        board[x+1][y+1].attacked = True
            else:
                if x > 0:
                    if x <= 5:
                        board[x-1][y-2].attacked = True
                    else:
                        board[x-1][y-1].attacked = True
                if x < 10:
                    if x < 5:
                        board[x+1][y-1].attacked = True
                    else:
                        board[x+1][y-2].attacked = True
        else:
            list_attack = self.first_list(board)
            for [x,y] in list_attack:
                board[x][y].attacked = True

        return board

    def pawn_on_last_line(self):
        if self.color == 'white' and self.y == 10 - abs(5-self.x):
            return True
        elif self.color == 'black' and self.y == 0:
            return True
        else:
            return False

    @property
    def save_data(self):
        data = f'{self.x} {self.y} {self.type} {self.color} '
        if self.type == 'pawn':
            add = 'y' if self.do_hod_now else 'n'
            data += f'{add}'
        return data + '\n'
    
    def from_saves(self,data):
        info = data.split()
        x, y, self.type = info[:3]
        self.x, self.y = int(x), int(y)
        if self.type != 'empty':
            self.color = info[3]
            if self.type == 'pawn':
                self.do_hod_now = info[4] == 'y'
            name = self.type[0] + self.color[0] + '.png'
            size = global_constants.Sizes
            folder = get_folder()
            self.rect = Rectangle(source=folder+name,size=[size.field_len]*2)
            global_constants.current_figure_canvas.add(self.rect)
            self.set_coords_on_board(self.x,self.y)


def rook_move(board,x,y,color):
    # up-down move
    a = 1
    my_hod = []
    m = 10 - abs(5-x)
    while y + a <= m and board[x][y+a].figure.type == 'empty':
        my_hod.append([x,y+a])
        a += 1
    if y + a <= m:
        if board[x][y+a].figure.color != color:
            my_hod.append([x,y+a])
    a = 1
    while y - a >= 0 and board[x][y-a].figure.type == 'empty':
        my_hod.append([x,y-a])
        a += 1
    if y - a >= 0:
        if board[x][y-a].figure.color != color:
            my_hod.append([x,y-a])
    a = 1
    b = 0
    # down left
    if x <= 5 : b = 1
    while x - a >= 0 and y - b >= 0 and board[x-a][y-b].figure.type == 'empty':
        my_hod += [[x-a,y-b]]
        if x - a <= 5:
            b += 1
        a += 1
    if x - a >= 0 and y - b >= 0:
        if board[x-a][y-b].figure.color != color:
            my_hod.append([x-a,y-b])
    a = 1
    b = 0
    # up left
    if x > 5: b = 1
    while x - a >= 0 and y + b <= 10 - abs(5 - x + a) and board[x-a][y+b].figure.type == 'empty':
        my_hod.append([x-a,y+b])
        if x - a > 5:
            b += 1
        a += 1
    if x - a >= 0 and y + b <= 10 - abs(5 - x + a):
        if board[x-a][y+b].figure.color != color:
                    my_hod.append([x-a,y+b])
    a = 1
    b = 0
    ind = True
    # right down
    if x >= 5:  
        b = 1
    while ind:
        if x + a == 11 or y - b < 0:
            ind = False
        elif board[x+a][y-b].figure.type != 'empty':
            ind = False
            if board[x+a][y-b].figure.color != color:
                my_hod.append([x+a,y-b])
        else:
            my_hod.append([x+a,y-b])
            if x + a >= 5:
                b += 1
            a += 1


    a = 1
    b = 0
    # right up
    if x < 5: b = 1
    while x + a < 11 and y + b <= 10 - abs(5 - x - a) and board[x+a][y + b].figure.type == 'empty':
                my_hod.append([x+a,y + b])
                if x + a < 5:
                    b += 1
                a += 1
    if x + a < 11 and y + b <= 10 - abs(5 - x - a):
                if board[x+a][y + b].figure.color != color:
                    my_hod.append([x+a,y+b])
    return my_hod

def horse_move(board,x,y,color):
    my_hod = []
    a = 0
    if x > 5:
        a = 1
    # left 
    if x - 1 >= 0:
        # up
        if y + a + 2 <= 10 - abs(6 - x) and board[x-1][y+a + 2].figure.color != color:
            my_hod.append([x-1,y+a + 2])
        a = 0
        if x < 6:
            a = 1
            # down
        if y - 2 - a >= 0 and board[x-1][y - 2 - a].figure.color != color:
            my_hod.append([x-1,y - a - 2])
    
    if x - 2 >= 0:
        a = 0
        if x == 6:
            a = 1
        if x > 6:
            a = 2
        if y + a + 1 <= 10 - abs(7 - x) and board[x - 2][y + a + 1].figure.color != color:
            my_hod.append([x-2,y+a+1])
        a = 0
        if x < 6:
            a = 2
        if x == 6:
            a = 1
        if y - 1 - a >= 0 and board[x-2][y - a - 1].figure.color != color:
            my_hod.append([x-2,y-1-a])
    if x - 3 >= 0:
        if x > 7:
            a = 1
        elif x == 7:
            a = 0
        elif x == 6:
            a = -1
        else:
            a = -2
        if y + a >= 0 and y + a <= 10 - abs(8-x) and board[x-3][y+a].figure.color != color :
            my_hod.append([x-3,y+a])
        a += 1
        if y + a <= 10 - abs(8-x) and y + a >= 0 and board[x-3][y+a].figure.color != color:
            my_hod.append([x-3,y+a])

    if x + 1 < 11:
        a = 0
        if x < 5:
            a = 1
        if y + 2 + a <= 10 - abs(4 - x) and board[x+1][y+2+a].figure.color != color:
            my_hod.append([x+1,y+2+a])
        a = 0
        if x > 4:
            a = 1
        if y - 2 - a >= 0 and board[x+1][y-2-a].figure.color != color:
            my_hod.append([x+1,y-a-2])
    if x + 2 < 11:
        a = 0
        if x == 4:
            a = 1
        if x < 4:
            a = 2
        if y + 1 + a <= 10 - abs(3-x) and board[x+2][y+1+a].figure.color != color:
            my_hod.append([x+2,y+1+a])
        a = 2 - a
        if y - 1 - a >= 0 and board[x+2][y-1-a].figure.color != color:
            my_hod.append([x+2,y-1-a])
    if x + 3 < 11:
        if x < 3:
            a = 2
        if x == 3:
            a = 1
        if x == 4:
            a = 0
        if x > 4:
            a = -1
        if y + a <= 10 - abs(2  - x) and y + a >= 0 and board[x+3][y+a].figure.color != color:
            my_hod.append([x+3,y+a])
        a -= 1
        if y + a >= 0 and y + a <= 10 - abs(2 - x) and board[x+3][y+a].figure.color != color:
            my_hod.append([x+3,y+a])
    
    return my_hod

def king_move(board,x,y,color):
    my_hod = []
    # up - down
    if y != 0:
        if board[x][y-1].figure.color != color:
            my_hod.append([x,y-1])
    if y < 10 - abs(5-x):
        if board[x][y+1].figure.color != color:
            my_hod.append([x,y+1])
    # down left-right
    if x >= 5:
        d = -1
    else:
        d = 0
    if y + d >= 0 and x != 10 and board[x+1][y+d].figure.color != color:
        my_hod.append([x+1,y+d])
    d = 0
    if x < 6:
        d = -1
    if y + d >= 0 and x != 0 and board[x-1][y+d].figure.color != color:
        my_hod.append([x-1,y+d])
    # up left right
    d = 0
    if x < 5:
        d = 1
    if x != 10 and y + d <= 10 - abs(4 - x) and board[x+1][y+d].figure.color != color:
        my_hod.append([x+1,y+d])
    d = 0
    if x > 5:
        d = 1
    if x != 0 and y + d <= 10 - abs(6-x) and board[x-1][y+d].figure.color != color:
        my_hod.append([x-1,y+d])
    
    # it was verticals
    # will diagonals
    # down
    d = -2
    if x < 5:
        d += 1
    if x != 10 and y + d  >= 0 and board[x+1][y+d].figure.color != color:
        my_hod.append([x+1,y+d])
    d = -2
    if x > 5:
        d = -1
    if x > 0 and y + d >= 0 and board[x-1][y+d].figure.color != color:
        my_hod.append([x-1,y+d])
    # up
    d = 1
    if x < 5:
        d = 2
    if x != 10 and y + d <= 10 - abs(4 - x) and board[x+1][y+d].figure.color != color:
        my_hod.append([x+1,y+d])
    d = 2
    if x <= 5:
        d = 1
    if x != 0 and y + d <= 10 - abs(6 - x) and board[x-1][y+d].figure.color != color :
        my_hod.append([x-1,y + d])
    # center line
    if x - 2 >= 0:
        d = -1
        if x == 6:
            d = 0
        if x > 6:
            d = 1
        if y + d >= 0 and y + d <= 10 - abs(5 - (x-2)) and board[x-2][y+d].figure.color != color:
            my_hod.append([x-2,y+d])
    if x + 2 < 11:
        d = 1
        if x == 4:
            d = 0
        if x > 4:
            d = -1
        if y + d >= 0 and y + d <= 10 - abs(5-(x+2)) and board[x+2][y+d].figure.color != color:
            my_hod.append([x+2,y+d])
    return my_hod

def pawn_move(board,x,y,color):
    my_hod = []
    if color == 'white':
        if board[x][y+1].figure.type == 'empty':
            my_hod.append([x,y+1])
            if y == 3 - abs(5-x) and x != 5:
                if board[x][y+2].figure.type == 'empty':
                    my_hod += [[x,y+2]]
        d = 2
        if x < 6:
            d = 1
        if x != 0 and board[x-1][y+d].figure.color == 'black':
            my_hod.append([x-1,y+d])
        d = 1
        if x < 5:
            d = 2
        if x != 10 and board[x+1][y+d].figure.color == 'black':
            my_hod.append([x+1,y+d])
    else:
        if board[x][y-1].figure.type == 'empty':
            my_hod.append([x,y-1])
            if y == 7 and x != 5:
                if board[x][y-2].figure.type == 'empty':
                    my_hod.append([x,y-2])
        if x != 0:
            d = -2
            if x > 5:
                d = -1
            if board[x-1][y+d].figure.color == 'white':
                my_hod.append([x-1,y+d])
        if x != 10:
            d = -2
            if x < 5:
                d = -1
            if board[x+1][y+d].figure.color == 'white':
                my_hod.append([x+1,y+d])
    return my_hod

def bishop_move(board,x,y,color):
    my_hod = []
    if x > 6:
        d = 1
    elif x == 6:
        d = 0
    else:
        d = -1
    a = 2
    ind = True
    # left center
    while x - a >=0 and ind and y + d >= 0 and y + d <= 10 - abs(5 - x + a): 
        if board[x-a][y+d].figure.color == color:
            ind = False
        elif board[x-a][y+d].figure.type != 'empty':
            ind = False
            my_hod.append([x-a,y+d])
        else:
            my_hod.append([x-a,y+d])
            if x - a > 6:
                d += 1
            elif x - a == 6:
                pass
            else:
                d -= 1
            a += 2
    a = 2
    ind = True
    if x < 4:
        d = 1
    elif x == 4:
        d = 0
    else:
        d = -1
        # right center
    while x + a < 11 and ind and y + d >= 0 and y + d <= 10 - abs(5 - x - a):
        if board[x+a][y+d].figure.color == color:
            ind = False
        elif board[x+a][y+d].figure.type != 'empty':
            ind = False
            my_hod.append([x+a,y+d])
        else:
            my_hod.append([x+a,y+d])
            if x + a < 4:
                d += 1
            elif x + a == 4:
                pass
            else:
                d -= 1
            a += 2
    a = 1
    ind = True
    d = 1
    if x < 5:
        d = 2
        # right up
    while x + a < 11 and ind and y + d <= 10 - abs(5 - x - a) :
        if board[x+a][y+d].figure.color == color:
            ind = False
        elif board[x+a][y+d].figure.type != 'empty':
            ind = False
            my_hod.append([x+a,y+d])
        else:
            my_hod.append([x+a,y+d])
            d += 1
            if x + a < 5:
                d += 1
            a += 1
    a = 1
    ind = True
    d = -1
    if x > 4:
        d = -2
        # down right
    while x + a < 11 and ind and y + d >= 0 :
        if board[x+a][y+d].figure.color == color:
            ind = False
        elif board[x+a][y+d].figure.type != 'empty':
            my_hod.append([x+a,y+d])
            ind = False
        else:
            my_hod.append([x+a,y+d])
            d -= 1
            if x + a > 4:
                d -= 1
            a += 1
    ind = True
    a = 1
    d = -2
    if x > 5:
        d += 1
    # left down
    while x - a >= 0 and y + d >= 0 and ind :
        if board[x-a][y+d].figure.color == color:
            ind = False
        elif board[x-a][y+d].figure.type != 'empty':
            ind = False
            my_hod.append([x-a,y+d])
        else:
            my_hod.append([x-a,y+d])
            d -= 1
            if x - a < 6:
                d -= 1
            a += 1
    ind = True
    a = 1
    d = 1
    if x > 5:
        d = 2
    # left up
    while ind and x - a >= 0 and y + d <= 10 - abs(5 - x + a):
        if board[x-a][y+d].figure.color == color:
            ind = False
        elif board[x-a][y+d].figure.type != 'empty':
            ind = False
            my_hod.append([x-a,y+d])
        else:
            my_hod.append([x-a,y+d])
            if x - a < 6:
                d += 1
            else :
                d += 2
            a += 1

    return my_hod


