import pygame

from classes.OptionsLabel import OptionsLabel
from classes.Button import MenuButton
from classes.Slider import Slider
from classes.Constants import *

RETURN_BUTTON = "Voltar"


class OptionsMenu:
    def __init__(self, return_function):
        self.screen = pygame.display.set_mode((800, 600))
        self.background_image = pygame.image.load('classes/assets/images/bg/options-menu-bg.png')
        self.return_button = MenuButton(RETURN_BUTTON, 200)
        # x, y, width, height
        s_data = [SCREEN_WIDTH - 350, 220, 300, 30]
        self.label = OptionsLabel("Volume",
                             self.screen,
                             s_data[0] + s_data[2] / 4,
                             s_data[1] - s_data[3] * 1.5)
        self.slider = Slider(s_data[0], s_data[1], s_data[2], s_data[3])
        self.slider.add_observer(self.label)
        self.slider.notify_observers()
        self.return_function = return_function

    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
        self.label.draw()
        self.slider.draw(self.screen)
        self.return_button.draw(self.screen)

    def handle_event(self, event):
        self.slider.handle_event(event)
        if self.return_button.is_clicked(event):
            self.return_function()
