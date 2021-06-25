import Basic_figure


class Figure(Basic_figure.Figure):
    def pawn_on_last_line(self):
        if self.color == 'white':
            if self.x == 0 and self.y > 3:
                return True
            if self.y == 7 and self.x < 4:
                return True
        else:
            if self.y == 0 and self.x > 3:
                return True
            if self.x == 7 and self.y < 4:
                return True
        return False

    def first_list(self, board):
        if self.type != 'pawn':
            return super().first_list(board)
        res = []

        if self.color == 'white':
            if self.x > 0 and self.y < 7 and board[self.x-1][self.y+1].figure.type == 'empty':
                res.append([self.x-1, self.y + 1])
            if self.y != 7 and board[self.x][self.y+1].figure.type != 'empty':
                if board[self.x][self.y+1].figure.color != self.color:
                    res.append([self.x, self.y+1])
            if self.x != 0 and board[self.x-1][self.y].figure.type != 'empty':
                if board[self.x-1][self.y].figure.color != self.color:
                    res.append([self.x-1,self.y])
        else:
            if self.x < 7 and self.y != 0 and board[self.x+1][self.y-1].figure.type == 'empty':
                res.append([self.x+1,self.y-1])
            if self.x != 7 and board[self.x+1][self.y].figure.type != 'empty':
                if board[self.x+1][self.y].figure.color != self.color:
                    res.append([self.x+1,self.y])
            if self.y != 0 and board[self.x][self.y-1].figure.type != 'empty':
                if board[self.x][self.y-1].figure.color != self.color:
                    res.append([self.x, self.y-1])
        return res

    def do_attack(self, board):
        if self.type != 'pawn':
            return super().do_attack(board)
        
        if self.color == 'white':
            if self.y != 7:
                board[self.x][self.y+1].attacked = True
            if self.x != 0:
                board[self.x-1][self.y].attacked = True
        else:
            if self.x < 7:
                board[self.x+1][self.y].attacked = True
            if self.y != 0:
                board[self.x][self.y-1].attacked = True

        return board





