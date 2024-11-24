import pygame


class Vector2(pygame.math.Vector2):
    
    def asTuple(self):
        return self.x, self.y


    def asInt(self):
        return int(self.x), int(self.y)
