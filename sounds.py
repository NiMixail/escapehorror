from pygame import mixer as pgmx
from os import listdir


class Audio:
    def __init__(self):
        pgmx.init()
        self.effects = {}
        for fn in listdir(path='data/sounds'):
            if not fn.startswith('ost_'):
                self.effects[fn[:-4]] = pgmx.Sound('data/sounds/' + fn)
        print(self.effects)

    def eff(self, name):
        return self.effects[name]

    def set_bg_music(self, name_with_extension):
        pgmx.music.load('data/sounds/ost_' + name_with_extension)

    def bg_music(self):
        return pgmx.music
