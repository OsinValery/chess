import Basic_figure
import global_constants
from kivy.graphics import Rectangle
import os
import settings


def get_folder():
    path = settings.Settings.get_folder()
    f_set = 'sovereign_figures'
    d = os.path.sep
    return   path + f'pictures{d}{f_set}{d}'


class Figure(Basic_figure.Figure):
    board_size = [16, 16]
    def set_coords_on_board(self,x,y):
        self.x = x
        self.y = y
        if self.type == 'empty':
            return
        size = global_constants.Sizes
        if global_constants.game.window == 'game':
            pos_x = x * size.field_size + size.x_top
            pos_y = y * size.field_size + size.y_top
        else:
            pos_x = x * size.field_size + size.x_top + size.x_top_board
            pos_y = y * size.field_size + size.y_top + size.y_top_board
        self.rect.pos = (pos_x, pos_y)
    
    def __init__(self, color, x, y, fig_type):
        self.color = color
        self.type = fig_type
        self.x = 0
        self.y = 0
        self.do_hod_before = False
        # some time i create empty figure named chose_figure
        if self.type != 'empty' and fig_type != '':
            name = fig_type[0] + color[0] + '.png'
            if color == 'blue':
                name = fig_type[0] + 'bl.png'
            if color == 'gray':
                name = fig_type[0] + 'gr.png'
            if color == 'pink':
                name = fig_type[0] + 'pi.png'
            size = global_constants.Sizes
            folder = get_folder()
            self.rect = Rectangle(source=folder+name,size=[size.field_size]*2)
            global_constants.current_figure_canvas.add(self.rect)
            self.set_coords_on_board(x,y)
    
    def first_list(self, board, game_state):
        if self.type == 'pawn':
            return pawn_moves(self,board,game_state)
        if self.type == 'horse':
            return horse_move(self,board,game_state)
        if self.type == 'king':
            return king_move(self,board,game_state)
        if self.type == 'rook':
            return rook_move(self,board,game_state)
        if self.type == 'bishop':
            return bishop_move(self,board,game_state)
        if self.type == 'queen':
            return queen_move(self,board,game_state)
        return super().first_list(board)

    def pawn_on_last_line(self):
        if self.x > 5 and self.x < 10 and self.y > 5 and self.y < 10:
            return True
        return False

    def do_attack(self, board,game_state):
        x,y = self.x, self.y
        if self.type == 'pawn':
            fields = pawn_taking(self,board,game_state)
            for x,y in fields:
                board[x][y].attacked = True
        else:
            list_attack = self.first_list(board,game_state)
            for element in list_attack:
                x,y = element[0],element[1]
                board[x][y].attacked = True

        return board

    def change_color(self,color):
        self.color = color
        name = self.type[0] + color[0] + '.png'
        if color == 'blue':
            name = self.type[0] + 'bl.png'
        if color == 'gray':
            name = self.type[0] + 'gr.png'
        if color == 'pink':
            name = self.type[0] + 'pi.png'
        self.rect.source = get_folder() + name

    def transform_to(self, fig_type):
        self.type = fig_type
        color = self.color
        name = self.type[0] + color[0] + '.png'
        if color == 'blue':
            name = self.type[0] + 'bl.png'
        if color == 'gray':
            name = self.type[0] + 'gr.png'
        if color == 'pink':
            name = self.type[0] + 'pi.png'
        self.rect.source = get_folder() + name

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
            self.do_hod_before = True
        if info[1] == 'y':
            self.do_hod_now = True
        if info[1] == 'n':
            self.do_hod_now = False
        # third possible variant is "e"
        if self.type != 'empty' :
            fig_type = self.type
            color = self.color
            name = fig_type[0] + self.color[0] + '.png'

            if color == 'blue':
                name = fig_type[0] + 'bl.png'
            if color == 'gray':
                name = fig_type[0] + 'gr.png'
            if color == 'pink':
                name = fig_type[0] + 'pi.png'

            size = global_constants.Sizes
            folder = get_folder()
            self.rect = Rectangle(source=folder+name,size=[size.field_size]*2)
            global_constants.current_figure_canvas.add(self.rect)
            self.set_coords_on_board(self.x,self.y)

    @property
    def pawn_on_penultimate_line(self):
        if self.pawn_on_last_line(): return False
        if self.x < 5 or self.y < 5: return False
        if self.y > 10 or self.x > 10: return False
        # i doo't check eagles, because pawn may take
        return True

    def movement_to_last_line(self):
        pass

