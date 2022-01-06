from kivy.uix.widget import Widget
import kivy.graphics
import sounds
"""
at the time of creation some classes send ghost copyes of 
object in this module for comfortable access to them
"""

game = None
Main_Window = Widget()
Sizes = None
Settings = None
Music = sounds.Music
current_figure_canvas = kivy.graphics.Canvas
Connection_manager = None

