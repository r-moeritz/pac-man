import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from random import randint

class Entity(object):

    def __init__(self, node):
        self.name = None
        self.directions = { UP: Vector2(0, -1),
                            DOWN: Vector2(0, 1),
                            LEFT: Vector2(-1, 0),
                            RIGHT: Vector2(1, 0),
                            STOP: Vector2() }
        self.direction = STOP
        self.setSpeed(100)
        self.radius =  10
        self.collideRadius = 5
        self.color = WHITE
        self.node = node
        self.setPosition()
        self.target = node
        self.visible = True
        self.disablePortal = False

    def setPosition(self):
        self.position = self.node.position.copy()

    def validDirection(self, direction):
        return True if direction is not STOP \
            and self.node.neighbors[direction] is not None \
            else False

    def getNewTarget(self, direction):
        return self.node.neighbors[direction] \
            if self.validDirection(direction) \
            else self.node

    def overshotTarget(self):
        if self.target is None:
            return False

        vec1 = self.target.position - self.node.position
        vec2 = self.position - self.node.position
        node2Target = vec1.magnitudeSquared()
        node2Self = vec2.magnitudeSquared()
        return node2Self >= node2Target

    def reverseDirection(self):
        self.direction *= -1
        self.node,self.target = self.target,self.node

    def oppositeDirection(self, direction):
        return True if direction is not STOP \
            and direction == self.direction * - 1 \
            else False

    def setSpeed(self, speed):
        self.speed = speed * TILEWIDTH / 16

    def render(self, screen):
        if not self.visible:
            return

        p = self.position.asInt()
        pygame.draw.circle(screen, self.color, p, self.radius)

    def update(self, dt):
        self.position += self.directions[self.direction] * self.speed * dt

        if self.overshotTarget():
            self.node = self.target
            directions = self.validDirections()
            direction = self.randomDirection(directions)
            if not self.disablePortal and self.node.neighbors[PORTAL] is not None:
                self.node = self.node.neighbors[PORTAL]
            self.target = self.getNewTarget(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.getNewTarget(self.direction)

            self.setPosition()

    def validDirections(self):
        directions = []
        for key in [UP, DOWN, LEFT, RIGHT]:
            if self.validDirection(key) and key != self.direction * -1:
                directions.append(key)
        if len(directions) == 0:
            directions.append(self.direction * -1)
        return directions

    def randomDirection(self, directions):
        return directions[randint(0, len(directions) - 1)]

                    