import pygame_gui
import pygame


class UIState:
    def handleState(self, game_ui):
        pass

class InactiveState(UIState):
    def handleState(self, game_ui):
        print("hiding UI")
        game_ui.selectableTroops.remove_items(list(map(lambda x: x['text'], game_ui.selectableTroops.item_list)))
        game_ui.selectableTroops.disable()
        if game_ui.blitzButton.is_enabled:
            game_ui.blitzButton.disable()
        game_ui.phase = 'Inactive'

class AttackState(UIState):
    def handleState(self, game_ui):
        game_ui.blitzButton.enable()
        game_ui.selectableTroops.enable()
        game_ui.phase = 'Attack'

class MoveState(UIState):
    def handleState(self, game_ui):
        game_ui.selectableTroops.enable()
        game_ui.phase = 'Move'

class DeployState(UIState):
    def handleState(self, game_ui):
        game_ui.selectableTroops.enable()
        game_ui.phase = 'Deploy'

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
        self.blitzButton.disable()

        self.selectableTroops = pygame_gui.elements.UISelectionList(
            relative_rect=pygame.Rect((308, -100), (200, 70)),
            item_list=[],
            manager=self.manager,
            anchors={
                'left': 'left',
                'bottom': 'bottom'
            }
        )
        self.selectableTroops.disable()

        self.state = InactiveState()
        self.phase = 'Inactive'  

    def addItemsToSelectableTroops(self, soldierRange: list[str]):
        self.selectableTroops.add_items(soldierRange)

    def setPhase(self, phase: str):
        if phase == 'Inactive':
            self.state = InactiveState()
        elif phase == 'Attack':
            self.state = AttackState()
        elif phase == 'Move':
            self.state = MoveState()
        elif phase == 'Deploy':
            self.state = DeployState()

        self.state.handleState(self)

    def getSelectedOptionFromList(self):
        selection = list(filter(lambda item: item['selected'], self.selectableTroops.item_list))
        print("selection:", selection)
        return int(selection[0]['text']) if selection else None

    def verifyMouseCollision(self, mouseX, mouseY):
        return self.blitzButton.hovered or self.selectableTroops.rect.collidepoint(mouseX, mouseY)

    def drawGUI(self, map: pygame.Surface):
        self.manager.draw_ui(map)