######################################################################
## figure movement logik
######################################################################

def pawn_taking(self,board,game_state):
    result = []
    x, y = self.x, self.y
    color = self.color

    if x < 8 and y < 8:
        # 3-rd part
        if board[x+1][y+1].figure.type != 'empty':
            if game_state.is_enemy(color, board[x+1][y+1].figure.color):
                result.append([x+1,y+1])
        if y > 0 and board[x+1][y-1].figure.type != 'empty':
            if game_state.is_enemy(color, board[x+1][y-1].figure.color):
                result.append([x+1, y-1])
        if x > 0 and board[x-1][y+1].figure.type != 'empty':
            if game_state.is_enemy(color, board[x-1][y+1].figure.color):
                result.append([x-1,y+1])

    elif y < 8:
        # 4 - th part
        if board[x-1][y+1].figure.type != 'empty':
            if game_state.is_enemy(color, board[x-1][y+1].figure.color):
                result.append([x-1,y+1])
        if y > 0 and board[x-1][y-1].figure.type != 'empty':
            if game_state.is_enemy(color, board[x-1][y-1].figure.color):
                result.append([x-1,y-1])
        if (x+1) < self.board_size[0] and board[x+1][y+1].figure.type != 'empty':
            if game_state.is_enemy(color, board[x+1][y+1].figure.color):
                result.append([x+1,y+1])

    elif x < 8:
        # 2-nd part
        if board[x+1][y-1].figure.type != 'empty':
            if game_state.is_enemy(color, board[x+1][y-1].figure.color):
                result.append([x+1,y-1])
        if (y + 1) < self.board_size[1] and board[x+1][y+1].figure.type != 'empty':
            if game_state.is_enemy(color,board[x+1][y+1].figure.color):
                result.append([x+1,y+1])
        if x > 0 and board[x-1][y-1].figure.type != 'empty':
            if game_state.is_enemy(color,board[x-1][y-1].figure.color):
                result.append([x-1,y-1])

    else:
        # 1-st
        if board[x-1][y-1].figure.type != 'empty':
            if game_state.is_enemy(color,board[x-1][y-1].figure.color):
                result.append([x-1,y-1])
        if (x+1) < self.board_size[0] and board[x+1][y-1].figure.type != 'empty':
            if game_state.is_enemy(color, board[x+1][y-1].figure.color):
                result.append([x+1,y-1])
        if (y+1) < self.board_size[1] and board[x-1][y+1].figure.type != 'empty':
            if game_state.is_enemy(color, board[x-1][y+1].figure.color):
                result.append([x-1,y+1])

    return result



