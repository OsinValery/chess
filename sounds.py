import threading
from kivy.core.audio import SoundLoader
import os
from settings import Settings
import global_constants
from threading import Thread


class Music_collector():
    def __init__(self):
        global_constants.Music = self
    def create(self):
        try:
            global music_dir
            music_dir = Settings.get_folder() + 'sounds' 
            
            self.effect = SoundLoader.load(os.path.join(music_dir,Settings.move_music))
            self.effect.volume = Settings.volume
            self.end_time = SoundLoader.load(os.path.join(music_dir,'timeend.ogg'))

            def load(arg=None):
                self.fon = SoundLoader.load(os.path.join(music_dir,Settings.fon_music))
                self.fon.loop = True
                self.fon.volume = Settings.volume
                self.start()
            sound = Thread(target=load,daemon=True)
            sound.start()
        except:
            pass

    def start(self):
        if Settings.with_sound:
            self.fon.play()
    
    def move(self):
        # calls from game
        if Settings.with_effects:
            try:
                self.effect.play()
            except:
                pass
    
    def time_passed(self):
        if Settings.with_sound or Settings.with_effects:
            try:
                self.end_time.volume = max(self.effect.volume, self.fon.volume)
                self.end_time.play()
            except:
                pass
    
    def stop(self):
        try:
            if self.effect.state == 'play':
                self.effect.stop()

            if self.fon.state == 'play':
                self.fon.stop()
        except:
            pass
    
    def renew(self):
        # этот метод нигде не используется, возможно, нужно удалить
        print('now i am in renew')
        try:
            self.stop()
            if Settings.with_effects:
                self.effect.volume = Settings.volume

            if Settings.with_sound:
                self.fon = SoundLoader.load(os.path.join(music_dir,Settings.fon_music))
                self.fon.loop = True
                self.fon.volume = Settings.volume
                self.start()
        except:
            pass

    def change_volume(self,value):
        try:
            self.effect.volume = value
            self.fon.volume = value
        except:
            pass

    def change_music(self,music):
        try:
            self.stop()
            self.fon.unload()
            def load(par=None):
                self.fon = SoundLoader.load(os.path.join(music_dir,music))
                self.fon.loop = True
                self.fon.volume = Settings.volume
                self.start()
            th = threading.Thread(target=load,daemon=1)
            th.start()
        except:
            pass

    def change_move(self,move):
        try:
            self.effect.unload()
            self.effect = SoundLoader.load(os.path.join(music_dir,move))
            self.effect.volume = Settings.volume
            if Settings.with_effects:
                self.effect.play()
        except:
            pass


Music = Music_collector()