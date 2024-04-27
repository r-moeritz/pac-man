import pygame
from pygame.mixer import Sound, Channel
from constants import *
from pathlib import PurePath

class Sounds(object):
    
    def __init__(self):
        pygame.mixer.set_num_channels(2)
        pygame.mixer.set_reserved(1) # reserve a channel
        self.prio_channel = Channel(0) # 1st channel (reserved) is for priority sounds
        prio_files = {
            INTROSND: 'intro',
            EXTRAPACSND: 'extrapac',
            DEATHSND: 'death',
            EATGHOSTSND: 'eatghost'
        }
        self.prio_sounds = { k: Sound(PurePath('assets', v + '.mp3')) for k,v in prio_files.items() }
        rem_files = {            
            CHOMPSND: 'chomp',
            EATFRUITSND: 'eatfruit',

        }
        self.rem_sounds = { k: Sound(PurePath('assets', v + '.mp3')) for k,v in rem_files.items() }
       
    def __del__(self):
        if pygame.mixer.get_init():
            pygame.mixer.stop()
        
    def play(self, soundid):
        sound = self.prio_sounds.get(soundid)
        if sound:
            self.prio_channel.play(sound)
        else:
            self.rem_sounds[soundid].play()
