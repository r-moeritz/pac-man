import pygame
from pygame.mixer import Sound, Channel
from constants import *
from pathlib import PurePath


class SoundInfo:

    def __init__(self,
                 name: str,
                 foreground: bool = False,
                 maxtime: int=0,
                 priority: bool=False,
                 next: 'SoundInfo'=None):
        self._sound = Sound(SoundInfo.filepath(name))
        self._foreground = foreground
        self._maxtime = maxtime
        self._priority = priority
        self._next = next


    @property
    def sound(self) -> Sound:
        return self._sound


    @property
    def foreground(self) -> bool:
        return self._foreground


    @property
    def maxtime(self) -> int:
        return self._maxtime


    @property
    def priority(self) -> bool:
        return self._priority


    @property
    def next(self) -> 'SoundInfo':
        return self._next


    @staticmethod
    def filepath(name: str) -> str:
        return PurePath('assets', name + '.mp3')


class Sounds:
    
    def __init__(self):
        pygame.mixer.set_num_channels(2)
        pygame.mixer.set_reserved(1) # reserve a channel
        self.fg_channel = Channel(0) # 1st channel (reserved) is for foreground sounds
        self.cur_sinf = None

        self.soundinfos = {
            INTROSND: SoundInfo('start', foreground=True),
            EXTRAPACSND: SoundInfo('extend', foreground=True, priority=True),
            DYINGSND: SoundInfo('death_0',
                                foreground=True,
                                maxtime=1500,
                                priority=True,
                                next=SoundInfo('death_1', foreground=True)),
            EATGHOSTSND: SoundInfo('eat_ghost', foreground=True),
            EATFRUITSND: SoundInfo('eat_fruit', foreground=True),
            CHOMPSND: SoundInfo('eat_dot_1', foreground=True),
            SIRENSND: SoundInfo('siren0'),
            FRIGHTSND: SoundInfo('fright'),
        }
       

    def __del__(self):
        if pygame.mixer.get_init():
            pygame.mixer.stop()


    def play(self, soundid):
        if self.cur_sinf and self.cur_sinf.priority \
            and self.cur_sinf.foreground and self.fg_channel.get_busy():
                return # Current sound has priority, ignore new sound

        new_sinf = self.soundinfos.get(soundid)

        if new_sinf.priority and self.cur_sinf:
            # New sound has priority, mute current sound
            self.cur_sinf.sound.set_volume(0)

        if new_sinf.foreground:
            self.fg_channel.play(new_sinf.sound,
                                 maxtime=new_sinf.maxtime)
            if new_sinf.next:
                self.fg_channel.queue(new_sinf.next.sound)
        else:
            new_sinf.sound.play(maxtime=new_sinf.maxtime)
            new_sinf.sound.set_volume(.75)

        self.cur_sinf = new_sinf
