import pygame
from pygame.locals import *
from vector import Vector2
from constants import *

class Pacman(object):
    def __init__(self, node):
        self.name = PACMAN
        self.directions = { STOP: Vector2(),
                            UP: Vector2(0,-1),
                            DOWN: Vector2(0,1),
                            LEFT: Vector2(-1,0),
                            RIGHT: Vector2(1,0) }
        self.direction = STOP
        self.speed = 100 * TILEWIDTH/16
        self.radius = 10
        self.color = YELLOW
        self.node = node
        self.setPosition()
        self.target = node

    def setPosition(self):
        self.position = self.node.position.copy()

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

    def validDirection(self, direction):
        return True if direction is not STOP and \
           self.node.neighbors[direction] is not None \
           else False

    def getNewTarget(self, direction):
        return self.node.neighbors[direction] \
            if self.validDirection(direction) \
               else self.node

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

    def render(self, screen):
        p = self.position.asInt()
        pygame.draw.circle(screen, self.color, p, self.radius)

    def overshotTarget(self):
        if self.target is None:
            return False

        vec1 = self.target.position -  self.node.position
        vec2 = self.position - self.node.position
        node2Target = vec1.magnitudeSquared()
        node2Self = vec2.magnitudeSquared()
        return node2Self >= node2Target

    def reverseDirection(self):
        self.direction *= -1
        self.node, self.target = self.target, self.node

    def oppositeDirection(self, direction):
        if direction is STOP:
            return False
        return True if direction == self.direction * -1 else False

    
