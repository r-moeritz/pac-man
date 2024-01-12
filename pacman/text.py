import pygame
from vector import Vector2
from constants import *

class Text(object):

    def __init__(self, text, color, x, y, size, time=None, id=None, visible=True):
        self.id = id
        self.text = text
        self.color = color
        self.size = size
        self.visible = visible
        self.position = Vector2(x, y)
        self.timer = 0
        self.lifespan = time
        self.label = None
        self.destroy = False
        self.setupFont('PressStart2P-Regular.ttf')
        self.createLabel()

    def setupFont(self, fontPath):
        self.font = pygame.font.Font(fontPath, self.size)

    def createLabel(self):
        self.label = self.font.render(self.text, 1, self.color)

    def setText(self, newText):
        self.text = str(newText)
        self.createLabel()

    def update(self, dt):
        if self.lifespan is None:
            return
        self.timer += dt
        if self.timer >= self.lifespan:
            self.timer = 0
            self.lifespan = None
            self.destroy = True

    def render(self, screen):
        if not self.visible:
            return
        x,y = self.position.asTuple()
        screen.blit(self.label, (x, y))

        
class TextGroup(object):

    def __init__(self):
        self.nextId = 10
        self.allText = {}
        self.setupText()
        self.showText(READYTXT)

    def addText(self,  text, color, x, y, size, time=None, id=None):
        self.nextId += 1
        self.allText[self.nextId] = Text(text, color, x, y, size, time=time, id=id)
        return self.nextId

    def removeText(self, id):
        self.allText.pop(id)

    def setupText(self):
        size = TILEHEIGHT
        self.allText[SCORETXT] = Text('0'.zfill(8), WHITE, 0, TILEHEIGHT, size)
        self.allText[LEVELTXT] = Text(str(1).zfill(3), WHITE, 23*TILEWIDTH, TILEHEIGHT, size)
        self.allText[READYTXT] = Text('READY!', YELLOW, 11.25*TILEWIDTH, 20*TILEHEIGHT, size, visible=False)
        self.allText[PAUSETXT] = Text('PAUSED!', YELLOW, 10.625*TILEWIDTH, 20*TILEHEIGHT, size, visible=False)
        self.allText[GAMEOVERTXT] = Text('GAMEOVER!', YELLOW, 10*TILEWIDTH, 20*TILEHEIGHT, size, visible=False)
        self.addText('SCORE', WHITE, 0, 0, size)
        self.addText('LEVEL', WHITE, 23*TILEWIDTH, 0, size)

    def update(self, dt):
        for tkey in list(self.allText.keys()):
            self.allText[tkey].update(dt)
            if self.allText[tkey].destroy:
                self.removeText(tkey)

    def showText(self, id):
        self.hideText()
        self.allText[id].visible = True

    def hideText(self):
        self.allText[READYTXT].visible = False
        self.allText[PAUSETXT].visible = False
        self.allText[GAMEOVERTXT].visible = False

    def updateScore(self, score):
        self.updateText(SCORETXT, str(score).zfill(8))

    def updateLevel(self, level):
        self.updateText(LEVELTXT, str(level + 1).zfill(3))

    def updateText(self, id, value):
        if id in self.allText.keys():
            self.allText[id].setText(value)

    def render(self, screen):
        for tkey in list(self.allText.keys()):
            self.allText[tkey].render(screen)

