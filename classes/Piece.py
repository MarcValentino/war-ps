import pygame

from classes.Territory import *

COLORS = ["bran", "verm", "verd", "azul", "pret", "amar"]
SELECTED_COLORS = [(38,41,44), (0,51,75), (32,33,26), (34,31,28), (21,21,21), (15,2,79)]

class Piece(pygame.sprite.Sprite):
  def __init__(self, territoryId: int, territoryName: str, territoryColor: str, troops: int, pos_x: int, pos_y: int, text_center_x: int, text_center_y: int):
    super().__init__()
    self.selected = False
    self.color = territoryColor
    self.territoryId = territoryId
    self.name = territoryName
    self.pos_x = pos_x
    self.pos_y = pos_y
    self.text_center_x = text_center_x
    self.text_center_y = text_center_y
    self.troops = troops
    self.loadImageGorup()
    self.updateDefaults()
    
  def loadImageGorup(self):
    self.all_images = pygame.sprite.Group()
    for color in COLORS:
      path = 'classes/assets/images/territories/' + self.name.lower() + '-' + color + '.png'
      sprite = pygame.sprite.Sprite()
      sprite.image = pygame.image.load(path).convert_alpha()
      self.all_images.add(sprite)
      if color == self.color:
        self.sprite = self.all_images.sprites()[len(self.all_images.sprites())-1]
  
  def updatePiece(self, relatedTerritory: Territory):
    self.troops = relatedTerritory.numberOfTroops
    self.sprite = self.all_images.sprites()[COLORS.index(relatedTerritory.color)]
    self.updateDefaults()
    
  def updateDefaults(self):
    self.image = self.sprite.image
    self.mask = pygame.mask.from_surface(self.image)
    imageRect = self.image.get_rect()
    self.rect = pygame.Rect(self.pos_x, self.pos_y, imageRect.width, imageRect.height)