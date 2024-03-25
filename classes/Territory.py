from functools import *

class Territory():
  def __init__(self, neighbours: list[int], regionId: int, territoryName: str, territoryId: int, pos_x: int, pos_y: int, text_center_x: int, text_center_y: int):
    self.id = territoryId
    self.neighbours = neighbours
    self.numberOfTroops = 4
    self.regionId = regionId
    self.name = territoryName
    # self.color = color            # RETIRAR DEPOIS DO TESTEEEEEEEE
    self.pos_x = pos_x
    self.pos_y = pos_y
    self.bst = 0      # border security threat -> quantidade de tropas inimigas em volta do territorio
    self.bsr = 0      # border security ratio  -> bst / quantidade de tropas no territorio
    self.text_x = text_center_x
    self.text_y = text_center_y
    
  def getNonDefendingTroops(self) -> int:
    return self.numberOfTroops - 1
  
  def getDefendingTroops(self) -> int:
    return self.numberOfTroops
  
  def canAttack(self) -> bool:
    return self.getNonDefendingTroops() > 0
  
  def hasAliveTroops(self) -> bool:
    return self.numberOfTroops > 0
  
  def colonize(self, colonizerColor: str):
    self.color = colonizerColor
  
  def gainTroops(self, troops: int) -> bool:
    if troops <= 0:
      return False
    self.numberOfTroops += troops
    return True
  
  def loseTroops(self, troops: int) -> int:
    if troops <= 0:
      return 0
    remainingTroops = max(self.numberOfTroops - troops, 0)
    troopsLost = self.numberOfTroops - remainingTroops
    self.numberOfTroops = remainingTroops
    return troopsLost
    
  def deallocateTroops(self, troops: int) -> int:
    return self.loseTroops(min(self.getNonDefendingTroops(), troops))


  # precisava usar essa funcao e nao dava pra importar de GammeMap
  # nao sei se vai dar tempo de fazer uma outra classe soh com funcoes auxiliares
  def getHostileTerritoryNeighbours(self, territories):
    hostiles = []
    neighbours_obj = []
    for territory in territories:
      if territory.id in self.neighbours:
        neighbours_obj.append(territory)
      
    for neighbour in neighbours_obj:
      if neighbour.color != self.color:
        hostiles.append(neighbour)

    return hostiles

  def set_bst(self, territories):
        self.bst = 0
        hostile_neighbours = self.getHostileTerritoryNeighbours(territories)
        for hostile in hostile_neighbours:
            self.bst = self.bst + hostile.getDefendingTroops()
    
  def set_bsr(self):
      self.bsr = 0
      self.bsr = self.bst / self.getDefendingTroops()
    