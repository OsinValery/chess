import random
import copy
import help_chess
Figure = help_chess.Figure
import global_constants

########################################################################
# magia
#########################################################################

def choose_magia(board,e_x,e_y):
    w = 0
    b = 0
    e = 0
    for (x,y) in (e_x,e_y),(e_x,e_y+1),(e_x+1,e_y),(e_x+1,e_y+1):
            if board[x][y].figure.type == 'empty':
                e += 1
            elif board[x][y].figure.color == 'white':
                w += 1
            else:
                b += 1
    var = [0,1,2,3,4,5,10,11]
    if (w == b and w != 0) or e == 0:
            var.remove(4)
    if e == 4:
            var.remove(3)
            var.remove(2)
            var.remove(1)
            var.remove(5)
    if w + b > 1:
        var.append(6)
        var.append(7)
    
    h = 0
    for x in range(8):
        if board[x][e_y].figure.type != 'empty':
            if board[x][e_y].figure.color == global_constants.game.Game_logik.color_do_hod_now:
                h += 1
    if h > 1:
        var += [8,9]

    # choose variant
    magia = 0
    if var != []:
        magia = random.choice(var)
    return magia

def magia_for_network_gen(board):
    e_x, e_y = random.randint(0,6), random.randint(0,6)    
    magia = choose_magia(board,e_x,e_y)
    w = 0
    b = 0
    e = 0
    for (x,y) in (e_x,e_y),(e_x,e_y+1),(e_x+1,e_y),(e_x+1,e_y+1):
            if board[x][y].figure.type == 'empty':
                e += 1
            elif board[x][y].figure.color == 'white':
                w += 1
            else:
                b += 1
    case = f'{magia},{e_x},{e_y},'

    if magia == 1:
        case += random.choice(['rook','horse','bishop','pawn','queen'])
    elif magia in [2,3,8,9,10,11]:
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
        for (x,y) in (e_x,e_y),(e_x,e_y+1),(e_x+1,e_y),(e_x+1,e_y+1):
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
    elif magia in [6, 7]:
        coords = []
        for (x,y) in (e_x,e_y),(e_x,e_y+1),(e_x+1,e_y),(e_x+1,e_y+1):
            if board[x][y].figure.type != 'empty':
                coords += [[x,y]]
        (x,y) = random.choice(coords)
        case += f'{x},{y}'
    
    return case

