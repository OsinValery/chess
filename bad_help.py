import bad_figure 
import random
import global_constants

Figure = bad_figure.Figure

class Field():
    def __init__(self):
        self.attacked = False
        self.figure = None
    def __str__(self):
        return str(self.figure)


def create_start_game_board(position=None):
    board = [[Field() for t in range(8)] for a in range(8)]
    for x in range(8):
        for y in range(8):
            board[x][y].figure = Figure('',0,0,'empty')
    for a in range(8):
        for t in range(8):
            board[a][t].attacked = False
    del x,y,a,t
    
    if position == None:
        figs = gen_random_position()
    else:
        figs = []
        for liter in position:
            if liter == 'r':
                figs += ['rook']
            elif liter == 'b':
                figs += ['bishop']
            elif liter == 'h':
                figs += ['horse']
            elif liter == 'k':
                figs += ['king']
            elif liter == 'p':
                figs += ['pawn']
            else:
                figs += ['queen']
    # END OF GEN start position of firures
    cur = 0
    for i in range(8):
        board[i][0].figure = Figure('white',i,0,figs[cur])
        cur += 1
    for i in range(8):
        board[i][1].figure = Figure('white',i,1,figs[cur])
        cur += 1
    # for black
    for i in range(8):
        board[i][6].figure = Figure('black',i,6,figs[cur])
        cur += 1
    for i in range(8):
        board[i][7].figure = Figure('black',i,7,figs[cur])
        cur += 1

    return board


def init_chess(game):
    if global_constants.game.state_game != 'one':
        game.board = create_start_game_board(global_constants.game.position)
        del global_constants.game.position
    else:
        game.board = create_start_game_board()


def gen_random_position():
    possible = ['horse','bishop', 'rook', 'queen', 'pawn']
    figs = ['empty' for x in range(32)]
    figs[4] = 'king'
    figs[28] = 'king'
    for i in range(32):
        if figs[i] == 'empty':
            figs[i] = random.choice(possible)
    return figs