from random import randint
from typing import Tuple
from classes.Territory import *
from classes.Region import *
from functools import *


MAX_OF_DICES_PER_ATTACK = 3

class GameMap():
  def __init__(self, territoryList: list[Territory], regionList: list[Region]):
    self.territories = territoryList
    self.regions = regionList
    self.selectedTerritories = [-1, -1]
   
  def getAllTerritoriesOfColors(self, color: str):
      return list(filter(lambda x: x.color == color, self.territories))
    
  def validateTerritoriesConnections(self) -> bool:
    result = True
    for ind, territory in enumerate(self.territories):
      isCorrect = all(ind in self.territories[neighInd].neighbours for neighInd in territory.neighbours)
      result = result and isCorrect
      if not isCorrect:
        print("Territory id error:", ind)
    return result
  
  def getTerritoryNeighbours(self, index: int) -> list[int]:
    return self.territories[index].neighbours
  
  def getFriendlyTerritoryNeighbours(self, index: int) -> list[int]:
    return list(filter(lambda x: self.territories[x].color == self.territories[index].color, self.territories[index].neighbours))
  
  def getHostileTerritoryNeighbours(self, index: int) -> list[int]:
    return list(filter(lambda x: self.territories[x].color != self.territories[index].color, self.territories[index].neighbours))

  def filterTerritoriesByRegion(self, regionId: int) -> list[int]:
    return list(map(lambda y: y.id, filter(lambda x: x.regionId == regionId, self.territories)))
  
  def canMoveTroopsBetweenFriendlyTerriroriesAux(self, fromTerritoryId: int, toTerritoryId: int, visitedTerritoriesId:list[int], currentPath: list[int]) -> Tuple[bool, list[int]]:
    if fromTerritoryId == toTerritoryId:
      return True, currentPath + [fromTerritoryId]
    if fromTerritoryId in visitedTerritoriesId:
      return False, []
    currentPath += [fromTerritoryId]
    visitedTerritoriesId.append(fromTerritoryId)
    listOfPossiblePaths = list(map(lambda t: self.canMoveTroopsBetweenFriendlyTerriroriesAux(t, toTerritoryId, visitedTerritoriesId, currentPath), self.getFriendlyTerritoryNeighbours(fromTerritoryId)))
    for possiblePath in listOfPossiblePaths:
      if possiblePath[0]:
        return True, possiblePath[1]
    return False, []
  
  def moveTroopsBetweenFriendlyTerrirories(self, fromTerritoryId: int, toTerritoryId: int, numberOfTroops: int, forAI: bool = False):
    if forAI:
      possiblePathToDestiny = self.canMoveTroopsBetweenFriendlyTerriroriesAux(fromTerritoryId, toTerritoryId, [], [])
      if not possiblePathToDestiny[1]:
        return []
    troopsLost = self.territories[fromTerritoryId].deallocateTroops(numberOfTroops)
    self.territories[toTerritoryId].gainTroops(troopsLost)
    # return possiblePathToDestiny[1]
  
  def canMoveTroopsBetweenFriendlyTerritories(self, fromTerritoryId: int, toTerritoryId: int):
    possiblePath = self.canMoveTroopsBetweenFriendlyTerriroriesAux(fromTerritoryId, toTerritoryId, [], [])
    if not possiblePath[1]: return False
    return True
  
  def moveDifferentNumberOfTroopsToColonyAfterAttack(self, colonyTerritoryId: int, newNumberOfTroopsInColony: int):
    if self.selectedTerritories[0] != colonyTerritoryId:
      return
    numberOfTroopsOverDesired = self.territories[colonyTerritoryId].numberOfTroops - newNumberOfTroopsInColony
    self.moveTroopsBetweenFriendlyTerrirories(colonyTerritoryId, self.selectedTerritories[1], numberOfTroopsOverDesired)
  
  def rollDices(self, numberOfDices: int) -> list[int]:
    finalNumberOfDices = min(numberOfDices, MAX_OF_DICES_PER_ATTACK)
    return list(randint(1, 6) for i in range(finalNumberOfDices))
  
  def setSelection(self, territoryId: int, position: int):
    self.selectedTerritories[position] = territoryId

  def resetSelection(self):
    self.selectedTerritories = [-1, -1]

  def rollDicesForAttackerAndDefender(self, numberOfAttackerTroops: int, numberOfDefenderTroops: int) -> Tuple[list[int], list[int]]:
    attackersDiceResult = self.rollDices(numberOfAttackerTroops)
    defendersDiceResult = self.rollDices(numberOfDefenderTroops)
    return attackersDiceResult, defendersDiceResult
  
  def colonize(self, colonizerTerritoryId: int, colonyTerritoryId: int):
    self.territories[colonyTerritoryId].colonize(self.territories[colonizerTerritoryId].color)
    self.selectedTerritories = (colonyTerritoryId, colonizerTerritoryId)
    self.moveTroopsBetweenFriendlyTerrirories(colonizerTerritoryId, colonyTerritoryId, self.territories[colonizerTerritoryId].getNonDefendingTroops())
  
  def isHostileNeighbour(self, territory1: int, territory2: int):
    return territory2 in self.getHostileTerritoryNeighbours(territory1)

  def getSuccessfullAttacks(self, attackersDiceResult: list[int], defendersDiceResult: list[int]) -> Tuple[int, int]:
    defendersDiceResult.sort(reverse=True)
    attackersDiceResult.sort(reverse=True)
    battlesWonByAttackers = 0
    battlesWonByDefenders = 0
    for i in range(len(attackersDiceResult) if len(attackersDiceResult) < len(defendersDiceResult) else len(defendersDiceResult)):
      if attackersDiceResult[i] > defendersDiceResult[i]:
        battlesWonByAttackers += 1
      else:
        battlesWonByDefenders += 1
    return battlesWonByAttackers, battlesWonByDefenders
  
  def attackEnemyTerritory(self, attackerTerritoryId: int, defenderTerritoryId: int, numberOfTroops) -> Tuple[int, int]:
    if not self.isHostileNeighbour(attackerTerritoryId, defenderTerritoryId): return 0, 0
    numberOfTroopsAttacking = min(min(numberOfTroops, MAX_OF_DICES_PER_ATTACK), self.territories[attackerTerritoryId].getNonDefendingTroops())
    numberOfDefendingTroops = self.territories[defenderTerritoryId].getDefendingTroops()
    diceResultOfAttackersAndDefenders = self.rollDicesForAttackerAndDefender(numberOfTroopsAttacking, numberOfDefendingTroops)
    print("dices (atk  def):", diceResultOfAttackersAndDefenders)
    battlesWonByAttackersAndDefenders = self.getSuccessfullAttacks(diceResultOfAttackersAndDefenders[0], diceResultOfAttackersAndDefenders[1])
    troopsLostByAttacker = self.territories[attackerTerritoryId].loseTroops(battlesWonByAttackersAndDefenders[1])
    troopsLostByDefender = self.territories[defenderTerritoryId].loseTroops(battlesWonByAttackersAndDefenders[0])
    if self.territories[defenderTerritoryId].hasAliveTroops():
      return troopsLostByAttacker, troopsLostByDefender
    self.colonize(attackerTerritoryId, defenderTerritoryId)
    return troopsLostByAttacker, troopsLostByDefender
    
  def attackEnemyTerritoryBlitz(self, attackerTerritoryId: int, defenderTerritoryId: int) -> Tuple[int, int]:
    totalTroopsLostByAttackerAndDefender = [0, 0]
    if not self.isHostileNeighbour(attackerTerritoryId, defenderTerritoryId): return totalTroopsLostByAttackerAndDefender
    while self.territories[attackerTerritoryId].canAttack() and self.territories[attackerTerritoryId].color != self.territories[defenderTerritoryId].color:
      #print("attackers available: {}".format(self.territories[attackerTerritoryId].getNonDefendingTroops()))
      troopsLostByAttackerAndDefender = self.attackEnemyTerritory(attackerTerritoryId, defenderTerritoryId, self.territories[attackerTerritoryId].getNonDefendingTroops())
      totalTroopsLostByAttackerAndDefender[0] += troopsLostByAttackerAndDefender[0]
      totalTroopsLostByAttackerAndDefender[1] += troopsLostByAttackerAndDefender[1]
    return totalTroopsLostByAttackerAndDefender
  
  def attackEnemyTerritoryExhausted(self, attackerTerritoryId: int, defenderTerritoryId: int, numberOfAttackerTroops: int) -> Tuple[int, int]:
    totalTroopsLostByAttackerAndDefender = [0, 0]
    numberOfTroopsAttacking = min(numberOfAttackerTroops, self.territories[attackerTerritoryId].getNonDefendingTroops())
    if not self.isHostileNeighbour(attackerTerritoryId, defenderTerritoryId): return totalTroopsLostByAttackerAndDefender
    while self.territories[attackerTerritoryId].canAttack() and self.territories[attackerTerritoryId].color != self.territories[defenderTerritoryId].color and 0 < numberOfTroopsAttacking - totalTroopsLostByAttackerAndDefender[0]:
      #print("attackers available: {}".format(self.territories[attackerTerritoryId].getNonDefendingTroops()))
      troopsLostByAttackerAndDefender = self.attackEnemyTerritory(attackerTerritoryId, defenderTerritoryId, numberOfTroopsAttacking - totalTroopsLostByAttackerAndDefender[0])
      totalTroopsLostByAttackerAndDefender[0] += troopsLostByAttackerAndDefender[0]
      totalTroopsLostByAttackerAndDefender[1] += troopsLostByAttackerAndDefender[1]
    return totalTroopsLostByAttackerAndDefender