import kuej_figure

Figure = kuej_figure.Figure

class Field():
    def __init__(self):
        self.attacked = False
        self.figure = None
    def __str__(self):
        return str(self.figure)


def create_start_game_board():
    board = [[Field() for t in range(11)] for a in range(11)]
    for x in range(11):
        for y in range(11):
            board[x][y].figure = Figure('',0,0,'empty')
    for x in 0,1,2 :
        board[5][x].figure = Figure('white',5,x,'bishop')
        board[5][10-x].figure = Figure('black',5,10-x,'bishop')
    board[5][3].figure = Figure('white',5,3,'pawn')
    board[5][7].figure = Figure('black',5,7,'pawn')
    for i in 0,1,2 :
        board[2+i][i].figure = Figure('white',2+i,i,'pawn')
        board[8-i][i].figure = Figure('white',8-i,i,'pawn')
        board[2+i][7].figure = Figure('black',2+i,7,'pawn')
        board[8-i][7].figure = Figure('black',8-i,7,'pawn')
    board[6][0].figure = Figure('white',6,0,'king')
    board[4][0].figure = Figure('white',4,0,'queen')
    board[3][0].figure = Figure('white',3,0,'rook')
    board[7][0].figure = Figure('white',7,0,'rook')
    board[4][1].figure = Figure('white',4,1,'horse')
    board[6][1].figure = Figure('white',6,1,'horse')
    board[6][9].figure = Figure('black',6,9,'king')
    board[4][9].figure = Figure('black',4,9,'queen')
    board[3][8].figure = Figure('black',3,8,'rook')
    board[7][8].figure = Figure('black',7,8,'rook')
    board[4][8].figure = Figure('black',4,8,'horse')
    board[6][8].figure = Figure('black',6,8,'horse')
    return board


def init_chess(game):
    game.board = create_start_game_board()
