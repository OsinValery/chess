import glin_figure

Figure = glin_figure.Figure

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
    board[5][4].figure = Figure('white',5,4,'pawn')
    board[5][6].figure = Figure('black',5,6,'pawn')
    for x in 0,1,2,3:
        board[1+x][x].figure = Figure('white',1+x,x,'pawn')
        board[9-x][x].figure = Figure('white',9-x,x,'pawn')
        board[1+x][6].figure = Figure('black',x+1,6,'pawn')
        board[9-x][6].figure = Figure('black',9-x,6,'pawn')
    board[6][0].figure = Figure('white',6,0,'king')
    board[6][9].figure = Figure('black',6,9,'king')
    board[4][0].figure = Figure('white',4,0,'queen')
    board[4][9].figure = Figure('black',4,9,'queen')
    board[2][0].figure = Figure('white',2,0,'rook')
    board[3][0].figure = Figure('white',3,0,'horse')
    board[7][0].figure = Figure('white',7,0,'horse')
    board[8][0].figure = Figure('white',8,0,'rook')

    board[8][7].figure = Figure('black',8,7,'rook')
    board[7][8].figure = Figure('black',7,8,'horse')
    board[3][8].figure = Figure('black',3,8,'horse')
    board[2][7].figure = Figure('black',2,7,'rook')
    return board


def init_chess(game):
    game.board = create_start_game_board()
