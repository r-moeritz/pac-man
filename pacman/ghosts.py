import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity
from modes import GhostModeController
from sprites import GhostSprites

class Ghost(Entity):

    # normal, fright, and portal speeds by level
    speeds = ( (int(SPEED*.75), int(SPEED*.5), int(SPEED*.4)),
               (int(SPEED*.85), int(SPEED*.55), int(SPEED*.45)),
               (int(SPEED*.85), int(SPEED*.55), int(SPEED*.45)),
               (int(SPEED*.85), int(SPEED*.55), int(SPEED*.45)),
               (int(SPEED*.95), int(SPEED*.6), int(SPEED*.5)) )
    
    def __init__(self, node, pacman, blinky=None):
        Entity.__init__(self, node)
        self.name = GHOST
        self.points = 200
        self.goal = Vector2()
        self.directionMethod = self.goalDirection
        self.pacman = pacman
        self.level = pacman.level
        self.mode = GhostModeController(self, self.level)
        self.blinky = blinky
        self.homeNode = node
        self.setSpeed(self.speeds[self.level if self.level < len(self.speeds) else -1][0])

    def update(self, dt):
        self.sprites.update(dt)
        self.mode.update(dt)
        if self.mode.current is SCATTER:
            self.scatter()
        elif self.mode.current is CHASE:
            self.chase()
        if self.mode.current in (SCATTER, CHASE):
            # Slow down in portal or speed back up
            i = 0 if self.node.neighbors[PORTAL] is None else 2
            self.setSpeed(self.speeds[self.level if self.level < len(self.speeds) else -1][i])
        Entity.update(self, dt)

    def scatter(self):
        self.goal = Vector2()

    def chase(self):
        self.goal = self.pacman.position

    def startFright(self):
        self.mode.setFrightMode()
        if self.mode.current is FRIGHT:
            self.setSpeed(self.speeds[self.level if self.level < len(self.speeds) else -1][1])
            self.directionMethod = self.randomDirection

    def normalMode(self):
        self.setSpeed(self.speeds[self.level if self.level < len(self.speeds) else -1][0])
        self.directionMethod = self.goalDirection
        self.homeNode.denyAccess(DOWN, self)

    def spawn(self):
        self.goal = self.spawnNode.position

    def setSpawnNode(self, node):
        self.spawnNode = node

    def startSpawn(self):
        self.mode.setSpawnMode()
        if self.mode.current is SPAWN:
            self.setSpeed(2 * self.speeds[self.level if self.level < len(self.speeds) else -1][0])
            self.directionMethod = self.goalDirection
            self.spawn()

    def reset(self):
        Entity.reset(self)
        self.setSpeed(self.speeds[self.level if self.level < len(self.speeds) else -1][0])
        self.points = 200
        self.directionmethod = self.goalDirection

        
