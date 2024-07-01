from classes.GraphicalMap import *
from classes.Jukebox import Jukebox
from classes.Window import *
from classes.Piece import *
from classes.GameUI import *
from classes.IA import *
from classes.Constants import *
from classes.database.models.SessaoJogo import *
from classes.database.models.SessaoJogador import *
from classes.database.models.TerritorioSessaoJogador import *
import pygame_gui


pygame.init()

class Game:
  def __init__(self):
        pygame.init()
        self.window = Window(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.graphicalMap = GraphicalMap("classes/assets/images/bg/water.png", self.window.width, self.window.height)
        self.players = self.create_players()
        self.territories = self.create_territories()
        self.piecesColors = {territory.id: "" for territory in self.territories}
        self.regions = self.create_regions()
        self.dealer = Dealer(NUMBER_OF_PLAYERS, self.territories, self.regions)
        self.distribute_territories()
        self.gameMap = GameMap(self.territories, self.regions)
        self.ia = IA()
        self.iaIsRunning = False
        self.validate_territories()
        self.font = pygame.font.SysFont("arialblack", TROOPS_FONT_SIZE)
        self.clock = pygame.time.Clock()
        self.gameUI = GameUI((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.pieces_group = self.create_pieces_group()
  
  def create_players(self):
        players = []
        for p in range(NUMBER_OF_PLAYERS):
            players.append(Player(p, "Jogador " + str(p + 1), list(COLORS)[p], p != PLAYER_ID))
        return players
  
  def create_territories(self):
        territories = [
          Territory([1,3,29],0,'Alaska',0,32,75,82,107),
          Territory([0,3,4,2],0,'Mackenzie',1,107,62,176,112),
          Territory([1,4,5,13],0,'Groelandia',2,285,25,358,73),
          Territory([0,1,4,6],0,'Vancouver',3,117,131,164,166),
          Territory([1,2,3,5,6,7],0,'Ottawa',4,198,134,225,179),
          Territory([4,7,2],0,'Labrador',5,260,129,299,177),
          Territory([3,7,8,4],0,'California',6,122,200,169,240),
          Territory([4,5,6,8],0,'NovaYork',7,179,200,238,259),
          Territory([6,7,9],0,'Mexico',8,131,278,178,327),
          Territory([8,10,11],1,'Colombia',9,203,359,245,387),
          Territory([9,11,12],1,'Bolivia',10,197,406,258,471),
          Territory([9,10,12,20],1,'Brasil',11,220,389,329,454),
          Territory([10,11],1,'Argentina',12,234,484,267,559),
          Territory([2,16,14],2,'Islandia',13,411,124,438,143),
          Territory([13,15,16,17],2,'Suecia',14,478,91,521,127),
          Territory([14,17,19,26,32,35],2,'Moscou',15,538,94,597,201),
          Territory([13,14,17,18],2,'Inglaterra',16,381,171,428,227),
          Territory([15,16,18,19,14],2,'Alemanha',17,467,185,516,235),
          Territory([16,17,19,20],2,'Portugal',18,404,250,445,300),
          Territory([17,18,20,21,35,15],2,'Polonia',19,475,249,527,291),
          Territory([11,18,19,21,22,23],3,'Argelia',20,417,344,481,422),
          Territory([20,22,35,19],3,'Egito',21,505,364,554,392),
          Territory([20,21,23,24,25,35],3,'Sudao',22,553,416,604,469),
          Territory([20,22,24],3,'Congo',23,503,457,554,508),
          Territory([22,23,25],3,'AfricadoSul',24,515,525,562,598),
          Territory([22,24],3,'Madagascar',25,625,534,654,578),
          Territory([15,27,33,32],4,'Omsk',26,668,69,700,170),
          Territory([26,28,30,31,33],4,'Dudinka',27,692,37,758,132),
          Territory([27,30,29],4,'Siberia',28,783,53,830,95),
          Territory([0,28,30,31,34],4,'Vladvostok',29,837,67,887,122),
          Territory([27,28,31,29],4,'Tchita',30,769,129,819,181),
          Territory([27,29,30,33,34],4,'Mongolia',31,775,186,830,242),
          Territory([26,15,35,36,33],4,'Aral',32,628,202,687,258),
          Territory([26,27,31,32,36,37],4,'China',33,722,222,807,305),
          Territory([29,31],4,'Japao',34,895,190,937,254),
          Territory([15,19,21,22,36,32],4,'OrienteMedio',35,550,302,628,366),
          Territory([32,35,33,37],4,'India',36,688,292,744,361),
          Territory([33,36,38],4,'Vietna',37,786,344,823,388),
          Territory([37,39,41],5,'Sumatra',38,782,454,840,498),
          Territory([38,40],5,'NovaGuine',39,881,444,930,473),
          Territory([39,41],5,'NovaZelandia',40,907,514,962,568),
          Territory([38,40],5,'Australia',41,840,530,881,595)]
        return territories
  
  def create_regions(self):
        return [Region('América do Norte', 3, 0), Region('América do Sul', 2, 1), Region('Europa', 2, 2), Region('Africa', 9, 3), Region('Ásia', 6, 4), Region('Oceania', 2, 5)]

  def distribute_territories(self):
        playersTerritories = self.dealer.listOfStartingTerritoriesOfAllPlayers()
        for playerInd, territories in enumerate(playersTerritories):
            ownerColor = self.players[playerInd].color
            for territoryInd in territories:
                self.territories[territoryInd].colonize(ownerColor)
                self.piecesColors[territoryInd] = ownerColor
  
  def validate_territories(self):
        validTerritories = self.gameMap.validateTerritoriesConnections()
        if validTerritories:
            print(">> Territories carregados")
        else:
            print(">> Erro na validacao dos territorios")
  
  def create_pieces_group(self):
        pieces_group = pygame.sprite.Group()
        for territory in self.territories:
            new_piece = Piece(territory.id, territory.name, territory.color, territory.numberOfTroops, territory.pos_x, territory.pos_y, territory.text_x, territory.text_y)
            pieces_group.add(new_piece)
        return pieces_group

  def onInit(self):
    self.running = True
    self.gameStage = GAME_STAGES[0]
    self.playerRound = randint(0, NUMBER_OF_PLAYERS-1)
    self.troopsToDeploy = 0
    self.cardReceiver = False
  
  def saveGame(self):
    if self.matchStatus == 'ongoing':
      newSession = SessaoJogo()
      newSession.save()
      for player in self.players:
        playerTerritories = list(filter(lambda t: t.color == player.color, self.territories))
        newPlayer = SessaoJogador(
          idJogador=player.id, 
          idSessao=newSession.get_id(), 
          vez=not player.isAI, # supondo que o jogador sempre vai sair na sua vez
          naPartida=len(playerTerritories)>0, 
          ehIA=player.isAI,
          cor=player.color
        )
        newPlayer.save()
        if len(playerTerritories) > 0:
          for territory in playerTerritories:
            TerritorioSessaoJogador(
              idSessaoJogador = newPlayer.get_id(),
              idTerritorio = territory.id+1,
              contagemTropas = territory.numberOfTroops
            ).save()

  def goToNextStage(self):
    self.gameStage = GAME_STAGES[(GAME_STAGES.index(self.gameStage) + 1) % len(GAME_STAGES)]
    print("\t>> new stage is", self.gameStage)
    if GAME_STAGES.index(self.gameStage) == 0:
      self.goToNextPlayerRound()
    
  def goToNextPlayerRound(self):
    self.playerRound = (self.playerRound + 1) % NUMBER_OF_PLAYERS
    print(f">> player turn: {self.players[self.playerRound].color}  cards: {self.players[self.playerRound].cards}")
    self.gameMap.selectedTerritories = [-1, -1]
    self.cardReceiver = False
  
  def checkVictory(self):
    player = self.players[self.playerRound]
    if len(self.gameMap.getAllTerritoriesOfColors(player.color)) >= len(self.territories) * VICTORY_MAP_RATE:
      self.hasWon(player)
    self.matchStatus = 'player victory'

  def hasWon(self, player: Player):
    for t in self.territories:
      t.colonize(player.color)
      t.numberOfTroops = 999
    print(f">>>> {player.color} GANHOU!")
    
  def handlePieceClick(self, pieceTerritoryId: int):
    switchedDeployTerritory = False
    if pieceTerritoryId == -1: #reset selected pieces
      self.gameMap.selectedTerritories = [-1, -1]
      self.gameUI.setPhase('Inactive')
      return
    if self.gameMap.selectedTerritories[0] == pieceTerritoryId:
        self.gameUI.setPhase('Inactive')
        self.gameMap.selectedTerritories = [-1, -1]
        return
    if self.gameMap.selectedTerritories[0] == -1:
      if self.players[PLAYER_ID].color != self.territories[pieceTerritoryId].color:
        return
      print("selected territory {}".format(self.territories[pieceTerritoryId].name))
      self.gameMap.selectedTerritories[0] = pieceTerritoryId
    else:
      if self.gameStage == 'DEPLOY': 
        if self.gameMap.territories[self.gameMap.selectedTerritories[0]].color == self.gameMap.territories[pieceTerritoryId].color:
          print("color is the same")
          self.gameMap.selectedTerritories[0] = pieceTerritoryId
          switchedDeployTerritory = True
        else: 
          print('different color')
          self.gameUI.setPhase('Inactive')
          self.gameMap.selectedTerritories = [-1, -1]
          return
      else: self.gameMap.selectedTerritories[1] = pieceTerritoryId
    
    if self.gameStage == "DEPLOY":
      # if self.gameMap.selectedTerritories[0] == pieceTerritoryId:
      #   self.gameUI.setPhase('Inactive')
      #   self.gameMap.selectedTerritories = [-1, -1]
      #   return
      print("fase é deploy")
      if not switchedDeployTerritory:
        self.gameUI.setPhase("Deploy")
        self.gameUI.addItemsToSelectableTroops(list(map(lambda x: str(x+1), range(self.troopsToDeploy))))
        print("selecao de territorios: {}".format(self.gameMap.selectedTerritories))
      return
  
    if self.gameStage == "ATTACK" and -1 not in self.gameMap.selectedTerritories:
      isAttackPossible = self.gameMap.isHostileNeighbour(self.gameMap.selectedTerritories[0], self.gameMap.selectedTerritories[1])
      if not isAttackPossible: 
        self.gameMap.selectedTerritories = [-1, -1]
      else:
        self.gameUI.addItemsToSelectableTroops(list(map(lambda x: str(x+1), range(self.territories[self.gameMap.selectedTerritories[0]].getNonDefendingTroops()))))
        self.gameUI.setPhase("Attack")
      return
        
    if self.gameStage == "FORTIFY" and -1 not in self.gameMap.selectedTerritories:

      isMovePossible = self.gameMap.canMoveTroopsBetweenFriendlyTerritories(self.gameMap.selectedTerritories[0], self.gameMap.selectedTerritories[1])
      if isMovePossible:
        self.gameUI.setPhase("Move")
        self.gameUI.addItemsToSelectableTroops(list(map(lambda x: str(x+1), range(self.territories[self.gameMap.selectedTerritories[0]].getNonDefendingTroops()))))
        print("selecao de territorios: {}".format(self.gameMap.selectedTerritories))
      else:
        self.gameMap.selectedTerritories = [-1, -1]
        print(pieceTerritoryId, self.gameMap.selectedTerritories)
      return
    

  def onEvent(self, event):
    mousePosition: Tuple[int, int] = pygame.mouse.get_pos()
    pieces: list[Piece] = self.pieces_group.sprites()
    if event.type == pygame.QUIT:
      self.running = False
    
    if event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
      print("Lista pressionada")
      print("Lista: {}".format(str(self.gameUI.selectableTroops.item_list)))
      selection = self.gameUI.getSelectedOptionFromList()
      if selection:
        print("selected item: {}".format(selection))
        print(self.gameMap.selectedTerritories)
        if self.gameUI.phase == 'Deploy':
          self.territories[self.gameMap.selectedTerritories[0]].gainTroops(selection)
          self.troopsToDeploy -= selection
        elif self.gameUI.phase == 'Move':
          self.gameMap.moveTroopsBetweenFriendlyTerrirories(self.gameMap.selectedTerritories[0], self.gameMap.selectedTerritories[1], selection)
          self.goToNextStage()
        elif self.gameUI.phase == 'Attack':
          territoriesBeforeAttack = self.gameMap.getAllTerritoriesOfColors(self.players[self.playerRound].color)
          self.gameMap.attackEnemyTerritoryExhausted(self.gameMap.selectedTerritories[0], self.gameMap.selectedTerritories[1], selection)
          territoriesAfterAttack = self.gameMap.getAllTerritoriesOfColors(self.players[self.playerRound].color)
          if not self.cardReceiver and len(territoriesAfterAttack) > len(territoriesBeforeAttack):
            self.cardReceiver = True
            self.players[self.playerRound].cards.append(self.dealer.getCardAfterSuccessfullAttack())
        self.gameMap.selectedTerritories = [-1, -1]
        self.gameUI.setPhase("Inactive")
    elif event.type == pygame_gui.UI_BUTTON_PRESSED:
      if self.gameUI.blitzButton.hovered:
        print("botao")
        territoriesBeforeAttack = self.gameMap.getAllTerritoriesOfColors(self.players[self.playerRound].color)
        self.gameMap.attackEnemyTerritoryBlitz(self.gameMap.selectedTerritories[0], self.gameMap.selectedTerritories[1])
        territoriesAfterAttack = self.gameMap.getAllTerritoriesOfColors(self.players[self.playerRound].color)
        if not self.cardReceiver and len(territoriesAfterAttack) > len(territoriesBeforeAttack):
          self.cardReceiver = True
          self.players[self.playerRound].cards.append(self.dealer.getCardAfterSuccessfullAttack())
        self.gameMap.selectedTerritories = [-1, -1]
        self.gameUI.setPhase("Inactive")
    elif event.type == pygame.MOUSEBUTTONDOWN: # botão é apertado
      print("mouse coordinates (x, y): {}, {}".format(mousePosition[0], mousePosition[1]))
      isPlayerTurn = self.playerRound == PLAYER_ID
      pieceClickedTerritorryId = -1
      if self.gameUI.verifyMouseCollision(mousePosition[0], mousePosition[1]): return
      for piece in pieces:
        if piece.rect.collidepoint(mousePosition[0], mousePosition[1]) and piece.mask.get_at((mousePosition[0] - piece.rect.x, mousePosition[1] - piece.rect.y)):
          print(">> clicked on", self.territories[piece.territoryId].color, "piece")
          pieceClickedTerritorryId = piece.territoryId
          break
          
      # se não for round dele, invalida
      if isPlayerTurn:
        self.handlePieceClick(pieceClickedTerritorryId)
        if pieceClickedTerritorryId != -1:
          # forca update do territorio clicado
          self.piecesColors[pieceClickedTerritorryId] = ""
        
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_SPACE:
          self.goToNextStage()
        
  def onLoop(self):
    player = self.players[self.playerRound]
    self.checkVictory()
    if self.gameStage == "DRAFT":
      territoryTroops = self.dealer.receiveArmyFromPossessedTerritories(player, self.territories)
      regionTroops = self.dealer.receiveArmyFromPossessedRegions(player, self.territories)
      cardTroops = self.dealer.receiveArmyFromTradingCards(player.cards, True)
      troopsToReceive = territoryTroops + regionTroops + cardTroops
      print(f">> {player.color} received {troopsToReceive} troops ({territoryTroops}:territories  {regionTroops}:region  {cardTroops}:cards)")
      self.troopsToDeploy = troopsToReceive
      self.goToNextStage()
      
    if self.gameStage == "DEPLOY" and self.troopsToDeploy <= 0:
      self.goToNextStage()
      
    if player.isAI and not self.iaIsRunning:
      self.iaIsRunning = True
      if self.gameStage == "DEPLOY":
        self.ia.supply(self.troopsToDeploy, self.gameMap, player.color)
      elif self.gameStage == "ATTACK":
        self.ia.initiation_attack(self.gameMap, player.color)
      elif self.gameStage == "FORTIFY":
        self.ia.move(self.gameMap, player.color)
      self.iaIsRunning = False
      self.goToNextStage()

  def onRender(self):
    self.window.showMap(self.graphicalMap.image)
    for piece in self.pieces_group:
      wasSelected = piece.selected
      piece.selected = False
      if piece.territoryId in self.gameMap.selectedTerritories:
        piece.selected = True
      if self.piecesColors == self.territories[piece.territoryId].color and wasSelected == piece.selected:
        continue
      self.piecesColors[piece.territoryId] = piece.color = self.territories[piece.territoryId].color
      piece.updatePiece(self.gameMap.territories[piece.territoryId])
      text = self.font.render(str(piece.troops), True, (150,150,150))
      text_rect = text.get_rect(center=(piece.text_center_x, piece.text_center_y))
      pieceimg = piece.image.copy()
      if piece.selected:
        pieceimg.fill(SELECTED_COLORS[COLORS.index(piece.color)], special_flags=pygame.BLEND_RGB_SUB)
      self.graphicalMap.scaleAndBlit(pieceimg, piece.pos_x, piece.pos_y)
      self.graphicalMap.scaleAndBlit(text, text_rect.x, text_rect.y)
    pygame.display.flip()
    self.gameUI.drawGUI(self.graphicalMap.image)
    # self.manager.draw_ui(self.graphicalMap.image)

  def onCleanup(self):
    self.saveGame()
    pygame.quit()

  def onExecute(self):
    if self.onInit() == False:
      self.running = False

    while(self.running):
      jukebox = Jukebox()
      jukebox.check_event()

      timeDelta = self.clock.tick(60)/1000.0
      for event in pygame.event.get():
        self.onEvent(event)
        self.gameUI.manager.process_events(event)
      self.gameUI.manager.update(timeDelta)
      self.onLoop()
      self.onRender()

    self.onCleanup()
 
if __name__ == "__main__" :
  theGame = Game()
  theGame.onExecute()