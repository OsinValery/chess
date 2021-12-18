from kivy.clock import Clock
from kivy.graphics import Color, Ellipse, Line
from Basic_figure import Figure
from translater import Get_text
from sounds import Music
import global_constants
import core_game_logik
import animals


class Green_line(Line):
    def __init__(self):
        super(Green_line, self).__init__()
        self.width = 3
        self.close = True
        self.drawed = False

    def get_canv(self, canvas):
        self.canvas = canvas

    def show_field(self, x, y):
        if self.drawed:
            self.canvas.remove(self)
            self.drawed = False
        if x != -1:
            pad_x = global_constants.Sizes.x_top_board + global_constants.Sizes.x_top
            pad_y = global_constants.Sizes.y_top_board + global_constants.Sizes.y_top
            size = global_constants.Sizes
            self.points = (
                pad_x + size.field_width * x,       pad_y + size.field_height * y,
                pad_x + size.field_width * (x+1),   pad_y + size.field_height * y,
                pad_x + size.field_width * (x+1),   pad_y + size.field_height * (y+1),
                pad_x + size.field_width * x,       pad_y + size.field_height * (y + 1)
            )
            with self.canvas:
                Color(0, 1, 0, 1)
                self.canvas.add(self)
                self.drawed = True
                Color(1, 1, 1, 1)


class Field():
    def __init__(self):
        self.figure = None
        self.player = ''
        self.type = 'land'
    
    def setType(self, tip, player):
        self.player = player
        self.type = tip

    def __str__(self):
        return str(self.figure)
    
    def toString(self):
        x, y = self.figure.x, self.figure.y
        return f'field on {x} {y} player: {self.player} type: {self.type}'


def create_start_game_board():
    board = [[Field() for y in range(9)] for x in range(7)]
    for x in range(7):
        for y in range(9):
            board[x][y].setType('land', '')
            board[x][y].figure = animals.Figure('', x, y, 'empty')
    board[3][0].setType('castle', 'white')
    board[3][8].setType('castle', 'black')
    for y in 3,4,5:
        for x in 1,2,4,5:
            board[x][y].setType('river', '')
    for (x,y) in (2,0), (4,0), (3,1):
        board[x][y].setType('trap', 'white')
    for (x,y) in (2,8), (4,8), (3,7):
        board[x][y].setType('trap', 'black')
    board[0][0].figure = animals.Figure('white', 0, 0, 'tiger')
    board[6][8].figure = animals.Figure('black', 6, 8, 'tiger')
    board[0][2].figure = animals.Figure('white', 0, 2, 'elephant')
    board[6][6].figure = animals.Figure('black', 6, 6, 'elephant')
    board[2][2].figure = animals.Figure('white', 2, 2, 'wolf')
    board[4][6].figure = animals.Figure('black', 4, 6, 'wolf')
    board[1][1].figure = animals.Figure('white', 1, 1, 'cat')
    board[5][7].figure = animals.Figure('black', 5, 7, 'cat')
    board[4][2].figure = animals.Figure('white', 4, 2, 'leopard')
    board[2][6].figure = animals.Figure('black', 2, 6, 'leopard')
    board[5][1].figure = animals.Figure('white', 5, 1, 'dog')
    board[1][7].figure = animals.Figure('black', 1, 7, 'dog')
    board[6][0].figure = animals.Figure('white', 6, 0, 'lion')
    board[0][8].figure = animals.Figure('black', 0, 8, 'lion')
    board[6][2].figure = animals.Figure('white', 6, 2, 'rat')
    board[0][6].figure = animals.Figure('black', 0, 6, 'rat')

    return board


