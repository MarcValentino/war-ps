import re
from classes.GameMap import *
from classes.Territory import *
from classes.Region import *
from classes.Card import *
from classes.Dealer import *
from copy import deepcopy

testTerritories: list[Territory] = [Territory([1, 2], 0, 'teste1', 0, 0, 0, 0, 0), Territory([0, 4], 0, 'teste2', 1, 0, 0, 0, 0), Territory([0, 3], 0, 'teste3', 2, 0, 0, 0, 0), Territory([2, 4, 5], 1, 'teste4', 3, 0, 0, 0, 0), Territory([3, 1], 1, 'teste5', 4, 0, 0, 0, 0), Territory([3], 0, 'teste6', 5, 0, 0, 0, 0), Territory([7], 2, 'teste6', 6, 0, 0, 0, 0), Territory([6], 2, 'teste7', 7, 0, 0, 0, 0)]
testTerritories[0].colonize('0')
testTerritories[1].colonize('0')
testTerritories[2].colonize('1')
testTerritories[3].colonize('1')
testTerritories[4].colonize('0')
testTerritories[5].colonize('1')
testTerritories[6].colonize('0')
testTerritories[7].colonize('0')
testRegions: list[Region] = [Region('a', 3, 0), Region('b', 2, 1), Region('c', 2, 2)]
testMap = GameMap(testTerritories, testRegions)
nonJokerCard = Card()
jokerCard = Card(True)
NUMBER_OF_PLAYERS = 5
dealer = Dealer(NUMBER_OF_PLAYERS, testTerritories, testRegions)
player0 = Player(0, "Jogador 0", '0', True)
player1 = Player(1, "Jogador 1", '1', True)

def test_neighbourhoods():
  assert testMap.validateTerritoriesConnections()
  assert testMap.getFriendlyTerritoryNeighbours(3) == [2, 5]
  assert testMap.getHostileTerritoryNeighbours(0) == [2]
  assert testMap.getHostileTerritoryNeighbours(5) == []
  assert testMap.getTerritoryNeighbours(3) == [2, 4, 5]

def test_regions():
  assert testMap.filterTerritoriesByRegion(1) == [3, 4]
  assert testMap.filterTerritoriesByRegion(0) == [0, 1, 2, 5]
  assert testMap.filterTerritoriesByRegion(2) == [6, 7]
  assert testMap.filterTerritoriesByRegion(3) == []

def test_region_bonus():
  assert dealer.receiveArmyFromPossessedRegions(player0, testTerritories) == 2
  assert dealer.receiveArmyFromPossessedRegions(player1, testTerritories) == 0
  
def test_troopsMovement():
  assert testMap.moveTroopsBetweenFriendlyTerrirories(0, 1, 5) == [0, 1]
  assert testTerritories[0].numberOfTroops == 10
  assert testTerritories[1].numberOfTroops == 20
  assert testMap.moveTroopsBetweenFriendlyTerrirories(0, 1, 5) == [0, 1]
  assert testTerritories[0].numberOfTroops == 5
  assert testTerritories[1].numberOfTroops == 25
  assert testMap.moveTroopsBetweenFriendlyTerrirories(2, 1, 2) == []
  assert testTerritories[2].numberOfTroops == 15 
  assert testTerritories[1].numberOfTroops == 25
  assert testMap.moveTroopsBetweenFriendlyTerrirories(2, 5, 2) == [2, 3, 5]
  assert testTerritories[2].numberOfTroops == 13
  assert testTerritories[5].numberOfTroops == 17
  
def test_troopsManipulation():
  testTerritories[6].gainTroops(2)
  testTerritories[6].loseTroops(15)
  testTerritories[6].gainTroops(2)
  testTerritories[6].deallocateTroops(3)
  assert testTerritories[6].getDefendingTroops() == 1

def test_diceRolls():
  assert len(testMap.rollDices(5)) == 3
  assert len(testMap.rollDices(2)) == 2
  
def test_colony():
  testMap.colonize(3, 4)
  assert testMap.getFriendlyTerritoryNeighbours(3) == [2, 4, 5]
  
def test_attacking():
  attackerDices = [5, 6, 6]
  defenderDices = [3, 6, 5]
  battlesWonByAttackersAndDefenders = testMap.getSuccessfullAttacks(attackerDices, defenderDices)
  assert battlesWonByAttackersAndDefenders[0] == 2
  assert battlesWonByAttackersAndDefenders[1] == 1

def test_card_creation():
  assert nonJokerCard.shape in ['T', 'S', 'C']
  assert jokerCard.shape == "J"
  canCreateRandomJokerCards = False
  for i in range(1000):
    jokerTest = dealer.getCardAfterSuccessfullAttack()
    if jokerTest.shape == "J":
      canCreateRandomJokerCards = True
      break
  assert canCreateRandomJokerCards
  
def test_dealing_territories():
  territoriesPerPlayer = dealer.listOfStartingTerritoriesOfAllPlayers()
  # testa se todos os territorios foram distribuidos
  assert len(testTerritories) == len(sum(territoriesPerPlayer, []))
  allTerritories = sum(territoriesPerPlayer, [])
  # testa se repetiu algum territorio
  assert len(allTerritories) == len(list(set(allTerritories)))
  minSize = len(testTerritories) // NUMBER_OF_PLAYERS
  assert all(minSize <= len(listOfTer) <= (minSize + 1) for listOfTer in territoriesPerPlayer)
  
def test_trading_cards():
  #TTTTTSSSCCCCCCCCJJ
  #TTTTTSSSCCCCCCCCJJ
  cards = []
  circle =  Card()
  circle.shape = 'C'
  triangle =  Card()
  triangle.shape = 'T'
  square =  Card()
  square.shape = 'S'
  joker =  Card()
  joker.shape = 'J'
  for i in range(8):
    cards.append(deepcopy(circle))
  for i in range(5):
    cards.append(deepcopy(triangle))
  for i in range(3):
    cards.append(deepcopy(square))
  for i in range(2):
    cards.append(deepcopy(joker))
  armyFromCards = dealer.receiveArmyFromTradingCards(cards, True)
  assert armyFromCards == 55
  