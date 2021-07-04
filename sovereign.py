
import copy
import sovereign_figure
Figure = sovereign_figure.Figure


class Field():
    def __init__(self):
        self.attacked = False
        self.figure = Figure('',0,0,'empty')

    def __str__(self):
        return str(self.figure)


class Game_State():
    control_points = {
            'white':[[8,7],[7,8]],
            'black':[[8,8],[7,7]],
            'yellow':[[10,5],[5,10]],
            'green':[[5,5],[10,10]],
            'blue':[[4,4],[11,11]],
            'cyan':[[5,7],[10,8]],
            'purple':[[7,5],[8,10]],
            'pink':[[8,5],[7,10]],
            'gray':[[6,9],[9,6]],
            'light':[[6,6],[9,9]],
            'red':[[4,11],[11,4]],
            'orange':[[5,8],[10,7]]
    }

    def __init__(self) -> None:
        # it is for player, it shows, which color it control fistly
        self.white_player = 'white'
        self.black_player = 'black'
        self.occupied_control_points = []
        self.colors_state = {
            'white':'',
            'black':'',
            'yellow':'',
            'green':'',
            'blue':'',
            'cyan':'',
            'purple':'',
            'pink':'',
            'gray':'',
            'light':'',
            'red':'',
            'orange':''
        }
    
    def copy(self):
        new = Game_State()
        for color in self.colors_state:
            new.colors_state[color] = self.colors_state[color]
        new.white_player = self.white_player
        new.black_player = self.black_player
        new.occupied_control_points = copy.copy(self.occupied_control_points)
        return new

    def get_owner(self,color):
        """
        white - 1-st player,
        black - second color,
        '' - nothing
        """
        if color == '':
            return ''
        while self.colors_state[color] != '':
            color = self.colors_state[color]
        if color == self.white_player:
            return 'white'
        if color == self.black_player:
            return 'black'
        return ''

    def is_enemy(self,color1, color2):
        # color1 - my color
        # coor2 - other figure color
        if color2 == color1:
            return False
        first = self.get_owner(color1)
        second = self.get_owner(color2)
        if first == '':
            return False
        if second == '':
            return False
        return first != second

    def is_control_point(self,x,y):
        for color in self.control_points:
            for point in self.control_points[color]:
                if [x,y] == point:
                    return True
        return False
    
    def can_visit(self,x,y,color):
        # могу ли я наступить на клетку этого цвета
        # color - цвет фигуры
        if [x,y] in self.control_points[color]:
            return False
        """
        for col in [self.white_player, self.black_player]:
            if [x,y] in self.control_points[col]:
                return False
        """
        if [x,y] in self.control_points[color]:
            return False

        if not self.is_control_point(x,y):
            return True
        for col in self.colors_state:
            if [x,y] in self.control_points[col]:
                if self.colors_state[col] != '':
                    if self.get_owner(col) == self.get_owner(color):
                        return True
                    else:
                        return [x,y] in self.occupied_control_points

        return True
    
    def check_control(self,movement,figure_color):
        x1, y1, x2, y2 = movement
        for color in self.control_points:
            if [x1, y1] in self.control_points[color]:
                if color not in [self.white_player,self.black_player]:
                    was = self.colors_state[color]
                    self.colors_state[color] = ''
                    self.occupied_control_points.remove([x1,y1])
                    for point in self.control_points[color]:
                        if point in self.occupied_control_points:
                            self.colors_state[color] = was
        # их  нельзя совместить в 1 цикл!!!!!
        for color in self.colors_state:
            if [x2,y2] in self.control_points[color]:
                if color not in [self.white_player,self.black_player]:
                    self.colors_state[color] = figure_color
                    self.occupied_control_points.append([x2,y2])

    def friend_colors(self, color):
        sovereign = self.get_owner(color)
        result = []
        for col in self.colors_state:
            if self.get_owner(col) == sovereign:
                result.append(col)
        return result
    
    def update_player_color(self,coplor1,color2):
        if self.white_player == coplor1:
            self.white_player = color2
        else:
            self.black_player = color2
        self.colors_state[color2] = ''
        for point in self.control_points[color2]:
            if point in self.occupied_control_points:
                self.occupied_control_points.remove(point)

    def get_control_point_color(self,point):
        for color in self.colors_state:
            if point in self.control_points[color]:
                return color
        return ''
    
    @property
    def save_data(self):
        result = f'{self.white_player}\n{self.black_player}\n'
        for point in self.occupied_control_points:
            result += f'{point[0]} {point[1]} '
        result += '\n'
        for color in self.colors_state:
            result += f'{color} {self.colors_state[color]} \n'
        return result
    
    def from_save_data(self, data):
        self.white_player = data[0]
        self.black_player = data[1]
        points = data[2].split()
        self.occupied_control_points = []
        i = 0
        if points != []:
            while i < len(points):
                point = []
                point.append(int(points[i]))
                point.append(int(points[i+1]))
                i += 2
                self.occupied_control_points.append(point)
        for el in data[3:]:
            colors = el.split()
            if len(colors) == 1:
                color = colors[0]
                value = ''
            else:
                color, value = colors
            self.colors_state[color] = value


