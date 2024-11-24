import pygame
from constants import *
import numpy as np
from animation import Animator
from pathlib  import PurePath

BASETILEWIDTH = 16
BASETILEHEIGHT = 16
DEATH = 5

class Spritesheet(object):

    def __init__(self):
        self.sheet = pygame.image.load(PurePath('assets', 'spritesheet.png')).convert()
        transcolor = self.sheet.get_at((0, 0))
        self.sheet.set_colorkey(transcolor)
        width = int(self.sheet.get_width() / BASETILEWIDTH * TILEWIDTH)
        height = int(self.sheet.get_height() / BASETILEHEIGHT * TILEHEIGHT)
        self.sheet = pygame.transform.scale(self.sheet, (width, height))

    def getImage(self, x, y, width, height):
        x *= TILEWIDTH
        y *= TILEHEIGHT
        self.sheet.set_clip(pygame.Rect(x, y, width, height))
        return self.sheet.subsurface(self.sheet.get_clip())


class PacmanSprites(Spritesheet):

    def __init__(self, entity):
        Spritesheet.__init__(self)
        self.entity = entity
        self.entity.image = self.getStartImage()
        self.animations = {}
        self.defineAnimations()
        self.stopImage = (8, 0)

    def getStartImage(self):
        return self.getImage(4, 0)

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)

    def defineAnimations(self):
        self.animations[LEFT] = Animator(((4,0), (6, 0), (8, 0), (6, 0)))
        self.animations[RIGHT] = Animator(((4,0), (2, 0), (0, 0), (2, 0)))
        self.animations[UP] = Animator(((4,0), (10, 0), (12, 0), (10, 0)))
        self.animations[DOWN] = Animator(((4,0), (14, 0), (16, 0), (14, 0)))
        self.animations[DEATH] = Animator(((0, 2), (2, 2), (4, 2),
                                           (6, 2), (8, 2), (10, 2),
                                           (12, 2), (14, 2), (16, 2),
                                           (18, 2), (20, 2)),
                                          speed=3.5, loop=False)

    def update(self, dt):
        if self.entity.alive:
            if self.entity.direction == LEFT:
                self.entity.image = self.getImage(*self.animations[LEFT].update(dt))
                self.stopimage = (6, 0)
            elif self.entity.direction == RIGHT:
                self.entity.image = self.getImage(*self.animations[RIGHT].update(dt))
                self.stopimage = (2, 0)
            elif self.entity.direction == DOWN:
                self.entity.image = self.getImage(*self.animations[DOWN].update(dt))
                self.stopimage = (14, 0)
            elif self.entity.direction == UP:
                self.entity.image = self.getImage(*self.animations[UP].update(dt))
                self.stopimage = (10, 0)
            elif self.entity.direction == STOP:
                self.entity.image = self.getImage(*self.stopimage)
        else:
            self.entity.image = self.getImage(*self.animations[DEATH].update(dt))

    def reset(self):
        for key in list(self.animations.keys()):
            self.animations[key].reset()
    

