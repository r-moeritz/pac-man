import pygame
from pygame.locals import *
from constants import *
from entity import Entity
from sprites import PacmanSprites
from modes import PacmanModeController

JOY_AXIS_TH = .7 # Threshold of joystick x/y axis (between 0 and 1)

class Pacman(Entity):

    # normal, pellet-eating, fright-mode, and fright-mode+pellet-eating speeds by level
    speeds = ( (int(SPEED*.8), int(SPEED*.71), int(SPEED*.9), int(SPEED*.79)),
               (int(SPEED*.9), int(SPEED*.79), int(SPEED*.95), int(SPEED*.83)),
               (int(SPEED*.9), int(SPEED*.79), int(SPEED*.95), int(SPEED*.83)),
               (int(SPEED*.9), int(SPEED*.79), int(SPEED*.95), int(SPEED*.83)),
               (SPEED, int(SPEED*.87), SPEED, int(SPEED*.87)),
               (SPEED, int(SPEED*.87), SPEED, int(SPEED*.87)),
               (SPEED, int(SPEED*.87), SPEED, int(SPEED*.87)),
               (SPEED, int(SPEED*.87), SPEED, int(SPEED*.87)),
               (SPEED, int(SPEED*.87), SPEED, int(SPEED*.87)),
               (SPEED, int(SPEED*.87), SPEED, int(SPEED*.87)),
               (SPEED, int(SPEED*.87), SPEED, int(SPEED*.87)),
               (SPEED, int(SPEED*.87), SPEED, int(SPEED*.87)),
               (SPEED, int(SPEED*.87), SPEED, int(SPEED*.87)),
               (SPEED, int(SPEED*.87), SPEED, int(SPEED*.87)),
               (SPEED, int(SPEED*.87), SPEED, int(SPEED*.87)),
               (SPEED, int(SPEED*.87), SPEED, int(SPEED*.87)),
               (SPEED, int(SPEED*.87), SPEED, int(SPEED*.87)),
               (SPEED, int(SPEED*.87), SPEED, int(SPEED*.87)),
               (SPEED, int(SPEED*.87), SPEED, int(SPEED*.87)),
               (SPEED, int(SPEED*.87), SPEED, int(SPEED*.87)),
               (int(SPEED*.9), int(SPEED*.79), int(SPEED*.95), int(SPEED*.83)) )
    
    def __init__(self, node, level, joysticks):
        Entity.__init__(self, node)
        self.name = PACMAN
        self.color = YELLOW
        self.direction = LEFT
        self.setBetweenNodes(LEFT)
        self.alive = True
        self.level = level
        self.joysticks = joysticks
        self.sprites = PacmanSprites(self)
        self.setSpeed(self.speeds[level if level < len(self.speeds) else -1][0])
        self.mode = PacmanModeController(self, self.level)

    def reset(self):
        Entity.reset(self)
        self.direction = LEFT
        self.setBetweenNodes(LEFT)
        self.alive = True
        self.image = self.sprites.getStartImage()
        self.sprites.reset()
        self.setSpeed(self.speeds[self.level if self.level < len(self.speeds) else -1][0])

    def die(self):
        self.alive = False
        self.direction = STOP
        self.normalMode()

    def update(self, dt):
        self.sprites.update(dt)
        self.mode.update(dt)
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
        if not self.visible or not self.alive:
            return STOP
        
        if len(self.joysticks) != 0:
            joy = self.joysticks[0]
            hx,hy = (0, 0) if joy.get_numhats() == 0 else joy.get_hat(0)
            ax,ay = (0, 0) if joy.get_numaxes() < 2 else (joy.get_axis(0), joy.get_axis(1))

            if hy == 1 or ay < -JOY_AXIS_TH:
                return UP
            elif hy == -1 or ay > JOY_AXIS_TH:
                return DOWN
            elif hx == -1 or ax < -JOY_AXIS_TH:
                return LEFT
            elif hx == 1 or ax > JOY_AXIS_TH:
                return RIGHT
        
        key_pressed = pygame.key.get_pressed()
        if self.alive:
            if key_pressed[K_UP]:
                return UP
            elif key_pressed[K_DOWN]:
                return DOWN
            elif key_pressed[K_LEFT]:
                return LEFT
            elif key_pressed[K_RIGHT]:
                return RIGHT
            
        return STOP

    def eatPellets(self, pelletList):
        eat = None
        for pellet in pelletList:
            if self.collideCheck(pellet):
                eat = pellet
                break
        if self.mode.fright:
            self.setSpeed(self.speeds[self.level if self.level < len(self.speeds) else -1][3 if eat else 2])
        else:
            self.setSpeed(self.speeds[self.level if self.level < len(self.speeds) else -1][1 if eat else 0])
        return eat

    def collideGhost(self, ghost):
        return self.collideCheck(ghost)

    def collideCheck(self, other):
        d = self.position - other.position
        dSquared = d.magnitude_squared()
        rSquared = (other.radius + self.collideRadius)**2
        return dSquared <= rSquared

    def startFright(self):
        self.mode.setFrightMode()
        self.setSpeed(self.speeds[self.level if self.level < len(self.speeds) else -1][2])

    def normalMode(self):
        self.setSpeed(self.speeds[self.level if self.level < len(self.speeds) else -1][0])