class Blinky(Ghost):

    # Elroy dots left, speed by level
    elroy1 = ( (20, int(SPEED*.8)),
               (30, int(SPEED*.9)),
               (40, int(SPEED*.9)),
               (40, int(SPEED*.9)),
               (40, SPEED),
               (50, SPEED),
               (50, SPEED),
               (50, SPEED),
               (60, SPEED),
               (60, SPEED),
               (60, SPEED),
               (80, SPEED),
               (80, SPEED),
               (80, SPEED),
               (100, SPEED),
               (100, SPEED),
               (100, SPEED),
               (100, SPEED),
               (120, SPEED) )
    elroy2 = ( (10, int(SPEED*.85)),
               (15, int(SPEED*.95)),
               (20, int(SPEED*.95)),
               (20, int(SPEED*.95)),
               (20, int(SPEED*1.05)),
               (25, int(SPEED*1.05)),
               (25, int(SPEED*1.05)),
               (25, int(SPEED*1.05)),
               (30, int(SPEED*1.05)),
               (30, int(SPEED*1.05)),
               (30, int(SPEED*1.05)),
               (40, int(SPEED*1.05)),
               (40, int(SPEED*1.05)),
               (40, int(SPEED*1.05)),
               (50, int(SPEED*1.05)),
               (50, int(SPEED*1.05)),
               (50, int(SPEED*1.05)),
               (50, int(SPEED*1.05)),
               (60, int(SPEED*1.05)) )

    def __init__(self, node, pacman, pellets, blinky=None):
        self.pellets = pellets
        Ghost.__init__(self, node, pacman, blinky)
        self.name = BLINKY
        self.color = RED
        self.sprites = GhostSprites(self)
        self.level = pacman.level

    def scatter(self):
        self.goal = Vector2(TILEWIDTH*NCOLS, 0)

    def setSpeed(self, speed):
        self.setElroySpeed() if self.isElroy else Entity.setSpeed(self, speed)

    def setElroySpeed(self):
        Entity.setSpeed(self, self.elroySpeed)
        
    @property
    def isElroy(self):
        return self.mode.current in (CHASE, SCATTER) \
            and self.elroy1[self.level if self.level < len(self.elroy1) else -1][0] >= self.pellets.remaining

    @property
    def elroySpeed(self):
        elroy2dots = self.elroy2[self.level if self.level < len(self.elroy2) else -1][0]
        return self.elroy2[self.level if self.level < len(self.elroy2) else -1][1] \
            if elroy2dots >= self.pellets.remaining \
            else self.elroy1[self.level if self.level < len(self.elroy1) else -1][1]


class Pinky(Ghost):

    def __init__(self, node, pacman, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = PINKY
        self.color = PINK
        self.sprites = GhostSprites(self)

    def chase(self):
        self.goal = self.pacman.position + \
            self.pacman.directions[self.pacman.direction] * TILEWIDTH * 4

        
class Inky(Ghost):

    def __init__(self, node, pacman, blinky):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = INKY
        self.color = TEAL
        self.sprites = GhostSprites(self)

    def scatter(self):
        self.goal = Vector2(TILEWIDTH*NCOLS, TILEHEIGHT*NROWS)

    def chase(self):
        vec1 = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 2
        vec2 = (vec1 - self.blinky.position) * 2
        self.goal = self.blinky.position + vec2

        
class Clyde(Ghost):

    def __init__(self, node, pacman, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = CLYDE
        self.color = ORANGE
        self.sprites = GhostSprites(self)

    def scatter(self):
        self.goal = Vector2(0, TILEHEIGHT*NROWS)

    def chase(self):
        d = self.pacman.position - self.position
        ds = d.magnitudeSquared()
        if ds <= (TILEWIDTH * 8)**2:
            self.scatter()
        else:
            self.goal = self.pacman.position \
                + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 4

            
class GhostGroup(object):

    def __init__(self, node, pacman, pellets):
        self.pacman = pacman
        self.blinky = Blinky(node, pacman, pellets)
        self.pinky = Pinky(node, pacman)
        self.inky = Inky(node, pacman, self.blinky)
        self.clyde = Clyde(node, pacman)
        self.ghosts = [self.blinky, self.pinky, self.inky, self.clyde]

    def __iter__(self):
        return iter(self.ghosts)

    def update(self, dt):
        for ghost in self:
            ghost.update(dt)

    def startFright(self):
        for ghost in self:
            ghost.startFright()
        self.pacman.startFright()
        self.resetPoints()

    def setSpawnNode(self, node):
        for ghost in self:
            ghost.setSpawnNode(node)

    def updatePoints(self):
        for ghost in self:
            ghost.points *= 2

    def resetPoints(self):
        for ghost in self:
            ghost.points = 200

    def reset(self):
        for ghost in self:
            ghost.reset()

    def hide(self):
        for ghost in self:
            ghost.visible = False

    def show(self):
        for ghost in self:
            ghost.visible = True

    def render(self, screen):
        for ghost in self:
            ghost.render(screen)

