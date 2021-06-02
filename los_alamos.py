import figure_alamos

Figure = figure_alamos.Figure

class Field():
    def __init__(self):
        self.attacked = False
        self.figure = None
    def __str__(self):
        return str(self.figure)


def create_start_game_board():
    board = [[Field() for t in range(6)] for a in range(6)]
    for x in range(6):
        for y in range(6):
            board[x][y].figure = Figure('',0,0,'empty')
            board[x][y].attacked = False

    
    figs = ['rook','horse','queen','king','horse','rook']
    for a in range(6):
        board[a][0].figure = Figure('white',a,0,figs[a])
        board[a][5].figure = Figure('black',a,5,figs[a])
        board[a][1].figure = Figure('white',a,1,'pawn')
        board[a][4].figure = Figure('black',a,4,'pawn')

    return board


def init_chess(game):
    game.board = create_start_game_board()