def copy_board(board):
    new_board = [[Field() for t in range(16)] for a in range(16)]
    for a in range(16):
        for b in range(16):
            new_board[a][b].figure = Figure('white', 0, 0, '')
            new_board[a][b].figure.color = copy.copy(board[a][b].figure.color)
            new_board[a][b].figure.type = copy.copy(board[a][b].figure.type)

    return new_board


def create_start_game_board():
    board = [[Field() for t in range(16)] for a in range(18)]
    for x in range(16):
        for y in range(16):
            board[x][y].figure = Figure('', 0, 0, 'empty')

    colors = [
        'gray', 'gray', 'pink', 'pink', 'white', 'white', 
        'white', 'white', 'white', 'white', 'white', 'white', 
        'green', 'green','light', 'light' ]
    figures = [
        'queen', 'bishop', 'rook', 'horse', 'rook', 'horse',
        'bishop', 'queen', 'king', 'bishop', 'horse', 'rook',
        'horse', 'rook', 'bishop', 'queen'
    ]
    for i in range(16):
        board[i][0].figure = Figure(colors[i],i,0,figures[i])
        if i not in [0,1,15,14]:
            board[i][1].figure = Figure(colors[i],i,1,'pawn')
    
    colors = [
        'light', 'light', 'purple', 'purple', 'black', 'black', 'black',
        'black', 'black', 'black', 'black', 'black', 'yellow', 'yellow', 
        'gray', 'gray'
    ]
    for i in range(16):
        board[i][15].figure = Figure(colors[i],i,15,figures[i])
        if i not in [0,1,15,14]:
            board[i][14].figure = Figure(colors[i],i,14,'pawn')
    board[0][1].figure = Figure('gray',0,1,'rook')
    board[1][1].figure = Figure('gray',1,1,'horse')
    board[14][1].figure = Figure('light',14,1,'horse')
    board[15][1].figure = Figure('light',15,1,'rook')
    board[0][14].figure = Figure('light',0,14,'rook')
    board[1][14].figure = Figure('light',1,14,'horse')
    board[14][14].figure = Figure('gray',14,14,'horse')
    board[15][14].figure = Figure('gray',15,14,'rook')
    colors = [
        'red', 'red', 'orange', 'orange', 'yellow', 'yellow', 'green',
        'green', 'cyan', 'cyan', 'blue', 'blue'
    ]
    figures = [
        'bishop', 'queen', 'rook', 'horse', 'bishop', 'queen',
        'queen', 'bishop', 'horse', 'rook', 'queen', 'bishop'
    ]
    for i in range(0,12):
        board[0][i+2].figure = Figure(colors[i],0,i+2,figures[i])
        board[1][i+2].figure = Figure(colors[i],1,i+2,'pawn')
    colors = [
        'cyan', 'cyan', 'blue', 'blue', 'purple', 'purple',
        'pink', 'pink', 'red', 'red', 'orange', 'orange'
    ]
    for i in range(0,12):
        board[15][i+2].figure = Figure(colors[i],15,i+2,figures[i])
        board[14][i+2].figure = Figure(colors[i],14,i+2,'pawn')
    
    return board


def find_rocking(figure,board,state):
    x, y = figure.x, figure.y
    result = []
    if figure.do_hod_before:
        return result
    result = [[x+2,y]]

    return result


def do_rocking(a,b,x,y,board):
    if abs(a-x) > 1:
        board[x-1][y].figure, board[x+1][y].figure = board[x+1][y].figure, board[x-1][y].figure
        board[x-1][y].figure.set_coords_on_board(x-1,y)
        board[x+1][y].figure.set_coords_on_board(x+1,y)








