from kivy.uix.widget import Widget
from kivy.graphics import Line,Ellipse,Color


def empty_action(wid,value):
    pass

class Switch_(Widget):
    def __init__(self,**kwargs):
        """
        all possible params 
        pos            - pos                [0, 0]\n
        size           - size               [100, 40]\n
        active_color   - color of widget    [0, .9, 1]\n
        disabled_color - color of widget    [.87, 1, 1]\n
        on_change      - action, when press  pass\n
        active         - active or not      False
        """
        Widget.__init__(self)
        if 'pos' in kwargs:
            self.pos = kwargs['pos']
        else:   self.pos = [0,0]
        if 'size' in kwargs:
            self.size = kwargs['size']
        else :   self.size = [100,40]
        if 'active_color' in kwargs:
            self.active_color = kwargs['active_color']
        else:   self.active_color = [0,.9,1]
        if 'disabled_color' in kwargs:
            self.disabled_color = kwargs['disabled_color']
        else:    self.disabled_color = [.87,1,1]
        if 'on_change' in kwargs:
            self.action__ = kwargs['on_change']
        else:
            self.action__ = empty_action
        self.active__ = False
        if 'active' in kwargs:
            self.active__ = kwargs['active']
        self.draw__()
    
    @property
    def active(self):
        return self.active__

    @active.setter
    def active(self,value):
        if self.active__ != value:
            self.active__ = value
            self.action__(self,value)
    
    def draw__(self):
        width = self.size[1]
        points = [
            self.pos[0]+width/2,self.pos[1]+width/2,
            self.pos[0]+self.size[0]-width/2, self.pos[1]+width/2
            ]
        r = 1.6 * width
        self.content__ = Line(width=width/2,points=points)
        self.handler__ = Ellipse(pos=[0,50],size=[r]*2)

        self.__handler_active_pos = [
            self.pos[0]-width/2-r/2+self.size[0], self.pos[1]+width/2-r/2
            ]
        self.__handler_disabled_pos = [self.pos[0]+width/2-r/2, self.pos[1]+width/2-r/2]

        if self.active:
            self.handler__.pos = self.__handler_active_pos
        else:
            self.handler__.pos = self.__handler_disabled_pos

        color = self.active_color if self.active else self.disabled_color
        with self.canvas:
            Color(*color,1)
            self.canvas.add(self.handler__)
            Color(*color,.5)
            self.canvas.add(self.content__)

    def redraw(self):
        #update color of widget when it is changing
        self.canvas.clear()
        color = self.active_color if self.active else self.disabled_color
        with self.canvas:
            Color(*color,1)
            self.canvas.add(self.handler__)
            Color(*color,.5)
            self.canvas.add(self.content__)
    
    def on_touch_down(self, touch):
        center = list(self.handler__.pos)
        center[0] += self.handler__.size[0] / 2
        center[1] += self.handler__.size[1] / 2
        x,y = touch.pos
        in_round = (x-center[0])**2 + (y-center[1])**2 <= \
            1/4 * self.handler__.size[0] ** 2

        if self.collide_point(*touch.pos) or in_round:
            self.active = not self.active
            if self.active:
                self.handler__.pos = self.__handler_active_pos
            else:
                self.handler__.pos = self.__handler_disabled_pos
            self.redraw()
            self.action__(self,self.active)
            return True
        else:
            return super(Switch_,self).on_touch_down(touch)


__all__ = [Switch_.__name__]
if __name__ == '__main__':
    from kivy.app import App
    from kivy.graphics import Rectangle

    class Test_App(App):
        def build(self):
            wid = Widget()
            with wid.canvas:
                Color(1,0,0,1)
                Rectangle(size=[700,700])

            wid.add_widget(Switch_(
                pos=[100,100],
                size = [100,40],
                active=False
            ))
            return wid
        
    Test_App().run()