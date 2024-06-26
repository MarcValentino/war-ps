import pygame

from classes.Button import MenuButton
from classes.Slider import Slider
from classes.Constants import *

RETURN_BUTTON = "Voltar"


class OptionsMenu:
    def __init__(self, return_function):
        self.screen = pygame.display.set_mode((800, 600))
        self.background_image = pygame.image.load('classes/assets/images/bg/options-menu-bg.png')
        self.return_button = MenuButton(RETURN_BUTTON, 200)
        self.slider = Slider(SCREEN_WIDTH - 350, 220, 300, 30, "Volume")  # Initialize the Slider object
        self.return_function = return_function

    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
        self.slider.draw(self.screen)
        self.return_button.draw(self.screen)

    def handle_event(self, event):
        self.slider.handle_event(event)
        if self.return_button.is_clicked(event):
            self.return_function()