def pawn_moves(self,board,game_state):
    x, y = self.x, self.y
    color = self.color
    result = []
    if x < 8 and y < 8:
        # up
        if not game_state.is_control_point(x,y+1) or game_state.can_visit(x,y+1,color):
            if y != 7 and board[x][y+1].figure.type == 'empty':
                result.append([x,y+1])
                if y < 2 and board[x][y+2].figure.type == 'empty':
                    if not game_state.is_control_point(x,y+2) or game_state.can_visit(x,y+2,color):
                            result.append([x,y+2])
        
        #right
        if not game_state.is_control_point(x+1,y) or game_state.can_visit(x+1,y,color):
            if x != 7 and board[x+1][y].figure.type == 'empty':
                result.append([x+1,y])
                if x < 2 and board[x+2][y].figure.type == 'empty':
                    if not game_state.is_control_point(x+2,y) or game_state.can_visit(x+2,y,color):
                            result.append([x+2,y])

    elif x > 7 and y < 8:
        # up
        if not game_state.is_control_point(x,y+1) or game_state.can_visit(x,y+1,color):
            if y != 7 and board[x][y+1].figure.type == 'empty':
                result.append([x,y+1])
                if y < 2 and board[x][y+2].figure.type == 'empty':
                    if not game_state.is_control_point(x,y+2) or game_state.can_visit(x,y+2,color):
                            result.append([x,y+2])
        
        # left
        if not game_state.is_control_point(x-1,y) or game_state.can_visit(x-1,y,color):
            if x != 8 and board[x-1][y].figure.type == 'empty':
                result.append([x-1,y])
                if x > 13 and board[x-2][y].figure.type == 'empty':
                    if not game_state.is_control_point(x-2,y) or game_state.can_visit(x-2,y,color):
                            result.append([x-2,y])

    elif x < 8 and y > 7:
        # down
        if not game_state.is_control_point(x,y-1) or game_state.can_visit(x,y-1,color):
            if y != 8 and board[x][y-1].figure.type == 'empty':
                result.append([x,y-1])
                if y > 13 and board[x][y-2].figure.type == 'empty':
                        result.append([x,y-2])
        
        # right
        if not game_state.is_control_point(x+1,y) or game_state.can_visit(x+1,y,color):
            if x != 7 and board[x+1][y].figure.type == 'empty':
                result.append([x+1,y])
                if x < 2 and board[x+2][y].figure.type == 'empty':
                    if not game_state.is_control_point(x+2,y) or game_state.can_visit(x+2,y,color):
                            result.append([x+2,y])

    else:
        # 4- th
        # down
        if not game_state.is_control_point(x,y-1) or game_state.can_visit(x,y-1,color):
            if y != 8 and board[x][y-1].figure.type == 'empty':
                result.append([x,y-1])
                if y > 13 and board[x][y-2].figure.type == 'empty':
                        result.append([x,y-2])
        
        # left
        if not game_state.is_control_point(x-1,y) or game_state.can_visit(x-1,y,color):
            if x != 8 and board[x-1][y].figure.type == 'empty':
                result.append([x-1,y])
                if x > 13 and board[x-2][y].figure.type == 'empty':
                        result.append([x-2,y])

    return result + pawn_taking(self,board,game_state)

def horse_move(self,board,game_state):
    result = []
    x, y = self.x, self.y
    color = self.color

    if x > 1 and y > 0:
        if not game_state.is_control_point(x-2,y-1) or game_state.can_visit(x-2,y-1,color):
            if board[x-2][y-1].figure.type == 'empty' or game_state.is_enemy(color, board[x-2][y-1].figure.color):
                result.append([x-2,y-1])

    if x > 0 and y > 1:
        if not game_state.is_control_point(x-1,y-2) or game_state.can_visit(x-1,y-2,color):
            if board[x-1][y-2].figure.type == 'empty' or game_state.is_enemy(color, board[x-1][y-2].figure.color):
                result.append([x-1,y-2])
    
    if x < self.board_size[0] - 1 and y > 1:
        if not game_state.is_control_point(x+1,y-2) or game_state.can_visit(x+1,y-2,color):
            if board[x+1][y-2].figure.type == 'empty' or game_state.is_enemy(color, board[x+1][y-2].figure.color):
                result.append([x+1,y-2])
    
    if (x < self.board_size[0] - 2) and y > 0:
        if not game_state.is_control_point(x+2,y-1) or game_state.can_visit(x+2,y-1,color):
            if board[x+2][y-1].figure.type == 'empty' or game_state.is_enemy(color, board[x+2][y-1].figure.color):
                result.append([x+2,y-1])
    
    if x < self.board_size[0] - 2 and y < self.board_size[1] - 1:
        if not game_state.is_control_point(x+2,y+1) or game_state.can_visit(x+2,y+1,color):
            if board[x+2][y+1].figure.type == 'empty' or game_state.is_enemy(color, board[x+2][y+1].figure.color):
                result.append([x+2,y+1])
    
    if (x + 1) < self.board_size[0] and (y + 2) < self.board_size[1]:
        if not game_state.is_control_point(x+1,y+2) or game_state.can_visit(x+1,y+2,color):
            if board[x+1][y+2].figure.type == 'empty' or game_state.is_enemy(color, board[x+1][y+2].figure.color):
                result.append([x+1,y+2])
    
    if x > 1 and (y+1) < self.board_size[1]:
        if not game_state.is_control_point(x-2,y+1) or game_state.can_visit(x-2,y+1,color):
            if board[x-2][y+1].figure.type == 'empty' or game_state.is_enemy(color, board[x-2][y+1].figure.color):
                result.append([x-2,y+1])
    
    if x > 0 and (y+2) < self.board_size[1]:
        if not game_state.is_control_point(x-1,y+2) or game_state.can_visit(x-1,y+2,color):
            if board[x-1][y+2].figure.type == 'empty' or game_state.is_enemy(color, board[x-1][y+2].figure.color):
                result.append([x-1,y+2])

    return result


