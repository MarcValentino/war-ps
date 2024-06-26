import pygame
from classes.Constants import *


class Slider:
    def __init__(self, x, y, width, height, label, initial_value=0.5):
        self.rect = pygame.Rect(x, y, width, height)
        self.label = label
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.handle_rect = pygame.Rect(x + initial_value * width, y - 10, 20, 50)
        self.value = initial_value
        self.font = pygame.font.Font(None, 36)
        self.dragging = False

    def draw(self, screen):
        volume_text = self.font.render(self.label + ":" + f"{int(self.value * 100)}%", True, (0, 0, 0))
        screen.blit(volume_text, (self.x + self.width / 4, self.y - self.height * 1.5))
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
                self.value = (self.handle_rect.x - self.rect.x) / self.rect.width
                pygame.mixer.music.set_volume(self.value)
