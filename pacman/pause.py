class Pause:

    def __init__(self, paused=False):
        self.paused = paused
        self.timer = 0
        self.pauseTime = None
        self.func = None


    def update(self, dt):
        if self.pauseTime is None:
            return
        self.timer += dt
        if self.timer < self.pauseTime:
            return None
        self.timer = 0
        self.paused = False
        self.pauseTime = None
        return self.func


    def setPause(self, pauseTime=None, func=None):
        self.timer = 0
        self.func = func
        self.pauseTime = pauseTime
        self.flip()


    def flip(self):
        self.paused = not self.paused
