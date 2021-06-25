from kivy.graphics import Rectangle
from math import sin,cos,radians
import os
from settings import Settings
import global_constants
import Basic_figure


def get_folder():
    f_set = Settings.get_fig_set()
    d = os.path.sep
    return Settings.get_folder() + f'pictures{d}{f_set}{d}'


class Figure(Basic_figure.Figure):
    def __init__(self,col,x,y,fig_type,moving=''):
        self.color = col
        self.type = fig_type
        self.x = 0
        self.y = 0
        if fig_type == 'pawn':
            self.moving = moving
        # some time i create empty figure named choose_figure
        if self.type != 'empty' and fig_type != '':
            name = fig_type[0] + col[0] + '.png'
            folder = get_folder()
            size = global_constants.Sizes 
            self.rect = Rectangle(source=folder+name,size=[size.r*0.9]*2)
            global_constants.current_figure_canvas.add(self.rect)
            self.set_coords_on_board(x,y)
    
    def set_coords_on_board(self,x,y):
        self.x = x
        self.y = y
        agle = y * 22.5 + 11.25
        size = global_constants.Sizes
        r = size.r_min + size.r * x + size.r * .5
        bx = cos(radians(agle)) * r - self.rect.size[0] / 2
        by = sin(radians(agle)) * r - self.rect.size[1] / 2
        self.rect.pos = (size.center[0]+bx, by+size.center[1])
        
    def first_list(self,board):
        my_hod = []
        if self.type == 'horse':
            my_hod = get_horse_moves(self,board)
        elif self.type == 'rook' :
            my_hod = get_rook_moves(self,board)
        elif self.type == 'pawn':
            my_hod = get_pawn_moves(self,board)
        elif self.type == 'king':
            my_hod = get_king_moves(self,board)
        elif self.type == 'bishop':
            my_hod = get_bishop_moves(self,board)
        elif self.type == 'queen':
            my_hod = get_queen_moves(self,board) 
        return my_hod

    def do_attack(self,board):
        x,y = self.x, self.y
        list_attack = []
        if self.type == 'pawn':
            list_attack = get_pawn_moves(self,board)
            for field in list_attack:
                if field[0] != self.x:
                    x,y = field[0],field[1]
                    board[x][y].attacked = True
        else:
            list_attack = self.first_list(board)
            for element in list_attack:
                x,y = element[0],element[1]
                board[x][y].attacked = True
        return board
    @property
    def save_data(self):
        data = f'{self.x} {self.y} {self.type} {self.color} '
        if self.type == 'pawn':
            data += f'{self.moving}'
        return data + '\n'
    
    def from_saves(self,data):
        info = data.split()
        x, y, self.type = info[:3]
        self.x, self.y = int(x), int(y)
        if self.type != 'empty':
            self.color = info[3]
            if self.type == 'pawn':
                self.moving = info[-1]
            name = self.type[0] + self.color[0] + '.png'
            size = global_constants.Sizes
            folder = get_folder()
            self.rect = Rectangle(source=folder+name,size=[size.r*0.9]*2)
            global_constants.current_figure_canvas.add(self.rect)
            self.set_coords_on_board(self.x,self.y)


def get_pawn_moves(figure,board):
    moves = list()
    x,y = figure.x,figure.y
    color = figure.color
    if figure.moving == 'up':
        if y == 15:
            y = -1
        if board[x][y+1].figure.type == 'empty':
            moves.append([x,y+1])
        if x > 0 and  board[x-1][y+1].figure.color != color and board[x-1][y+1].figure.type != 'empty':
            moves.append([x-1,y+1])
        if x < 3 and  board[x+1][y+1].figure.color != color and board[x+1][y+1].figure.type != 'empty':
            moves.append([x+1,y+1])
    else:
        if y == 0:
            y = 16
        if board[x][y-1].figure.type == 'empty':
            moves.append([x,y-1])
        if x > 0 and board[x-1][y-1].figure.color != color and board[x-1][y-1].figure.type != 'empty':
            moves.append([x-1,y-1])
        if x < 3 and board[x+1][y-1].figure.color != color and board[x+1][y-1].figure.type != 'empty':
            moves.append([x+1,y-1])
    return moves

def get_horse_moves(figure,board):
    x,y = figure.x,figure.y
    color = figure.color
    moves = list()
    if x < 2:
        y2 = y
        if y == 15:
            y2 = -1
        if board[x+2][y2+1].figure.type == 'empty' or board[x+2][y2+1].figure.color != color:
            moves.append([x+2,y2+1])
        y2 = y
        if y == 0:
            y2 = 16
        if board[x+2][y2-1].figure.type == 'empty' or board[x+2][y2-1].figure.color != color:
            moves.append([x+2,y2-1])
    if x in [2,3]:
        y2 = y
        if y == 15:
            y2 = -1
        if board[x-2][y2+1].figure.type == 'empty' or board[x-2][y2+1].figure.color != color:
            moves.append([x-2,y2+1])
        y2 = y
        if y == 0:
            y2 = 16
        if board[x-2][y2-1].figure.type == 'empty' or board[x-2][y2-1].figure.color != color:
            moves.append([x-2,y2-1])
    if x != 0:
        y2 = y
        if y < 2:
            y2 += 16
        if board[x-1][y2-2].figure.type == 'empty' or board[x-1][y2-2].figure.color != color:
            moves.append([x-1,y2-2])
        y2 = y
        if y > 13:
            y2 -= 16
        if board[x-1][y2+2].figure.type == 'empty' or board[x-1][y2+2].figure.color != color:
            moves.append([x-1,y2+2])
        
    if x != 3:
            y2 = y
            if y < 2:
                y2 += 16
            if board[x+1][y2-2].figure.type == 'empty' or board[x+1][y2-2].figure.color != color:
                moves.append([x+1,y2-2])
            y2 = y
            if y > 13:
                y2 -= 16
            if board[x+1][y2+2].figure.type == 'empty' or board[x+1][y2+2].figure.color != color:
                moves.append([x+1,y2+2])
    return moves

