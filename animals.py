import Basic_figure
from kivy.graphics import Rectangle
import os
import global_constants

class Figure(Basic_figure.Figure):
    board_size = [7,9]

    def __init__(self, color, x, y, fig_type):
        self.power = 0
        self.cur_power = 0
        self.type = fig_type        
        if self.type != 'empty':
            self.power = getPower(self.type)
            self.cur_power = self.power
        self.color = color
        self.x = x
        self.y = y

        if self.type != 'empty':
            filename = 'r' if self.color == 'black' else 'b'
            if self.type != 'leopard':
                filename += self.type[0]
            else:
                filename += 'p'
            path = global_constants.Settings.get_folder()
            size = global_constants.Sizes
            filepath = os.path.join(path, 'pictures', 'jungles', filename + '.png')
            self.rect = Rectangle(
                size = [size.field_width, size.field_height], 
                source = filepath
            )
            global_constants.current_figure_canvas.add(self.rect)
            self.set_coords_on_board(self.x, self.y)

    def first_list(self, board):
        if self.type == 'rat':
            return rat_move(self, board)
        elif self.type == 'cat':
            return cat_move(self, board)
        # these figures heve same logik
        elif self.type in ['dog', 'leopard', 'wolf']:
            return cat_move(self, board)
        elif self.type in ['lion','tiger']:
            return cat_move(self, board) + jump_move(self, board)
        elif self.type == 'elephant':
            return elephant_move(self, board)
        print('unknown figure')
        return []
    
    def destroy(self):
        super().destroy()
        self.type = 'empty'
        self.color = ''
        self.power = 0
        self.cur_power = 0
    
    def set_coords_on_board(self, x, y):
        if self.color == 'black':
            if (self.x, self.y) in [(2,0), (4,0), (3,1)]:
                self.cur_power = self.power
            if (x, y) in [(2,0), (4,0), (3,1)]:
                self.cur_power = 0
        elif self.color == 'white':
            if (self.x, self.y) in [(2,8), (4,8), (3,7)]:
                self.cur_power = self.power
            if (x, y) in [(2,8), (4,8), (3,7)]:
                self.cur_power = 0
        self.x  = x
        self.y = y
        size = global_constants.Sizes
        pos_x = x * size.field_width + size.x_top + size.x_top_board
        pos_y = y * size.field_height + size.y_top + size.y_top_board
        self.rect.pos = (pos_x, pos_y)
    
    @property
    def save_data(self):
        return f'{self.x} {self.y} {self.type} {self.color} '
    
    def from_saves(self, data):
        x, y, tip, color = data.split()
        self.x = int(x)
        self.y = int(y)
        self.color = color
        self.type = tip
        self.power = getPower(self.type)
        self.cur_power = self.power
        if self.color == 'white':
            if (self.x, self.y) in [(2,8), (4,8), (3,7)]:
                self.cur_power = 0
        if self.color == 'black':
            if (self.x, self.y) in [(2,0), (4,0), (3,1)]:
                self.cur_power = 0
        if self.type != 'empty':
            filename = 'r' if self.color == 'black' else 'b'
            if self.type != 'leopard':
                filename += self.type[0]
            else:
                filename += 'p'
            path = global_constants.Settings.get_folder()
            size = global_constants.Sizes
            filepath = os.path.join(path, 'jungles', filename + '.png')
            self.rect = Rectangle(
                size = [size.field_width, size.field_height], 
                source = filepath
            )
            global_constants.current_figure_canvas.add(self.rect)
            self.set_coords_on_board(self.x, self.y)
    

def getPower(tip):
    """returns power of animal in points: \n
    0 - empty\n
    1 - rat\n
    2 - cat\n
    3 - dog\n
    4 - wolf\n
    5 - leopard\n
    6 - tiger\n
    7 - lion\n
    8 - elephant
    """
    if tip == 'cat': return 2
    elif tip == 'rat': return 1
    elif tip == 'dog': return 3
    elif tip == 'wolf': return 4
    elif tip == 'leopard': return 5
    elif tip == 'tiger': return 6
    elif tip == 'lion': return 7
    elif tip == 'elephant': return 8
    return 0

