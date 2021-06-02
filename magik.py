import random
import copy
import help_chess
Figure = help_chess.Figure

def choose_magia(board):
    w = 0
    b = 0
    e = 0
    for (x,y) in (3,3),(3,4),(4,3),(4,4):
            if board[x][y].figure.type == 'empty':
                e += 1
            elif board[x][y].figure.color == 'white':
                w += 1
            else:
                b += 1
    var = [1,2,3,4,5]
    if (w == b and w != 0) or e == 0:
            var.remove(4)
    if e == 4:
            var.remove(3)
            var.remove(2)
            var.remove(1)
            var.remove(5)
    magia = 0
    if var != []:
        magia = random.choice(var)
    return magia

def magia_for_network_gen(board):
    magia = choose_magia(board)
    w = 0
    b = 0
    e = 0
    for (x,y) in (3,3),(3,4),(4,3),(4,4):
            if board[x][y].figure.type == 'empty':
                e += 1
            elif board[x][y].figure.color == 'white':
                w += 1
            else:
                b += 1
    case = f'{magia},'

    if magia == 1:
        case += random.choice(['rook','horse','bishop','pawn','queen'])
    elif magia in [2,3]:
        pass
    elif magia == 4:
        if w == b:
            color = random.choice(['white','black'])
        elif w > b:
            color = 'white'
        else:
            color = 'black'
        tip = random.choice(['rook','horse','bishop','pawn','queen'])
        fields = []
        for (x,y) in (3,3),(3,4),(4,3),(4,4):
            if board[x][y].figure.type == 'empty':
                fields.append([x,y])
        (x,y) = random.choice(fields)
        case += f'{x},{y},{color},{tip}'
    elif magia == 5:
        figs = [1,2,3,4]
        for i in range(100):
            if random.randint(0,50) % 7:
                x,y = random.randint(0,3),random.randint(0,3)
                if x != y:
                    figs[x],figs[y] = figs[y],figs[x]
        for el in figs:
            case += f'{el}'
    
    return case

def magia_for_network_run(board,case:str):
    case = case.split(',')
    case[0] = int(case[0])

    if case[0] == 1:
        figure = case[1]
        for (x,y) in (3,3),(3,4),(4,3),(4,4):
            if board[x][y].figure.type not in  ['empty','king']:
                color = board[x][y].figure.color
                board[x][y].figure.destroy()
                board[x][y].figure = Figure(color,x,y,figure)
    
    elif case[0] == 2:
        for (x,y) in (3,3),(3,4),(4,3),(4,4):
            if board[x][y].figure.type not in ['empty','king']:
                board[x][y].figure.destroy()
                board[x][y].figure = Figure('',x,y,'empty')
    elif case[0] == 3:
        for (x,y) in (3,3),(3,4),(4,3),(4,4):
            if board[x][y].figure.type not in ['empty','king']:
                color = board[x][y].figure.color
                if color == 'white':
                    color = 'black'
                else:
                    color = 'white'
                board[x][y].figure.destroy()
                board[x][y].figure = Figure(color,x,y,board[x][y].figure.type)
    
    elif case[0] == 4:
        x = int(case[1])
        y = int(case[2])
        color = case[3]
        tip = case[4]
        board[x][y].figure = Figure(color,x,y,tip)
    
    elif case[0] == 5:
        pos = [int(i) - 1 for i in case[1]]
        figs = []
        for [x,y] in [3,3],[3,4],[4,3],[4,4]:
            figs.append(board[x][y].figure)
        for i in 0,1,2,3:
            x,y = [[3,3],[3,4],[4,3],[4,4] ][i]
            board[x][y].figure = figs[pos[i]]
            figs[pos[i]].x = x
            figs[pos[i]].y = y
            if figs[pos[i]].type != 'empty':
                figs[pos[i]].set_coords_on_board(x,y)

def magik(board,magia=0):
    #1.все фигуры превращаются в пешек, коней, слонов, ладей, либо ферзей
    #2.все фигуры погибают
    #3.все фигуры меняют цвет на проиивоположный, т.е. становятся предателями
    #4.в этом квадрате рождается фигура, и в зависимости от тогo
    # каких фигур больше в этом квадрате, тому она и будет 
    # принадлежать, дабы стимулировать игроков гнать фигуры в центр.
    #5. все фигуры перемешиваются
    if magia == 0:
        magia = choose_magia(board)
    w = 0
    b = 0
    e = 0
    for (x,y) in (3,3),(3,4),(4,3),(4,4):
            if board[x][y].figure.type == 'empty':
                e += 1
            elif board[x][y].figure.color == 'white':
                w += 1
            else:
                b += 1

    if magia == 1:
        figure = random.choice(['rook','horse','bishop','pawn','queen'])
        for (x,y) in (3,3),(3,4),(4,3),(4,4):
            if board[x][y].figure.type not in  ['empty','king']:
                color = board[x][y].figure.color
                board[x][y].figure.destroy()
                board[x][y].figure = Figure(color,x,y,figure)
    elif magia == 2:
        for (x,y) in (3,3),(3,4),(4,3),(4,4):
            if board[x][y].figure.type not in ['empty','king']:
                board[x][y].figure.destroy()
                board[x][y].figure = Figure('',x,y,'empty')
    elif magia == 3:
        for (x,y) in (3,3),(3,4),(4,3),(4,4):
            if board[x][y].figure.type not in ['empty','king']:
                color = board[x][y].figure.color
                if color == 'white':
                    color = 'black'
                else:
                    color = 'white'
                board[x][y].figure.destroy()
                board[x][y].figure = Figure(color,x,y,board[x][y].figure.type)
    elif magia == 4:
        if w == b:
            color = random.choice(['white','black'])
        elif w > b:
            color = 'white'
        else:
            color = 'black'
        tip = random.choice(['rook','horse','bishop','pawn','queen'])
        fields = []
        for (x,y) in (3,3),(3,4),(4,3),(4,4):
            if board[x][y].figure.type == 'empty':
                fields.append([x,y])
        (x,y) = random.choice(fields)
        board[x][y].figure = Figure(color,x,y,tip)
    elif magia == 5:
        figs = []
        for [x,y] in [3,3],[3,4],[4,3],[4,4]:
            figs.append(board[x][y].figure)
        for i in range(100):
            if random.randint(0,50) % 7:
                x,y = random.randint(0,3),random.randint(0,3)
                if x != y:
                    figs[x],figs[y] = figs[y],figs[x]
        for i in 0,1,2,3:
            x,y = [[3,3],[3,4],[4,3],[4,4] ][i]
            board[x][y].figure = figs[i]
            figs[i].x = x
            figs[i].y = y
            if figs[i].type != 'empty':
                figs[i].set_coords_on_board(x,y)


    
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
            board[x][y].figure = help_chess.Figure('',0,0,'empty')
    for a in range(8):
        for t in range(8):
            board[a][t].attacked = False
    
    figs = ['rook','horse','bishop','queen','king','bishop','horse','rook']
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

def clear(game):
    del game.clear
    del game.do_rocking
    del game.can_do_rocking


def init_chess(game):
    game.board = create_start_game_board()
    game.do_rocking = do_rocking
    game.can_do_rocking = can_do_rocking
    game.clear = clear