def get_king_moves(figure,board):
    moves = list()
    x,y = figure.x,figure.y
    color = figure.color
    if x != 0:
        if board[x-1][y].figure.color != color:
            moves.append([x-1,y])
        y2 = y
        if y == 0:
            y2 = 16
        if board[x-1][y2-1].figure.color != color:
            moves.append([x-1,y2-1])
        y2 = y
        if y == 15:
            y2 = -1
        if board[x-1][y2+1].figure.color != color:
            moves.append([x-1,y2+1])
    
    y2 = y
    if y == 0:
        y2 = 16
    if board[x][y2-1].figure.color != color:
        moves.append([x,y2-1])
    y2 = y
    if y == 15:
        y2 = -1
    if board[x][y2+1].figure.color != color:
        moves.append([x,y2+1])
    
    if x != 3:
        if board[x+1][y].figure.color != color:
            moves.append([x+1,y])
        y2 = y
        if y == 0:
            y2 = 16
        if board[x+1][y2-1].figure.color != color:
            moves.append([x+1,y2-1])
        y2 = y
        if y == 15:
            y2 = -1
        if board[x+1][y2+1].figure.color != color:
            moves.append([x+1,y2+1])
    return moves

def get_rook_moves(figure,board):
    moves = []
    x,y = figure.x,figure.y
    color = figure.color
    a = 1
    while x - a >= 0 and board[x-a][y].figure.type == 'empty':
        moves.append([x-a,y])
        a += 1
    if x - a > -1 and board[x-a][y].figure.color != color:
        moves.append([x-a,y])
    a = 1
    while x + a < 4 and board[x+a][y].figure.type == 'empty':
        moves.append([x+a,y])
        a += 1
    if x + a < 4 and board[x+a][y].figure.color != color:
        moves.append([x+a,y])
    # up y
    a = 1
    while y + a < 16 and board[x][y+a].figure.type == 'empty':
        moves.append([x,y+a])
        a += 1
    if y + a < 16:
        if board[x][y+a].figure.color != color:
            moves.append([x,y+a])
    else:
        a -= 16
        while a != 0 and board[x][y+a].figure.type == 'empty':
            moves.append([x,y+a])
            a += 1
        if a != 0:
            if board[x][y+a].figure.color != color :
                moves.append([x,y+a])
        else:
            return moves
    # down y
    a = 1
    while y - a >= 0 and board[x][y-a].figure.type == 'empty':
        moves.append([x,y-a])
        a += 1
    if y - a > -1:
        if board[x][y-a].figure.color != color:
            moves.append([x,y-a])
    else:
        a -= 16
        while board[x][y-a].figure.type == 'empty':
            moves.append([x,y-a])
            a += 1
        if board[x][y-a].figure.color != color :
            moves.append([x,y-a])
    return moves

def get_bishop_moves(figure,board):
    color = figure.color
    x = figure.x
    y = figure.y
    moves = []
    
    if x in [0,1]:
        y2 = y
        y2 += 2
        y3 = y + 1
        if y3 > 15:
            y3 -= 16
        if y2 > 15:
            y2 -= 16
        if board[x+2][y2].figure.type == 'empty' or board[x+2][y2].figure.color != color:
            if board[x+1][y3].figure.type == 'empty':
                moves.append([x+2,y2])
        y2 = y - 2
        y3 = y -1
        if y3 < 0:
            y3 += 16
        if y2 < 0:
            y2 += 16
        if board[x+2][y2].figure.type == 'empty' or board[x+2][y2].figure.color != color:
            if board[x+1][y3].figure.type == 'empty':
                moves.append([x+2,y2])

    if x in [2,3]:
        y2 = y
        y2 += 2
        y3 = y + 1
        if y3 > 15:
            y3 -= 16
        if y2 > 15:
            y2 -= 16
        if board[x-2][y2].figure.type == 'empty' or board[x-2][y2].figure.color != color:
            if board[x-1][y3].figure.type == 'empty':
                moves.append([x-2,y2])
        y2 = y - 2
        y3 = y - 1
        if y3 < 0:
            y3 += 16
        if y2 < 0:
            y2 += 16
        if board[x-2][y2].figure.type == 'empty' or board[x-2][y2].figure.color != color:
            if board[x-1][y3].figure.type == 'empty':
                moves.append([x-2,y2])

    return moves

def get_queen_moves(figure,board):
    moves = []
    x,y = figure.x,figure.y
    color = figure.color

    if x != 0:
        y2 = y - 1
        if y2 == -1 :
            y2 = 15
        if board[x-1][y2].figure.type == 'empty' or board[x-1][y2].figure.color != color:
            moves.append([x-1,y2])
        y2 = y + 1
        if y2 == 16:
            y2 = 0
        if board[x-1][y2].figure.type == 'empty' or board[x-1][y2].figure.color != color:
            moves.append([x-1,y2])

    if x != 3:
        y2 = y - 1
        if y2 == -1 :
            y2 = 15
        if board[x+1][y2].figure.type == 'empty' or board[x+1][y2].figure.color != color:
            moves.append([x+1,y2])
        y2 = y + 1
        if y2 == 16:
            y2 = 0
        if board[x+1][y2].figure.type == 'empty' or board[x+1][y2].figure.color != color:
            moves.append([x+1,y2])

    return moves

