import pygame

class GraphicalMap:
  def __init__(self, mapImageLocation: str, windowWidth: int, windowHeight: int):
    self.unscaledMap: pygame.Surface = pygame.image.load(mapImageLocation)
    self.width = windowWidth
    self.height = windowHeight
    self.scale = [windowWidth / self.unscaledMap.get_width(), windowHeight / self.unscaledMap.get_height()]
    self.image: pygame.Surface = pygame.transform.smoothscale(self.unscaledMap, (self.unscaledMap.get_width() * self.scale[0], self.unscaledMap.get_height() * self.scale[1]))

  def scaleAndBlit(self, surface: pygame.Surface, posX: int, posY: int):
    scaledSurf = pygame.transform.scale(surface.convert_alpha(), (surface.get_width() * self.scale[0], surface.get_height() * self.scale[1]))
    self.image.blit(scaledSurf, [posX, posY])