class Game_logik(core_game_logik.CoreGameLogik):
    def build_game(self):
        super().build_game()
        self.Figure = animals.Figure
        self.board = create_start_game_board()


    def init_game(self):
        Main_Window = global_constants.Main_Window
        self.create_interface(Main_Window, global_constants.Sizes)
        global_constants.current_figure_canvas = Main_Window.wid.canvas
        self.build_game()
        self.choose_figure = animals.Figure('white', 0, 0, 'empty')
        self.green_line = Green_line()
        self.green_line.get_canv(Main_Window.canvas)

    def change_color(self, time=None):
        if global_constants.game.with_time:
            self.time.cancel()
            self.time = Clock.schedule_interval(self.tick, 1)
            if time != None:
                if self.color_do_hod_now != global_constants.game.play_by:
                    self.players_time['white'] = int(time[0])
                    self.players_time['black'] = int(time[1])
            self.players_time[self.color_do_hod_now] += global_constants.game.add_time
        if self.color_do_hod_now == 'white':
            if global_constants.game.ind:
                self.interfase.do_info(Get_text('game_red_move'))
            self.color_do_hod_now = 'black'
        elif self.color_do_hod_now == 'black':
            if global_constants.game.ind:
                self.interfase.do_info(Get_text('game_blue_move'))
            self.color_do_hod_now = 'white'
        if global_constants.game.with_time:
            self.interfase.set_time(self.players_time)

    def tick(self, cd):
        self.players_time[self.color_do_hod_now] -= 1
        self.interfase.set_time(self.players_time)
        if self.players_time[self.color_do_hod_now] == 0:
            global_constants.game.ind = False
            Music.time_passed()
            text = Get_text('game_end_time') + '!\n'
            if self.color_do_hod_now == 'white':
                text += Get_text('game_blue_lose')
            else:
                text += Get_text('game_red_lose')
            self.interfase.do_info(text)
            self.time.cancel()
    
    def create_tips(self, a, b, board):
        list1 = self.find_fields(board, board[a][b].figure)
        Sizes = global_constants.Sizes

        top_x = Sizes.x_top + Sizes.x_top_board
        top_y = Sizes.y_top + Sizes.y_top_board
        width = Sizes.field_width
        height = Sizes.field_height
        r = Sizes.field_height // 6

        color = [0, 1, 0, .8]
        if self.color_do_hod_now != board[a][b].figure.color:
            color = [1, 0, 0, .8]
        if global_constants.game.state_game != 'one' and \
            self.color_do_hod_now != global_constants.game.play_by:
                color = [1, 0, 0, .8]
        with global_constants.Main_Window.wid.canvas:
            Color(*color, mode='rgba')
        self.tips_drawed = True

        for el in list1:
            x, y = el
            global_constants.Main_Window.wid.canvas.add(Ellipse(
                pos=[top_x - r/2 + (x+0.5)*width, top_y - r/2 + (y+0.5)*height],
                size=[r, r]
            ))
        with global_constants.Main_Window.wid.canvas:
            Color(1, 1, 1, 1, mode='rgba')
    
    def fit_field(self, event):
        x, y = 0, 0
        e_x, e_y = event.x, event.y
        s = global_constants.Sizes
        if e_x <= s.x_top + s.x_top_board or e_y <= s.y_top + s.y_top_board:
            return -1, -1
        elif (e_y >= s.y_top + s.y_top_board + s.field_height * 9) or \
                (e_x >= s.x_top + s.x_top_board + s.field_width * 7):
            return -1, -1
        else:
            e_x -= (s.x_top + s.x_top_board)
            x = e_x // s.field_width
            e_y -= (s.y_top + s.y_top_board)
            y = e_y // s.field_height
        return round(x), round(y)
    
    def is_end_of_game(self, board):
        if board[3][0].figure.type != 'empty':
            if board[3][0].figure.color != board[3][0].player:
                self.interfase.do_info(Get_text(f'game_white_lose_castle'))
                global_constants.game.ind = False
            else:
                print('непоняятная ситуация')
        if board[3][8].figure.type != 'empty':
            if board[3][8].figure.color != board[3][8].player:
                self.interfase.do_info(f'game_black_lose_castle')
                global_constants.game.ind = False
            else:
                print('непоняятная ситуация')
        if not global_constants.game.ind:
            return 
        # проверить, есть ли фигуры на доске у игроков
        players = {'white': 0, 'black': 0}
        for x in range(7):
            for y in range(9):
                if board[x][y].figure.type != 'empty':
                    players[board[x][y].figure.color] += 1
        if players['black'] == 0:
            global_constants.game.ind = False
            self.interfase.do_info(Get_text('game_jungles_black_lost'))
        elif players['white'] == 0:
            global_constants.game.ind = False
            self.interfase.do_info(Get_text('game_jungles_white_lost'))

    def find_fields(self, board, figure: Figure):
        return figure.first_list(board)
    
    def move_figure(self, board, x, y, options=None):
        self.message = f'move {self.choose_figure.x} {self.choose_figure.y} {x} {y}'
        Music.move()
        if self.choose_figure.color == 'white':
            self.made_moves += 1
        # move it
        a, b = self.choose_figure.x, self.choose_figure.y
        board[a][b].figure = animals.Figure('', 0, 0, 'empty')
        board[x][y].figure.destroy()
        board[x][y].figure = self.choose_figure
        board[x][y].figure.set_coords_on_board(x, y)
        # after moving
        if global_constants.game.state_game != 'one' and self.color_do_hod_now == global_constants.game.play_by:
            self.message += f" {self.players_time['white']} {self.players_time['black']}"
            global_constants.Connection_manager.send(self.message)
            self.message = ''
        self.choose_figure = self.Figure('', 0, 0, 'empty')
        self.change_color(options)
        self.is_end_of_game(board)
        self.delete_tips()
        self.green_line.show_field(x=-1, y=-1)
        self.list_of_hod_field = []
        return board

    def surrend(self, click):
        if not global_constants.game.ind:
            return
        Sizes = global_constants.Sizes

        def yes():
            global_constants.game.ind = False
            if global_constants.game.state_game == 'one':
                if self.color_do_hod_now == 'white':
                    f = Get_text('game_blue_surrend')
                else:
                    f = Get_text('game_red_surrend')
            else:
                f = Get_text('game_you_surrend')
            self.interfase.do_info(f)
            if global_constants.game.with_time:
                self.time.cancel()
            if global_constants.game.state_game != 'one':
                global_constants.Connection_manager.send(self.message)

        def no():
            self.want_surrend = False

        if self.made_moves < 4 or (self.made_moves == 3 and self.color_do_hod_now == 'black'):
            core_game_logik.create_message(Get_text('game_cant_surrend'))
        elif not self.pause and not self.need_change_figure and not self.want_surrend:
            self.want_surrend = True
            core_game_logik.Window(
                btn_texts=[Get_text('game_want_surrend'), Get_text('game_not_surrend')],
                btn_commands=[yes, no],
                text=Get_text('game_agree?'),
                title=Get_text('game_press_surrend'),
                size=[Sizes.board_size[0], .5 * Sizes.board_size[1]],
                title_color=[.1, 0, 1, 1]
            ).open()