def queen_move(self,board,game_state):
    return rook_move(self,board,game_state) + bishop_move(self,board,game_state)


def bishop_move(self,board,game_state):
    result = []
    x, y = self.x, self.y
    color = self.color

    a = 1
    stop = False
    while not stop:
        if x - a < 0 or y - a < 0:
            stop = True
        elif game_state.is_control_point(x-a,y-a) and not game_state.can_visit(x-a,y-a,color):
            stop = True
        elif board[x-a][y-a].figure.type == 'empty':
            result.append([x-a, y-a])
        else:
            stop = True
            if game_state.is_enemy(color, board[x-a][y-a].figure.color):
                result.append([x-a,y-a])
        a += 1
        if a == 9:
            stop = True
    
    a = 1
    stop = False
    while not stop:
        if x + a >= self.board_size[0] or y - a < 0:
            stop = True
        elif game_state.is_control_point(x+a,y-a) and not game_state.can_visit(x+a,y-a,color):
            stop = True
        elif board[x+a][y-a].figure.type == 'empty':
            result.append([x+a, y-a])
        else:
            stop = True
            if game_state.is_enemy(color, board[x+a][y-a].figure.color):
                result.append([x+a,y-a])
        a += 1
        if a == 9:
            stop = True

    a = 1
    stop = False
    while not stop:
        if x - a < 0 or y + a >= self.board_size[1]:
            stop = True
        elif game_state.is_control_point(x-a,y+a) and not game_state.can_visit(x-a,y+a,color):
            stop = True
        elif board[x-a][y+a].figure.type == 'empty':
            result.append([x-a, y+a])
        else:
            stop = True
            if game_state.is_enemy(color, board[x-a][y+a].figure.color):
                result.append([x-a,y+a])
        a += 1
        if a == 9:
            stop = True

    a = 1
    stop = False
    while not stop:
        if x + a >= self.board_size[0] or y + a >= self.board_size[1]:
            stop = True
        elif game_state.is_control_point(x+a,y+a) and not game_state.can_visit(x+a,y+a,color):
            stop = True
        elif board[x+a][y+a].figure.type == 'empty':
            result.append([x+a, y+a])
        else:
            stop = True
            if game_state.is_enemy(color, board[x+a][y+a].figure.color):
                result.append([x+a,y+a])
        a += 1
        if a == 9:
            stop = True

    return result


