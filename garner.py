
import copy
from sounds import Music
from connection import Connection
import global_constants
import core_game_logik


import garner_figure 



class Game_logik(core_game_logik.CoreGameLogik):
    def build_game(self):
        super().build_game()
        self.Figure = garner_figure.Figure
        self.board = create_start_game_board()

    def copy_board(self,board):
        x = len(board)
        y = len(board[0])
        Field = core_game_logik.Field
        new_board = [[Field() for b in range(y)] for a in range(x)]
        for a in range(x):
            for b in range(y):
                new_board[a][b].figure = self.Figure('',a,b,'empty')
                new_board[a][b].figure.color = copy.copy(board[a][b].figure.color)
                new_board[a][b].figure.type = copy.copy(board[a][b].figure.type)
        return new_board

    def move_figure(self,board,x,y,options=None):
        self.message = f'move {self.choose_figure.x} {self.choose_figure.y} {x} {y}'
        Music.move()
        if self.choose_figure.color == 'white':
            self.made_moves += 1

        a , b = self.choose_figure.x , self.choose_figure.y
        board[a][b].figure = self.Figure('',0,0,'empty')
        board[x][y].figure.destroy()
        board[x][y].figure = self.choose_figure
        board[x][y].figure.set_coords_on_board(x,y)

        if self.choose_figure.type == 'pawn' and board[x][y].figure.pawn_on_last_line():
                if global_constants.game.state_game != 'one' and self.color_do_hod_now != global_constants.game.play_by:
                    n , m = self.choose_figure.x , self.choose_figure.y
                    self.board[n][m].figure.transform_to(options[1])
                    self.choose_figure = self.Figure('',0,0,'empty')
                    options = options[2:]
                    self.change_color(options)
                    self.is_end_of_game(board)
                else:
                    self.do_transformation(self.color_do_hod_now,x,y,options)
        else:
            if global_constants.game.state_game != 'one' and self.color_do_hod_now == global_constants.game.play_by:
                self.message += f" {self.players_time['white']} {self.players_time['black']}"
                Connection.messages += [self.message]
                self.message = ''
            self.choose_figure = self.Figure('',0,0,'empty')
            self.change_color(options)
            self.is_end_of_game(board)

        self.delete_tips()
        self.green_line.show_field(x=-1,y=-1)
        self.list_of_hod_field = []
        return board

    def fit_field(self, event):
        x,y = 0,0
        e_x,e_y = event.x,event.y
        s = global_constants.Sizes
        if e_x <= s.x_top + s.x_top_board or e_y <= s.y_top + s.y_top_board:
            return -1,-1
        elif (e_y >= -s.y_top + s.y_top_board + s.board_size[1]) or \
            (e_x >= -s.x_top + s.x_top_board + s.board_size[0]) :
            return -1,-1
        else:
            e_x -= (s.x_top + s.x_top_board)
            x = e_x // s.field_size
            e_y -= (s.y_top + s.y_top_board)
            y = e_y // s.field_size
            x = round(x)
            y = round(y)
            return x,y



def create_start_game_board():
    Field = core_game_logik.Field
    Figure = garner_figure.Figure
    board = [[Field() for t in range(5)] for a in range(5)]
    for x in range(5):
        for y in range(5):
            board[x][y].figure = Figure('',0,0,'empty')
    line = ['king','queen','bishop','horse','rook']    
    for x in range(5):
        board[x][1].figure = Figure('white',x,1,'pawn')
        board[x][3].figure = Figure('black',x,3,'pawn')
        board[x][0].figure = Figure('white',x,0,line[x])
        board[x][4].figure = Figure('black',x,4,line[x])
    return board



