import pygame
from classes.Constants import *


class Slider:
    def __init__(self, x, y, width, height, initial_value=0.5):
        self.rect = pygame.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.handle_rect = pygame.Rect(x + initial_value * width, y - 10, 20, 50)
        self.value = initial_value
        self.font = pygame.font.Font(None, 36)
        self.dragging = False
        self.observers = []

    def draw(self, screen):
        pygame.draw.rect(screen, DARK_GRAY, self.rect)
        pygame.draw.rect(screen, GRAY, self.handle_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.handle_rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.handle_rect.x = min(max(event.pos[0] - self.handle_rect.width // 2, self.rect.x),
                                         self.rect.right - self.handle_rect.width)
                self.value = (self.handle_rect.x - self.rect.x) / (self.rect.width - self.handle_rect.width)
                pygame.mixer.music.set_volume(self.value)
                self.notify_observers()

    def add_observer(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)

    def remove_observer(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update(self.value)
