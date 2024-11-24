from constants import *


class GhostMainMode:

    # times for scatter/chase mode cycles by level
    cycles = ( ((7, 20), (7, 20), (5, 20), (5, float('inf'))),
               ((7, 20), (7, 20), (5, 1033), (.017, float('inf'))),
               ((7, 20), (7, 20), (5, 1033), (.017, float('inf'))),
               ((7, 20), (7, 20), (5, 1033), (.017, float('inf'))),
               ((5, 20), (5, 20), (5, 1037), (.017, float('inf'))) )


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
        self.time = self.cycles[self.level if self.level < len(self.cycles) else -1][self.cycle][0]
        self.timer = 0


    def chase(self):
        self.mode = CHASE
        self.time = self.cycles[self.level if self.level < len(self.cycles) else -1][self.cycle][1]
        if self.cycle < 3:
            self.cycle += 1
        self.timer = 0


# fright times by level
FRIGHT_TIMES = ( 6, 5, 4, 3, 2, 5, 2, 2,
                 1, 5, 2, 1, 1, 3, 1 )


class GhostModeController:

    def __init__(self, entity, level):
        self.timer = 0
        self.time = None
        self.level = level
        self.mainmode = GhostMainMode(level)
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
                    self.time += int(FRIGHT_TIMES[self.level if self.level < len(FRIGHT_TIMES) else -1] * .4)
                else:
                    self.flashing = False
                    self.entity.normalMode()
                    self.current = self.mainmode.mode
        elif self.current in [SCATTER, CHASE]:
            self.flashing = False
            self.current = self.mainmode.mode

        if self.current is SPAWN:
            self.flashing = False
            if self.entity.node == self.entity.spawnNode:
                self.entity.normalMode()
                self.current = self.mainmode.mode


    def setSpawnMode(self):
        if self.current is FRIGHT:
            self.current = SPAWN


    def setFrightMode(self):
        if self.current in (SCATTER, CHASE):
            self.timer = 0
            self.time = int(FRIGHT_TIMES[self.level if self.level < len(FRIGHT_TIMES) else -1] * .6)
            self.current = FRIGHT
        elif self.current is FRIGHT:
            self.timer = 0


class PacmanModeController:

    def __init__(self, entity, level):
        self.timer = 0
        self.time = None
        self.fright = False
        self.entity = entity
        self.level = level


    def update(self, dt):
        if not self.fright:
            return
        self.timer += dt
        if self.timer < self.time:
            return
        self.fright = False
        self.entity.normalMode()


    def setFrightMode(self):
        self.timer = 0
        if self.fright:
            return
        self.fright = True
        self.time = FRIGHT_TIMES[self.level if self.level < len(FRIGHT_TIMES) else -1]
