import pygame
from entity import Entity
from constants import *
from sprites import FruitSprites

# points for fruit by level
POINTS = ( 100, # cherries
           300, # strawberry
           500, # orange
           500, # orange
           700, # apple
           700, # apple
           1000, # pineapple
           1000, # pineapple
           2000, # bird
           2000, # bird
           3000, # bell
           3000, # bell
           5000 ) # key

class Fruit(Entity):

    def __init__(self, node, level=0):
        Entity.__init__(self, node)
        self.name = FRUIT
        self.color = GREEN
        self.lifespan = 9.5 # actually varies between 9.33 and 9.75 seconds but couldn't be bothered
        self.timer = 0
        self.destroy = False
        self.points = POINTS[level] if level < len(POINTS) else POINTS[-1]
        self.setBetweenNodes(RIGHT)
        self.image = FruitSprites(level).image

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.lifespan:
            self.destroy = True
