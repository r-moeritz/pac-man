import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity
from sprites import PacmanSprites

class Pacman(Entity):

    # normal and pellet-eating speeds by level
    speeds = { 0: (int(SPEED*.8), int(SPEED*.71)),
               1: (int(SPEED*.9), int(SPEED*.79)),
               2: (int(SPEED*.9), int(SPEED*.79)),
               3: (int(SPEED*.9), int(SPEED*.79)),
               4: (SPEED, int(SPEED*.87)),
               5: (SPEED, int(SPEED*.87)),
               6: (SPEED, int(SPEED*.87)),
               7: (SPEED, int(SPEED*.87)),
               8: (SPEED, int(SPEED*.87)),
               9: (SPEED, int(SPEED*.87)),
               10: (SPEED, int(SPEED*.87)),
               11: (SPEED, int(SPEED*.87)),
               12: (SPEED, int(SPEED*.87)),
               13: (SPEED, int(SPEED*.87)),
               14: (SPEED, int(SPEED*.87)),
               15: (SPEED, int(SPEED*.87)),
               16: (SPEED, int(SPEED*.87)),
               17: (SPEED, int(SPEED*.87)),
               18: (SPEED, int(SPEED*.87)),
               19: (SPEED, int(SPEED*.87)),
               20: (int(SPEED*.9), int(SPEED*.79)) }
    
    def __init__(self, node, level):
        Entity.__init__(self, node)
        self.name = PACMAN
        self.color = YELLOW
        self.direction = LEFT
        self.setBetweenNodes(LEFT)
        self.alive = True
        self.level = level
        self.sprites = PacmanSprites(self)
        self.setSpeed(self.speeds[level if level < 20 else 20][0])

    def reset(self):
        Entity.reset(self)
        self.direction = LEFT
        self.setBetweenNodes(LEFT)
        self.alive = True
        self.image = self.sprites.getStartImage()
        self.sprites.reset()
        self.setSpeed(self.speeds[self.level if self.level < 20 else 20][0])

    def die(self):
        self.alive = False
        self.direction = STOP

    def update(self, dt):
        self.sprites.update(dt)
        self.position += self.directions[self.direction] * self.speed * dt
        dir = self.getValidKey()
        if self.overshotTarget():
            self.node = self.target
            if self.node.neighbors[PORTAL] is not None:
                self.node = self.node.neighbors[PORTAL]
                
            self.target = self.getNewTarget(dir)
            
            if self.target is not self.node:
                self.direction = dir
            else:
                self.target = self.getNewTarget(self.direction)
            
            if self.target is self.node:
                self.direction = STOP
                
            self.setPosition()
        elif self.oppositeDirection(dir):
            self.reverseDirection()

    def getValidKey(self):
        key_pressed = pygame.key.get_pressed()
        if self.alive:
            if key_pressed[K_UP]:
                return UP
            if key_pressed[K_DOWN]:
                return DOWN
            if key_pressed[K_LEFT]:
                return LEFT
            if key_pressed[K_RIGHT]:
                return RIGHT
        return STOP

    def eatPellets(self, pelletList):
        eat = None
        for pellet in pelletList:
            if self.collideCheck(pellet):
                eat = pellet
                break
        self.setSpeed(self.speeds[self.level if self.level < 20 else 20][1 if eat else 0])
        return eat

    def collideGhost(self, ghost):
        return self.collideCheck(ghost)

    def collideCheck(self, other):
        d = self.position - other.position
        dSquared = d.magnitudeSquared()
        rSquared = (other.radius + self.collideRadius)**2
        return dSquared <= rSquared
