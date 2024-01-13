import pygame
from entity import Entity
from constants import *
from sprites import FruitSprites

POINTS = { 0: 100, # cherries
           1: 300, # strawberry
           2: 500, # orange
           3: 500, # orange
           4: 700, # apple
           5: 700, # apple
           6: 1000, # pineapple
           7: 1000, # pineapple
           8: 2000, # bird
           9: 2000, # bird
           10: 3000, # bell
           11: 3000, # bell
           12: 5000 } # key

class Fruit(Entity):

    def __init__(self, node, level=0):
        Entity.__init__(self, node)
        self.name = FRUIT
        self.color = GREEN
        self.lifespan = 5
        self.timer = 0
        self.destroy = False
        self.points = POINTS[level] if level < 12 else POINTS[12]
        self.setBetweenNodes(RIGHT)
        self.sprites = FruitSprites(self, level)

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.lifespan:
            self.destroy = True
