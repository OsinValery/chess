from classic import Field, do_rocking, can_do_rocking
import help_chess


def create_start_game_board():
    board = [[Field() for t in range(8)] for a in range(8)]
    for x in range(8):
        for y in range(8):
            board[x][y].figure = help_chess.Figure('',0,0,'empty')
            board[x][y].attacked = False
    
    figs = ['rook','horse','bishop','queen','king','bishop','horse','rook']
    for a in range(8):
        board[a][0].figure = help_chess.Figure('black',a,0,figs[a])
        board[a][7].figure = help_chess.Figure('white',a,7,figs[a])
        board[a][1].figure = help_chess.Figure('black',a,1,'pawn')
        board[a][6].figure = help_chess.Figure('white',a,6,'pawn')

    return board


def init_chess(game):
    game.board = create_start_game_board()
    game.do_rocking = do_rocking
    game.can_do_rocking = can_do_rocking