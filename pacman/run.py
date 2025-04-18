import pygame
from pygame.locals import *
from constants import *
from pacman import Pacman
from nodes import NodeGroup
from pellets import PelletGroup
from ghosts import GhostGroup
from fruit import Fruit
from pause import Pause
from text import TextGroup
from sprites import LifeSprites, MazeSprites, FruitSprites
from hiscore import HighScore
from sounds import Sounds
from pathlib import PurePath


class GameController:
    
    def __init__(self):
        pygame.mixer.pre_init(frequency=48000,
                              size=-16,
                              channels=2,
                              buffer=1024)
        pygame.mixer.init()
        pygame.init()
        icon = pygame.image.load(PurePath('assets', 'icon.png'))
        pygame.display.set_icon(icon)
        pygame.display.set_caption("Pac-Man")
        self.sounds = Sounds()
        self.screen = pygame.display.set_mode(size=SCREENSIZE,
                                              flags=pygame.SCALED | pygame.RESIZABLE)
        self.joysticks = []
        self.background = None
        self.background_norm = None
        self.background_flash = None
        self.clock = pygame.time.Clock()
        self.fruit = None
        self.pause = Pause(False)
        self.level = 0
        self.lives = NUMLIVES
        self.score = 0
        self.hiscore = HighScore()
        self.textgroup = TextGroup()
        self.lifesprites = LifeSprites(self.lives)
        self.flashBG = False
        self.flashTime = 0.2
        self.flashTimer = 0
        self.lastFruit = [FruitSprites(self.level)]
        self.gotExtraLife = False
        self.textgroup.updateScores(self.score, self.hiscore)


    def restartGame(self):
        self.lives = NUMLIVES
        self.lifesprites.resetLives(self.lives)
        self.level = 0
        self.fruit = None
        self.score = 0
        self.textgroup.updateScores(self.score, self.hiscore)
        self.textgroup.showText(READYTXT)
        self.lastFruit = [FruitSprites(self.level)]
        self.pause.setPause() # resume
        self.startGame()


    def resetLevel(self):
        self.pacman.reset()
        self.ghosts.reset()
        self.fruit = None
        self.textgroup.showText(READYTXT)
        self.pause.setPause(pauseTime=1, func=lambda: self.textgroup.hideText() or self.showEntities())


    def nextLevel(self):
        self.level += 1
        self.fruit = None
        if len(self.lastFruit) == 7:
            self.lastFruit.pop(0) # only show last 6 fruit
        self.lastFruit.append(FruitSprites(self.level))
        self.pause.setPause(pauseTime=1, func=lambda: self.startGame(intro=False))


    def setBackground(self):
        self.background_norm = pygame.surface.Surface(SCREENSIZE).convert()
        self.background_norm.fill(BLACK)
        self.background_flash = pygame.surface.Surface(SCREENSIZE).convert()
        self.background_flash.fill(BLACK)
        self.background_norm = self.mazesprites.constructBackground(self.background_norm, 0)
        self.background_flash = self.mazesprites.constructBackground(self.background_flash, 1)
        self.flashBG = False
        self.background = self.background_norm


    def startGame(self, intro=True):
        self.mazesprites = MazeSprites('data/maze', 'data/rotmaze')
        self.setBackground()
        self.nodes = NodeGroup('data/maze')
        self.nodes.setPortalPair((0,17), (27,17))
        homekey = self.nodes.createHomeNodes(11.5, 14)
        self.nodes.connectHomeNodes(homekey, (12,14), LEFT)
        self.nodes.connectHomeNodes(homekey, (15,14), RIGHT)        
        self.pacman = Pacman(self.nodes.getNodeFromTiles(15, 26), self.level, self.joysticks)
        self.pellets = PelletGroup('data/maze')
        self.ghosts = GhostGroup(self.nodes.getStartTempNode(), self.pacman, self.pellets)
        self.ghosts.blinky.setStartNode(self.nodes.getNodeFromTiles(2+11.5, 0+14))
        self.ghosts.pinky.setStartNode(self.nodes.getNodeFromTiles(2+11.5, 3+14))
        self.ghosts.inky.setStartNode(self.nodes.getNodeFromTiles(0+11.5, 3+14))
        self.ghosts.clyde.setStartNode(self.nodes.getNodeFromTiles(4+11.5, 3+14))        
        self.ghosts.setSpawnNode(self.nodes.getNodeFromTiles(2+11.5, 3+14))
        self.nodes.denyHomeAccess(self.pacman)
        self.nodes.denyHomeAccessList(self.ghosts)
        self.nodes.denyAccessList(2+11.5, 3+14, LEFT, self.ghosts)
        self.nodes.denyAccessList(2+11.5, 3+14, RIGHT, self.ghosts)
        self.ghosts.inky.startNode.denyAccess(RIGHT, self.ghosts.inky)
        self.ghosts.clyde.startNode.denyAccess(LEFT, self.ghosts.clyde)
        self.nodes.denyAccessList(12, 14, UP, self.ghosts)
        self.nodes.denyAccessList(15, 14, UP, self.ghosts)
        self.nodes.denyAccessList(12, 26, UP, self.ghosts)
        self.nodes.denyAccessList(15, 26, UP, self.ghosts)

        if intro:
            self.sounds.play(INTROSND)
            self.pause.setPause(pauseTime=4.5,
                                func=lambda: self.textgroup.hideText() \
                                    or self.showEntities())
        else:
            self.pause.setPause(pauseTime=1,
                                func=lambda: self.textgroup.hideText() \
                                    or self.showEntities())


    def update(self):
        dt = self.clock.tick(60) / 1000.0
        self.textgroup.update(dt)
        self.pellets.update(dt)

        if not self.pause.paused:
            self.ghosts.update(dt)
            if self.fruit is not None:
                self.fruit.update(dt)
            self.checkPelletEvents()
            self.checkGhostEvents()
            self.checkFruitEvents()

        if self.pacman.alive:
            if not self.pause.paused:
                self.pacman.update(dt)
        else:
            self.pacman.update(dt)

        if self.flashBG:
            self.flashTimer += dt
            if self.flashTimer >= self.flashTime:
                self.flashTimer = 0
                if self.background == self.background_norm:
                    self.background = self.background_flash
                else:
                    self.background = self.background_norm
            
        afterPauseMethod = self.pause.update(dt)
        if afterPauseMethod is not None:
            afterPauseMethod()
        self.checkEvents()
        self.render()


    def updateScore(self, points):
        self.score += points
        self.hiscore.set(self.score)
        self.textgroup.updateScores(self.score, self.hiscore)


    def checkFruitEvents(self):
        if (self.pellets.numEaten == 70 or self.pellets.numEaten == 170) \
           and self.fruit is None:
            self.fruit = Fruit(self.nodes.getNodeFromTiles(9, 20), self.level)

        if self.fruit is None:
            return
        if self.pacman.collideCheck(self.fruit):
            self.sounds.play(EATFRUITSND)
            self.updateScore(self.fruit.points)
            self.textgroup.addText(str(self.fruit.points), WHITE,
                                   self.fruit.position.x,
                                   self.fruit.position.y,
                                   8, time=1)
            self.fruit = None
        elif self.fruit.destroy:
            self.fruit = None


    def checkGhostEvents(self):
        for ghost in self.ghosts:
            if not self.pacman.collideGhost(ghost):
                continue
            if ghost.mode.current is FRIGHT:                
                self.pacman.visible = False
                ghost.visible = False
                self.sounds.play(EATGHOSTSND)
                self.updateScore(ghost.points)
                self.textgroup.addText(str(ghost.points), WHITE,
                                       ghost.position.x, ghost.position.y,
                                       8, time=1)
                self.ghosts.updatePoints()
                self.pause.setPause(pauseTime=1, func=self.showEntities)
                ghost.startSpawn()
                self.nodes.allowHomeAccess(ghost)
            elif ghost.mode.current is not SPAWN and self.pacman.alive:
                self.lives -= 1
                self.lifesprites.removeImage()                
                self.pacman.die()                
                self.ghosts.hide()
                if self.lives == 0:
                    self.fruit = None
                    self.textgroup.showText(GAMEOVERTXT)
                    self.pause.setPause()
                else:
                    self.pause.setPause(pauseTime=4, func=self.resetLevel)
                self.sounds.play(DYINGSND)


    def checkEvents(self):
        for event in pygame.event.get():
            if (event.type == KEYUP and event.key == K_ESCAPE) \
               or event.type == QUIT:
                exit()
            elif event.type == JOYDEVICEADDED and len(self.joysticks) == 0:
                self.joysticks.append(pygame.joystick.Joystick(event.device_index))
            elif event.type == JOYDEVICEREMOVED and len(self.joysticks) != 0:
                joy = self.joysticks[0]
                if joy.get_instance_id() == event.instance_id:
                    self.joysticks.pop()
            elif ((event.type == KEYDOWN and event.key == K_SPACE) \
                  or event.type == JOYBUTTONDOWN) and not self.flashBG \
                  and not self.pacman.alive and self.lives == 0:
                    self.restartGame()


    def render(self):
        self.screen.blit(self.background, (0,0))
        self.pellets.render(self.screen)
        if self.fruit is not None:
            self.fruit.render(self.screen)
        self.pacman.render(self.screen)
        self.ghosts.render(self.screen)
        self.textgroup.render(self.screen)
        for i in range(len(self.lifesprites.images)):
            x = self.lifesprites.images[i].get_width() * i
            y = SCREENHEIGHT - self.lifesprites.images[i].get_height()
            self.screen.blit(self.lifesprites.images[i], (x, y))
        for i in range(len(self.lastFruit)):
            x = SCREENWIDTH - self.lastFruit[i].image.get_width() * (i+1)
            y = SCREENHEIGHT - self.lastFruit[i].image.get_height()
            self.screen.blit(self.lastFruit[i].image, (x, y))
        pygame.display.update()


    def checkPelletEvents(self):
        if self.pacman.mode.fright:
            self.sounds.play(FRIGHTSND)
        else:
            self.sounds.play(SIRENSND)
        pellet = self.pacman.eatPellets(self.pellets.pelletList)
        if not pellet:
            return
        self.sounds.play(CHOMPSND)
        self.pellets.numEaten += 1
        self.updateScore(pellet.points)
        if self.score >= EXTRALIFE and not self.gotExtraLife:
            self.sounds.play(EXTRAPACSND)
            self.lives += 1
            self.lifesprites.addImage()
            self.gotExtraLife = True
        self.pellets.pelletList.remove(pellet)
        if pellet.name is POWERPELLET:
            self.ghosts.startFright()
        if self.pellets.isEmpty:
            self.flashBG = True
            self.hideEntities()
            self.pause.setPause(pauseTime=3, func=self.nextLevel)
        elif self.ghosts.blinky.isElroy:
            self.ghosts.blinky.setElroySpeed()


    def showEntities(self):
        self.pacman.visible = True
        self.ghosts.show()


    def hideEntities(self):
        self.pacman.visible = False
        self.ghosts.hide()


if __name__ == '__main__':
    game = GameController()
    game.startGame()

    while True:
        game.update()
