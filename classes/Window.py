import pygame
from pygame import Surface

class Window:
    _instance = None

    def __new__(cls, width, height):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self, width, height):
        if self.__initialized:
            return
        self.__initialized = True
        self.displaySize = self.width, self.height = width, height
        self.display = pygame.display.set_mode(self.displaySize, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.display.fill((12, 101, 164))

    def showMap(self, mapSurface: Surface):
        self.display.blit(mapSurface, mapSurface.get_rect())


