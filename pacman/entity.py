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
        self.radius =  10
        self.collideRadius = 5
        self.color = WHITE
        self.visible = True
        self.goal = None
        self.directionMethod = self.randomDirection
        self.setStartNode(node)
        self.speed = 0
        self.image = None

    def setStartNode(self, node):
        self.node = node
        self.startNode = node
        self.target = node
        self.setPosition()

    def setPosition(self):
        self.position = self.node.position.copy()

    def validDirection(self, direction):
        return True if direction is not STOP \
            and self.name in self.node.access[direction] \
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
        node2Target = vec1.magnitude_squared()
        node2Self = vec2.magnitude_squared()
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
        if self.image is None:
            p = self.position.asInt()
            pygame.draw.circle(screen, self.color, p, self.radius)
        else:
            adjust = Vector2(TILEWIDTH, TILEHEIGHT) / 2
            p = self.position - adjust
            screen.blit(self.image, p.asTuple())

    def update(self, dt):
        self.position += self.directions[self.direction] * self.speed * dt

        if self.overshotTarget():
            self.node = self.target
            directions = self.validDirections()
            direction = self.directionMethod(directions)
            if self.node.neighbors[PORTAL] is not None:
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

    def goalDirection(self, directions):
        distances = []
        for direction in directions:
            vec = self.node.position + self.directions[direction]*TILEWIDTH - self.goal
            distances.append(vec.magnitude_squared())
        index = distances.index(min(distances))
        return directions[index]

    def setBetweenNodes(self, direction):
        if self.node.neighbors[direction] is None:
            return
        self.target = self.node.neighbors[direction]
        self.position = (self.node.position + self.target.position) / 2.0
        
    def reset(self):
        self.setStartNode(self.startNode)
        self.direction = STOP
        self.visible = True
