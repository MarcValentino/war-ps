import pygame
from classes.Constants import *

class Button:
    def __init__(self, text, x, y, width, height, default_button=True, background_image_path=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = GRAY
        self.hover_color = DARK_GRAY
        self.border_color = DARK_GRAY
        self.border_radius = 5 if default_button else 0
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.text_surface = self.font.render(text, True, BLACK)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        self.background_image = None
        self.background_image_hovered = None

        if background_image_path:
            bg_path = background_image_path + ".png"
            bg_hovered_path = background_image_path + "_hovered.png"
            self.background_image = pygame.image.load(bg_path)
            self.background_image = pygame.transform.scale(self.background_image, (width, height))
            self.background_image_hovered = pygame.image.load(bg_hovered_path)
            self.background_image_hovered = pygame.transform.scale(self.background_image_hovered, (width, height))

    def draw(self, screen):
        if self.background_image:
            screen.blit(self.background_image_hovered
                        if self.is_hovered(pygame.mouse.get_pos())
                        else self.background_image, self.rect.topleft)
        else:
            current_color = self.hover_color if self.is_hovered(pygame.mouse.get_pos()) else self.color

            pygame.draw.rect(screen, current_color, self.rect, border_radius=self.border_radius)

        if self.border_radius != 0:
            pygame.draw.rect(screen, self.border_color, self.rect, 2, border_radius=self.border_radius)

        screen.blit(self.text_surface, self.text_rect)

    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.is_hovered(event.pos)

class MenuButton(Button):
    BUTTON_WIDTH = 300
    BUTTON_HEIGHT = 60
    BG_IMG = 'classes/assets/images/bg/main-menu-btn'

    def __init__(self, text, y):
        super().__init__(text, 0, y, self.BUTTON_WIDTH, self.BUTTON_HEIGHT, False, self.BG_IMG)
