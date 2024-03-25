from classes.Card import *
class Player():
  def __init__(self, playerId: int, playerName: str, color: str, isAI: bool = False):
    self.id = playerId
    self.color = color
    self.name = playerName
    self.isAI = isAI
    self.cards: list[Card] = []
