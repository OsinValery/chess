import copy

from sounds import Music
import global_constants
import core_game_logik

import schatranj_figure

def create_start_game_board():
    Field = core_game_logik.Field
    Figure = schatranj_figure.Figure
    board = [[Field() for t in range(8)] for a in range(8)]
    for x in range(8):
        for y in range(8):
            board[x][y].figure = Figure('',0,0,'empty')
            board[x][y].attacked = False
    
    figs = ['rook','horse','bishop','king','queen','bishop','horse','rook']
    for a in range(8):
        board[a][0].figure = Figure('white',a,0,figs[a])
        board[a][7].figure = Figure('black',a,7,figs[a])
        board[a][1].figure = Figure('white',a,1,'pawn')
        board[a][6].figure = Figure('black',a,6,'pawn')
    return board


class Game_logik(core_game_logik.CoreGameLogik):
    def build_game(self):
        super().build_game()
        self.Figure = schatranj_figure.Figure
        self.board = create_start_game_board()

    def copy_board(self, board):
        Field = core_game_logik.Field
        new_board = [[Field() for a in range(8)] for b in range(8)]
        for a in range(8):
            for b in range(8):
                new_board[a][b].figure = self.Figure('white',0,0,'')
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
            board[x][y].figure.transform_to('queen')
        self.choose_figure = self.Figure('',0,0,'empty')
        if global_constants.game.state_game != 'one' and self.color_do_hod_now == global_constants.game.play_by:
            self.message += f" {self.players_time['white']} {self.players_time['black']}"
            global_constants.Connection_manager.send(self.message)
        self.message = ''
        self.change_color(options)
        self.is_end_of_game(board)
        self.delete_tips()
        self.green_line.show_field(x=-1,y=-1)
        self.list_of_hod_field = []
        return board
