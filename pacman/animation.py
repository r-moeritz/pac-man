from constants import *

class Animator(object):

    def __init__(self, frames=[], speed=20, loop=True):
        self.frames = frames
        self.current = 0
        self.speed = speed
        self.loop = loop
        self.dt = 0
        self.finished = False

    def reset(self):
        self.current = 0
        self.finished = False

    def update(self, dt):
        if not self.finished:
            self.nextFrame(dt)
        if self.current == len(self.frames):
            if self.loop:
                self.current = 0
            else:
                self.finished = True
                self.current -= 1
        return self.frames[self.current]

    def nextFrame(self, dt):
        self.dt += dt
        if self.dt < (1.0 / self.speed):
            return
        self.current += 1
        self.dt = 0
