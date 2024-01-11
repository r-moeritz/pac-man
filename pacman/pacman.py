import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity

class Pacman(Entity):
    
    def __init__(self, node):
        Entity.__init__(self, node)
        self.name = PACMAN
        self.color = YELLOW

    def update(self, dt):
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
        for pellet in pelletList:
            d = self.position - pellet.position
            dSquared = d.magnitudeSquared()
            rSquared = (pellet.radius + self.collideRadius)**2
            if dSquared <= rSquared:
                return pellet

        return None
