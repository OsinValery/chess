
from sounds import Music
import global_constants
import core_game_logik

import kamikadze_help
import kamikadze_figure


class Game_logik(core_game_logik.CoreGameLogik):
    def build_game(self):
        super().build_game()
        self.Figure = kamikadze_figure.Figure
        kamikadze_help.init_chess(self)
  
    def find_fields(self,board,figure):
        list2 = super().find_fields(board,figure)
        if figure.type == 'king' and not figure.do_hod_before :
            list2 = self.can_do_rocking(self,board,figure,list2)
        return list2

    def move_figure(self,board,x,y,options=None):
        self.message = f'move {self.choose_figure.x} {self.choose_figure.y} {x} {y}'
        Music.move()
        if self.choose_figure.color == 'white':
            self.made_moves += 1
        # if this figure kill other figure, it must die by rools of this type of chess
        # it beat figure, if field is not empty
        # if on field stay my figure, move_figure will not be called
        must_die = board[x][y].figure.type != 'empty'

        if self.choose_figure.type == 'pawn':
            # taking on the pass
            if x != self.choose_figure.x:
                if board[x][y].figure.type == 'empty':
                    board[x][self.choose_figure.y].figure.destroy()
                    must_die = True

        if self.choose_figure.type == 'king' and not self.choose_figure.do_hod_before:
            board = self.do_rocking(board,x,y,self.choose_figure)
        else:
            a , b = self.choose_figure.x , self.choose_figure.y
            board[a][b].figure = self.Figure('',0,0,'empty')
            board[x][y].figure.destroy()
            board[x][y].figure = self.choose_figure
            board[x][y].figure.set_coords_on_board(x,y)
                
        if self.choose_figure.type == 'pawn' and abs(y-b) == 2:
            self.choose_figure.do_hod_now = True
        board[x][y].figure.do_hod_before = True

        if must_die:
            self.choose_figure.destroy()

        if self.choose_figure.type == 'pawn' and board[x][y].figure.pawn_on_last_line():
            if global_constants.game.state_game != 'one' and self.color_do_hod_now != global_constants.game.play_by:
                # type of figure was taken in message from partner
                self.choose_figure.transform_to(options[1])
                self.choose_figure = self.Figure('',0,0,'empty')
                options = options[2:]
                self.change_color(options)
                self.is_end_of_game(board)
            else:
                self.do_transformation(self.color_do_hod_now,x,y,options)
        else:
            if global_constants.game.state_game != 'one' and self.color_do_hod_now == global_constants.game.play_by:
                self.message += f" {self.players_time['white']} {self.players_time['black']}"
                global_constants.Connection_manager.send(self.message)
                self.message = ''
            self.choose_figure = self.Figure('',0,0,'empty')
            self.change_color(options)
            self.is_end_of_game(board)
        
        self.delete_tips()
        self.green_line.show_field(x=-1,y=-1)
        for a in range(8):
            for b in range(8):
                if board[a][b].figure.type == 'pawn':
                    if board[a][b].figure.color == self.color_do_hod_now:
                        board[a][b].figure.do_hod_now = False
        self.list_of_hod_field = []
        return board



