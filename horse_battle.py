import help_chess

Figure = help_chess.Figure

class Field():
    def __init__(self):
        self.attacked = False
        self.figure = None
    def __str__(self):
        return str(self.figure)


def create_start_game_board():
    board = [[Field() for t in range(8)] for a in range(8)]
    for x in range(8):
        for y in range(8):
            board[x][y].figure = help_chess.Figure('',0,0,'empty')
    for a in range(8):
        for t in range(8):
            board[a][t].attacked = False
    
    figs = ['horse','horse','horse','horse','king','horse','horse','horse']
    for a in range(8):
        board[a][0].figure = help_chess.Figure('white',a,0,figs[a])
        board[a][7].figure = help_chess.Figure('black',a,7,figs[a])
        board[a][1].figure = help_chess.Figure('white',a,1,'pawn')
        board[a][6].figure = help_chess.Figure('black',a,6,'pawn')

    return board

def do_rocking(board,x,y,choose_figure):
    a , b = choose_figure.x , choose_figure.y
    board[a][b].figure = Figure('',0,0,'empty')
    board[x][y].figure.destroy()
    board[x][y].figure = choose_figure
    board[x][y].figure.set_coords_on_board(x,y)
    return board

def can_do_rocking(my_game,board,figure,list2):
    return list2


def init_chess(game):
    game.board = create_start_game_board()
    game.do_rocking = do_rocking
    game.can_do_rocking = can_do_rocking