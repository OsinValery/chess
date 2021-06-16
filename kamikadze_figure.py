import Basic_figure

def get_widget(widget,size_app):
    Basic_figure.get_widget(widget,size_app)

class Figure(Basic_figure.Figure):
    def first_list(self,board):
        if self.type in ['horse', 'rook', 'bishop', 'queen', 'pawn']:
            return super(Figure,self).first_list(board)
        my_hod = []
        x , y = self.x , self.y
        # logik of king
        if y != 7 :
            if x < 7 and board[x+1][y+1].figure.type == 'empty':
                my_hod.append([x+1,y+1])
            if board[x][y+1].figure.type == 'empty' :
                my_hod.append([x,y+1])
            if x >= 1 and board[x-1][y+1].figure.type == 'empty' :
                my_hod.append([x-1,y+1])
        if y != 0 :
            if x < 7 and board[x+1][y-1].figure.type == 'empty' :
                my_hod.append([x+1,y-1])
            if board[x][y-1].figure.type == 'empty' :
                my_hod.append([x,y-1])
            if x >= 1 and board[x-1][y-1].figure.type == 'empty' :
                my_hod.append([x-1,y-1])
        if x < 7 and board[x+1][y].figure.type == 'empty' :
            my_hod.append([x+1,y])
        if x  > 0 and board[x-1][y].figure.type == 'empty' :
            my_hod.append([x-1,y])

        return my_hod