def magia_for_network_run(board,case:str):
    case = case.split(',')
    case[0] = int(case[0])
    e_x, e_y = case[1:3]
    e_x, e_y = int(e_x), int(e_y)

    if case[0] == 1:
        figure = case[3]
        for (x,y) in (e_x,e_y),(e_x,e_y+1),(e_x+1,e_y),(e_x+1,e_y+1):
            if board[x][y].figure.type not in  ['empty','king']:
                color = board[x][y].figure.color
                board[x][y].figure.destroy()
                board[x][y].figure = Figure(color,x,y,figure)
    
    elif case[0] == 2:
        for (x,y) in (e_x,e_y),(e_x,e_y+1),(e_x+1,e_y),(e_x+1,e_y+1):
            if board[x][y].figure.type not in ['empty','king']:
                board[x][y].figure.destroy()
    elif case[0] == 3:
        for (x,y) in (e_x,e_y),(e_x,e_y+1),(e_x+1,e_y),(e_x+1,e_y+1):
            if board[x][y].figure.type not in ['empty','king']:
                color = board[x][y].figure.color
                if color == 'white':
                    color = 'black'
                else:
                    color = 'white'
                board[x][y].figure.destroy()
                board[x][y].figure = Figure(color,x,y,board[x][y].figure.type)

    elif case[0] == 4:
        x = int(case[3])
        y = int(case[4])
        color = case[5]
        tip = case[6]
        board[x][y].figure = Figure(color,x,y,tip)

    elif case[0] == 5:
        pos = [int(i) - 1 for i in case[3]]
        figs = []
        for [x,y] in (e_x,e_y),(e_x,e_y+1),(e_x+1,e_y),(e_x+1,e_y+1):
            figs.append(board[x][y].figure)
        for i in 0,1,2,3:
            x,y = [(e_x,e_y),(e_x,e_y+1),(e_x+1,e_y),(e_x+1,e_y+1)][i]
            if not board[x][y].figure is figs[pos[i]]:
                figs[pos[i]].do_hod_before = True
            board[x][y].figure = figs[pos[i]]
            figs[pos[i]].x = x
            figs[pos[i]].y = y
            if figs[pos[i]].type != 'empty':
                figs[pos[i]].set_coords_on_board(x,y)
    elif case[0] == 6:
        x, y = case[3:5]
        x, y = int(x), int(y)
        if y < 6:
            # up
            if board[x][y+1].figure.type != 'empty' and board[x][y+2].figure.type == 'empty':
                board[x][y+1].figure, board[x][y+2].figure = board[x][y+2].figure, board[x][y+1].figure
                board[x][y+2].figure.set_coords_on_board(x,y+2)
        if y > 1:
            # down
            if board[x][y-1].figure.type != 'empty' and board[x][y-2].figure.type == 'empty':
                board[x][y-1].figure, board[x][y-2].figure = board[x][y-2].figure, board[x][y-1].figure
                board[x][y-2].figure.set_coords_on_board(x,y-2)
        if x > 1:
            # left
            if board[x-1][y].figure.type != 'empty' and board[x-2][y].figure.type == 'empty':
                board[x-1][y].figure, board[x-2][y].figure = board[x-2][y].figure, board[x-1][y].figure
                board[x-2][y].figure.set_coords_on_board(x-2,y)
        if x < 6:
            # right
            if board[x+1][y].figure.type != 'empty' and board[x+2][y].figure.type == 'empty':
                board[x+2][y].figure, board[x+1][y].figure = board[x+1][y].figure, board[x+2][y].figure
                board[x+2][y].figure.set_coords_on_board(x+2,y)

    elif case[0] == 7:
        x, y = case[3:5]
        x, y = int(x), int(y)
        if y < 6:
            # up
            if board[x][y+1].figure.type != 'empty' and board[x][y+2].figure.type == 'empty':
                board[x][y+1].figure, board[x][y+2].figure = board[x][y+2].figure, board[x][y+1].figure
                board[x][y+2].figure.set_coords_on_board(x,y+2)
        if y > 1:
            # down
            if board[x][y-1].figure.type != 'empty' and board[x][y-2].figure.type == 'empty':
                board[x][y-1].figure, board[x][y-2].figure = board[x][y-2].figure, board[x][y-1].figure
                board[x][y-2].figure.set_coords_on_board(x,y-2)
        if x > 1:
            # left
            if board[x-1][y].figure.type != 'empty' and board[x-2][y].figure.type == 'empty':
                board[x-1][y].figure, board[x-2][y].figure = board[x-2][y].figure, board[x-1][y].figure
                board[x-2][y].figure.set_coords_on_board(x-2,y)
        if x < 6:
            # right
            if board[x+1][y].figure.type != 'empty' and board[x+2][y].figure.type == 'empty':
                board[x+2][y].figure, board[x+1][y].figure = board[x+1][y].figure, board[x+2][y].figure
                board[x+2][y].figure.set_coords_on_board(x+2,y)
        if x > 1 and y > 1:
            # down - left
            if board[x-1][y-1].figure.type != 'empty' and board[x-2][y-2].figure.type == 'empty':
                board[x-1][y-1].figure, board[x-2][y-2].figure = board[x-2][y-2].figure, board[x-1][y-1].figure
                board[x-2][y-2].figure.set_coords_on_board(x-2,y-2)
        if x > 1 and y < 6:
            # up - left
            if board[x-1][y+1].figure.type != 'empty' and board[x-2][y+2].figure.type == 'empty':
                board[x-1][y+1].figure, board[x-2][y+2].figure = board[x-2][y+2].figure, board[x-1][y+1].figure
                board[x-2][y+2].figure.set_coords_on_board(x-2,y+2)
        if x < 6 and y < 6:
            # up - right
            if board[x+1][y+1].figure.type != 'empty' and board[x+2][y+2].figure.type == 'empty':
                board[x+1][y+1].figure, board[x+2][y+2].figure = board[x+2][y+2].figure, board[x+1][y+1].figure
                board[x+2][y+2].figure.set_coords_on_board(x+2,y+2)
        if x < 6 and y > 1:
            # down - right
            if board[x+1][y-1].figure.type != 'empty' and board[x+2][y-2].figure.type == 'empty':
                board[x+1][y-1].figure, board[x+2][y-2].figure = board[x+2][y-2].figure, board[x+1][y-1].figure
                board[x+2][y-2].figure.set_coords_on_board(x+2,y-2)

    elif case[0] == 8:
        for x in range(8):
            if board[x][e_y].figure.color == global_constants.game.Game_logik.color_do_hod_now:
                if board[x][e_y].figure.color == 'white' and e_y != 7:
                    if board[x][e_y+1].figure.type == 'empty' and \
                        board[x][e_y].figure.type != 'empty':
                            board[x][e_y].figure, board[x][e_y+1].figure =   \
                                    board[x][e_y+1].figure, board[x][e_y].figure
                            board[x][e_y+1].figure.set_coords_on_board(x,e_y+1)
                            board[x][e_y+1].figure.do_hod_before = True
                elif board[x][e_y].figure.color == 'black' and e_y != 0:
                    if board[x][e_y-1].figure.type == 'empty' and \
                        board[x][e_y].figure.type != 'empty':
                        board[x][e_y].figure, board[x][e_y-1].figure = \
                            board[x][e_y-1].figure, board[x][e_y].figure
                        board[x][e_y-1].figure.set_coords_on_board(x,e_y-1)
                        board[x][e_y-1].figure.do_hod_before = True
    elif case[0] == 9:
        for x in range(8):
            if board[x][e_y].figure.color == global_constants.game.Game_logik.color_do_hod_now:
                if board[x][e_y].figure.color == 'black' and e_y != 7:
                    if board[x][e_y+1].figure.type == 'empty' and \
                        board[x][e_y].figure.type != 'empty':
                            board[x][e_y].figure, board[x][e_y+1].figure =   \
                                    board[x][e_y+1].figure, board[x][e_y].figure
                            board[x][e_y+1].figure.set_coords_on_board(x,e_y+1)
                            board[x][e_y+1].figure.do_hod_before = True
                elif board[x][e_y].figure.color == 'white' and e_y != 0:
                    if board[x][e_y-1].figure.type == 'empty' and \
                        board[x][e_y].figure.type != 'empty':
                        board[x][e_y].figure, board[x][e_y-1].figure = \
                            board[x][e_y-1].figure, board[x][e_y].figure
                        board[x][e_y-1].figure.set_coords_on_board(x,e_y-1)
                        board[x][e_y-1].figure.do_hod_before = True
    elif case[0] == 10:
        if global_constants.game.Game_logik.color_do_hod_now == 'white':
            for x in range(8):
                for y in range(1,8):
                    if board[x][y-1].figure.type == 'empty' and board[x][y].figure.type != 'empty':
                        if board[x][y].figure.color == 'white':
                            board[x][y].figure, board[x][y-1].figure = \
                                board[x][y-1].figure, board[x][y].figure
                            board[x][y-1].figure.set_coords_on_board(x,y-1)
                            board[x][y-1].figure.do_hod_before = True
        else:
            for x in range(8):
                for y in range(6,-1,-1):
                    if board[x][y].figure.type != 'empty' and board[x][y].figure.color == 'black':
                        if board[x][y+1].figure.type == 'empty':
                            board[x][y].figure, board[x][y+1].figure = \
                                board[x][y+1].figure, board[x][y].figure
                            board[x][y+1].figure.set_coords_on_board(x,y+1)
                            board[x][y+1].figure.do_hod_before = True
    elif case[0] == 11:
        if global_constants.game.Game_logik.color_do_hod_now == 'white':
            for x in range(8):
                for y in range(6,-1,-1):
                    if board[x][y].figure.color == 'white' and board[x][y].figure.type != 'empty':
                        if board[x][y+1].figure.type == 'empty':
                            board[x][y].figure, board[x][y+1].figure = \
                                board[x][y+1].figure, board[x][y].figure
                            board[x][y+1].figure.set_coords_on_board(x,y+1)
                            board[x][y+1].figure.do_hod_before = True
        else:
            for x in range(8):
                for y in range(1,8):
                    if board[x][y].figure.type != 'empty':
                        if board[x][y].figure.color == 'black':
                            if board[x][y-1].figure.type == 'empty':
                                board[x][y].figure, board[x][y-1].figure = \
                                    board[x][y-1].figure, board[x][y].figure
                                board[x][y-1].figure.do_hod_before = True
                                board[x][y-1].figure.set_coords_on_board(x,y-1)

