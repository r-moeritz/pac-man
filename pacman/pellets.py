import pygame
from vector import Vector2
from constants import *
import numpy as np


class Pellet:

    def __init__(self, row, column):
        self.name = PELLET
        self.position = Vector2(column*TILEWIDTH, row*TILEHEIGHT)
        self.color = LTPINK
        self.radius = int(2 * TILEWIDTH/16)
        self.collideRadius = int(2 * TILEWIDTH/16)
        self.points = 10
        self.visible = True


    def render(self, screen):
        if not self.visible:
            return
        adjust = Vector2(TILEWIDTH, TILEHEIGHT) / 2
        p = self.position + adjust
        pygame.draw.circle(screen, self.color, p.asInt(), self.radius)

        
class PowerPellet(Pellet):

    def __init__(self, row, column):
        Pellet.__init__(self, row, column)
        self.name = POWERPELLET
        self.radius = int(8 * TILEWIDTH / 16)
        self.points = 50
        self.flashTime = 0.2
        self.timer = 0


    def update(self, dt):
        self.timer += dt
        if self.timer < self.flashTime:
            return

        self.visible = not self.visible
        self.timer = 0

        
class PelletGroup:

    def __init__(self, pelletfile):
        self.pelletList = []
        self.powerpellets = []
        self.createPelletList(pelletfile)
        self.numEaten = 0


    def update(self, dt):
        for powerpellet in self.powerpellets:
            powerpellet.update(dt)


    def createPelletList(self, pelletfile):
        data = self.readPelletFile(pelletfile)
        for row in range(data.shape[0]):
            for col in range(data.shape[1]):
                if data[row][col] in ['.', '+']:
                    self.pelletList.append(Pellet(row, col))
                elif data[row][col] in ['P', 'p']:
                    pp = PowerPellet(row, col)
                    self.pelletList.append(pp)
                    self.powerpellets.append(pp)


    def readPelletFile(self, textfile):
        return np.loadtxt(textfile, dtype='<U1')


    @property
    def isEmpty(self):
        return True if len(self.pelletList) == 0 else False


    @property
    def remaining(self):
        return len(self.pelletList)


    def render(self, screen):
        for pellet in self.pelletList:
            pellet.render(screen)

            