class GhostSprites(Spritesheet):

    def __init__(self, entity):
        Spritesheet.__init__(self)
        self.y = { BLINKY:4, PINKY:6, INKY:8, CLYDE:10 }
        self.entity = entity
        self.entity.image = self.getStartImage()
        self.flashTime = 0.2
        self.flashTimer = 0
        self.flashed = False
        self.animations = {}
        self.frightAnimations = {}
        self.flashAnimations = {}
        self.defineAnimations()

    def getStartImage(self):
        return self.getImage(4, self.y[self.entity.name])

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)

    def defineAnimations(self):
        y = self.y[self.entity.name]
        self.animations[LEFT] = Animator(((8, y), (10, y)))
        self.animations[RIGHT] = Animator(((0, y), (2, y)))
        self.animations[UP] = Animator(((0, y), (2, y)))
        self.animations[DOWN] = Animator(((12, y), (14, y)))
        y = 14
        self.frightAnimations = Animator(((0, y), (2, y)))
        self.flashAnimations = Animator(((4, y), (6, y)))
    
    def update(self, dt):
        y = self.y[self.entity.name]
        if self.entity.mode.current in [SCATTER, CHASE]:
            self.flashTimer = 0
            self.flashed = False
            if self.entity.direction == LEFT:
                self.entity.image = self.getImage(*self.animations[LEFT].update(dt))
            elif self.entity.direction == RIGHT:
                self.entity.image = self.getImage(*self.animations[RIGHT].update(dt))
            elif self.entity.direction == DOWN:
                self.entity.image = self.getImage(*self.animations[DOWN].update(dt))
            elif self.entity.direction == UP:
                self.entity.image = self.getImage(*self.animations[UP].update(dt))
        elif self.entity.mode.current is FRIGHT:
            if self.entity.mode.flashing:
                self.flashTimer += dt
                if self.flashTimer >= self.flashTime:
                    self.flashTimer = 0
                    if self.flashed:
                        self.entity.image = self.getImage(*self.flashAnimations.update(dt))
                        self.flashed = False
                    else:
                        self.entity.image = self.getImage(*self.frightAnimations.update(dt))
                        self.flashed = True
            else:
                self.entity.image = self.getImage(*self.frightAnimations.update(dt))
        elif self.entity.mode.current is SPAWN:
            self.flashTimer = 0
            self.flashed = False
            if self.entity.direction == LEFT:
                self.entity.image = self.getImage(8, 12)
            elif self.entity.direction == RIGHT:
                self.entity.image = self.getImage(0, 12)
            elif self.entity.direction == DOWN:
                self.entity.image = self.getImage(4, 12)
            elif self.entity.direction == UP:
               self.entity.image = self.getImage(12, 12)


class FruitSprites(Spritesheet):

    sprites = ( (6,16), # cherries
                (4,16), # strawberry
                (2,16), # orange
                (2,16), # orange
                (0,16), # apple
                (0,16), # apple
                (8,16), # pineapple
                (8,16), # pineapple
                (10,16), # bird
                (10,16), # bird
                (12,16), # bell
                (12,16), # bell
                (14,16) )  # key
    
    def __init__(self, level):
        Spritesheet.__init__(self)
        self.image = self.getStartImage(level if level < len(self.sprites) else -1)

    def getStartImage(self, key):
        return self.getImage(*self.sprites[key])

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)


class LifeSprites(Spritesheet):

    def __init__(self, numlives):
        Spritesheet.__init__(self)
        self.resetLives(numlives)

    def removeImage(self):
        if len(self.images) != 0:
            self.images.pop(0)

    def addImage(self):
        self.images.append(self.getImage(6, 0))

    def resetLives(self, numlives):
        self.images = []
        for i in range(numlives):
            self.images.append(self.getImage(6, 0))

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)


class MazeSprites(Spritesheet):

    def __init__(self, mazefile, rotfile):
        Spritesheet.__init__(self)
        self.data = self.readMazeFile(mazefile)
        self.rotdata = self.readMazeFile(rotfile)

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, TILEWIDTH, TILEHEIGHT)

    def readMazeFile(self, mazefile):
        return np.loadtxt(mazefile, dtype='<U1')

    def constructBackground(self, background, y):
        for row in list(range(self.data.shape[0])):
            for col in list(range(self.data.shape[1])):
                if self.data[row][col].isdigit():
                    x = int(self.data[row][col])                    
                    sprite = self.getImage(x, y + 20)
                    rotval = int(self.rotdata[row][col])
                    sprite = self.rotate(sprite, rotval)
                    background.blit(sprite, (col*TILEWIDTH, row*TILEHEIGHT))
                elif self.data[row][col] == '=':
                    sprite = self.getImage(10, 20)
                    background.blit(sprite, (col*TILEWIDTH, row*TILEHEIGHT))
        return background

    def rotate(self, sprite, value):
        return pygame.transform.rotate(sprite, value*90)
