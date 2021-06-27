from kivy.uix.button import Button
from kivy.graphics import Color,Line
import settings


class Button_(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not 'size' in kwargs:
            self.size = [200,100]
        if not 'font_name' in kwargs:
            self.font_name = settings.Settings.get_font()
        with self.canvas:
            Color(*self.color)
            Line(rectangle=tuple([*self.pos,*self.size]),width=2)
            Color(0,0,0,0)





if __name__ == '__main__':
    from kivy.app import App
    from kivy.uix.widget import Widget

    class TestApp(App):
        def build(self):
            wid = Widget()

            wid.add_widget(Button_(
                text = 'test',
                background_normal = '',
                background_color = [0,1,0,1]
            ))


            return wid
    
    TestApp().run()