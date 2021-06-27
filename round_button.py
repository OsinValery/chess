from kivy.graphics import Color,Line
from kivy.uix.label import Label
from kivy.uix.widget import Widget
import global_constants

def empty_action(touch):
    pass

class RoundButton(Widget):
    def __init__(self, **kwargs):
        """
        text   - text on button     ''\n
        size   - button size       [100,50]\n
        pos    - position          [0,0]\n
        background_color           [1,0,1,1]\n
        color  - text color        [1,1,1,1]\n
        on_press                   pass\n
        font_size                  30
        """
        super(RoundButton,self).__init__()
        self.size = [100,50]
        self.pos = [0,0]
        self.background_color = [1,0,1,1]
        self.text = 'test'
        self.color = [1,1,1,1]
        self.on_press = empty_action
        self.font_size = 30
        self.font_name = global_constants.Settings.get_font()
        if 'text' in kwargs:
            self.text = kwargs['text']
        if 'size' in kwargs:
            self.size = kwargs['size']
        if 'pos' in kwargs:
            self.pos = kwargs['pos']
        if 'color' in kwargs:
            self.color = kwargs['color']
        if 'background_color' in kwargs:
            self.background_color = kwargs['background_color']
        if 'font_size' in kwargs:
            self.font_size = kwargs['font_size']
        self.draw()
        if 'on_press' in kwargs:
            self.on_press = kwargs['on_press']
    
    def draw(self):
        width = self.size[1]
        points = [
            self.pos[0] + width/2, self.pos[1] + width/2,
            self.pos[0] + self.size[0] - width/2,self.pos[1] + width/2
                ]

        with self.canvas:
            Color(*self.background_color)
            Line(
                width = width/2,
                points = points
            )
        self.add_widget(Label(
            size = self.size,
            pos = self.pos,
            color = self.color,
            text = self.text,
            font_size=self.font_size,
            font_name=self.font_name
        ))

    def on_touch_down(self,touch):
        x,y = touch.pos
        in_shape = True
        r = self.size[1] / 2
        if y < self.pos[1] or y > self.pos[1] + self.size[1]:
            in_shape = False
        if x < self.pos[0] or x > self.pos[0] + self.size[0]:
            in_shape = False
        if x < self.pos[0] + r and in_shape:
            center = [self.pos[0]+r,self.pos[1]+r]
            if (x-center[0])**2 + (y-center[1])**2 > r**2:
                in_shape = False
        if in_shape and x > self.pos[0] + self.size[0] - r:
            center = [self.pos[0]-r+self.size[0], self.pos[1]+r]
            if (x-center[0])**2 + (y-center[1])**2 > r**2:
                in_shape = False
        if in_shape:
            self.on_press(self)
            return True
        else:
            return super().on_touch_down(touch)



if __name__ == '__main__':
    from kivy.app import App

    def test_action(touch):
        print('click')

    class testApp(App):
        def build(self):
            wid = Widget()
            wid.add_widget(RoundButton(
                text = 'test',
                pos = [100,100],
                size = [700,200],
                on_press = test_action,
                color = [1,1,0,1]
            ))
            return wid
    
    testApp().run()