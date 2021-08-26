from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
import kivy.core.window as window


def default_command(wid,text):
    print(text)


class Spinner(Button):
    def __init__(self,on_change=default_command,**kwargs):
        """
        possible arguments: \n

        for compact piece:
             on_change - what to do if value in changing - default nothing 
            pos - position of widget [x,y] - default [0,0] 
             size - size of widget - default [150,50] 
            value or text - current choosen value - default '' 
             values - list of possible variants - default [] 
            background_normal - background picture - default window_for.png 
             background_color - default [1,0,0,1] 
            color or text_color - color of text - default [0,1,0,1]
             direction   - up or down      default is 'up' if it is possible
        
        for dropped list:
            drop_background_normal - default self.background_normal 
             drop_background_color  - default self.background_color 
            drop_color - color of menu button text - default self.color
             drop_spacing - space between neibour buttons - default 2 pixel 
            drop_height - height of elements of menu - default self.sise[1]


        """
        super(Spinner,self).__init__()
        self.on_change = on_change
        self.bind(on_press = self.__press__)

        self.opened = False
        self.background_normal = 'window_fon.png'
        self.background_color = [1,0,0,1]
        self.color = [0,1,0,1]
        self.drop_color = self.color
        self.size = [150,50]
        self.pos = [0,0]
        self.value = ''
        self.values = []

        if 'pos' in kwargs:
            self.pos = kwargs['pos']
        if 'values' in kwargs:
            self.values = kwargs['values']
        if 'value' in kwargs:
            self.text = kwargs['value']
        if 'size' in kwargs:
            self.size = kwargs['size']
        if 'size_hint' in kwargs:
            self.size_hint = kwargs['size_hint']
        if 'text' in kwargs:
            self.text = kwargs['text']
        if 'background_normal' in kwargs:
            self.background_normal = kwargs['background_normal']
        if 'background_color' in kwargs:
            self.background_color = kwargs['background_color']
        if 'color' in kwargs:
            self.color = kwargs['color']
        if 'text_color' in kwargs:
            self.color = kwargs['text_color']

        self.drop_background_color = self.background_color
        self.drop_background_normal = self.background_normal
        self.drop_height = self.size[1]
        self.drop_spacing = 2
        self.drop_color = self.color
        
        if 'drop_height' in kwargs:
            self.drop_height = kwargs['drop_height']
        if 'drop_spacing' in kwargs:
            self.drop_spacing = kwargs['drop_spacing']
        if 'drop_background_color' in kwargs:
            self.drop_background_color = kwargs['drop_background_color']
        if 'drop_background_normal' in kwargs:
            self.drop_background_normal = kwargs['drop_background_normal']
        if 'drop_color' in kwargs:
            self.drop_color = kwargs['drop_color']

        if 'direction' in kwargs:
            self.direction = kwargs['direction']
        else:
            self.direction = 'up'
            height = len(self.values) * self.drop_height 
            height += self.drop_spacing * len(self.values)
            pos = [self.pos[0], self.size[1] + self.pos[1] + self.drop_spacing]
            if pos[1] + height > window.Window.size[1]:
                self.direction = 'down'

    def __press__(self,arg=None):
        if self.opened:
            self.close()
        else:
            def press(info=None):
                if info.text != self.text:
                    self.text = info.text
                    self.clear_widgets()
                    self.opened = False
                    self.on_change(self,self.text)
                else:
                    self.opened = False
                    self.clear_widgets()

            height = len(self.values) * (self.drop_height + self.drop_spacing)
            if self.direction == 'up':
                pos = [self.pos[0], self.size[1] + self.pos[1] + self.drop_spacing]
            elif self.direction == 'down':
                pos = [self.pos[0], self.pos[1] - self.drop_spacing - height]
            else:
                raise Exception(f'wrong argument for direction: {self.direction}')
        
            grid = GridLayout(
                cols=1,
                pos = pos,
                size = [self.size[0], height ],
                spacing = [0,self.drop_spacing]
                )

            for i in range(len(self.values)):
                grid.add_widget(Button(
                    text = self.values[i],
                    on_press = press,
                    background_color = self.drop_background_color,
                    background_normal = self.drop_background_normal,
                    color = self.drop_color
                ))
            self.add_widget(grid)
            self.opened = True
    
    def on_touch_down(self,par):
        must_close = True
        coord = par.pos
        if self.collide_point(*coord) or not self.opened:
            must_close = False
        else:
            for wid in self.children:
                if wid.collide_point(*coord):
                    must_close = False
        if must_close:
            self.close()
        return  super(Spinner,self).on_touch_down(par)

    def close(self):
        if self.opened:
            self.opened = False
            self.clear_widgets()
        

if __name__ == '__main__':
    from kivy.app import App
    from kivy.uix.widget import Widget

    class Test_App(App):
        def build(self):
            wid = Widget()
            values = [str(i) for i in range(1,15,1)]
            wid.add_widget(Spinner(
                pos = [300,300],
                values = values,
                text = '3',
                size = [150,70],
                background_normal = '',
                drop_height = 30,
                drop_spacing = 20,
                background_color = [1,1,0,0.3],
                drop_background_color = [0,1,1,.5],
                drop_background_normal = ''
            ))
            wid.add_widget(Spinner(
                pos = [500,700],
                values = values,
                text = '3',
                size = [150,70],
                background_normal = '',
                drop_height = 30,
                drop_spacing = 20,
                background_color = [1,1,0,0.3],
                drop_background_color = [0,1,1,.5],
                drop_background_normal = ''
            ))
            return wid

    Test_App().run()