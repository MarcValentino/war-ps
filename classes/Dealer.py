from classes.Territory import *
from classes.Region import *
from classes.Card import *
from classes.Player import *
from random import randrange


class Dealer():
  JOKERCARDS = 2
  MIN_ARMY_FROM_TERRITORIES_POSSESSED = 3
  CARD_QUANTITY_OF_ARMY_RECEIVED_PER_TRADE = [4, 6, 8, 10, 12, 15] #...20, 25, 30, 35, 40...
    
  def __init__(self, playersInGame: int, initialTerritoryList: list[Territory], regionList: list[Region]):
    self.players = playersInGame
    self.initialTerritoryList = initialTerritoryList
    self.regionList = regionList
    self.startingTerritories = []
    self.numberOfTrades = 0

  # retorna a instancia da carta sorteada para o jogador
  # tem chance de virar joker
  def getCardAfterSuccessfullAttack(self) -> Card:
      lenTerritoriesList = len(self.initialTerritoryList)
      territoryId = randrange(0, lenTerritoriesList + self.JOKERCARDS)
      return Card(territoryId >= lenTerritoriesList)
      
  # retorna a lista de territorios iniciais por id de jogador
  def listOfStartingTerritoriesOfAllPlayers(self) -> list[list[int]]:
      usersTerritories = [[] for p in range(self.players)]
      allTerritoriesId = list(map(lambda t : t.id, self.initialTerritoryList))
      # Arbitrario, pode vir como parametro
      nextPlayerToReceiveTerritory = 0 
      while allTerritoriesId:
          randomListPosition = randrange(0, len(allTerritoriesId))
          usersTerritories[nextPlayerToReceiveTerritory].append(allTerritoriesId[randomListPosition])
          allTerritoriesId.pop(randomListPosition)
          nextPlayerToReceiveTerritory = (nextPlayerToReceiveTerritory + 1) % self.players
      self.startingTerritories = usersTerritories
      return usersTerritories
  
  # retorna a lista de territorios iniciais do jogador
  def startingTerritoriesOfPlayer(self, playerId: int) -> list[int]:
      if not self.startingTerritories:
          self.listOfStartingTerritoriesOfAllPlayers()
      return self.startingTerritories[playerId]
  
  # retorna a quantidade de exercitos que deve ser colocado no tabuleiro antes do ataque
  # metade dos territorios conquistados 
  # minimo de exercitos a receber é sempre 3
  def receiveArmyFromPossessedTerritories(self, player: Player, currentTerritoriesList: list[Territory]) -> int:
      playerTerritoriesList = list(filter(lambda x: x.color == player.color, currentTerritoriesList))
      return max(self.MIN_ARMY_FROM_TERRITORIES_POSSESSED, len(playerTerritoriesList) // 2)
  
  # retorna a quantidade de exercitos que deve ser colocado no tabuleiro antes do ataque
  # troca de cartas
  # jogador não pode ter mais de 5 cartas na mao
  def receiveArmyFromTradingCards(self, handOfCards: list[Card], doAllPossibleTrades: bool = False) -> int:
      bonusArmy = 0
      maxTrades = (len(handOfCards) // 3) + 1
      for i in range(maxTrades):
        if not self.hasCardsToTrade(handOfCards):
            break
        self.tradeThreeCards(handOfCards)
        if self.numberOfTrades < len(self.CARD_QUANTITY_OF_ARMY_RECEIVED_PER_TRADE):
            bonusArmy += self.CARD_QUANTITY_OF_ARMY_RECEIVED_PER_TRADE[self.numberOfTrades]
        else:
            bonusArmy += (self.numberOfTrades - len(self.CARD_QUANTITY_OF_ARMY_RECEIVED_PER_TRADE) + 1) * 5 + self.CARD_QUANTITY_OF_ARMY_RECEIVED_PER_TRADE[-1]
        self.numberOfTrades += 1
        if not doAllPossibleTrades:
            break
      return bonusArmy
  
  def hasCardsToTrade(self, handOfCards: list[Card]) -> bool:
      listOfCardsShapes = list(map(lambda c : c.shape, handOfCards))
      # Com certeza tem combinação de cartas pra troca
      if len(handOfCards) >= 5:
          return True
      # Tem trocas de mesma forma
      if listOfCardsShapes.count('T') + listOfCardsShapes.count('J') >= 3 or listOfCardsShapes.count('S') + listOfCardsShapes.count('J') >= 3 or listOfCardsShapes.count('C') + listOfCardsShapes.count('J') >= 3:
          return True
      # Tem trocas de formas diferentes
      differentShapesInList = 0
      if 'T' in listOfCardsShapes:
          differentShapesInList += 1
      if 'S' in listOfCardsShapes:
          differentShapesInList += 1
      if 'C' in listOfCardsShapes:
          differentShapesInList += 1
      if 'J' in listOfCardsShapes:
          differentShapesInList += 1
      return differentShapesInList >= 3
  
  # previne remover cartas sem conseguir efetuar trocas
  # embora so entre nessa funcao se tiver ja verificado se consegue trocar
  def tradeThreeCards(self, handOfCards: list[Card]):
      listOfCardsShapes = list(map(lambda c : c.shape, handOfCards))
      cardsRemoved = 0
      if listOfCardsShapes.count('T') + listOfCardsShapes.count('J') >= 3:
          cardsRemoved += self.tryRemoveCardsShapeFromList(handOfCards, 'T')
          if cardsRemoved >= 3:
              return
          cardsRemoved += self.tryRemoveCardsShapeFromList(handOfCards, 'J', 3-cardsRemoved)
          return
          
      if listOfCardsShapes.count('S') + listOfCardsShapes.count('J') >= 3:
          cardsRemoved += self.tryRemoveCardsShapeFromList(handOfCards, 'S')
          if cardsRemoved >= 3:
              return
          cardsRemoved += self.tryRemoveCardsShapeFromList(handOfCards, 'J', 3-cardsRemoved)
          return
          
      if listOfCardsShapes.count('C') + listOfCardsShapes.count('J') >= 3:
          cardsRemoved += self.tryRemoveCardsShapeFromList(handOfCards, 'C')
          if cardsRemoved >= 3:
              return
          cardsRemoved += self.tryRemoveCardsShapeFromList(handOfCards, 'J', 3-cardsRemoved)
          return
          
      differentShapesInList = 0
      if 'T' in listOfCardsShapes:
          differentShapesInList += 1
      if 'S' in listOfCardsShapes:
          differentShapesInList += 1
      if 'C' in listOfCardsShapes:
          differentShapesInList += 1
      if 'J' in listOfCardsShapes:
          differentShapesInList += 1
      if differentShapesInList < 3:
          return
      
      if 'T' in listOfCardsShapes:
          cardsRemoved += self.tryRemoveCardsShapeFromList(handOfCards, 'T', 1)
      if 'S' in listOfCardsShapes:
          cardsRemoved += self.tryRemoveCardsShapeFromList(handOfCards, 'S', 1)
      if 'C' in listOfCardsShapes:
          cardsRemoved += self.tryRemoveCardsShapeFromList(handOfCards, 'C', 1)
      if cardsRemoved >= 3:
          return
      if 'J' in listOfCardsShapes:
          cardsRemoved += self.tryRemoveCardsShapeFromList(handOfCards, 'J', 1)
      
  def tryRemoveCardsShapeFromList(self, cards: list[Card], shape: str, maxCardsRemoved: int = 3) -> int:
      removed = 0
      for card in cards:
          if removed >= maxCardsRemoved:
            break      
          if card.shape == shape:
            cards.remove(card)    
            removed += 1
      return removed
      
  # retorna a quantidade de exercitos que deve ser colocado no tabuleiro antes do ataque
  # bonus de regiao conquistada
  def receiveArmyFromPossessedRegions(self, player: Player, currentTerritoriesList: list[Territory]) -> int:
      troops = 0
      for regionId in range(len(self.regionList)):
          regionTerritories = list(filter(lambda x: x.regionId == regionId, currentTerritoriesList))
          if all(territory.color == player.color for territory in regionTerritories):
              troops += self.regionList[regionId].troopBonus
      return troops
  