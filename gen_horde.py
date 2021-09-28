import horde_figure
import copy

Figure = horde_figure.Figure

class Field():
    def __init__(self):
        self.attacked = False
        self.figure = None
    def __str__(self):
        return str(self.figure)

def copy_board(board):
    new_board = [[Field() for t in range(8)] for a in range(8)]
    for a in range(8):
        for b in range(8):
            new_board[a][b].figure = Figure('white',0,0,'')
            new_board[a][b].figure.color = copy.copy(board[a][b].figure.color)
            new_board[a][b].figure.type = copy.copy(board[a][b].figure.type)
            new_board[a][b].figure.do_hod_before = copy.copy(board[a][b].figure.do_hod_before)

    return new_board

def create_start_game_board():
    board = [[Field() for t in range(8)] for a in range(8)]
    for x in range(8):
        for y in range(8):
            board[x][y].figure = horde_figure.Figure('',0,0,'empty')
    for a in range(8):
        for t in range(8):
            board[a][t].attacked = False
    
    figs = ['rook','horse','bishop','queen','king','bishop','horse','rook']
    for a in range(8):
        board[a][7].figure = horde_figure.Figure('black',a,7,figs[a])
        board[a][6].figure = horde_figure.Figure('black',a,6,'pawn')
        for y in range(0,4):
            board[a][y].figure = Figure('white',a,y,'pawn')
    for  a in [1,2,5,6]:
            board[a][4].figure = Figure('white',a,4,'pawn')

    return board

def do_rocking(board,x,y,choose_figure):
    a , b = choose_figure.x , choose_figure.y
    board[a][b].figure = Figure('',0,0,'empty')
    board[x][y].figure.destroy()
    board[x][y].figure = choose_figure
    board[x][y].figure.set_coords_on_board(x,y)
    if x == 6:
        board[5][choose_figure.y].figure = board[7][choose_figure.y].figure
        board[7][b].figure = Figure('',7,b,'empty')
        board[5][b].figure.do_hod_before = True
        board[5][b].figure.set_coords_on_board(5,b)
    if x == 2 :
        board[3][choose_figure.y].figure = board[0][choose_figure.y].figure
        board[0][b].figure = Figure('',1,b,'empty')
        board[3][b].figure.do_hod_before = True
        board[3][b].figure.set_coords_on_board(3,b)
        del x,b
    return board

def can_do_rocking(my_game,board,figure,list2):
        c = figure.y
        board2 = copy_board(board)
        for a in board2:
            for b in a:
                b.attacked = False
        for x in range(8):
            for y in range(8):
                if board2[x][y].figure.color != my_game.color_do_hod_now:
                    board2 = board[x][y].figure.do_attack(board2)
        #короткая рокировка
        if board[6][c].figure.type == 'empty' and board[5][c].figure.type == 'empty':
            if not board2[5][c].attacked and not board2[6][c].attacked and not board2[4][c].attacked:
                if board[7][c].figure.type == 'rook' and not board[7][c].figure.do_hod_before and \
                board[7][c].figure.color == figure.color :
                    list2.append([6,c]) 
        #длинная
        if board[1][c].figure.type == 'empty' and board[2][c].figure.type == 'empty' and \
        board[3][c].figure.type == 'empty':
            if not board2[2][c].attacked and not board2[3][c].attacked:      
                if not board2[4][c].attacked:
                    if board[0][c].figure.type == 'rook' and not board[0][c].figure.do_hod_before and \
                    board[0][c].figure.color == figure.color :
                        list2.append([2,c])
        return list2


def init_chess(game):
    game.board = create_start_game_board()
    game.do_rocking = do_rocking
    game.can_do_rocking = can_do_rocking