
from sounds import Music
import global_constants
import core_game_logik
import help_chess


class Field():
    def __init__(self):
        self.attacked = False
        self.figure = None

    def __str__(self):
        return str(self.figure)


def create_start_game_board():
    Figure = help_chess.Figure
    board = [[Field() for t in range(8)] for a in range(8)]
    for x in range(8):
        for y in range(8):
            board[x][y].figure = Figure('',0,0,'empty')
            board[x][y].attacked = False
    
    for x in range(8):
        board[x][1].figure = Figure('white',x,1,'pawn')
    board[4][0].figure = Figure('white',4,0,'king')
    board[4][7].figure = Figure('black',4,7,'king')
    board[4][6].figure = Figure('black',4,6,'pawn')
    for x in 1,2,5,6:
        board[x][7].figure = Figure('black',x,7,'horse')
    
    return board



class Game_logik(core_game_logik.CoreGameLogik):
    def build_game(self):
        super().build_game()
        self.Figure = help_chess.Figure
        self.board = create_start_game_board()

    def move_figure(self, board, x, y, options=None):
        self.message = f'move {self.choose_figure.x} {self.choose_figure.y} {x} {y}'
        Music.move()
        if self.choose_figure.color == 'white':
            self.made_moves += 1

        if self.choose_figure.type == 'pawn':
            if x != self.choose_figure.x:
                if board[x][y].figure.type == 'empty':
                    board[x][self.choose_figure.y].figure.destroy()

        a, b = self.choose_figure.x, self.choose_figure.y
        board[a][b].figure = self.Figure('', 0, 0, 'empty')
        board[x][y].figure.destroy()
        board[x][y].figure = self.choose_figure
        board[x][y].figure.set_coords_on_board(x, y)

        if self.choose_figure.type == 'pawn':
            if abs(y-b) == 2:
                self.choose_figure.do_hod_now = True
            if board[x][y].figure.pawn_on_last_line():
                board[x][y].figure.transform_to('horse')

        if global_constants.game.state_game != 'one' and self.color_do_hod_now == global_constants.game.play_by:
                self.message += f" {self.players_time['white']} {self.players_time['black']}"
                global_constants.Connection_manager.send(self.message)
                self.message = ''
        self.choose_figure = self.Figure('', 0, 0, 'empty')
        self.change_color(options)
        self.is_end_of_game(board)
        self.delete_tips()
        self.green_line.show_field(x=-1, y=-1)
        for a in range(8):
            for b in range(8):
                if board[a][b].figure.type == 'pawn':
                    if board[a][b].figure.color == self.color_do_hod_now:
                        board[a][b].figure.do_hod_now = False
        self.list_of_hod_field = []
        return board