def rat_move(self, board):
    result, x, y, = [], self.x, self.y
    if board[x][y].type == 'river':
        # rat can't attack from river and can visit river
        # right
        if board[x+1][y].type == 'river':
            result.append([x+1, y])
        elif board[x+1][y].figure.type == 'empty':
            result.append([x+1, y])
        # up
        if board[x][y+1].type == 'river':
            result.append([x, y+1])
        elif board[x][y+1].figure.type == 'empty':
            result.append([x, y+1])
        # left
        if board[x-1][y].type == 'river':
            result.append([x-1, y])
        elif board[x-1][y].figure.type == 'empty':
            result.append([x-1, y])
        # down
        if board[x][y-1].type == 'river':
            result.append([x, y-1])
        elif board[x][y-1].figure.type == 'empty':
            result.append([x, y-1])
    else:
        # right
        if x != 6:
            if board[x+1][y].type == 'river':
                result.append([x+1, y])
            elif board[x+1][y].type == 'castle':
                if board[x+1][y].player != self.color:
                    result.append([x+1, y])
            elif board[x+1][y].figure.type == 'empty':
                result.append([x+1, y])
            elif board[x+1][y].figure.color != self.color:
                if board[x+1][y].figure.cur_power <= self.cur_power:
                    result.append([x+1, y])
                elif board[x+1][y].figure.type == 'elephant':
                    result.append([x+1, y])
        # up
        if y != 8:
            if board[x][y+1].type == 'river':
                result.append([x, y+1])
            elif board[x][y+1].type == 'castle':
                if board[x][y+1].player != self.color:
                    result.append([x, y+1])
            elif board[x][y+1].figure.type == 'empty':
                result.append([x, y+1])
            elif board[x][y+1].figure.color != self.color:
                if board[x][y+1].figure.type == 'elephant':
                    result.append([x, y+1])
                elif board[x][y+1].figure.cur_power <= self.cur_power:
                    result.append([x, y+1])
        # left
        if x != 0:
            if board[x-1][y].type == 'river':
                result.append([x-1, y])
            elif board[x-1][y].type == 'castle':
                if board[x-1][y].player != self.color:
                    result.append([x-1, y])
            elif board[x-1][y].figure.type == 'empty':
                result.append([x-1, y])
            elif board[x-1][y].figure.color != self.color:
                if board[x-1][y].figure.cur_power <= self.cur_power:
                    result.append([x-1, y])
                elif board[x-1][y].figure.type == 'elephant':
                    result.append([x-1, y])
        # down
        if y != 0:
            if board[x][y-1].type == 'river':
                result.append([x, y-1])
            elif board[x][y-1].type == 'castle':
                if board[x][y-1].player != self.color:
                    result.append([x, y-1])
            elif board[x][y-1].figure.type == 'empty':
                result.append([x, y-1])
            elif board[x][y-1].figure.color != self.color:
                if board[x][y-1].figure.type == 'elephant':
                    result.append([x, y-1])
                elif board[x][y-1].figure.cur_power <= self.cur_power:
                    result.append([x, y-1])
    return result

