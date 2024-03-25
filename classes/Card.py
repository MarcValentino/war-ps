from pickle import FALSE
from random import choice

class Card():
  def __init__(self, isJoker: bool = False):
    if isJoker:
      self.turnIntoJoker()
      return
    # T = triangle
    # S = square
    # C = circle
    possibleCardShapes = ['T', 'S', 'C']
    self.shape = choice(possibleCardShapes)
    
  def turnIntoJoker(self):
    self.shape = 'J'
