import Basic_figure


class Figure(Basic_figure.Figure):
    def first_list(self, board):
        if self.type != 'king':
            return super().first_list(board)
        my_hod = []
        x,y = self.x, self.y
        max_x, max_y = self.board_size
        if y + 1 != max_y :
            if x + 1 < max_x and board[x+1][y+1].figure.color != self.color:
                my_hod.append([x+1,y+1])
            if board[x][y+1].figure.color != self.color :
                my_hod.append([x,y+1])
            if x - 1 >=0 and board[x-1][y+1].figure.color != self.color:
                my_hod.append([x-1,y+1])
        if y  != 0 :
            if x + 1 < max_x and board[x+1][y-1].figure.color != self.color:
                my_hod.append([x+1,y-1])
            if board[x][y-1].figure.color != self.color :
                my_hod.append([x,y-1])
            if x - 1 >=0 and board[x-1][y-1].figure.color != self.color:
                my_hod.append([x-1,y-1])
        if x + 1 < max_x and board[x+1][y].figure.color != self.color :
            my_hod.append([x+1,y])
        if x  > 0 and board[x-1][y].figure.color != self.color :
            my_hod.append([x-1,y])
        return my_hod