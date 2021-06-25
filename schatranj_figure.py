import  Basic_figure


class Figure(Basic_figure.Figure):
    board_size = [8,8]

    def first_list(self, board):
        my_hod = []
        x,y = self.x, self.y
        color = self.color
        if self.type in ['king','horse','rook']:
            return super().first_list(board)
        if self.type == 'pawn':
            max_x = self.board_size[0]
            if self.color == 'white':
                if board[x][y+1].figure.type == 'empty':
                    my_hod.append([x,y+1])
                if x != 0 and board[x-1][y+1].figure.color =='black':
                    my_hod.append([x-1,y+1])
                if x != max_x - 1 and board[x+1][y+1].figure.color == 'black':
                    my_hod.append([x+1,y+1])
            else:
                if board[x][y-1].figure.type == 'empty':
                    my_hod.append([x,y-1])
                if x!=0 and board[x-1][y-1].figure.color =='white':
                    my_hod.append([x-1,y-1])
                if x != max_x - 1 and board[x+1][y-1].figure.color == 'white':
                    my_hod.append([x+1,y-1])
        elif self.type == 'queen':
            if x > 0 and y != 7 and board[x-1][y+1].figure.color != color:
                my_hod.append([x-1,y+1])
            if x > 0 and y > 0 and board[x-1][y-1].figure.color != color:
                my_hod.append([x-1,y-1])
            if x != 7 and y != 7 and board[x+1][y+1].figure.color != color:
                my_hod += [[x+1,y+1]]
            if x != 7 and y != 0 and board[x+1][y-1].figure.color != color:
                my_hod.append([x+1,y-1])
        elif self.type == 'bishop':
            if x > 1 and y > 1 and board[x-2][y-2].figure.color != color:
                my_hod.append([x-2,y-2])
            if x < 6 and y < 6 and board[x+2][y+2].figure.color != color:
                my_hod.append([x+2,y+2])
            if x > 1 and y < 6 and board[x-2][y+2].figure.color != color:
                my_hod.append([x-2,y+2])
            if x < 6 and y > 1 and board[x+2][y-2].figure.color != color:
                my_hod.append([x+2,y-2])

        return my_hod

    def __init__(self, color, x, y, fig_type):
        super().__init__(color, x, y, fig_type)
        del self.do_hod_before
        if fig_type == 'pawn':
            del self.do_hod_now
