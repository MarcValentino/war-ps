import pygame
from pygame import Surface

class Window:
  def __init__(self, width, height):
    self.displaySize = self.width, self.height = width, height
    self.display = pygame.display.set_mode(self.displaySize, pygame.HWSURFACE | pygame.DOUBLEBUF)
    self.display.fill((12, 101, 164))
    
  def showMap(self, mapSurface: Surface):
    self.display.blit(mapSurface, mapSurface.get_rect())
