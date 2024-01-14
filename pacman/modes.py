from constants import *

class MainMode(object):

    cycles = { 0: ((7, 20), (7, 20), (5, 20), (5, float('inf'))),
               1: ((7, 20), (7, 20), (5, 1033), (.017, float('inf'))),
               2: ((7, 20), (7, 20), (5, 1033), (.017, float('inf'))),
               3: ((7, 20), (7, 20), (5, 1033), (.017, float('inf'))),
               4: ((5, 20), (5, 20), (5, 1037), (.017, float('inf'))) }
    
    def __init__(self, level):
        self.timer = 0
        self.cycle = 0
        self.level = level
        self.scatter()

    def update(self, dt):
        self.timer += dt
        if self.timer < self.time:
            return
        if self.mode is SCATTER:
            self.chase()
        elif self.mode is CHASE:
            self.scatter()

    def scatter(self):
        self.mode = SCATTER
        self.time = self.cycles[self.level if self.level < 4 else 4][self.cycle][0]
        self.timer = 0

    def chase(self):
        self.mode = CHASE
        self.time = self.cycles[self.level if self.level < 4 else 4][self.cycle][1]
        if self.cycle < 3:
            self.cycle += 1
        self.timer = 0

        
class ModeController(object):

    def __init__(self, entity, level):
        self.timer = 0
        self.time = None
        self.mainmode = MainMode(level)
        self.current = self.mainmode.mode
        self.entity = entity
        self.flashing = False

    def update(self, dt):
        self.mainmode.update(dt)
        if self.current is FRIGHT:
            self.timer += dt
            if self.timer >= self.time:
                if not self.flashing:
                    self.flashing = True
                    self.time += 2
                else:
                    self.flashing = False
                    self.entity.normalMode()
                    self.current = self.mainmode.mode
        elif self.current in [SCATTER, CHASE]:            
            self.current = self.mainmode.mode

        if self.current is SPAWN and self.entity.node == self.entity.spawnNode:
            self.entity.normalMode()
            self.current = self.mainmode.mode

    def setSpawnMode(self):
        if self.current is FRIGHT:
            self.current = SPAWN                

    def setFrightMode(self):
        if self.current in [SCATTER, CHASE]:
            self.timer = 0
            self.time = 5
            self.current = FRIGHT
        elif self.current is FRIGHT:
            self.timer = 0