def cat_move(self, board):
    result, x, y = [], self.x, self.y
    # up
    if y != 8:
        if board[x][y+1].type == 'castle':
            if board[x][y+1].player != self.color:
                result += [[x, y+1]]
        elif board[x][y+1].type != 'river':
            if board[x][y+1].figure.type == 'empty':
                result += [[x, y+1]]
            elif board[x][y+1].figure.color != self.color:
                if board[x][y+1].figure.cur_power <= self.cur_power:
                    result.append([x, y+1])
    # down
    if y != 0:
        if board[x][y-1].type == 'castle':
            if board[x][y-1].player != self.color:
                result += [[x, y-1]]
        elif board[x][y-1].type != 'river':
            if board[x][y-1].figure.type == 'empty':
                result += [[x, y-1]]
            elif board[x][y-1].figure.color != self.color:
                if board[x][y-1].figure.cur_power <= self.cur_power:
                    result.append([x, y-1])
    # right
    if x != 6:
        if board[x+1][y].type == 'castle':
            if board[x+1][y].player != self.color:
                result.append([x+1, y])
        elif board[x+1][y].type != 'river':
            if board[x+1][y].figure.type == 'empty':
                result.append([x+1, y])
            elif board[x+1][y].figure.color != self.color:
                if board[x+1][y].figure.cur_power <= self.cur_power:
                    result += [[x+1, y]]
    # left
    if x != 0:
        if board[x-1][y].type == 'castle':
            if board[x-1][y].player != self.color:
                result.append([x-1, y])
        elif board[x-1][y].type != 'river':
            if board[x-1][y].figure.type == 'empty':
                result.append([x-1, y])
            elif board[x-1][y].figure.color != self.color:
                if board[x-1][y].figure.cur_power <= self.cur_power:
                    result += [[x-1, y]]
    return result

def jump_move(self, board):
    """this function works jump across the river """
    x, y, result = self.x, self.y, []
    # up
    if y != 8:
        if board[x][y+1].type == 'river':
            if board[x][y+1].figure.type == 'empty' and board[x][y+2].figure.type == 'empty':
                if board[x][y+3].figure.type == 'empty':
                    fig = board[x][y+4].figure
                    if fig.type == 'empty':
                        result += [[x, y+4]]
                    elif fig.color != self.color and fig.cur_power <= self.cur_power:
                        result += [[x, y+4]]
    # down
    if y != 0:
        if board[x][y-1].type == 'river':
            if board[x][y-1].figure.type == 'empty' and board[x][y-2].figure.type == 'empty':
                if board[x][y-3].figure.type == 'empty':
                    fig = board[x][y-4].figure
                    if fig.type == 'empty':
                        result += [[x, y-4]]
                    elif fig.color != self.color and fig.cur_power <= self.cur_power:
                        result.append([x, y-4])
    # right
    if x != 6:
        if board[x+1][y].type == 'river':
            if board[x+1][y].figure.type == 'empty' and board[x+2][y].figure.type == 'empty':
                fig = board[x+3][y].figure
                if fig.type == 'empty':
                    result += [[x+3, y]]
                elif fig.color != self.color and self.cur_power >= fig.cur_power:
                    result.append([x+3, y])
    # left
    if x != 0:
        if board[x-1][y].type == 'river':
            if board[x-1][y].figure.type == 'empty' and board[x-2][y].figure.type == 'empty':
                fig = board[x-3][y].figure
                if fig.type == 'empty':
                    result += [[x-3, y]]
                elif fig.color != self.color and self.cur_power >= fig.cur_power:
                    result.append([x-3, y])
    return result


def elephant_move(self, board):
    result, x, y = [], self.x, self.y
    # up
    if y != 8:
        if board[x][y+1].type != 'river':
            if board[x][y+1].figure.type == 'empty':
                 result.append([x, y+1])
            elif board[x][y].type == 'castle':
                if board[x][y+1].player != self.color:
                    result += [[x, y+1]]
            elif board[x][y+1].figure.color != self.color:
                result.append([x, y+1])
    # down
    if y != 0:
        if board[x][y-1].type != 'river':
            if board[x][y-1].type == 'castle':
                if board[x][y-1].player != self.color:
                    result.append([x, y-1])
            elif board[x][y-1].figure.color != self.color:
                result.append([x, y-1])
    # right
    if x != 6:
        if board[x+1][y].type != 'river':
            if board[x+1][y].type == 'castle':
                if board[x+1][y].player != self.color:
                    result.append([x+1, y])
            elif board[x+1][y].figure.color != self.color:
                result += [[x+1, y]]
    # left
    if x != 0:
        if board[x-1][y].type != 'river':
            if board[x-1][y].type == 'castle':
                if board[x-1][y].player != self.color:
                    result.append([x-1, y])
            elif board[x-1][y].figure.color != self.color:
                result.append([x-1, y])
    return result

