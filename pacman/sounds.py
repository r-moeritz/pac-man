import pygame
from pygame.mixer import Sound, Channel
from constants import *
from pathlib import PurePath

class Sounds(object):
    
    def __init__(self):
        pygame.mixer.set_num_channels(2)
        pygame.mixer.set_reserved(1) # reserve a channel
        self.fg_channel = Channel(0) # 1st channel (reserved) is for foreground sounds
        self.cur_sound = None

        fg_files = {
            INTROSND: 'start',
            CREDITSND: 'credit',
            EXTRAPACSND: 'extend',
            DYINGSND: 'death_0',
            DEADSND: 'death_1',
            EATGHOSTSND: 'eat_ghost',
            EATFRUITSND: 'eat_fruit',
            CHOMPSND: 'eat_dot_1',
        }
        self.fg_sounds = { k: Sound(PurePath('assets', v + '.mp3')) for k,v in fg_files.items() }
        bg_files = {
            SIRENSND: 'siren0',
            FRIGHTSND: 'fright',
        }
        self.bg_sounds = { k: Sound(PurePath('assets', v + '.mp3')) for k,v in bg_files.items() }
       
    def __del__(self):
        if pygame.mixer.get_init():
            pygame.mixer.stop()
        
    def play(self, soundid):
        if soundid == DYINGSND and self.cur_sound is not None:
            # Mute current sound on Pac-Man death
            self.cur_sound.set_volume(0)

        self.cur_sound = self.fg_sounds.get(soundid) \
            or self.bg_sounds.get(soundid)

        if soundid in self.fg_sounds:
            self.fg_channel.play(self.cur_sound)
            if soundid == DYINGSND:
                nxt_sound = self.fg_sounds.get(DEADSND)
                self.fg_channel.queue(nxt_sound)
        else:
            self.cur_sound.play()
            self.cur_sound.set_volume(.75)
