
import copy
import bad_help
import core_game_logik
import bad_figure


class Field():
    def __init__(self):
        self.attacked = False
        self.figure = None
    def __str__(self):
        return str(self.figure)


class Game_logik(core_game_logik.CoreGameLogik):
    def build_game(self):
        super(Game_logik,self).build_game()
        self.Figure = bad_figure.Figure
        bad_help.init_chess(self)
    
    def copy_board(self, board):
        new_board = [[Field() for b in range(len(board[0]))] for a in range(len(board))]
        for a in range(len(board)):
            for b in range(len(board[0])):
                new_board[a][b].figure = self.Figure('white', 0, 0, '')
                new_board[a][b].figure.color = copy.copy(board[a][b].figure.color)
                new_board[a][b].figure.type = copy.copy(board[a][b].figure.type)

        return new_board

