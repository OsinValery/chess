import help_chess
import global_constants
import random
import copy

Figure = help_chess.Figure

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

def is_empty_diapazon(board2,a,b,y,figure):
        if a == b:
            return True
        if a > b:
            a,b = b,a
        for x in range(a,b+1):
            if (board2[x][y].figure.type != 'empty') :
                return False
            elif figure == 'king':
                if (board2[x][y].attacked):
                    return False
        return True

def create_start_game_board(position=None):
    board = [[Field() for t in range(8)] for a in range(8)]
    for x in range(8):
        for y in range(8):
            board[x][y].figure = help_chess.Figure('',0,0,'empty')
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
            else:
                figs += ['queen']
    # END OF GEN start position of firures
    for a in range(8):
        board[a][0].figure = help_chess.Figure('white',a,0,figs[a])
        board[a][7].figure = help_chess.Figure('black',a,7,figs[a])
        board[a][1].figure = help_chess.Figure('white',a,1,'pawn')
        board[a][6].figure = help_chess.Figure('black',a,6,'pawn')

    return board

def do_rocking(board,x,y,choose_figure):
    a,b = choose_figure.x, choose_figure.y
    rook = -1
    if x > a:
        # short rocking
        for n in range(a,8):
            if board[n][b].figure.type == 'rook' and board[n][b].figure.color == choose_figure.color :
                if not board[n][b].figure.do_hod_before :
                    rook = n
    if x < a:
        # long rocking
        for n in range(0,a):
            if board[n][b].figure.type == 'rook' and board[n][b].figure.color == choose_figure.color :
                if not board[n][b].figure.do_hod_before :
                    rook = n
    if rook != -1:
        figure = board[rook][b].figure
        print('ext', figure)

    # this code move king
    board[a][b].figure = Figure('',0,0,'empty')
    board[x][y].figure.destroy()
    board[x][y].figure = choose_figure
    board[x][y].figure.set_coords_on_board(x,y)

    if x == 6 and rook != -1:
        print(figure)
        if figure.type == 'empty':
            figure = Figure(choose_figure.color, rook, b, 'rook')
        if rook != 5:
            board[5][b].figure = figure
            board[5][b].figure.set_coords_on_board(5,b)
            if board[rook][b].figure.type == 'rook':
                # likely, king stay this field
                board[rook][b].figure = Figure('',7,b,'empty')

    if x == 2 and rook != -1:
        print(figure)
        if figure.type == 'empty':
            figure = Figure(choose_figure.color, rook, b, 'rook')
        if rook != 3:
            board[3][b].figure = figure
            board[3][b].figure.set_coords_on_board(3,b)
            if board[rook][b].figure.type == 'rook':
                board[rook][b].figure = Figure('',1,b,'empty')

    return board

def rocking_do_rook(board,figure,fields):
    # when king on the field,where it must stay in the rocking
    king = -1
    for x in range(8):
        if board[x][figure.y].figure.type == 'king' and board[x][figure.y].figure.color == figure.color:
            king = x
    if king == -1:
        # there is not king on the line
        return fields
    y = figure.y

    if king == 6 and figure.x == 7:
        # try to do short rocking
        if board[5][y].figure.type == 'empty':
            fields.append( [5, y] )

    if king == 2 and figure.x in [0,1]:
        # try to do long rocking
        if (figure.x == 0 and board[1][y].figure.type != 'empty'):
            return fields
        if board[3][y].figure.type == 'empty':
            fields.append( [3, y] )
    return fields

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
        # find pos of king
        for x in range(8):
            if board2[x][c].figure.type == 'king' and board2[x][c].figure.color == figure.color:
                king = x
        # king can't do rocking if his field was attacked
        if board2[king][c].attacked:
            return list2
        
        # i take out 1 figure in [king,rook] and see , can another figure move to place in rocking , 
        # if yes, i take this figure and return for another figure
        #короткая рокировка
        count = 0
        # find rook
        for x in range(king+1,8):
            if board2[x][c].figure.type == 'rook' and board2[x][c].figure.color == figure.color:
                rook = x
                count +=1
        # if count != 1 board has not rook right of king or diapazon is not empty,I have not test this fact
        if count == 1 :
            if not board2[rook][c].figure.do_hod_before :
                board2[king][c].figure.type = 'empty'
                if 5 > rook:
                    d = 1
                elif rook > 5:
                    d = -1
                if rook == 5 or is_empty_diapazon(board2,5,rook+d,c,'rook'):
                    board2[king][c].figure.type = 'king'
                    board2[rook][c].figure.type = 'empty'
                    if king == 7:
                        d = -1
                    elif king < 6:
                        d = 1
                    if king == 6 or is_empty_diapazon(board2,6,king+d,c,'king'):
                        list2.append([6,c])
                    board2[rook][c].figure.type = 'rook'
                
        
        count = 0
        # long rocking
        # this code copy algoritm of short rocking
        for x in range(0,king):
            if board2[x][c].figure.type == 'rook' and board2[x][c].figure.color == figure.color:
                rook = x
                count +=1
        if count == 1 :
            if not board2[rook][c].figure.do_hod_before :
                board2[king][c].figure.type = 'empty'
                if rook > 3:
                    d = -1
                elif rook < 3:
                    d = 1
                if rook == 3 or is_empty_diapazon(board2,3,rook+d,c,'rook'):
                    board2[king][c].figure.type = 'king'
                    board2[rook][c].figure.type = 'empty'
                    if king > 2:
                        d = -1
                    elif king < 2:
                        d = 1
                    if king == 2 or is_empty_diapazon(board2,2,king+d,c,'king'):
                        list2.append([2,c])
                    board2[rook][c].figure.type = 'rook'

        return list2

def is_it_rocking(figure,board,field):
    x,y = figure.x,figure.y
    king = -1
    for a in range(8):
        if board[a][y].figure.type == 'king' and board[a][y].figure.color == figure.color:
            king = a
    if king != -1:
        if king == 6 and x == 7 and field == 5:
            board[king][y].figure.do_hod_before = True
        if king  == 2 and x in [0,1]:
            if field == 3:
                board[king][y].figure.do_hod_before = True

def init_chess(game):
    if global_constants.game.state_game != 'one':
        game.board = create_start_game_board(global_constants.game.position)
        del global_constants.game.position
    else:
        game.board = create_start_game_board()
    game.do_rocking = do_rocking
    game.can_do_rocking = can_do_rocking
    game.rocking_do_rook = rocking_do_rook
    game.is_it_rocking = is_it_rocking



def gen_random_position():
    figs = ['empty' for x in range(8)]
    #there are  960 random start positions
    king = random.randint(2,6)
    figs[king] = 'king'
    rook = random.randint(king+1,7)
    figs[rook] = 'rook'
    rook = random.randint(0,king-1)
    figs[rook] = 'rook'
    # white empty fields
    empty = [x for x in range(0,8,2) if figs[x] == 'empty']
    bishop = random.choice(empty)
    figs[bishop] = 'bishop'
    # black empty fields
    empty = [x for x in range(1,8,2) if figs[x] == 'empty']
    bishop = random.choice(empty)
    figs[bishop] = 'bishop'
    # all empty fields in this moment ,it is 3 fields
    empty = [x for x in range(8) if figs[x] == 'empty']
    figure = ['horse','horse','queen']
    for x in range(3):
        pos = random.choice(empty)
        empty.remove(pos)
        figs[pos] = figure[x]
    return figs