def magik(board,magia=0):
    '''
    0.nothing
    1.все фигуры превращаются в пешек, коней, слонов, ладей, либо ферзей
    2.все фигуры погибают
    3.все фигуры меняют цвет на проиивоположный, т.е. становятся предателями
    4.в этом квадрате рождается фигура, и в зависимости от тогo
    # каких фигур больше в этом квадрате, тому она и будет 
    # принадлежать, дабы стимулировать игроков гнать фигуры в центр.
    5. все фигуры перемешиваются
    6. взрыв малый - по вертикали и горизонтали
    7. взрыв большой - во все стороны
    8. личная инициатива - часть фигур выдвигается на 1 поле в сторону врага
    9. отступают
    10. все совсем фигуры отступают
    11. нападают

    10. предательство - фигура рубит свою фигуру
    11. временные фигуры на пару ходов
    12. общая фигура(ходить ей могут оба и срубить тоже)

    другое
    '''
    e_x, e_y = random.randint(0,6), random.randint(0,6)
    if magia == 0:
        magia = choose_magia(board,e_x,e_y)
    w = 0
    b = 0
    e = 0
    for (x,y) in (e_x,e_y),(e_x,e_y+1),(e_x+1,e_y),(e_x+1,e_y+1):
        if board[x][y].figure.type == 'empty':
            e += 1
        elif board[x][y].figure.color == 'white':
            w += 1
        else:
            b += 1

    if magia == 1:
        figure = random.choice(['rook','horse','bishop','pawn','queen'])
        for (x,y) in (e_x,e_y),(e_x,e_y+1),(e_x+1,e_y),(e_x+1,e_y+1):
            if board[x][y].figure.type not in  ['empty','king']:
                color = board[x][y].figure.color
                board[x][y].figure.destroy()
                board[x][y].figure = Figure(color,x,y,figure)
    elif magia == 2:
        for (x,y) in (e_x,e_y),(e_x,e_y+1),(e_x+1,e_y),(e_x+1,e_y+1):
            if board[x][y].figure.type not in ['empty','king']:
                board[x][y].figure.destroy()
    elif magia == 3:
        for (x,y) in (e_x,e_y),(e_x,e_y+1),(e_x+1,e_y),(e_x+1,e_y+1):
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
        for (x,y) in (e_x,e_y),(e_x,e_y+1),(e_x+1,e_y),(e_x+1,e_y+1):
            if board[x][y].figure.type == 'empty':
                fields.append([x,y])
        (x,y) = random.choice(fields)
        board[x][y].figure.destroy()
        board[x][y].figure = Figure(color,x,y,tip)
    elif magia == 5:
        figs = []
        for [x,y] in (e_x,e_y),(e_x,e_y+1),(e_x+1,e_y),(e_x+1,e_y+1):
            figs.append(board[x][y].figure)
        for i in range(100):
            if random.randint(0,50) % 7:
                x,y = random.randint(0,3),random.randint(0,3)
                if x != y:
                    figs[x],figs[y] = figs[y],figs[x]
        for i in 0,1,2,3:
            x,y = [(e_x,e_y),(e_x,e_y+1),(e_x+1,e_y),(e_x+1,e_y+1)][i]
            if not board[x][y].figure is figs[i]:
                figs[i].do_hod_before = True
            board[x][y].figure = figs[i]
            figs[i].x = x
            figs[i].y = y
            if figs[i].type != 'empty':
                figs[i].set_coords_on_board(x,y)
    elif magia == 6:
        coords = []
        for (x,y) in (e_x,e_y),(e_x,e_y+1),(e_x+1,e_y),(e_x+1,e_y+1):
            if board[x][y].figure.type != 'empty':
                coords += [[x,y]]
        (x,y) = random.choice(coords)
        if y < 6:
            # up
            if board[x][y+1].figure.type != 'empty' and board[x][y+2].figure.type == 'empty':
                board[x][y+1].figure, board[x][y+2].figure = board[x][y+2].figure, board[x][y+1].figure
                board[x][y+2].figure.set_coords_on_board(x,y+2)
        if y > 1:
            # down
            if board[x][y-1].figure.type != 'empty' and board[x][y-2].figure.type == 'empty':
                board[x][y-1].figure, board[x][y-2].figure = board[x][y-2].figure, board[x][y-1].figure
                board[x][y-2].figure.set_coords_on_board(x,y-2)
        if x > 1:
            # left
            if board[x-1][y].figure.type != 'empty' and board[x-2][y].figure.type == 'empty':
                board[x-1][y].figure, board[x-2][y].figure = board[x-2][y].figure, board[x-1][y].figure
                board[x-2][y].figure.set_coords_on_board(x-2,y)
        if x < 6:
            # right
            if board[x+1][y].figure.type != 'empty' and board[x+2][y].figure.type == 'empty':
                board[x+2][y].figure, board[x+1][y].figure = board[x+1][y].figure, board[x+2][y].figure
                board[x+2][y].figure.set_coords_on_board(x+2,y)
    elif magia == 7:
        coords = []
        for (x,y) in (e_x,e_y),(e_x,e_y+1),(e_x+1,e_y),(e_x+1,e_y+1):
            if board[x][y].figure.type != 'empty':
                coords += [[x,y]]
        (x,y) = random.choice(coords)
        if y < 6:
            # up
            if board[x][y+1].figure.type != 'empty' and board[x][y+2].figure.type == 'empty':
                board[x][y+1].figure, board[x][y+2].figure = board[x][y+2].figure, board[x][y+1].figure
                board[x][y+2].figure.set_coords_on_board(x,y+2)
        if y > 1:
            # down
            if board[x][y-1].figure.type != 'empty' and board[x][y-2].figure.type == 'empty':
                board[x][y-1].figure, board[x][y-2].figure = board[x][y-2].figure, board[x][y-1].figure
                board[x][y-2].figure.set_coords_on_board(x,y-2)
        if x > 1:
            # left
            if board[x-1][y].figure.type != 'empty' and board[x-2][y].figure.type == 'empty':
                board[x-1][y].figure, board[x-2][y].figure = board[x-2][y].figure, board[x-1][y].figure
                board[x-2][y].figure.set_coords_on_board(x-2,y)
        if x < 6:
            # right
            if board[x+1][y].figure.type != 'empty' and board[x+2][y].figure.type == 'empty':
                board[x+2][y].figure, board[x+1][y].figure = board[x+1][y].figure, board[x+2][y].figure
                board[x+2][y].figure.set_coords_on_board(x+2,y)
        if x > 1 and y > 1:
            # down - left
            if board[x-1][y-1].figure.type != 'empty' and board[x-2][y-2].figure.type == 'empty':
                board[x-1][y-1].figure, board[x-2][y-2].figure = board[x-2][y-2].figure, board[x-1][y-1].figure
                board[x-2][y-2].figure.set_coords_on_board(x-2,y-2)
        if x > 1 and y < 6:
            # up - left
            if board[x-1][y+1].figure.type != 'empty' and board[x-2][y+2].figure.type == 'empty':
                board[x-1][y+1].figure, board[x-2][y+2].figure = board[x-2][y+2].figure, board[x-1][y+1].figure
                board[x-2][y+2].figure.set_coords_on_board(x-2,y+2)
        if x < 6 and y < 6:
            # up - right
            if board[x+1][y+1].figure.type != 'empty' and board[x+2][y+2].figure.type == 'empty':
                board[x+1][y+1].figure, board[x+2][y+2].figure = board[x+2][y+2].figure, board[x+1][y+1].figure
                board[x+2][y+2].figure.set_coords_on_board(x+2,y+2)
        if x < 6 and y > 1:
            # down - right
            if board[x+1][y-1].figure.type != 'empty' and board[x+2][y-2].figure.type == 'empty':
                board[x+1][y-1].figure, board[x+2][y-2].figure = board[x+2][y-2].figure, board[x+1][y-1].figure
                board[x+2][y-2].figure.set_coords_on_board(x+2,y-2)
    elif magia == 8:
        for x in range(8):
            if board[x][e_y].figure.color == global_constants.game.Game_logik.color_do_hod_now:
                if board[x][e_y].figure.color == 'white' and e_y != 7:
                    if board[x][e_y+1].figure.type == 'empty' and \
                        board[x][e_y].figure.type != 'empty':
                            board[x][e_y].figure, board[x][e_y+1].figure =   \
                                    board[x][e_y+1].figure, board[x][e_y].figure
                            board[x][e_y+1].figure.set_coords_on_board(x,e_y+1)
                            board[x][e_y+1].figure.do_hod_before = True
                elif board[x][e_y].figure.color == 'black' and e_y != 0:
                    if board[x][e_y-1].figure.type == 'empty' and \
                        board[x][e_y].figure.type != 'empty':
                        board[x][e_y].figure, board[x][e_y-1].figure = \
                            board[x][e_y-1].figure, board[x][e_y].figure
                        board[x][e_y-1].figure.set_coords_on_board(x,e_y-1)
                        board[x][e_y-1].figure.do_hod_before = True
    elif magia == 9:
        for x in range(8):
            if board[x][e_y].figure.color == global_constants.game.Game_logik.color_do_hod_now:
                if board[x][e_y].figure.color == 'black' and e_y != 7:
                    if board[x][e_y+1].figure.type == 'empty' and \
                        board[x][e_y].figure.type != 'empty':
                            board[x][e_y].figure, board[x][e_y+1].figure =   \
                                    board[x][e_y+1].figure, board[x][e_y].figure
                            board[x][e_y+1].figure.set_coords_on_board(x,e_y+1)
                            board[x][e_y+1].figure.do_hod_before = True
                elif board[x][e_y].figure.color == 'white' and e_y != 0:
                    if board[x][e_y-1].figure.type == 'empty' and \
                        board[x][e_y].figure.type != 'empty':
                        board[x][e_y].figure, board[x][e_y-1].figure = \
                            board[x][e_y-1].figure, board[x][e_y].figure
                        board[x][e_y-1].figure.set_coords_on_board(x,e_y-1)
                        board[x][e_y-1].figure.do_hod_before = True
    elif magia == 10:
        if global_constants.game.Game_logik.color_do_hod_now == 'white':
            for x in range(8):
                for y in range(1,8):
                    if board[x][y-1].figure.type == 'empty' and board[x][y].figure.type != 'empty':
                        if board[x][y].figure.color == 'white':
                            board[x][y].figure, board[x][y-1].figure = \
                                board[x][y-1].figure, board[x][y].figure
                            board[x][y-1].figure.set_coords_on_board(x,y-1)
                            board[x][y-1].figure.do_hod_before = True
        else:
            for x in range(8):
                for y in range(6,-1,-1):
                    if board[x][y].figure.type != 'empty' and board[x][y].figure.color == 'black':
                        if board[x][y+1].figure.type == 'empty':
                            board[x][y].figure, board[x][y+1].figure = \
                                board[x][y+1].figure, board[x][y].figure
                            board[x][y+1].figure.set_coords_on_board(x,y+1)
                            board[x][y+1].figure.do_hod_before = True
    elif magia == 11:
        if global_constants.game.Game_logik.color_do_hod_now == 'white':
            for x in range(8):
                for y in range(6,-1,-1):
                    if board[x][y].figure.color == 'white' and board[x][y].figure.type != 'empty':
                        if board[x][y+1].figure.type == 'empty':
                            board[x][y].figure, board[x][y+1].figure = \
                                board[x][y+1].figure, board[x][y].figure
                            board[x][y+1].figure.set_coords_on_board(x,y+1)
                            board[x][y+1].figure.do_hod_before = True
        else:
            for x in range(8):
                for y in range(1,8):
                    if board[x][y].figure.type != 'empty':
                        if board[x][y].figure.color == 'black':
                            if board[x][y-1].figure.type == 'empty':
                                board[x][y].figure, board[x][y-1].figure = \
                                    board[x][y-1].figure, board[x][y].figure
                                board[x][y-1].figure.do_hod_before = True
                                board[x][y-1].figure.set_coords_on_board(x,y-1)
            

###################################################################
# standart chess methoods
###################################################################

class Field():
    def __init__(self):
        self.attacked = False
        self.figure = None
    def __str__(self):
        return str(self.figure)

def copy_board(board):
    new_board = [[Field() for b in range(8)] for a in range(8)]
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
            board[x][y].figure = Figure('',0,0,'empty')
            board[x][y].attacked = False
    
    figs = ['rook','horse','bishop','queen','king','bishop','horse','rook']
    for a in range(8):
        board[a][0].figure = Figure('white',a,0,figs[a])
        board[a][7].figure = Figure('black',a,7,figs[a])
        board[a][1].figure = Figure('white',a,1,'pawn')
        board[a][6].figure = Figure('black',a,6,'pawn')

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




