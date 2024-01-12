import pygame
from pygame.locals import *
from constants import *
from pacman import Pacman
from nodes import NodeGroup
from pellets import PelletGroup
from ghosts import GhostGroup
from fruit import Fruit
from pause import Pause

class GameController(object):
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.background = None
        self.clock = pygame.time.Clock()
        self.fruit = None
        self.pause = Pause(True)
        self.level = 0
        self.lives = 3

    def restartGame(self):
        self.lives = 3
        self.level = 0
        self.pause.paused = True
        self.fruit = None
        self.startGame()

    def resetLevel(self):
        self.pause.paused = True
        self.pacman.reset()
        self.ghosts.reset()
        self.fruit = None

    def nextLevel(self):
        self.showEntities()
        self.level += 1
        self.pause.paused = True
        self.fruit = None
        self.startGame()

    def setBackground(self):
        self.background = pygame.surface.Surface(SCREENSIZE).convert()
        self.background.fill(BLACK)

    def startGame(self):
        self.setBackground()
        self.nodes = NodeGroup('maze.txt')
        self.nodes.setPortalPair((0,17), (27,17))
        homekey = self.nodes.createHomeNodes(11.5, 14)
        self.nodes.connectHomeNodes(homekey, (12,14), LEFT)
        self.nodes.connectHomeNodes(homekey, (15,14), RIGHT)        
        self.pacman = Pacman(self.nodes.getNodeFromTiles(15, 26))        
        self.pellets = PelletGroup('maze.txt')
        self.ghosts = GhostGroup(self.nodes.getStartTempNode(), self.pacman)
        self.ghosts.blinky.setStartNode(self.nodes.getNodeFromTiles(2+11.5, 0+14))
        self.ghosts.pinky.setStartNode(self.nodes.getNodeFromTiles(2+11.5, 3+14))
        self.ghosts.inky.setStartNode(self.nodes.getNodeFromTiles(0+11.5, 3+14))
        self.ghosts.clyde.setStartNode(self.nodes.getNodeFromTiles(4+11.5, 3+14))
        self.ghosts.setSpawnNode(self.nodes.getNodeFromTiles(2+11.5, 3+14))

    def update(self):
        dt = self.clock.tick(30) / 1000.0
        self.pellets.update(dt)
        if not self.pause.paused:
            self.pacman.update(dt)
            self.ghosts.update(dt)
            if self.fruit is not None:
                self.fruit.update(dt)
            self.checkPelletEvents()
            self.checkGhostEvents()
            self.checkFruitEvents()
        afterPauseMethod = self.pause.update(dt)
        if afterPauseMethod is not None:
            afterPauseMethod()
        self.checkEvents()
        self.render()

    def checkFruitEvents(self):
        if (self.pellets.numEaten == 50 or self.pellets.numEaten == 140) \
           and self.fruit is None:
            self.fruit = Fruit(self.nodes.getNodeFromTiles(9, 20))

        if self.fruit is None:
            return
        if self.pacman.collideCheck(self.fruit) \
           or self.fruit.destroy:
            self.fruit = None

    def checkGhostEvents(self):
        for ghost in self.ghosts:
            if not self.pacman.collideGhost(ghost):
                return
            if ghost.mode.current is FREIGHT:
                self.pacman.visible = False
                ghost.visible = False
                self.pause.setPause(pauseTime=1, func=self.showEntities)
                ghost.startSpawn()
            elif ghost.mode.current is not SPAWN and self.pacman.alive:
                self.lives -= 1
                self.pacman.die()
                self.ghosts.hide()
                if self.lives == 0:
                    self.pause.setPause(pauseTime=3, func=self.restartGame)
                else:
                    self.pause.setPause(pauseTime=3, func=self.resetLevel)

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN and event.key == K_SPACE \
                 and self.pacman.alive:
                self.pause.setPause(playerPaused=True)
                if not self.pause.paused:
                    self.showEntities()
                else:
                    self.hideEntities()

    def render(self):
        self.screen.blit(self.background, (0,0))
        self.nodes.render(self.screen)
        self.pellets.render(self.screen)
        if self.fruit is not None:
            self.fruit.render(self.screen)
        self.pacman.render(self.screen)
        self.ghosts.render(self.screen)
        pygame.display.update()

    def checkPelletEvents(self):
        pellet = self.pacman.eatPellets(self.pellets.pelletList)
        if not pellet:
            return
        self.pellets.numEaten += 1
        self.pellets.pelletList.remove(pellet)
        if pellet.name is POWERPELLET:
            self.ghosts.startFreight()
        if self.pellets.isEmpty():
            self.hideEntities()
            self.pause.setPause(pauseTime=3, func=self.nextLevel)

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
