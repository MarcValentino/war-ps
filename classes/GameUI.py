import pygame_gui
import pygame

class GameUI:
  def __init__(self, coordinates: tuple[int, int]):
    self.manager = pygame_gui.UIManager(coordinates)
    self.blitzButton = pygame_gui.elements.UIButton(
      relative_rect=pygame.Rect((-340, -100), (100, 50)),
      text='Blitz',
      manager=self.manager,
      anchors={
        'right': 'right',
        'bottom': 'bottom'
      }
    )
    # self.blitzButton.hide()
    self.blitzButton.disable()
    self.selectableTroops = pygame_gui.elements.UISelectionList(
      relative_rect=pygame.Rect((308, -100), (200, 70)),
      item_list=[], manager=self.manager,
      anchors={
        'left': 'left',
        'bottom': 'bottom'
      }
    )
    # self.selectableTroops.hide()
    self.selectableTroops.disable()

    self.phase = 'Inactive'
  
  def addItemsToSelectableTroops(self, soldierRange: list[str]):
    self.selectableTroops.add_items(soldierRange)

  def setPhase(self, phase: str):    
    if phase == 'Inactive':
      print("hiding ui")
      self.selectableTroops.remove_items(list(map(lambda x: x['text'], self.selectableTroops.item_list)))
      self.selectableTroops.disable()
      if self.blitzButton.is_enabled:
        self.blitzButton.disable()
    elif phase == 'Attack':
      self.blitzButton.enable()
      self.selectableTroops.enable()
    elif phase == 'Move' or phase == 'Deploy':
      self.selectableTroops.enable()
    self.phase = phase

  def getSelectedOptionFromList(self):
    selection = list(filter(lambda item: item['selected'] == True, self.selectableTroops.item_list))
    print("selection: {}".format(selection))
    if len(selection) == 0: return None
    return int(selection[0]['text'])
  
  def verifyMouseCollision(self, mouseX, mouseY):
    return self.blitzButton.hovered or self.selectableTroops.rect.collidepoint(mouseX, mouseY)
  
  def drawGUI(self, map: pygame.Surface):
    self.manager.draw_ui(map)
    