def king_move(self,board,game_state):
    x, y = self.x, self.y
    color = self.color
    result = []
    if x > 0:
        if y > 0 :
            if not game_state.is_control_point(x-1,y-1) or game_state.can_visit(x-1,y-1,color):
                if board[x-1][y-1].figure.type == 'empty' or game_state.is_enemy(color, board[x-1][y-1].figure.color):
                    result.append([x-1,y-1])
        if (y + 1) < self.board_size[1]:
            if not game_state.is_control_point(x-1,y+1) or game_state.can_visit(x-1,y+1,color):
                if board[x-1][y+1].figure.type == 'empty' or game_state.is_enemy(color, board[x-1][y+1].figure.color):
                    result.append([x-1,y+1])
        if not game_state.is_control_point(x-1,y) or game_state.can_visit(x-1,y,color):
            if board[x-1][y].figure.type == 'empty' or game_state.is_enemy(color, board[x-1][y].figure.color):
                result.append([x-1,y])
    
    if (x + 1) < self.board_size[0]:
        if y > 0 :
            if not game_state.is_control_point(x+1,y-1) or game_state.can_visit(x+1,y-1,color):
                if board[x+1][y-1].figure.type == 'empty' or game_state.is_enemy(color, board[x+1][y-1].figure.color):
                    result.append([x+1,y-1])
        if (y + 1) < self.board_size[1]:
            if not game_state.is_control_point(x+1,y+1) or game_state.can_visit(x+1,y+1,color):
                if board[x+1][y+1].figure.type == 'empty' or game_state.is_enemy(color, board[x+1][y+1].figure.color):
                    result.append([x+1,y+1])
        if not game_state.is_control_point(x+1,y) or game_state.can_visit(x+1,y,color):
            if board[x+1][y].figure.type == 'empty' or game_state.is_enemy(color, board[x+1][y].figure.color):
                result.append([x+1,y])
    
    if y > 0:
        if not game_state.is_control_point(x,y-1) or game_state.can_visit(x,y-1,color):
            if board[x][y-1].figure.type == 'empty' or game_state.is_enemy(color, board[x][y-1].figure.color):
                result.append([x,y-1])
    
    if (y + 1) < self.board_size[1]:
        if not game_state.is_control_point(x,y+1) or game_state.can_visit(x,y+1,color):
            if board[x][y+1].figure.type == 'empty' or game_state.is_enemy(color, board[x][y+1].figure.color):
                result.append([x,y+1])
    
    return result


def  rook_move(self,board,game_state):
    result = []
    x, y = self.x, self.y
    color = self.color
    a = 1
    stop = False
    # up
    while not stop:
        if (y + a) < self.board_size[1]:
            if not game_state.is_control_point(x,y+a) or game_state.can_visit(x,y+a,color):
                if board[x][y+a].figure.type == 'empty' or game_state.is_enemy(color, board[x][y+a].figure.color):
                    result.append([x,y+a])
                    if board[x][y+a].figure.type != 'empty':
                        stop = True
                else:
                    stop = True
            elif game_state.is_control_point(x,y+a) and not game_state.can_visit(x,y+a,color):
                stop = True
        else:
            stop = True
        a += 1
        if a == 9:
            stop = True

    a = 1
    stop = False
    # down
    while not stop:
        if y - a >= 0:
            if not game_state.is_control_point(x,y-a) or game_state.can_visit(x,y-a,color):
                if board[x][y-a].figure.type == 'empty' or game_state.is_enemy(color, board[x][y-a].figure.color):
                    result.append([x, y-a])
                    if board[x][y-a].figure.type != 'empty':
                        stop = True
                else:
                    stop = True
            else:
                stop = True
        else:
            stop = True
        a += 1
        if a == 9:
            stop = True
    
    a = 1
    stop = False
    # right
    while not stop:
        if x + a >= self.board_size[0]:
            stop = True
        else:
            if game_state.is_control_point(x+a,y) and not game_state.can_visit(x+a,y,color):
                stop = True
            else:
                if board[x+a][y].figure.type != 'empty' and not game_state.is_enemy(color, board[x+a][y].figure.color):
                    stop = True
                else:
                    result.append([x+a, y])
                    if board[x+a][y].figure.type != 'empty':
                        stop = True
        a += 1
        if a == 9:
            stop = True
    
    a = 1
    stop = False
    # left
    while not stop:
        if x - a < 0:
            stop = True
        else:
            if game_state.is_control_point(x-a,y) and not game_state.can_visit(x-a,y,color):
                stop = True
            else:
                if board[x-a][y].figure.type != 'empty' and not game_state.is_enemy(color, board[x-a][y].figure.color):
                    stop = True
                else:
                    result.append([x-a, y])
                    if board[x-a][y].figure.type != 'empty':
                        stop = True
        a += 1
        if a == 9:
            stop = True

    return result











