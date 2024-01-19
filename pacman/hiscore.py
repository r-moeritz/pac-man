import os.path
import pickle

class HiScoreImpl(object):

    def __init__(self, hs):
        self.hs = hs

    def set(self, hs):
        if hs > self.hs:
            self.hs = hs
            return True
        return False

    def __str__(self):
        return str(self.hs) if self.hs > 0 else ''

    
class HighScore(object):

    HSFILE='hiscore'

    def __init__(self):
        if os.path.isfile(self.HSFILE):
            with open(self.HSFILE, 'rb') as f:
                self.impl = pickle.load(f)
        else:
            self.impl = HiScoreImpl(0)

    def set(self, hs):
        if not self.impl.set(hs):
            return
        with open(self.HSFILE, 'wb') as f:
            bytes = pickle.dumps(self.impl)
            f.write(bytes)

    def __str__(self):
        return str(self.impl)
