from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Rectangle,Color


class Window(Popup):
    def __init__(self,btn_texts,btn_commands,text,**kwargs):
        super(Window,self).__init__(**kwargs)
        self.auto_dismiss = False
        self.size_hint = [None]*2
        self.size_hint_y = None
        self.pos = [0,0]
        self.background = 'window_fon.png'
        if not 'background_color' in kwargs:
            self.background_color = [1,0,0,.25]

        grid = GridLayout(cols = 1)        
        self.add_widget(grid)
        grid.add_widget(Label(
            text = text,
            color = [0,1,1,1]
        ))
        btn_grid = GridLayout(rows = 1,size_hint_y=None,spacing=[20,0])
        grid.add_widget(btn_grid)
        def command(click):
            self.dismiss()
            for i in range(len(btn_texts)):
                if btn_texts[i] == click.text:
                    btn_commands[i]()
        for el in btn_texts:
            but = Button(
                text = el,
                size_hint_y = None,
                on_press = command,
                background_normal = 'window_fon.png',
                background_color = [1,.1,1,.7]
            )
            btn_grid.add_widget(but)
