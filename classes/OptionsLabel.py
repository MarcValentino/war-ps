import pygame

from classes.Constants import FONT_SIZE
from classes.Observer import Observer


class OptionsLabel(Observer):

    def __init__(self, label, screen, width, height):
        self.screen = screen
        self.width = width
        self.label = label
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.text_render = self.font.render(self.label + ":", True, (0, 0, 0))
        self.height = height

    def update(self, value):
        self.text_render = self.font.render(self.label + ":" + f"{int(value * 100)}%", True, (0, 0, 0))

    def draw(self):
        self.screen.blit(self.text_render, (self.width, self.height))
